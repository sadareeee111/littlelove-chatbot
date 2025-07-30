from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

# Initialize Gemini API
import os
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


# Create Flask app
app = Flask(__name__)

# Homepage route – loads chatbot UI
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.json.get('question')

    prompt = (
        "You are a friendly assistant for the Little Love brand. "
        "Little Love makes educational and business-building kits for children aged 4–12. "
        "You help parents understand how these kits work, how they help children grow, and give general parenting support. "
        "If the question is about delivery or orders, reply: 'Please contact our support at care@littlelove.in'.\n\n"
        f"Parent's question: {user_question}\n"
        "Answer:"
    )

    try:
        chat_model = genai.GenerativeModel("gemini-pro")
        chat = chat_model.start_chat()
        response = chat.send_message(prompt)
        return jsonify({"answer": response.text.strip()})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use Render's provided port
    app.run(host='0.0.0.0', port=port)
