### About
Natural language is converted into sql queries using googlepalm llm by langchain which is a framework to create applications upon llm.
This llm will have access to our database and converts the question to sql query and returns the answer. We need to complext questions in few shot learning where llm
can't understand any complex questions given by the user.

### To start the project
> streamlit run main.py
<br>Used local database , the sql query file is given at /database

![T-Shirt Image](images/page.png)

###  Requirements
To install all the dependencies run
> pip install -r requirements.txt