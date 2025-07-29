from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

# Initialize Gemini API
import os
genai.configure(api_key=os.getenv("AIzaSyBH9aVSEb8kj6owXW-rWHz5-LrGlQzrmmo"))


# Create Flask app
app = Flask(__name__)

# Homepage route – loads chatbot UI
@app.route('/')
def home():
    return render_template('index.html')

# Chatbot API route
@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.json.get('question')

    # Custom prompt for Little Love assistant
    prompt = (
        "You are a friendly assistant for the Little Love brand. "
        "Little Love makes educational and business-building kits for children aged 4–12. "
        "You help parents understand how these kits work, how they help children grow, and give general parenting support. "
        "If the question is about delivery or orders, reply: 'Please contact our support at care@littlelove.in'.\n\n"
        f"Parent's question: {user_question}\n"
        "Answer:"
    )

    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)

        return jsonify({'answer': response.text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # use Render's assigned port
    app.run(host='0.0.0.0', port=port)
