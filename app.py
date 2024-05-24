from flask import Flask, request, jsonify
from PyPDF2 import PdfReader
from langchain.chains import ConversationChain
from langchain_openai import OpenAI  # Updated import

app = Flask(__name__)


def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

# Load company policies from the PDF file


pdf_path = 'data/company_policies.pdf'
company_policies = extract_text_from_pdf(pdf_path)

# Initialize LangChain components
llm = OpenAI(api_key='YOUR_OPENAI_API_KEY')  # Replace with your OpenAI API key
conversation = ConversationChain(llm=llm)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Generate response using LangChain
    response = conversation.run(user_message, context=company_policies)
    
    return jsonify({'response': response})


if __name__ == '__main__':
    app.run(debug=True)
