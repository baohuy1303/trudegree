"""
Configuration file for test_agent.py
Easily switch between different parsed degree files for testing
"""

# Available parsed degree files
PARSED_DEGREE_FILES = {
    "default": "./parsedDegree/gpt4o_optimized.json",
    "gpt4_mini": "./parsedDegree/gpt4.1_mini-letterP-FinalTest.json",
    "gpt4_mini_2": "./parsedDegree/gpt4.1_mini-letterP-2.json",
    "gpt5_mini": "./parsedDegree/gpt5_mini-lowReason.json",
    "gpt5_nano": "./parsedDegree/gpt5_nano-lowReason.json",
    "student_profile": "./parsedDegree/student_profile_fixed_5.json",
}

# Select which file to use (change this to test different data)
ACTIVE_PARSED_DEGREE = "default"

# Common test prompts to try
TEST_PROMPTS = [
    "What courses should I take next semester?",
    "What are my remaining requirements?",
    "Help me plan my schedule for the next semester",
    "What Disciplinary Perspectives do I still need to complete?",
    "Can you recommend some courses that match my interests?",
    "Show me my completed courses",
    "What's my progress towards graduation?",
]

# You can add custom test scenarios here
CUSTOM_SCENARIOS = {
    "basic_recommendation": "I need help planning my next semester. Can you recommend 4-5 courses?",
    "specific_perspective": "I need to complete my Social Perspective requirement. What courses should I take?",
    "workload_concern": "I want to take 15 credits next semester. What's a balanced course load?",
    "major_focus": "I want to focus on my major requirements. What should I take?",
}


def get_active_degree_path():
    """Get the path to the currently active parsed degree file"""
    return PARSED_DEGREE_FILES.get(ACTIVE_PARSED_DEGREE, PARSED_DEGREE_FILES["default"])


def list_available_files():
    """List all available parsed degree files"""
    print("\n📁 Available Parsed Degree Files:")
    print("=" * 50)
    for key, path in PARSED_DEGREE_FILES.items():
        active = "✓" if key == ACTIVE_PARSED_DEGREE else " "
        print(f"[{active}] {key}: {path}")
    print("=" * 50)


def list_test_prompts():
    """List suggested test prompts"""
    print("\n💡 Suggested Test Prompts:")
    print("=" * 50)
    for i, prompt in enumerate(TEST_PROMPTS, 1):
        print(f"{i}. {prompt}")
    print("\n📝 Custom Scenarios:")
    for name, prompt in CUSTOM_SCENARIOS.items():
        print(f"- {name}: {prompt}")
    print("=" * 50)


if __name__ == "__main__":
    list_available_files()
    print()
    list_test_prompts()

