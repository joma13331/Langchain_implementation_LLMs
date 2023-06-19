import time
import langchain

from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.document_loaders import DirectoryLoader
from langchain.schema import Document
from langchain.text_splitter import TokenTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores.base import VectorStoreRetriever
from langchain.memory import ConversationBufferMemory

langchain.debug = True

class ConversationalRetrieverQA:

    def __init__(self) -> None:

        open_ai_api_key = open("./openai_api_key.txt", 'r').read().strip('/n')
        callbacks = [StreamingStdOutCallbackHandler()]
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.llm = ChatOpenAI(callbacks=callbacks, verbose=True, temperature=0.01, openai_api_key=open_ai_api_key)
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    def load_documents(self, folder_path = "./Docs")-> Document:
        loader = DirectoryLoader(folder_path)
        self.docs = loader.load()
        return self.docs
        
    def store_data_in_vector_store(self, chunk_size: int = 250, vector_store_type: str = "FAISS") -> None:
        documents = self.load_documents()
        text_splitter = TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)
        
        if vector_store_type == "FAISS":
            db = FAISS.from_documents(docs, self.embeddings)
            db.save_local(f"{vector_store_type}_index")

    
    def obtain_retriever_from_index(self,num_relevant_text, vector_store_type="FAISS", min_score=0.1) -> VectorStoreRetriever:
         
         db = FAISS.load_local(folder_path=f"{vector_store_type}_index", embeddings=self.embeddings)
         retriever = db.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": min_score,"k": num_relevant_text})

         return retriever
    
    def ask_question(self, query: str, num_relevant_text: int = 5, 
                     return_sources: bool = False, core_chains="stuff",
                     vector_store_type="FAISS", min_score=0.1):
         
        retriever = self.obtain_retriever_from_index(num_relevant_text=num_relevant_text, vector_store_type=vector_store_type, min_score=min_score)

        conv_retrieval_qa = ConversationalRetrievalChain.from_llm(
            llm=self.llm, 
            chain_type=core_chains, 
            retriever=retriever, 
            verbose=True,
            return_source_documents=return_sources,
            memory=self.memory
        )
        
        conv_retrieval_qa
        response = conv_retrieval_qa(query)

        return response