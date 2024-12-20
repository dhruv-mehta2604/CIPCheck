from sentence_transformers import SentenceTransformer, util
import pandas as pd
import numpy as np
import base64
from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient
import io



def create_base_encoding():
  TENANT_ID = "ZTRkOThkZDItOTE5OS00MmU1LWJhOGItZGEzZTc2M2VkZTJl"
  CLIENT_ID = "NjY1NTA1ODctOTE5NC00NWIxLTg1MDktZjY2MDczNDNjYTlh"
  CLIENT_SECRET="T2Z5OFF+aHo0Z1FxVzZNcDRYRnAzSThzU2JlblhkUTE4cWFVdWRyNQ=="
  STORAGE_ACCOUNT_NAME = "bWFxcmVzdW1lcw=="
  CONTAINER_NAME = "Y2lwaWRlYXNkYXRh"
  credential = ClientSecretCredential(
    tenant_id=base64.b64decode(TENANT_ID.encode('utf-8')).decode('utf-8'),
    client_id=base64.b64decode(CLIENT_ID.encode('utf-8')).decode('utf-8'),
    client_secret=base64.b64decode(CLIENT_SECRET.encode('utf-8')).decode('utf-8')
    )
  blob_service_client = BlobServiceClient(
    account_url=f"https://{base64.b64decode(STORAGE_ACCOUNT_NAME.encode('utf-8')).decode('utf-8')}.blob.core.windows.net",
    credential=credential
    )
  FileName="CIP Idea List.csv"
  blob_client = blob_service_client.get_blob_client(container=base64.b64decode(CONTAINER_NAME.encode('utf-8')).decode('utf-8'), blob="base_encoding.npy")
  blob_data = blob_client.download_blob().readall()
  buffer = io.BytesIO(blob_data)
  statement_embeddings=np.load(buffer,allow_pickle=True)
  return statement_embeddings

def create_input_encoding(input_statement,baseencoding):
  # Initialize the pre-trained model
  model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

  input_embedding = model.encode(input_statement)

  # Compute cosine similarity scores
  similarity_scores = util.cos_sim(input_embedding, baseencoding)
  return similarity_scores


def generate_output(similarity_scores,statemets):
  o=[]
  for i in range(len(similarity_scores[0])):
    o.append([i,similarity_scores[0][i].item()])
    v=pd.DataFrame(o,columns=['index','similarity']).sort_values('similarity',ascending=[False])[:5]['index']
  outputstr=[]
  for i in v:
    outputstr.append(statemets[i])
  return outputstr
