# Langchain Implementaion of Various LLMs

## Introduction
In this project, we implement a Question Answering system using the LangChain framework and various Large Language Models. For the moment only Chatgpt is integrated, but we plan to integrate more LLMs in the future. The front-end for the project is implemented using Streamlit framework. 

The front-end allows to upload various documents, which are then stored in a local vector store. The user can then ask questions about the documents, and the system will return the most relevant answers.

Question answering can be done in two ways:
1. Using A Simple Retriever: This method answers one question at a time with no history of previously asked questions.
2. Using a Conversational Retriever: This method allows to ask multiple questions in a conversation. The system will keep track of the previously asked questions and will try to answer the new question in the context of the previous questions.

For testing purposes 5 articles are provided in the Docs folder on which questions can be asked.

## Installation

1. Clone the repository
2. Create a text file names openai_ai_key.txt in the root directory of the project. This file should contain your OpenAI API key.
3. Create a virtual environment and install the requirements mentioned in requirements.txt.
4. Run the following command from the root directory of the project to start the streamlit app:
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
7. [Conversation buffer memory](https://python.langchain.com/docs/modules/memory/how_to/buffer)
8. [Conversational Retrieval QA](https://python.langchain.com/docs/modules/chains/popular/chat_vector_db)



