### About
Natural language is converted into sql queries using Gemini llm and langchain which is a framework to create applications upon llm.
This llm will have access to our database and converts the question to sql query and returns the answer. We need to add complex questions in few shot learning where llm
can't understand any complex questions given by the user.So, it uses semanticsimilarity examples to learn from it.


Home page:
![T-Shirt Image](images/home.png)
<br>

### To start the project
-> To run streamlit app:
> streamlit run main.py <br>
-> To run flask app:
> flask run <br>

Used local database , the sql query file is given at `database/sql.sql` <br>

###  Requirements
To install all the dependencies run
> pip install -r requirements.txt

### Deployment 
-> local sql database hosted on aiven web database <br>
-> Flask Application hosted on web through render <br>
-> The site can be viewed on Link https://svamretail.onrender.com <br>
(Note:The website may take a minute to load)