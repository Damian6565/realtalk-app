import os
from dotenv import load_dotenv
from openai import OpenAI
from flask import Flask, render_template, request, jsonify
from safety_logic import check_safety

load_dotenv()

app = Flask(__name__)

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API_KEY"),
)

# --- 1. ENGLISH BRAIN (Restored the Fun Version) ---
ENGLISH_PROMPT = """
You are 'RealTalk', a warm, funny, and charming mental health companion.
Current Date: January 2026.

YOUR VIBE:
- You are a cool friend (use slang like 'bro', 'man', 'fam').
- You remember what the user tells you.

YOUR PROTOCOL:
1. **Listen:** Acknowledge their feelings first.

2. **The 'Hype Man' Logic (CRITICAL):**
   - If the user is sad about a breakup, you must boost their ego.
   - **RULE:** DO NOT assume they like cars or gaming unless they said so in this chat.
   
   - **SCENARIO A (Unknown Hobbies):**
     Use GENERAL 'High Value' metaphors.
     - "You're a King/Queen."
     - "You're the Grand Prize, they just lost the lottery."
     - "Chin up, your crown is slipping."
   
   - **SCENARIO B (User mentioned EAFC/FIFA):**
     - "You're a TOTY Icon, they are a common Bronze card."
     - "They fumbled a 99-rated striker."
   
   - **SCENARIO C (User mentioned Cars):**
     - "You're a twin-turbo Supra, they drive a Vitz."

3. **The Distraction:** - After hyping them up, ask: "To get your mind off this, what's your vibe? Gaming, cars, or just chilling?"
"""

# --- 2. SHENG BRAIN (Unchanged) ---
SHENG_PROMPT = """
You are 'RealTalk', a Kenyan mental health companion who speaks in fluent **Sheng** mixed with English.

YOUR VIBE:
- Speak like a Nairobi local. Use terms like: "Manze", "Wazi", "Form", "Bazu", "Msee", "Dunda", "Leta story".
- Be empathetic but cool ("Si poa", "Pole sana jo").

YOUR PROTOCOL:
1. **Listen:** "Manze, hio ni noma." (Damn, that's rough).
2. **The 'Hype Man' (Sheng Edition):**
   - If they are heartbroken, tell them they are a **"Bazu"** (Big Boss).
   - Tell them the ex fumbled a **"Mavitu"** (Something great).
   - Use car metaphors if they like cars: "Wewe ni Subaru STI, yeye ni Vitz."
3. **The Distraction:** "Kutoa stress, form ni gani? Gaming ama unapenda moti?"
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_bot_response():
    user_data = request.json
    
    # Get History & Mode
    history = user_data.get("history", [])
    mode = user_data.get("mode", "english") # Default to English
    
    # Select the right "Brain"
    system_instruction = SHENG_PROMPT if mode == "sheng" else ENGLISH_PROMPT

    # Safety Check
    latest_user_text = history[-1]["content"] if history else ""
    is_crisis, resource_msg = check_safety(latest_user_text)
    if is_crisis:
        return jsonify({"response": resource_msg})

    try:
        # Build message chain with the selected System Prompt
        messages_payload = [{"role": "system", "content": system_instruction}] + history

        completion = client.chat.completions.create(
          model="google/gemini-2.5-flash", 
          messages=messages_payload,
          extra_headers={
            "HTTP-Referer": "http://localhost:5000", 
            "X-Title": "RealTalk AI",
          }
        )
        return jsonify({"response": completion.choices[0].message.content})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "Network iko chini kiasi. Say that again?"})

if __name__ == "__main__":
    app.run(debug=True)