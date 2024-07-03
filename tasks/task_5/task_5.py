import sys
import os
import streamlit as st
sys.path.append(os.path.abspath('../../'))
from tasks.task_3.task_3 import DocumentProcessor
from tasks.task_4.task_4 import EmbeddingClient

# Import Task libraries
from langchain_core.documents import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma

class ChromaCollectionCreator:
    def __init__(self, processor, embed_model, persist_directory):
        """
        Initializes the ChromaCollectionCreator with a DocumentProcessor instance and embeddings configuration.
        :param processor: An instance of DocumentProcessor that has processed documents.
        :param embed_model: An embedding client for embedding documents.
        :param persist_directory: Directory to persist the Chroma collection.
        """
        self.processor = processor      # This will hold the DocumentProcessor from Task 3
        self.embed_model = embed_model
        self.persist_directory = persist_directory # This will hold the EmbeddingClient from Task 4
        self.db = None                  # This will hold the Chroma collection
    
    def create_chroma_collection(self):
        """
        Task: Create a Chroma collection from the documents processed by the DocumentProcessor instance.
        
        Steps:
        1. Check if any documents have been processed by the DocumentProcessor instance. If not, display an error message using streamlit's error widget.
        
        2. Split the processed documents into text chunks suitable for embedding and indexing. Use the CharacterTextSplitter from Langchain to achieve this. You'll need to define a separator, chunk size, and chunk overlap.
        https://python.langchain.com/docs/modules/data_connection/document_transformers/
        
        3. Create a Chroma collection in memory with the text chunks obtained from step 2 and the embeddings model initialized in the class. Use the Chroma.from_documents method for this purpose.
        https://python.langchain.com/docs/integrations/vectorstores/chroma#use-openai-embeddings
        https://docs.trychroma.com/getting-started
        
        Instructions:
        - Begin by verifying that there are processed pages available. If not, inform the user that no documents are found.
        
        - If documents are available, proceed to split these documents into smaller text chunks. This operation prepares the documents for embedding and indexing. Look into using the CharacterTextSplitter with appropriate parameters (e.g., separator, chunk_size, chunk_overlap).
        
        - Next, with the prepared texts, create a new Chroma collection. This step involves using the embeddings model (self.embed_model) along with the texts to initialize the collection.
        
        - Finally, provide feedback to the user regarding the success or failure of the Chroma collection creation.
        
        Note: Ensure to replace placeholders like [Your code here] with actual implementation code as per the instructions above.
        """
        
        # Step 1: Check for processed documents
        if len(self.processor.pages) == 0:
            st.error("No documents found!", icon="🚨")
            return

        # Step 2: Split documents into text chunks
        text_splitter = CharacterTextSplitter(
            separator="\n\n",
            chunk_size=2000,  # Adjusted chunk size
            chunk_overlap=400,
            length_function=len,
            is_separator_regex=False,
        )

        aux_array = list(map(lambda page: page.page_content, self.processor.pages))
        texts = text_splitter.create_documents(aux_array)

        if texts is not None:
            st.success(f"Successfully split pages to {len(texts)} documents!", icon="✅")
        print(f"Number of texts: {len(texts)}")

        # Debugging: Print the first few text chunks to verify
        for idx, text in enumerate(texts[:5]):
            print(f"Text Chunk {idx}: {text.page_content}")

        # Ensure there are no empty text chunks
        texts = [text for text in texts if text.page_content.strip() != ""]
        if len(texts) == 0:
            st.error("All text chunks are empty after processing!", icon="🚨")
            return

        print(f"Number of texts after removing empty chunks: {len(texts)}")

        # Step 3: Create the Chroma Collection in batches
        try:
            for i in range(0, len(texts), 25):
                batch_texts = texts[i:i + 25]
                print(f"Processing batch {i // 25 + 1} with {len(batch_texts)} documents.")
                
                # Debugging: Print details about the current batch
                for idx, doc in enumerate(batch_texts):
                    print(f"Batch {i // 25 + 1}, Document {idx}: {doc.page_content}")

                if self.db is None:
                    self.db = Chroma.from_documents(batch_texts, self.embed_model, persist_directory=self.persist_directory)
                else:
                    # If self.db already exists, update it with new documents
                    self.db.add_documents(batch_texts)
        except Exception as e:
            print(f"Error creating Chroma collection: {e}")
            st.error(f"Error creating Chroma collection: {e}", icon="🚨")
        
        if self.db:
            st.success("Successfully created Chroma Collection!", icon="✅")
        else:
            st.error("Failed to create Chroma Collection!", icon="🚨")
    
    def as_retriever(self):
        return self.db.as_retriever()

    def query_chroma_collection(self, query) -> Document:
        """
        Queries the created Chroma collection for documents similar to the query.
        :param query: The query string to search for in the Chroma collection.
        
        Returns the first matching document from the collection with similarity score.
        """
        if self.db:
            docs = self.db.similarity_search_with_relevance_scores(query)
            if docs:
                # Debugging: Print the returned documents
                print(f"Returned Docs: {docs}")
                return docs[0][0]  # Ensure to return the Document object, not a tuple
            else:
                st.error("No matching documents found!", icon="🚨")
        else:
            st.error("Chroma Collection has not been created!", icon="🚨")

if __name__ == "__main__":
    processor = DocumentProcessor() # Initialize from Task 3
    processor.ingest_documents()
    
    embed_config = {
        "model_name": "textembedding-gecko@003",
        "project": "sample-mission-427021",
        "location": "us-central1",
        "google_api_key": "AIzaSyAT5ks9-CV8iTA3Lq7G8sT6Wts--qk6vX4"
    }
    
    embed_client = EmbeddingClient(**embed_config) # Initialize from Task 4
    
    persist_directory = './chroma_db'  # Ensure this is passed correctly
    chroma_creator = ChromaCollectionCreator(processor, embed_client, persist_directory)
    
    with st.form("Load Data to Chroma"):
        st.write("Select PDFs for Ingestion, then click Submit")
        
        submitted = st.form_submit_button("Submit")
        if submitted:
            chroma_creator.create_chroma_collection()
