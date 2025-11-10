"""
Test Agent Runner - For testing the AI advisor agent with custom prompts
"""

import json
import time
from datetime import datetime
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from typing import List

# Import the necessary functions and objects from ai.py
from ai import (
    run_agent,
    save_history_simple,
    agent,
    parsedDegreeWorks  # This will use the global variable from ai.py
)


def print_separator():
    """Print a nice separator line"""
    print("=" * 70)


def print_welcome():
    """Print welcome message"""
    print_separator()
    print("🎓 Academic Advisor Agent - Test Environment")
    print_separator()
    print("\nCommands:")
    print("  - Type your question/prompt and press Enter")
    print("  - Type 'exit' to quit and save conversation")
    print("  - Type 'history' to view conversation history")
    print("  - Type 'clear' to clear conversation history")
    print("  - Type 'info' to see loaded student data")
    print_separator()
    print()


def print_student_info():
    """Print information about the loaded student data"""
    print("\n📋 Loaded Student Data:")
    print_separator()
    
    if parsedDegreeWorks:
        # Print basic info if available
        if "student_info" in parsedDegreeWorks:
            info = parsedDegreeWorks["student_info"]
            print(f"Student Name: {info.get('name', 'N/A')}")
            print(f"Student ID: {info.get('id', 'N/A')}")
            print(f"Major: {info.get('major', 'N/A')}")
        
        # Print some statistics
        if "completed_courses" in parsedDegreeWorks:
            completed = parsedDegreeWorks["completed_courses"]
            print(f"\nCompleted Courses: {len(completed)}")
        
        if "remaining_requirements" in parsedDegreeWorks:
            remaining = parsedDegreeWorks["remaining_requirements"]
            print(f"Remaining Requirements: {len(remaining)}")
    else:
        print("⚠️  No student data loaded")
    
    print_separator()


def print_history(history: List[BaseMessage]):
    """Print the conversation history"""
    print("\n📜 Conversation History:")
    print_separator()
    
    if not history:
        print("No conversation history yet.")
    else:
        for i, message in enumerate(history):
            role = "You" if hasattr(message, 'type') and message.type == 'human' else 'Agent'
            content = message.content
            
            # Truncate long responses for display
            if len(content) > 200:
                content = content[:200] + "..."
            
            print(f"\n{role}: {content}")
    
    print_separator()


def main():
    """Main test loop"""
    history = []
    print_welcome()
    
    while True:
        try:
            user_input = input("\n💬 You: ").strip()
            
            # Handle special commands
            if user_input.lower() == "exit":
                if history:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"./finalConvos/test_session_{timestamp}.txt"
                    save_history_simple(history, filename)
                    print(f"\n✅ Chat history saved to {filename}")
                print("👋 Goodbye!")
                break
            
            elif user_input.lower() == "history":
                print_history(history)
                continue
            
            elif user_input.lower() == "clear":
                history = []
                print("\n✅ Conversation history cleared")
                continue
            
            elif user_input.lower() == "info":
                print_student_info()
                continue
            
            elif not user_input:
                print("⚠️  Please enter a prompt or command")
                continue
            
            # Run the agent
            print("\n🤖 Agent: ", end="", flush=True)
            start_time = time.time()
            
            result = run_agent(user_input, history)
            
            # Handle the response based on its format
            if isinstance(result, dict) and "message" in result:
                response = result["message"]
                time_taken = result["time_taken"]
            else:
                response = result
                time_taken = time.time() - start_time
            
            # Print the response
            print(response.content)
            print(f"\n⏱️  Time taken: {time_taken:.2f} seconds")
            
            # Update conversation history
            history.append(HumanMessage(content=user_input))
            history.append(response)
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user")
            if history:
                save_choice = input("Save conversation history? (y/n): ").strip().lower()
                if save_choice == 'y':
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"./finalConvos/test_session_{timestamp}.txt"
                    save_history_simple(history, filename)
                    print(f"✅ Chat history saved to {filename}")
            print("👋 Goodbye!")
            break
        
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
            print("\nContinuing... (type 'exit' to quit)")


if __name__ == "__main__":
    main()

