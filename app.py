from flask import Flask, render_template, request
from langchain_helper import get_few_shot_db_chain

app = Flask(__name__)

# Cache-like function (can use Flask-Cache for production use)
def fetch_response(question):
    chain = get_few_shot_db_chain(question)
    return chain.run(question)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/submit',methods=['POST','GET'])
def submit():
    answer = ""
    if request.method == 'POST':
        question = request.form['question']
        try:
            answer = fetch_response(question)
        except Exception as e:
            answer = f"An error occurred: {e}"

    return render_template('submit.html', answer=answer)

if __name__ == '__main__':
    app.run(debug=True)
