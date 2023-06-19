"""
This python file will create a web app using streamlit. The app will sattisfy the following requirements:
1. There will be a sidebar with the following options:
    a. A Home Page
    b. A web page to upload documents and create a vector store out of them
    c. A web page to ask questions and get answers from the vector store
    d. A web page to ask questions and get answers from the vector store using a conversational approach

2. The web page to upload documents will have the following options:
    a. A file uploader to upload documents
    b. An input box to enter chunk size
    c. a dropdown to select the type of vector store
    d. A button to create the vector store

3. The web page to ask questions will have the following options:
    a. An input box to enter the number of relevant text to consider for the answer
    b. An input box to enter the question
    c. A button to select whether sources should be returned
    d. A radio button to select which core chains for working with Documents  
    e. A text box to display the answer    

4. The Home Page will have the following information:
    a. A brief description of the project
    
"""
import os
import streamlit as st
from ChatGpt.SimpleRetrieverQA import SimpleRetrieverQA
from ChatGpt.ConversationalRetrieverQA import ConversationalRetrieverQA



# setting the title of the web app
st.title("Question Answering System Using Large Language Models and Langchain")

# Creating a sidebar
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", ["Home", "Upload Documents", "Ask Questions", "Ask Questions Using Conversational Approach"])

# Creating a home page
if selection == "Home":

    # A subheader for the home page
    st.subheader("Home")

    # Brief description of the project
    st.write("This is a web app that uses large language models and langchain to answer questions.") 
    st.write("It provides a simple interface to upload documents and create a vector store out of them. It also provides an interface to ask questions and get answers from the vector store.")

    # Describe what the sidebar options do
    st.write("The sidebar options are as follows:")
    st.write("1. Home: This is the home page. It contains a brief description of the project.")
    st.write("2. Upload Documents: This page allows you to upload documents and create a vector store out of them.")
    st.write("3. Ask Questions: This page allows you to ask questions and get answers from the vector store.")
    st.write("4. Ask Questions Using Conversational Approach: This page allows you to ask questions and get answers from the vector store using a conversational approach.")

elif selection == "Upload Documents":
    
    # A subheader for the upload documents page
    st.subheader("Upload Documents")

    # A file uploader to upload documents
    st.write("Upload the documents you want to create a vector store out of.")
    uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=True)

    # An input box to enter chunk size
    st.write("Enter the chunk size for the vector store.")
    chunk_size = st.number_input("Enter the chunk size", min_value=1, max_value=1024, value=250, step=1)

    # a dropdown to select the type of vector store
    st.write("Select the type of vector store you want to create.")
    vector_store_type = st.selectbox("Select the type of vector store", ["FAISS", "ElasticVectorSearch"])


    # A button to create the vector store
    st.write("Click the button below to create the vector store.")
    create_vector_store = st.button("Create Vector Store")

    # If the user clicks the create vector store button
    if create_vector_store:
        # If the user has not uploaded any files
        if uploaded_files is None:
            st.write("Please upload some files.")
        # If the user has uploaded some files
        else:
            # Create a folder to store the uploaded files
            folder_path = "./Docs"
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)
            # Save the uploaded files in the folder
            for uploaded_file in uploaded_files:
                with open(os.path.join(folder_path, uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())
            # Create a vector store out of the uploaded files
            SimpleRetrieverQA.store_data_in_vector_store(chunk_size=chunk_size, vector_store_type=vector_store_type)
            st.write("Vector store created successfully.")

elif selection == "Ask Questions":
    
    # A subheader for the ask questions page
    st.subheader("Ask Questions")

    chatgpt_utils = SimpleRetrieverQA()

    # a dropdown to select the type of vector store
    st.write("Select the vector store you want to access.")
    vector_store_type = st.selectbox("Select the vector store you want to access.", ["FAISS", "ElasticVectorSearch"])

    # An input box to enter the number of relevant text to consider for the answer
    st.write("Enter the number of relevant text to consider for the answer.")
    num_relevant_text = st.number_input("Enter the number of relevant text", min_value=1, max_value=20, value=5, step=1)

    # An input box to enter the question
    st.write("Enter the question you want to ask.")
    question = st.text_input("Enter the question")

    # A button to select whether sources should be returned
    st.write("Select whether you want to return the sources.")
    return_sources = st.checkbox("Return Sources")

    # An input box to enter the minimum score to consider for the answer
    st.write("Enter the minimum score to consider for the answer.")
    min_score = st.number_input("Enter the minimum score", min_value=0.0, max_value=1.0, value=0.1, step=0.1)

    # A radio button to select which core chains for working with Documents
    st.write("Select which core chains for working with Documents.")
    core_chains = st.radio("Select which core chains for working with Documents", ["stuff", "refine", "map_reduce", "map_rerank"])

    # A button to ask the question
    st.write("Click the button below to ask the question.")
    ask_question = st.button("Ask Question")

    # If the user clicks the ask question button
    if ask_question:
        # If the user has not created a vector store
        if not os.path.exists(f"{vector_store_type}_index") and vector_store_type == "FAISS":
            st.write("Please create a vector store first.")
        # If the user has created a vector store
        else:
            # Ask the question
            response = chatgpt_utils.ask_question(query=question, num_relevant_text=num_relevant_text, 
                                                  return_sources=return_sources, core_chains=core_chains,
                                                  vector_store_type=vector_store_type, min_score=min_score)
            # Print the response in a text box
            st.write(response)

elif selection == "Ask Questions Using Conversational Approach":

    # A subheader for the ask questions using conversational approach page
    st.subheader("Ask Questions Using Conversational Approach")

    # A radio button to select whether to use previous context
    st.write("Select whether you want to use previous context.")
    use_previous_context = st.radio("Select whether you want to use previous context", ["Yes", "No"])

    if use_previous_context == "No":
        st.session_state.chatgpt_utils = ConversationalRetrieverQA()

    # Creating a session state to store the utils
    if st.session_state.get("chatgpt_utils", None) is None:
        st.session_state.chatgpt_utils = ConversationalRetrieverQA()

    # a dropdown to select the type of vector store
    st.write("Select the vector store you want to access.")
    vector_store_type = st.selectbox("Select the vector store you want to access.", ["FAISS", "ElasticVectorSearch"])

    # An input box to enter the number of relevant text to consider for the answer
    st.write("Enter the number of relevant text to consider for the answer.")
    num_relevant_text = st.number_input("Enter the number of relevant text", min_value=1, max_value=20, value=5, step=1)

    # An input box to enter the question
    st.write("Enter the question you want to ask.")
    question = st.text_input("Enter the question")


    # An input box to enter the minimum score to consider for the answer
    st.write("Enter the minimum score to consider for the answer.")
    min_score = st.number_input("Enter the minimum score", min_value=0.0, max_value=1.0, value=0.1, step=0.1)

    # A radio button to select which core chains for working with Documents
    st.write("Select which core chains for working with Documents.")
    core_chains = st.radio("Select which core chains for working with Documents", ["stuff", "refine", "map_reduce", "map_rerank"])

    # A button to ask the question
    st.write("Click the button below to ask the question.")
    ask_question = st.button("Ask Question")

    # If the user clicks the ask question button
    if ask_question:
        # If the user has not created a vector store
        if not os.path.exists(f"{vector_store_type}_index") and vector_store_type == "FAISS":
            st.write("Please create a vector store first.")
        # If the user has created a vector store
        else:
            # Ask the question
            response = st.session_state.chatgpt_utils.ask_question(query=question, num_relevant_text=num_relevant_text, 
                                                  return_sources=False, core_chains=core_chains,
                                                  vector_store_type=vector_store_type, min_score=min_score)
            # Print the response in a text box
            st.write(response)

    




            



