import sys
import os
import streamlit as st

# Add parent directory to the system path
sys.path.append(os.path.abspath('../../'))

# Debugging: Print the system path
print("System Path:")
print(sys.path)

# Debugging: Print the current directory and its contents
print("Current Directory:")
print(os.getcwd())
print("Directory Contents:")
print(os.listdir(os.getcwd()))

# Import necessary modules
try:
    from tasks.task_3.task_3 import DocumentProcessor
    from tasks.task_4.task_4 import EmbeddingClient
    from tasks.task_5.task_5 import ChromaCollectionCreator as BaseChromaCollectionCreator
except ImportError as e:
    print(f"ImportError: {e}")

from langchain_core.documents import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma

class ChromaCollectionCreator(BaseChromaCollectionCreator):
    def __init__(self, processor, embed_model, persist_directory):
        print(f"Initializing ChromaCollectionCreator with processor: {processor}, embed_model: {embed_model}, persist_directory: {persist_directory}")
        super().__init__(processor, embed_model, persist_directory)
        self.persist_directory = persist_directory
        self.db = None

        # Ensure the directory exists and is writable
        os.makedirs(self.persist_directory, exist_ok=True)
        if not os.access(self.persist_directory, os.W_OK):
            raise PermissionError(f"The directory {self.persist_directory} is not writable.")

    def create_chroma_collection(self):
        print("Starting create_chroma_collection method")
        # Step 1: Check for processed documents
        if len(self.processor.pages) == 0:
            st.error("No documents found!", icon="🚨")
            return

        # Step 2: Split documents into text chunks
        text_splitter = CharacterTextSplitter(
            separator="\n\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            is_separator_regex=False,
        )

        aux_array = list(map(lambda page: page.page_content, self.processor.pages))
        texts = text_splitter.create_documents(aux_array)

        if texts is not None:
            st.success(f"Successfully split pages to {len(texts)} documents!", icon="✅")
        print(f"Number of texts: {len(texts)}")

        # Debugging: Print the first few text chunks to verify
        print("Text Chunks:", texts[:5])

        # Step 3: Create the Chroma Collection
        try:
            self.db = Chroma.from_documents(texts, self.embed_model, persist_directory=self.persist_directory)
        except Exception as e:
            print(f"Error creating Chroma collection: {e}")
        
        if self.db:
            st.success("Successfully created Chroma Collection!", icon="✅")
        else:
            st.error("Failed to create Chroma Collection!", icon="🚨")
    
    def query_chroma_collection(self, query):
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
    st.header("Quizzify")

    # Configuration for EmbeddingClient
    embed_config = {
        "model_name": "textembedding-gecko@003",
        "project": "sample-mission-427021",
        "location": "us-central1",
        "google_api_key": os.getenv("GOOGLE_API_KEY")
    }
    
    screen = st.empty() # Screen 1, ingest documents
    with screen.container():
        # 1) Initialize DocumentProcessor and Ingest Documents from Task 3

        processor = DocumentProcessor() # Initialize from Task 3
        processor.ingest_documents()

        # Ensure the Chroma DB path exists
        chroma_db_path = './chroma_db'  # In-memory database
        if not os.path.exists(chroma_db_path):
            os.makedirs(chroma_db_path)
        
        print(f"Chroma DB Path: {chroma_db_path}")

        # 2) Initialize the EmbeddingClient from Task 4 with embed config
        embed_client = EmbeddingClient(
            model_name=embed_config["model_name"],
            project=embed_config["project"],
            location=embed_config["location"],
            google_api_key=embed_config["google_api_key"]
        )
        
        print(f"Embedding Client: {embed_client}")

        # 3) Initialize the ChromaCollectionCreator from Task 5 with persist_directory
        chroma_creator = ChromaCollectionCreator(processor, embed_client, persist_directory=chroma_db_path)
        print(f"Chroma Collection Creator: {chroma_creator}")

        with st.form("Load Data to Chroma"):
            st.subheader("Quiz Builder")
            st.write("Select PDFs for Ingestion, the topic for the quiz, and click Generate!")

            # 4) Use streamlit widgets to capture the user's input for the quiz topic and the desired number of questions
            st.write("Topic for Generative Quiz")
            topic_input = st.text_input(label='Topic for Generative Quiz', placeholder='Enter the topic of the document', label_visibility='hidden')

            st.write("Number of Questions")
            n_questions = st.slider(label='Number of Questions', min_value=1, max_value=10, label_visibility='hidden')
            
            document = None
            
            submitted = st.form_submit_button("Generate a Quiz!")
            if submitted:
                # 5) Use the create_chroma_collection() method to create a Chroma collection from the processed documents
                chroma_creator.create_chroma_collection()

                # Uncomment the following lines to test the query_chroma_collection() method
                document = chroma_creator.query_chroma_collection(topic_input) 
                print(f"Queried Document: {document}")
                
    if document:
        screen.empty() # Screen 2
        with st.container():
            st.header("Query Chroma for Topic, top Document: ")
            st.write(document.page_content)
