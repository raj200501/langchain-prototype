from flask import Flask, request, jsonify
from langchain.chains import ConversationChain
from langchain.prompts import load_prompt
from langchain.llms import OpenAI

# Initialize Flask app
app = Flask(__name__)

# Load extracted company policies
with open('data/company_policies.txt', 'r') as file:
    company_policies = file.read()

# Initialize LangChain components
llm = OpenAI(api_key='YOUR_OPENAI_API_KEY')  # Replace with your OpenAI API key
conversation = ConversationChain(llm=llm)

# Define a route for the chatbot
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Generate response using LangChain
    response = conversation.run(user_message, context=company_policies)
    
    return jsonify({'response': response})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
