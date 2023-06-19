# Langchain Implementaion of Various LLMs

## Introduction
In this project, we implement a Question Answering system using the LangChain framework and various Large Language Models. For the moment only Chatgpt is integrated, but we plan to integrate more LLMs in the future. The front-end for the project is implemented using Streamlit framework. 

The front-end allows to upload various documents, which are then stored in a local vector store. The user can then ask questions about the documents, and the system will return the most relevant answers.

For testing purposes 5 articles are provided in the Docs folder on which questions can be asked.

## Installation

1. Clone the repository
2. Create a text file names openai_ai_key.txt in the root directory of the project. This file should contain your OpenAI API key.
3. Create a virtual environment and install the requirements mentioned in requirements.txt.
4. Run the following command to start the streamlit app:
```
streamlit run StreamlitApp/app.py
```

## References

1. [LangChain](https://python.langchain.com)
2. [Streamlit](https://streamlit.io)
3. [OpenAI API](https://beta.openai.com)
4. [Vector Stores](https://python.langchain.com/docs/modules/data_connection/vectorstores/)
5. [Vector store-backed retriever](https://python.langchain.com/docs/modules/data_connection/retrievers/how_to/vectorstore)
6. [Chain Types](https://python.langchain.com/docs/modules/chains/document/)



