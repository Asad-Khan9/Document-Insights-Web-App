# Document Insights Web App

Document Insights is a web application that allows users to extract insights from CSV or PDF documents using natural language prompts. Users can upload their documents, input queries, and receive responses tailored to their inquiries.

## Features

- Upload CSV or PDF documents.
- Input natural language prompts to query document insights.
- Backend server processes user prompts and document data using an LLM (Large Language Model) API.
- Responses include basic answers to the query, mathematically calculated results, or Python code for visualizing document contents.

## Getting Started

To run the web application locally, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/Asad-Khan9/Document-Insights-Web-App.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the Streamlit application:

    ```bash
    streamlit run streamlit_.py
    ```

4. Access the application in your web browser at `http://localhost:8501`.

## Dependencies

- Streamlit: Web application framework for building interactive web apps with Python.
- Pandas: Data manipulation library for processing CSV files.
- PyPDF2: Library for reading and extracting text from PDF documents.
- OpenAI: API for natural language processing tasks.
- Dotenv: Library for loading environment variables from a `.env` file.
