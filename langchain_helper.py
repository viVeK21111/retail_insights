
#from langchain.llms import GooglePalm
""" googlepalm api is stopped by google """

# using gemini from geni
import google.generativeai as genai
from langchain.llms.base import LLM
from typing import Optional, List

from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.prompts import FewShotPromptTemplate
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX
from langchain.prompts.prompt import PromptTemplate
from few_shorts import few_shots
from sql_prompt import mysql_prompt 
from dbaiven import db_userr,db_passwordd,db_hostt,db_namee,db_users,db_hosts,db_names,db_passwords
#from keys import google_api_key
import os 
#from dotenv import load_dotenv
#load_dotenv()
google_api_key = os.getenv('GOOGLE_API_KEY') 


def get_few_shot_db_chain(question):
    
    db_user = db_userr
    db_password = db_passwordd
    db_host = db_hostt 
    db_name = db_namee

    genai.configure(api_key=google_api_key)
    class GeminiLLM(LLM):
        model: str = "gemini-1.5-flash"
        def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
            model = genai.GenerativeModel(self.model)
            response = model.generate_content(prompt)
            generated_text = response.candidates[0].content.parts[0].text
            return (generated_text)

        @property #(Decorator where the method can be accesses as variable by an instance)
        def _llm_type(self) -> str:
            return "GeminiLLM"

    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}",
                              sample_rows_in_table_info=3)
    #llm = GooglePalm(google_api_key=google_api_key, temperature=0.2)
    llm=GeminiLLM()
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    to_vectorize = [" ".join(example.values()) for example in few_shots]

    vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=few_shots)

    
    example_selector = SemanticSimilarityExampleSelector(
        vectorstore=vectorstore,
        k=2,
    )
    example_selector.select_examples({"Question": question})

    example_prompt = PromptTemplate(
        input_variables=["Question", "SQLQuery", "SQLResult","Answer",],
        template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",
    )

    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix=mysql_prompt,
        suffix=PROMPT_SUFFIX,
        input_variables=["input", "table_info", "top_k"], #These variables are used in the prefix and suffix
    )
    chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, prompt=few_shot_prompt)
    return chain
