import sqlite3
import google.generativeai as genai
import os

from dotenv import load_dotenv
load_dotenv() 
google_api_key = os.getenv('GOOGLE_API_KEY') 

from langchain_community.utilities import SQLDatabase
from langchain.prompts import FewShotPromptTemplate
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.prompts.prompt import PromptTemplate
import google.generativeai as genai
from langchain.llms.base import LLM
from typing import Optional, List 
from langchain_experimental.sql import SQLDatabaseChain
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


db_user = "root"
db_password = "vivek123"
db_host = "localhost"
db_name = "k_tshirts"

db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}",sample_rows_in_table_info=3)

genai.configure(api_key=google_api_key)

# Custom LangChain-compatible LLM for Gemini
class GeminiLLM(LLM):
    model: str = "gemini-1.5-flash"
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        model = genai.GenerativeModel(self.model)
        response = model.generate_content(prompt)
        try:
            generated_text = response.candidates[0].content.parts[0].text
        except (KeyError, IndexError):
            raise ValueError("Unexpected response format from Gemini model.")
        return (generated_text)

    @property
    def _llm_type(self) -> str:
        return "GeminiLLM"


llm=GeminiLLM()


few_shots = [
    {"Question": "How many white Nike t-shirts are available",
     "SQLQuery": "select sum(stock_quantity) from t_shirts where color='White' and brand='Nike';",
     'SQLResult':"[(Decimal('87'),)]",
      'Answer': "87"
     },
      {
     "Question": "How many black adidas tshirts are available",
     "SQLQuery": "select sum(stock_quantity) from t_shirts where color='Black' and brand='Adidas';",
     'SQLResult':"[(Decimal('235'),)]",
      "Answer": "235"
     },
     {
      "Question": "How many Red Nike t-shirts are left in the stock",
     "SQLQuery": "select sum(stock_quantity) from t_shirts where color='Red' and brand='Nike';",
     'SQLResult':"[(Decimal('136'),)]",
      "Answer": "136"
     },
     {
     "Question": "How many Black Adidas t-shirts are left in the stock",
     "SQLQuery": "select sum(stock_quantity) from t_shirts where color='Black' and brand='Adidas';",
     'SQLResult':"[(Decimal('235'),)]",
      "Answer": "235"
     },
     {
     "Question": "How many Blue Van huesen t-shirts are left in the stock",
     "SQLQuery": "select sum(stock_quantity) from t_shirts where color='Blue' and brand='Van Huesen';",
     'SQLResult':"[(Decimal('102'),)]",
      "Answer": "102"
     },
     {"Question": "what is the stock left for white Nike t-shirts",
     "SQLQuery": "select sum(stock_quantity) from t_shirts where color='White' and brand='Nike';",
     'SQLResult':"[(Decimal('87'),)]",
      'Answer': "87"
     },
      {
     "Question": "what is the stock left for Black Adidas t-shirts",
     "SQLQuery": "select sum(stock_quantity) from t_shirts where color='Black' and brand='Adidas';",
     'SQLResult':"[(Decimal('235'),)]",
      "Answer": "235"
     },
     {
      "Question": "what is the stock available for Red Nike t-shirts",
     "SQLQuery": "select sum(stock_quantity) from t_shirts where color='Red' and brand='Nike';",
     'SQLResult':"[(Decimal('136'),)]",
      "Answer": "136"
     },
      {
      "Question": "How many total van huesen tshirts are left",
     "SQLQuery": "select brand,sum(stock_quantity) as total from t_shirts where brand='Van Huesen';",
     'SQLResult':"[(Decimal('608'),)]",
      "Answer": "608"
     },
      {
      "Question": "How many total Nike tshirts are left",
     "SQLQuery": "select brand,sum(stock_quantity) as total from t_shirts where brand='Nike';",
     'SQLResult':"[(Decimal('675'),)]",
      "Answer": "675"
     },
      {
        "Question": "How many Nike t-shirts are there?",
        "SQLQuery": "select brand,sum(stock_quantity) as total from t_shirts where brand='Nike';",
        'SQLResult':"[(Decimal('675'),)]",
        "Answer": "675"
     },
      {
        "Question": "How many Adidas t-shirts are there?",
        "SQLQuery": "select brand,sum(stock_quantity) as total from t_shirts where brand='Adidas';",
        'SQLResult':"[(Decimal('884'),)]",
        "Answer": "884"
     },
      {
     "Question": "what is the revenue generatd if all the Black nike t shirts with discount sold out",
     "SQLQuery": "select sum(t1.price*t1.stock_quantity-((t1.price*t1.stock_quantity*t2.pct_discount)/100)) as rev from t_shirts t1 join discounts t2 on t1.t_shirt_id=t2.t_shirt_id where t1.brand='Nike' and t1.color='Black';",
     'SQLResult':"[(Decimal('799.2'),)]",
      "Answer": '799.200'   
     },
      {
     "Question": "what is the revenue generatd if all the Blue VanHuesen t shirts with discount sold out",
     "SQLQuery": "select sum(t1.price*t1.stock_quantity-((t1.price*t1.stock_quantity*t2.pct_discount)/100)) as rev from t_shirts t1 join discounts t2 on t1.t_shirt_id=t2.t_shirt_id where t1.brand='Van Huesen' and t1.color='Blue';",
     'SQLResult':"[(Decimal('399.0'),)]",
      "Answer": '399.0'   
     },
      {
     "Question": "what is the revenue generatd if all the levi red t shirts without discount sold out",
     "SQLQuery": "select sum(price*stock_quantity) as rev from t_shirts where brand='Levi' and color='Red' and t_shirt_id not in(select t_shirt_id from discounts);",
     'SQLResult':"[(Decimal('8886'),)]",
      "Answer": '8886'   
     },
     {
     "Question": "what is the revenue generatd if all the white adidas t shirts without discount sold out",
     "SQLQuery": "select sum(price*stock_quantity) as rev from t_shirts where brand='Adidas' and color='White' and t_shirt_id not in(select t_shirt_id from discounts);",
     'SQLResult':"[(Decimal('5024'),)]",
      "Answer": '5024'   
     },
      {
     "Question": "what is the revenue generatd if all the van huesen blue t shirts without discount sold out",
     "SQLQuery": "select sum(price*stock_quantity) as rev from t_shirts where brand='Van Huesen' and color='Blue' and t_shirt_id not in(select t_shirt_id from discounts);",
     'SQLResult':"[(Decimal('3872.0'),)]",
      "Answer": '3872.0'   
     },
      {
        "Question": "which brand has Highest number of tshirt stock quantity?",
        "SQLQuery": "SELECT brand,SUM(stock_quantity) as quantity from t_shirts GROUP BY brand order by quantity DESC LIMIT 1;",
        'SQLResult':"[('Adidas', Decimal('884'))]",
        "Answer": "The brand with the highest t-shirt stock quantity is Adidas with 884."
     },
     {
        "Question": "what is the total number of t shirts",
        "SQLQuery": "SELECT SUM(stock_quantity) as Total FROM t_shirts;",
        'SQLResult':"[(Decimal('2933'),)]",
        "Answer": "The total number of t-shirts is 2933"
     },
     {
        "Question": "what is the total number of t shirts present",
        "SQLQuery": "SELECT SUM(stock_quantity) as Total FROM t_shirts;",
        'SQLResult':"[(Decimal('2933'),)]",
        "Answer": "The total number of t-shirts is 2933"
     },
     {
        "Question": "what is the Total stock of t shirts",
        "SQLQuery": "SELECT SUM(stock_quantity) as Total FROM t_shirts;",
        'SQLResult':"[(Decimal('2933'),)]",
        "Answer": "The total number of t-shirts is 2933"
     },


]

to_join=[" ".join(x.values()) for x in few_shots]

embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
vectorstore=Chroma.from_texts(to_join,embedding=embeddings,metadatas=few_shots)

### my sql based instruction prompt
mysql_prompt = """You are a MySQL expert. Given an input question, first create a syntactically correct MySQL query to run, then look at the results of the query and return the answer to the input question.
Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per MySQL. You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Pay attention to use CURDATE() function to get the current date, if the question involves "today".

Use the following format:

Question: Question here
SQLQuery: Query to run with no pre-amble
SQLResult: Result of the SQLQuery
Answer: Final answer here

*Note: The Answer should match with SQLResult in the above format 

No pre-amble.
"""

def result(query):
    example_selector = SemanticSimilarityExampleSelector(
    vectorstore=vectorstore,
    k=3,)
    
    example_prompt = PromptTemplate(
    input_variables=["Question", "SQLQuery", "SQLResult","Answer",],
    template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",)
    
    few_shot_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix=mysql_prompt,
    suffix=PROMPT_SUFFIX,
    input_variables=["input", "table_info", "top_k"], #These variables are used in the prefix and suffix
    ) 
    new_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, prompt=few_shot_prompt)
    qts = new_chain.invoke(query)
    return qts  






