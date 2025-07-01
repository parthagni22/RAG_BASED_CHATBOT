import os
from src.utils import load_keys
#import asyncio
import time 
from pinecone import Pinecone 
# from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from pinecone import ServerlessSpec
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain.vectorstores import Pinecone as PineconeLang
from langchain_community.vectorstores.utils import DistanceStrategy

from langchain.document_loaders import PyPDFDirectoryLoader

from langchain.schema import (
    SystemMessage,
    HumanMessage
)

from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = load_keys()["openai"]
os.environ["PINECONE_API_KEY"] = load_keys()["pcsk_5iG23p_7bSMdSp7m9cRfDdVCeH9dyPJU4aZERYEXrudU8idA8Vrs7ArUfJ1BwC8sx2vb9g"]

class AggieeRag:

    def __init__(self) -> None:
        self.chatbot = ChatOpenAI( openai_api_key=os.environ["OPENAI_API_KEY"], model='gpt-4o-mini', temperature = 0.2)
        self.embeddings = OpenAIEmbeddings(model="text-embedding-ada-002",api_key=os.environ["OPENAI_API_KEY"])
        self.pine = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
        self.spec = ServerlessSpec(
                                    cloud="aws", region="us-east-1"
                                  )
        self.index_name = "indianconsti"
        self.index = self.init_pinecone()
        self.messages = [
            SystemMessage(content= """You are University Course Information Assistant, designed to provide accurate, reliable information about graduate-level courses and programs from the CSCE (Computer Science & Engineering) and ECEN (Electrical & Computer Engineering) departments at Texas A&M University, College Station. Your responses must be drawn exclusively from the PDFs you have access to, which include official course listings, degree requirements, and graduate handbooks.

When answering, provide detailed responses on:

Course descriptions, including credit hours and prerequisites.
Degree plan requirements for MS and PhD programs.
Specializations and research areas within each department.
Relevant rules, guidelines, or policies mentioned in the documents.
Ensure that all answers are factual and directly referenced from the PDFs, avoiding any interpretation or information beyond what is included in the provided documents.""")]

    def init_pinecone(self):
        # connect to index
        self.index = self.pine.Index(self.index_name)
        time.sleep(1)
        return self.index
    
    def generate_insert_embeddings_(self, docs):

        for j in range(len(docs)):
            embeddings = [{"metadata": ""}]

            ids = [str(j)]

            # Generate embeddings and ensure it's a flat list of floats
            embeds = self.embeddings.embed_documents(docs[j].page_content)
            embeddings[0]["metadata"]= str(docs[j].page_content)
            #print(embeds)
            # print(embeddings)
            self.index.upsert(vectors=zip(ids, embeds, embeddings))
    

    def chunk_data(self, docs,chunk_size=800,chunk_overlap=50):
        self.text_splitter=RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap)
        self.doc=self.text_splitter.split_documents(docs)
        return self.doc

    def read_doc(self, directory):
        file_loader=PyPDFDirectoryLoader(directory)
        documents=file_loader.load()

        return documents
    
    def augment_prompt(self, query: str):
        vectorstore = PineconeLang(
                        self.index,  self.embeddings.embed_query,"metadata", distance_strategy = DistanceStrategy.DOT_PRODUCT
                        )
        # get top 3 results from knowledge base
        results = vectorstore.similarity_search(query, k=2)
        # get the text from the results
        source_knowledge = "\n".join([x.page_content for x in results])
        # feed into an augmented prompt
        augmented_prompt = f"""Using the contexts below, answer the query.

        Contexts:
        {source_knowledge}

        Query: {query}"""
        return augmented_prompt
    

    
# if __name__ == "__main__":

#     llm = AggieeRag()

#     ######################################################################
#     ##To Generate new embedding -- Uncomment below line of code--
#     print("Embedding Started")
#     doc = llm.read_doc("Database/")
#     documents=llm.chunk_data(docs=doc)
#     #print(len(documents))
#     embeddings = llm.generate_insert_embeddings_(documents)
#     #####################################################################

    # query = "what is degree requirement for MS in. computer engineering non thesis ecen department of texas a&m university"
    # prompt = asyncio.run(llm.augment_prompt(query=query))
    # prompt = HumanMessage(
    # content=prompt
    # )

    # llm.messages.append(prompt)

    # res = llm.chatbot(llm.messages)
    # print("#############----Output----###########################")
    # print(res.content)


#-----------------------------------------------  MRR Testing #-----------------------------------------------#-----------------------------------------------#-----------------------------------------------#-----------------------------------------------
        # def chunk_data(self, docs,chunk_size=800,chunk_overlap=50):

    #     #self.text_splitter=RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap)
    #     self.text_splitter = SemanticChunker(
    #         embeddings=self.embeddings,
    #         buffer_size=1,
    #         add_start_index=False,
    #         breakpoint_threshold_type="percentile",
    #         breakpoint_threshold_amount=95.0,
    #         sentence_split_regex=r"(?<=[.?!])\s+"
    #     )
        
    #     self.doc=self.text_splitter.split_documents(docs)
    #     #print(self.doc)
    #     return self.doc
    
        # async def augment_prompt(self, query: str, mmr_lambda: float = 0.5):
    #     vectorstore = PineconeLang(
    #                     self.index,  self.embeddings.embed_query,"metadata", distance_strategy = DistanceStrategy.COSINE
    #                     )
    #     results = await vectorstore.amax_marginal_relevance_search(query, k=3, fetch_k=10, lambda_mult=mmr_lambda)
    #     # get top 3 results from knowledge base
    #     #results = vectorstore.similarity_search(query, k=3)
    #     # get the text from the results
    #     print(results)
    #     source_knowledge = "\n".join([x.page_content for x in results])
    #     print("*************************************************************************************************************************************")
    #     print(source_knowledge)
    #     print("*************************************************************************************************************************************")

    #     # feed into an augmented prompt
    #     augmented_prompt = f"""Using the contexts below, answer the query.

    #     Contexts:
    #     {source_knowledge}

    #     Query: {query}"""
    #     return augmented_prompt
