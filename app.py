from flask import Flask,request,jsonify
import pandas as pd
from helper_function import create_base_encoding,generate_output,create_input_encoding

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello World :)"

@app.route("/cipcheck",methods=['POST'])
def search_duplicate():
    query = request.json.get('query')
    baseencoding=create_base_encoding()
    df=pd.read_pickle("df_embedded 1.pkl")
    df['Intermediate Description']=df['ID1'].astype(str)+": "+df['Idea Title Statement']+". "+df['Summarized Idea']
    df['Intermediate Description'] = df['Intermediate Description'].apply(lambda x: (x[:600] + '...') if len(x) > 100 else x)
    x=create_input_encoding(query,baseencoding)
    results=generate_output(x,df['Intermediate Description'].tolist())
    return jsonify(results=results)
    #return "Hello World"
    
