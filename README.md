# AI-Powered Quiz Builder

## Overview
The **AI-Powered Quiz Builder** is an innovative application designed to automatically generate multiple-choice questions from PDF documents. Leveraging advanced text embedding techniques and the capabilities of **Vertex AI**, this tool streamlines the quiz creation process for educational institutions, corporate training programs, and e-learning platforms.

## Introduction
This project focuses on developing an AI-powered application that generates multiple-choice questions from PDF documents. It utilizes **text embeddings** and the **Chroma collection** to ensure accurate and relevant question generation.

## Features
- **Automated Quiz Generation** – Automatically generate multiple-choice questions from PDF documents.
- **Advanced Text Embedding** – Uses embeddings to understand and process text efficiently.
- **Interactive Interface** – Built with **Streamlit** for a user-friendly experience.
- **Secure and Scalable** – Utilizes **environment variables** for secure API key handling and ensures optimized processing.

## Technologies Used
- **Programming Language:** Python
- **Frameworks:** Streamlit for building the web application interface

## Tools and Libraries
- **DocumentProcessor** – Processes PDF documents.
- **EmbeddingClient** – Embeds and understands text content.
- **ChromaCollectionCreator** – Creates and manages **Chroma collections**.
- **QuizGenerator** – Generates multiple-choice questions.
- **QuizManager** – Manages quiz creation and user interaction.
- **Services:** **Vertex AI** for advanced language models and embedding capabilities.

---

## Installation

### 1. Install Dependencies
Ensure you have **Python 3.7+** installed. Then, install the required Python packages using:
```
pip install -r requirements.txt
```
### 2. Set Up Environment Variables

Create a .env file in the root directory and add your API keys and other environment variables:
```
API_KEY=your_api_key_here
```
---

Usage

### 1. Run the Application

Start the Streamlit app by running:
```
streamlit run app.py
```
### 2. Upload a PDF

Use the web interface to upload a PDF document.

### 3. Generate Questions

The application will process the document and generate multiple-choice questions, which will be displayed on the interface.

---

Project Structure
```

.
├── app.py                     # Main application file for Streamlit
├── tasks                       # Directory containing task modules
│   ├── task_3.py               # DocumentProcessor module
│   ├── task_4.py               # EmbeddingClient module
│   ├── task_5.py               # ChromaCollectionCreator module
│   ├── task_6.py
│   ├── task_7.py
│   ├── task_8.py               # QuizGenerator module
│   └── task_9.py               # QuizManager module
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not included in repo)
└── README.md                   # Project documentation
```

---

License

This project is licensed under the MIT License. See the LICENSE file for more details.

