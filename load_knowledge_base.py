# load the knowledge base data from a json file and add it to the chromadb
import json
import os
from dotenv import load_dotenv
from enhanced_chatbot import EnhancedDepartmentRouterChatbot

def load_knowledge_from_json(chatbot: EnhancedDepartmentRouterChatbot, json_file: str):
    """Load knowledge base from JSON file."""
    
    print(f"\n{'='*70}")
    print("KNOWLEDGE BASE LOADER")
    print(f"{'='*70}\n")
    
    try:
        with open(json_file, 'r') as f:
            knowledge_data = json.load(f)
        
        print(f"✓ Loaded {len(knowledge_data)} entries from {json_file}")
        
        # Add each entry to knowledge base
        for idx, entry in enumerate(knowledge_data, 1):
            content = entry.get('content', '')
            metadata = entry.get('metadata', {})
            
            if content:
                chatbot.add_to_knowledge_base(content, metadata)
                print(f"  [{idx}/{len(knowledge_data)}] Added: {content[:60]}...")
        
        print(f"\n✓ Successfully loaded {len(knowledge_data)} knowledge base entries!")
        
        # Get updated stats
        stats = chatbot.get_conversation_stats()
        print(f"\n📊 Updated Statistics:")
        print(f"   Total Knowledge Base Entries: {stats['knowledge_base_entries']}")
        print(f"   Total Conversations: {stats['total_conversations']}")
        
    except FileNotFoundError:
        print(f"❌ Error: File '{json_file}' not found!")
    except json.JSONDecodeError:
        print(f"❌ Error: Invalid JSON format in '{json_file}'!")
    except Exception as e:
        print(f"❌ Error loading knowledge base: {e}")


def main():
    """Main function."""
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY not found in .env file!")
        return
    
    print("✓ API Key loaded successfully!")
    
    # Initialize chatbot
    try:
        chatbot = EnhancedDepartmentRouterChatbot(api_key)
        print("✓ ChromaDB initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing chatbot: {e}")
        return
    
    # Get current stats
    stats = chatbot.get_conversation_stats()
    print(f"\n📊 Current Statistics:")
    print(f"   Knowledge Base Entries: {stats['knowledge_base_entries']}")
    print(f"   Total Conversations: {stats['total_conversations']}")
    
    # Load knowledge base
    json_file = "knowledge_base_data.json"
    if os.path.exists(json_file):
        print(f"\nFound knowledge base file: {json_file}")
        choice = input("Do you want to load this data? (yes/no): ").strip().lower()
        
        if choice in ['yes', 'y']:
            load_knowledge_from_json(chatbot, json_file)
        else:
            print("\nSkipped loading knowledge base.")
    else:
        print(f"\n⚠️  Knowledge base file not found: {json_file}")
        print("Create a JSON file with your knowledge base data to load.")
    
    print(f"\n{'='*70}")
    print("✓ Knowledge base loader completed!")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
