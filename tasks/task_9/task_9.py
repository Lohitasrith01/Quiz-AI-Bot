import streamlit as st
import os
import sys
import tempfile
sys.path.append(os.path.abspath('../../'))
from tasks.task_3.task_3 import DocumentProcessor
from tasks.task_4.task_4 import EmbeddingClient
from tasks.task_5.task_5 import ChromaCollectionCreator
from tasks.task_8.task_8 import QuizGenerator

class QuizManager:
    def __init__(self, questions: list):
        self.questions = questions
        self.total_questions = len(self.questions)

    def get_question_at_index(self, index: int):
        valid_index = index % self.total_questions
        return self.questions[valid_index]
    
    def next_question_index(self, direction=1):
        current_index = st.session_state.get("question_index", 0)
        new_index = (current_index + direction) % self.total_questions
        st.session_state["question_index"] = new_index

# Test Generating the Quiz
if __name__ == "__main__":
    
    embed_config = {
        "model_name": "textembedding-gecko@003",
        "project": "sample-mission-427021",
        "location": "us-central1",
        "google_api_key": "AIzaSyAT5ks9-CV8iTA3Lq7G8sT6Wts--qk6vX4"
    }
    
    # Create a temporary directory for persist_directory
    persist_directory = tempfile.mkdtemp()
    sys.path.append(persist_directory)
    
    screen = st.empty()
    with screen.container():
        st.header("Quiz Builder")
        processor = DocumentProcessor()
        processor.ingest_documents()
    
        embed_client = EmbeddingClient(**embed_config) 
    
        chroma_creator = ChromaCollectionCreator(processor, embed_client, persist_directory=persist_directory)
    
        question = None
        question_bank = None
    
        with st.form("Load Data to Chroma"):
            st.subheader("Quiz Builder")
            st.write("Select PDFs for Ingestion, the topic for the quiz, and click Generate!")
            
            topic_input = st.text_input("Topic for Generative Quiz", placeholder="Enter the topic of the document")
            questions = st.slider("Number of Questions", min_value=1, max_value=10, value=1)
            
            submitted = st.form_submit_button("Submit")
            if submitted:
                chroma_creator.create_chroma_collection()
                
                st.write(topic_input)
                
                generator = QuizGenerator(topic_input, questions, chroma_creator)
                question_bank = generator.generate_quiz()
                st.session_state["question_bank"] = question_bank

    if "question_bank" in st.session_state:
        question_bank = st.session_state["question_bank"]
        screen.empty()
        with st.container():
            st.header("Generated Quiz Questions: ")
            
            quiz_manager = QuizManager(question_bank)
            
            if "question_index" not in st.session_state:
                st.session_state["question_index"] = 0

            # Enclose the entire quiz question and submit button inside an st.form()
            with st.form("Quiz Form"):
                index_question = quiz_manager.get_question_at_index(st.session_state["question_index"])
                
                choices = [f"{choice['key']}) {choice['value']}" for choice in index_question['choices']]
                
                st.write("**Question:** " + index_question['question'])
                
                answer = st.radio('Choose the correct answer', choices, key="current_answer")
                
                answer_submitted = st.form_submit_button("Submit Answer")
                if answer_submitted:
                    correct_answer_key = index_question['answer']
                    if answer.startswith(correct_answer_key):
                        st.success("Correct!")
                    else:
                        st.error("Incorrect!")
            
            col1, col2 = st.columns(2)
            if col1.button("Previous Question"):
                quiz_manager.next_question_index(direction=-1)
                st.experimental_rerun()
            if col2.button("Next Question"):
                quiz_manager.next_question_index(direction=1)
                st.experimental_rerun()
