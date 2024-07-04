AI-Powered Quiz Builder
Overview
The AI-Powered Quiz Builder is an innovative application designed to automatically generate multiple-choice questions from PDF documents. Leveraging advanced text embedding techniques and the capabilities of Vertex AI, this tool aims to streamline the quiz creation process for educational institutions, corporate training programs, and e-learning platforms.

Introduction

This project focuses on creating an AI-powered application that generates multiple-choice questions from PDF documents. The application leverages advanced text embedding techniques and the Chroma collection to deliver accurate and relevant questions.

Features

Automated Quiz Generation: Generate multiple-choice questions from PDF documents.
Advanced Text Embedding: Use embeddings to understand and process text.
Interactive Interface: Built with Streamlit for ease of use.
Secure and Scalable: Utilizes environment variables for secure API key handling and is optimized for efficient processing.
Technologies Used
Programming Languages: Python
Frameworks: Streamlit for building the web application interface

Tools and Libraries

DocumentProcessor: For processing PDF documents.

EmbeddingClient: For embedding and understanding text content.

ChromaCollectionCreator: For creating and managing Chroma collections.

QuizGenerator: For generating multiple-choice questions.

QuizManager: For managing quiz creation and user interaction.

Services: Vertex AI for advanced language models and embedding capabilities.

Install Dependencies:

Ensure you have Python 3.7+ installed. Install the required Python packages using pip:
pip install -r requirements.txt

Set Up Environment Variables:
Create a .env file in the root directory and add your API keys and other environment variables:
API_KEY=your_api_key_here

Usage

Run the Application:

Start the Streamlit app by running:
streamlit run app.py

Upload a PDF:
Use the web interface to upload a PDF document.

Generate Questions:
The application will process the document and generate multiple-choice questions which will be displayed on the interface.

Project Structure

.
├── app.py                     # Main application file for Streamlit

├── tasks                      # Directory containing task modules

│   ├── task_3.py              # DocumentProcessor module

│   ├── task_4.py              # EmbeddingClient module

│   ├── task_5.py              # ChromaCollectionCreator module

│   ├── task_6.py              

│   ├── task_7.py              

│   ├── task_8.py              # QuizGenerator module

│   └── task_9.py              # QuizManager module

├── requirements.txt           # Python dependencies

├── .env                       # Environment variables (not included in repo)

└── README.md                  # This README file

License:
This project is licensed under the MIT License. See the LICENSE file for details.
