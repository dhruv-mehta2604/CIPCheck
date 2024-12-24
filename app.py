from flask import Flask,request,jsonify
import pandas as pd
from helper_function import create_base_encoding,generate_output,create_input_encoding

app = Flask(__name__)

# Define the API key
Encrypt_API_KEY = 'cm5kXzNBdzY5UXo5bEt3dnQ1ZmZBclN3MFFSM3VKSk0='

# Middleware to check API key
@app.before_request
def before_request():
    api_key = request.headers.get('Authorization')
    if not api_key or api_key != f'{API_KEY}':
        return jsonify({"error": "Unauthorized"}), 401

@app.route('/')
def hello_world():
    return "Hello World :)"

@app.route("/cipcheck",methods=['POST'])
def search_duplicate():
    query = request.json.get('query')
    baseencoding=create_base_encoding()
    df=pd.read_pickle("df_embedded 1.pkl")
    df['Intermediate Description']=df['ID1'].astype(str)+": "+df['Idea Title Statement']+". "+df['Summarized Idea']
    df['Intermediate Description'] = df['Intermediate Description'].apply(lambda x: (x[:600] + '...') if len(x) > 600 else x)
    x=create_input_encoding(query,baseencoding)
    results=generate_output(x,df['Intermediate Description'].tolist())
    return jsonify(results=results)
    #return "Hello World"
    
