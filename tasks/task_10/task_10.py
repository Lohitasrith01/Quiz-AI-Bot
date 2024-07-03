import streamlit as st
import os
import sys
import json
sys.path.append(os.path.abspath('../../'))
from tasks.task_3.task_3 import DocumentProcessor
from tasks.task_4.task_4 import EmbeddingClient
from tasks.task_5.task_5 import ChromaCollectionCreator
from tasks.task_8.task_8 import QuizGenerator
from tasks.task_9.task_9 import QuizManager

if __name__ == "__main__":
    
    embed_config = {
        "model_name": "textembedding-gecko@003",
        "project": "sample-mission-427021",
        "location": "us-central1",
        "google_api_key": "AIzaSyAT5ks9-CV8iTA3Lq7G8sT6Wts--qk6vX4"
    }
    
persist_directory = os.path.abspath('./chroma_persist_directory')
if not os.path.exists(persist_directory):
    os.makedirs(persist_directory)
sys.path.append(persist_directory)

# Add Session State
if 'question_bank' not in st.session_state:
    # Step 1: Initialize the necessary session state variables
    st.session_state['question_bank'] = []
    st.session_state['display_quiz'] = False
    st.session_state['question_index'] = 0

screen = st.empty()

if 'display_quiz' not in st.session_state or not st.session_state['display_quiz']:
    with screen.container():
        st.header("Quiz Builder")
        
        # Create a new st.form flow control for Data Ingestion
        with st.form("Load Data to Chroma"):
            st.write("Select PDFs for Ingestion, the topic for the quiz, and click Generate!")
            
            processor = DocumentProcessor()
            processor.ingest_documents()
        
            embed_client = EmbeddingClient(**embed_config) 
        
            chroma_creator = ChromaCollectionCreator(processor, embed_client, persist_directory=persist_directory)
            
            # Step 2: Set topic input and number of questions
            topic_input = st.text_input("Topic for the Quiz", placeholder="Enter the topic of the document")
            questions = st.slider("Number of Questions", min_value=1, max_value=10, value=1)
                
            submitted = st.form_submit_button("Submit")
            
            if submitted:
                chroma_creator.create_chroma_collection()
                    
                if len(processor.pages) > 0:
                    st.write(f"Generating {questions} questions for topic: {topic_input}")
                
                    # Step 3: Initialize a QuizGenerator class using the topic, number of questions, and the chroma collection
                    generator = QuizGenerator(topic_input, questions, chroma_creator)
                    question_bank = generator.generate_quiz()
                    
                    # Step 4: Initialize the question bank list in st.session_state
                    st.session_state['question_bank'] = question_bank
                    # Step 5: Set a display_quiz flag in st.session_state to True
                    st.session_state['display_quiz'] = True
                    # Step 6: Set the question_index to 0 in st.session_state
                    st.session_state['question_index'] = 0


if st.session_state["display_quiz"]:
    screen.empty()
    screen = st.empty()
    with screen.container():
        st.header("Generated Quiz Question: ")
        quiz_manager = QuizManager(st.session_state["question_bank"])
        
        # Format the question and display it
        with st.form("MCQ"):
            # Step 7: Set index_question using the Quiz Manager method get_question_at_index passing the st.session_state["question_index"]
            index_question = quiz_manager.get_question_at_index(st.session_state["question_index"])
            
            # Unpack choices for radio button
            choices = [f"{choice['key']}) {choice['value']}" for choice in index_question['choices']]
            
            # Display the Question
            st.write(f"{st.session_state['question_index'] + 1}. {index_question['question']}")
            answer = st.radio(
                "Choose an answer",
                choices,
                key="current_answer"
            )
            
            answer_choice = st.form_submit_button("Submit Answer")
            
            # Navigation buttons
            next_button = st.form_submit_button("Next Question", on_click=lambda: quiz_manager.next_question_index(direction=1))
            prev_button = st.form_submit_button("Previous Question", on_click=lambda: quiz_manager.next_question_index(direction=-1))

            if answer_choice and answer is not None:
                correct_answer_key = index_question['answer']
                if answer.startswith(correct_answer_key):
                    st.success("Correct!")
                else:
                    st.error("Incorrect!")
                st.write(f"Explanation: {index_question['explanation']}")

            if next_button:
                st.experimental_rerun()
            if prev_button:
                st.experimental_rerun()