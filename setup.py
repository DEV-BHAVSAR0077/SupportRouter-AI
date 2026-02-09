#!/usr/bin/env python3
"""
Automated Setup Script for Enhanced Chatbot
Guides user through installation and configuration
"""

import os
import sys
import subprocess

def print_header(text):
    """Print formatted header."""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def print_step(step_num, text):
    """Print step number."""
    print(f"\n{'='*70}")
    print(f"STEP {step_num}: {text}")
    print(f"{'='*70}\n")

def check_python_version():
    """Check if Python version is compatible."""
    print_step(1, "Checking Python Version")
    
    version = sys.version_info
    print(f"Current Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ ERROR: Python 3.8 or higher is required!")
        print("Please upgrade Python and try again.")
        return False
    
    print("✓ Python version is compatible!")
    return True

def install_dependencies():
    """Install required packages."""
    print_step(2, "Installing Dependencies")
    
    print("Installing required Python packages...")
    print("This may take a few minutes...\n")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt",
            "--break-system-packages"
        ])
        print("\n✓ All dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("\n❌ Error installing dependencies!")
        print("Please try manually: pip install -r requirements.txt --break-system-packages")
        return False

def setup_env_file():
    """Guide user through .env file setup."""
    print_step(3, "Setting Up Environment Variables")
    
    if os.path.exists('.env'):
        print("⚠️  .env file already exists!")
        overwrite = input("Do you want to overwrite it? (yes/no): ").strip().lower()
        if overwrite not in ['yes', 'y']:
            print("Keeping existing .env file.")
            return True
    
    print("\nLet's set up your environment variables.")
    print("You'll need:")
    print("  1. Gemini API Key (required)")
    print("  2. Email credentials (optional, for email routing)\n")
    
    # Get Gemini API key
    print("─"*70)
    print("GEMINI API KEY")
    print("─"*70)
    print("Get your free API key from: https://makersuite.google.com/app/apikey")
    gemini_key = input("Enter your Gemini API key: ").strip()
    
    if not gemini_key:
        print("❌ Gemini API key is required!")
        return False
    
    # Get email configuration
    print("\n" + "─"*70)
    print("EMAIL CONFIGURATION (Optional)")
    print("─"*70)
    print("For automated email routing to departments.")
    setup_email = input("Do you want to configure email? (yes/no): ").strip().lower()
    
    sender_email = ""
    sender_password = ""
    smtp_server = "smtp.gmail.com"
    smtp_port = "587"
    
    if setup_email in ['yes', 'y']:
        print("\nFor Gmail:")
        print("  1. Enable 2-Factor Authentication")
        print("  2. Generate an App Password: https://myaccount.google.com/apppasswords")
        print("  3. Use the 16-character App Password (not your regular password)\n")
        
        sender_email = input("Enter sender email: ").strip()
        sender_password = input("Enter email password/app password: ").strip()
        
        custom_smtp = input("Use custom SMTP server? (default: Gmail) (yes/no): ").strip().lower()
        if custom_smtp in ['yes', 'y']:
            smtp_server = input("Enter SMTP server: ").strip()
            smtp_port = input("Enter SMTP port: ").strip()
    
    # Create .env file
    env_content = f"""# Gemini API Configuration
GEMINI_API_KEY={gemini_key}

# Email Configuration
SENDER_EMAIL={sender_email}
SENDER_PASSWORD={sender_password}
SMTP_SERVER={smtp_server}
SMTP_PORT={smtp_port}
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("\n✓ .env file created successfully!")
        return True
    except Exception as e:
        print(f"\n❌ Error creating .env file: {e}")
        return False

def test_configuration():
    """Test the configuration."""
    print_step(4, "Testing Configuration")
    
    try:
        from dotenv import load_dotenv
        import google.generativeai as genai
        
        load_dotenv()
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("❌ GEMINI_API_KEY not found in .env file!")
            return False
        
        print("Testing Gemini API connection...")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-flash-latest')
        response = model.generate_content("Hello")
        
        print("✓ Gemini API is working!")
        print(f"✓ Test response: {response.text[:50]}...")
        
        # Test email configuration
        sender_email = os.getenv("SENDER_EMAIL")
        if sender_email:
            print(f"✓ Email configured: {sender_email}")
        else:
            print("⚠️  Email not configured (optional)")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def initialize_knowledge_base():
    """Initialize the knowledge base."""
    print_step(5, "Initializing Knowledge Base")
    
    try:
        print("Loading knowledge base with sample data...")
        
        from enhanced_chatbot import EnhancedDepartmentRouterChatbot, initialize_knowledge_base as init_kb
        from dotenv import load_dotenv
        
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        
        chatbot = EnhancedDepartmentRouterChatbot(api_key)
        
        # Check if already initialized
        stats = chatbot.get_conversation_stats()
        if stats["knowledge_base_entries"] > 0:
            print(f"⚠️  Knowledge base already has {stats['knowledge_base_entries']} entries.")
            reinit = input("Do you want to add sample data anyway? (yes/no): ").strip().lower()
            if reinit not in ['yes', 'y']:
                print("Skipping knowledge base initialization.")
                return True
        
        init_kb(chatbot)
        stats = chatbot.get_conversation_stats()
        
        print(f"\n✓ Knowledge base initialized!")
        print(f"   Total entries: {stats['knowledge_base_entries']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error initializing knowledge base: {e}")
        print("You can initialize it later by running the chatbot.")
        return True  # Non-critical, so return True

def print_next_steps():
    """Print what to do next."""
    print_step(6, "Setup Complete!")
    
    print("✓ Your enhanced chatbot is ready to use!\n")
    print("What's next?\n")
    print("1. TEST THE CHATBOT:")
    print("   python test_chatbot.py\n")
    print("2. RUN THE CLI VERSION:")
    print("   python enhanced_chatbot.py\n")
    print("3. START THE API SERVER:")
    print("   python enhanced_backend_api.py\n")
    print("4. LOAD ADDITIONAL KNOWLEDGE:")
    print("   python load_knowledge_base.py\n")
    print("5. READ THE DOCUMENTATION:")
    print("   cat README.md\n")
    print("─"*70)
    print("\nQuick Test Command:")
    print("  python test_chatbot.py")
    print("\n" + "="*70 + "\n")

def main():
    """Main setup function."""
    print("\n" + "="*70)
    print("  ENHANCED CHATBOT - AUTOMATED SETUP")
    print("="*70)
    print("\nThis script will help you set up the enhanced chatbot system.")
    print("The setup process includes:")
    print("  • Checking Python version")
    print("  • Installing dependencies")
    print("  • Configuring environment variables")
    print("  • Testing the configuration")
    print("  • Initializing the knowledge base")
    print("\nPress Enter to continue or Ctrl+C to cancel...")
    input()
    
    # Step 1: Check Python version
    if not check_python_version():
        return
    
    # Step 2: Install dependencies
    if not install_dependencies():
        print("\nSetup incomplete. Please resolve dependency issues.")
        return
    
    # Step 3: Setup .env file
    if not setup_env_file():
        print("\nSetup incomplete. Please configure .env file manually.")
        return
    
    # Step 4: Test configuration
    if not test_configuration():
        print("\nSetup incomplete. Please check your configuration.")
        return
    
    # Step 5: Initialize knowledge base
    initialize_knowledge_base()
    
    # Step 6: Print next steps
    print_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
