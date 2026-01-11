# safety_logic.py

# We only want to trigger the hard block for IMMEDIATE life-threatening danger.
# We removed words like "depressed" or "sad" so the AI can talk about them.
CRISIS_KEYWORDS = [
    "commit suicide", 
    "kill myself", 
    "end my life", 
    "overdose", 
    "hang myself"
]

# This message only shows if the user is in immediate physical danger.
EMERGENCY_RESPONSE = """
🚨 **RealTalk Safety Alert** 🚨

I hear you, and I am very worried about your safety right now. 
Because you mentioned ending your life, I cannot continue this chat. 
Please contact these people who can actually help keep you safe:

- 🇰🇪 **Befrienders Kenya:** +254 722 178 177
- 🌍 **Global Emergency:** 911 or 112
- 🏥 **Go to the nearest Hospital Emergency Room.**

Please reach out to them. You are important.
"""

def check_safety(user_text):
    """Checks if the user input contains immediate self-harm keywords."""
    user_text = user_text.lower()
    for word in CRISIS_KEYWORDS:
        if word in user_text:
            return True, EMERGENCY_RESPONSE
    return False, None