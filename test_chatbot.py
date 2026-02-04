"""
Testing Script for Enhanced Chatbot
Demonstrates all features with sample interactions
"""

import os
from dotenv import load_dotenv
from enhanced_chatbot import EnhancedDepartmentRouterChatbot, initialize_knowledge_base


def print_header(text):
    """Print a formatted header."""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")


def print_result(result):
    """Print formatted result."""
    print(f"🤖 Bot Response:")
    print(f"   {result['bot_response']}\n")
    print(f"📋 Analysis:")
    print(f"   Department: {result['analysis']['department']}")
    print(f"   Confidence: {result['analysis']['confidence']}%")
    print(f"   Reason: {result['analysis']['reason']}")
    print(f"   Status: {result['status']}")
    
    if result.get('knowledge_context'):
        print(f"\n💡 Knowledge Context: {len(result['knowledge_context'])} relevant entries found")
    
    if result.get('similar_conversations'):
        print(f"📚 Similar Conversations: {len(result['similar_conversations'])} found")


def test_basic_queries(chatbot):
    """Test basic department routing."""
    print_header("TEST 1: Basic Department Routing")
    
    test_queries = [
        "What's the price for building an e-commerce website?",
        "My website is down and showing an error",
        "I want to apply for a developer position",
        "When will I receive my invoice?",
        "I'm not satisfied with the project delivery"
    ]
    
    for query in test_queries:
        print(f"💬 User: {query}")
        result = chatbot.process_message(query)
        print_result(result)
        print("\n" + "-"*70)
        
        # Reset for next test
        chatbot.reset_conversation()


def test_context_awareness(chatbot):
    """Test context-aware conversations."""
    print_header("TEST 2: Context-Aware Multi-Turn Conversation")
    
    conversation = [
        "Hi, I need a new website",
        "It's for my online clothing store",
        "What features do you offer for e-commerce?",
        "How much would it cost?",
        "What about payment options?"
    ]
    
    for message in conversation:
        print(f"💬 User: {message}")
        result = chatbot.process_message(message)
        print_result(result)
        print("\n" + "-"*70)
    
    chatbot.reset_conversation()


def test_knowledge_base_search(chatbot):
    """Test knowledge base integration."""
    print_header("TEST 3: Knowledge Base Search")
    
    query = "What are your support hours?"
    print(f"💬 User: {query}")
    
    # Search knowledge base directly
    kb_results = chatbot.search_knowledge_base(query, n_results=3)
    
    print(f"\n🔍 Knowledge Base Search Results:")
    for idx, result in enumerate(kb_results, 1):
        print(f"\n   Result {idx}:")
        print(f"   Content: {result['content'][:100]}...")
        print(f"   Metadata: {result['metadata']}")
    
    # Process with full context
    result = chatbot.process_message(query)
    print_result(result)
    
    chatbot.reset_conversation()


def test_similar_conversations(chatbot):
    """Test similar conversation search."""
    print_header("TEST 4: Similar Conversation Search")
    
    # Create some conversation history
    history_queries = [
        "My website loads very slowly",
        "The checkout page isn't working",
        "Users can't upload images"
    ]
    
    print("📝 Creating conversation history...")
    for query in history_queries:
        chatbot.process_message(query)
        print(f"   Stored: {query}")
    
    chatbot.reset_conversation()
    
    # Search for similar conversation
    search_query = "Website performance issues"
    print(f"\n🔍 Searching for conversations similar to: '{search_query}'")
    
    similar = chatbot.search_similar_conversations(search_query, n_results=3)
    
    print(f"\n📚 Found {len(similar)} similar conversations:")
    for idx, conv in enumerate(similar, 1):
        print(f"\n   {idx}. {conv['content']}")
        print(f"      Session: {conv['metadata'].get('session_id', 'N/A')[:8]}...")
        print(f"      Department: {conv['metadata'].get('department', 'N/A')}")
    
    chatbot.reset_conversation()


def test_statistics(chatbot):
    """Test statistics functionality."""
    print_header("TEST 5: System Statistics")
    
    stats = chatbot.get_conversation_stats()
    
    print("📊 Current System Statistics:")
    print(f"   Total Conversations: {stats['total_conversations']}")
    print(f"   Knowledge Base Entries: {stats['knowledge_base_entries']}")
    print(f"   Current Session Messages: {stats['current_session_messages']}")


def test_email_generation(chatbot):
    """Test email content generation."""
    print_header("TEST 6: Email Content Generation")
    
    query = "I need urgent help - my website is completely down!"
    print(f"💬 User: {query}")
    
    result = chatbot.process_message(query)
    print_result(result)
    
    if result['department']:
        print(f"\n📧 Email Details:")
        print(f"   To: {chatbot.departments[result['department']]['email']}")
        print(f"   Department: {result['department']}")
        print(f"   Session ID: {result['session_id']}")
        print(f"   Note: Email would be automatically generated and sent")
    
    chatbot.reset_conversation()


def run_interactive_demo(chatbot):
    """Run interactive demo mode."""
    print_header("INTERACTIVE DEMO MODE")
    
    print("Try these sample queries:")
    print("  1. 'How much does web development cost?'")
    print("  2. 'I need technical support'")
    print("  3. 'What job openings do you have?'")
    print("  4. 'I want to cancel my subscription'")
    print("  5. Type 'stats' to see statistics")
    print("  6. Type 'quit' to exit\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() == 'quit':
            print("\n✓ Exiting demo mode...\n")
            break
        
        if user_input.lower() == 'stats':
            test_statistics(chatbot)
            continue
        
        if user_input.lower() == 'reset':
            chatbot.reset_conversation()
            print("\n✓ Conversation reset!\n")
            continue
        
        result = chatbot.process_message(user_input)
        print_result(result)
        print("\n" + "-"*70 + "\n")


def main():
    """Main testing function."""
    print("\n" + "="*70)
    print("  ENHANCED CHATBOT - COMPREHENSIVE TESTING SUITE")
    print("="*70)
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("\n❌ ERROR: GEMINI_API_KEY not found!")
        print("Please create a .env file with your API key.")
        return
    
    print("\n✓ API Key loaded successfully!")
    
    # Initialize chatbot
    try:
        chatbot = EnhancedDepartmentRouterChatbot(api_key)
        print("✓ ChromaDB initialized successfully!")
        
        # Initialize knowledge base if needed
        stats = chatbot.get_conversation_stats()
        if stats["knowledge_base_entries"] == 0:
            print("\n📚 Initializing knowledge base with sample data...")
            initialize_knowledge_base(chatbot)
        
    except Exception as e:
        print(f"\n❌ Error initializing chatbot: {e}")
        return
    
    # Show menu
    print("\n" + "="*70)
    print("  SELECT TEST MODE")
    print("="*70)
    print("\n1. Run all automated tests")
    print("2. Basic department routing")
    print("3. Context-aware conversation")
    print("4. Knowledge base search")
    print("5. Similar conversations")
    print("6. System statistics")
    print("7. Email generation")
    print("8. Interactive demo")
    print("9. Exit")
    
    choice = input("\nEnter choice (1-9): ").strip()
    
    if choice == '1':
        test_basic_queries(chatbot)
        test_context_awareness(chatbot)
        test_knowledge_base_search(chatbot)
        test_similar_conversations(chatbot)
        test_statistics(chatbot)
        test_email_generation(chatbot)
    elif choice == '2':
        test_basic_queries(chatbot)
    elif choice == '3':
        test_context_awareness(chatbot)
    elif choice == '4':
        test_knowledge_base_search(chatbot)
    elif choice == '5':
        test_similar_conversations(chatbot)
    elif choice == '6':
        test_statistics(chatbot)
    elif choice == '7':
        test_email_generation(chatbot)
    elif choice == '8':
        run_interactive_demo(chatbot)
    elif choice == '9':
        print("\n✓ Exiting...\n")
        return
    else:
        print("\n❌ Invalid choice!")
        return
    
    print("\n" + "="*70)
    print("  TESTING COMPLETED")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
