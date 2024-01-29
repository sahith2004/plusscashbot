from langchain.document_loaders import CSVLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
import os
from flask import jsonify
from flask_cors import CORS
from flask import Flask
from pyngrok import ngrok
from flask import Flask, request,render_template
import requests

import locale
locale.getpreferredencoding = lambda: "UTF-8"

os.environ["OPENAI_API_KEY"] = "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"

loader = CSVLoader(file_path='mutual_funds_info.csv')
index_creator = VectorstoreIndexCreator()
docsearch = index_creator.from_loaders([loader])
chain = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=docsearch.vectorstore.as_retriever(), input_key="question")
query = "Do you have a column called age?"
response = chain({"question": query})
print(response['result'])

portno = 8000


app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
  return render_template("chat.html")
@app.route('/prompt/<input_text>', methods=['GET'])
def get_response(input_text):
    # Call your query_engine function with the input_text
    response = chain({"question": input_text})
    
    # Prepare the response data
    response_data = {
        'messages': [
            {'content': input_text}
        ],
        'candidates': [
            {'content': response['result']}
        ]
    }

    # Return the response as JSON
    return response_data
@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    response = chain({"question": input})
    

    return response['result']



#print(f"to access go to {public_url}")
