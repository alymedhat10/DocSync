import os
from datetime import datetime
from google.cloud import bigquery, aiplatform
import pandas as pd
import numpy as np
import time
import tqdm
from vertexai.preview.language_models import TextEmbeddingModel
import streamlit as st
from google.oauth2 import service_account

# Constants
LOCATION = "us-central1"
UID = datetime.now().strftime("%m%d%H%M")
PROJECT_ID = 'tokyo-country-189103'
<<<<<<< HEAD
GOOGLE_APPLICATION_CREDENTIALS = os.path.join(os.path.dirname(__file__), 'Key', 'tokyo-country-189103-4ce23189dd39.json')

# Check if the file exists
if not os.path.isfile(GOOGLE_APPLICATION_CREDENTIALS):
    raise FileNotFoundError(f"Service account key not found at {GOOGLE_APPLICATION_CREDENTIALS}")
=======
GOOGLE_APPLICATION_CREDENTIALS = r"C:\Users\DELL\Python projects\DocSync\V2\Key\tokyo-country-189103-4ce23189dd39.json"
os.environ['PATH'] += os.pathsep + r'C:\Users\DELL\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin'
>>>>>>> f88e10bd603a15c0ef026dd7db7d0e611d64b3bf

# Authenticate using service account
credentials = service_account.Credentials.from_service_account_file(
    GOOGLE_APPLICATION_CREDENTIALS
)

# Initialize BigQuery and Vertex AI clients
bq_client = bigquery.Client(project=PROJECT_ID, credentials=credentials)
aiplatform.init(project=PROJECT_ID, location=LOCATION, credentials=credentials)

# Load the text embeddings model
model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")

# Helper functions
BATCH_SIZE = 5

def get_embeddings_wrapper(texts):
    embs = []
    for i in tqdm.tqdm(range(0, len(texts), BATCH_SIZE)):
        time.sleep(1)  # to avoid the quota error
        result = model.get_embeddings(texts[i : i + BATCH_SIZE])
        embs = embs + [e.values for e in result]
    return embs

def compare_requirements(new_df, old_df):
    new_df = new_df.assign(embedding=get_embeddings_wrapper(list(new_df.Requirement)))
    old_df = old_df.assign(embedding=get_embeddings_wrapper(list(old_df.Requirement)))

<<<<<<< HEAD
    new_embeddings = np.array(new_df['embedding'].tolist())
    old_embeddings = np.array(old_df['embedding'].tolist())

    similarity_matrix = np.dot(new_embeddings, old_embeddings.T)

    most_similar_indices = np.argmax(similarity_matrix, axis=1)
    most_similar_scores = np.max(similarity_matrix, axis=1)

=======
    # Convert the embeddings to numpy arrays for similarity calculation
    new_embeddings = np.array(new_df['embedding'].tolist())
    old_embeddings = np.array(old_df['embedding'].tolist())

    # Calculate the similarity matrix using dot product
    similarity_matrix = np.dot(new_embeddings, old_embeddings.T)

    # Find the most similar requirement in the old excel for each requirement in the new excel
    most_similar_indices = np.argmax(similarity_matrix, axis=1)
    most_similar_scores = np.max(similarity_matrix, axis=1)

    # Create the comparison dataframe
>>>>>>> f88e10bd603a15c0ef026dd7db7d0e611d64b3bf
    comparison_df = pd.DataFrame({
        'new_requirement_id': new_df['Requirement ID'],
        'new_requirement_text': new_df['Requirement'],
        'most_similar_requirement_text': old_df['Requirement'].iloc[most_similar_indices].values,
        'most_similar_requirement_id': old_df['Requirement ID'].iloc[most_similar_indices].values,
        'matching_percentage': most_similar_scores
    })
    return comparison_df

# Streamlit UI
st.title("DocSync")

st.subheader("New Excel File")
new_excel = st.file_uploader("Choose the new Excel file", type="xlsx")

st.subheader("Old Excel File")
old_excel = st.file_uploader("Choose the old Excel file", type="xlsx")

if st.button("Run Comparison"):
    if new_excel is not None and old_excel is not None:
        st.write("Processing...")

        new_df = pd.read_excel(new_excel)
        old_df = pd.read_excel(old_excel)
        
        progress_bar = st.progress(0)
        
        progress_bar.progress(10)
        comparison_df = compare_requirements(new_df, old_df)
        progress_bar.progress(100)
        
        st.success("Comparison finished!")
        
        st.write("Download the comparison file:")
        st.download_button(
            label="Download comparison_df",
            data=comparison_df.to_csv(index=False),
            file_name='comparison_df.csv',
            mime='text/csv'
        )
    else:
        st.error("Please upload both Excel files.")
