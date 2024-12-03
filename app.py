from flask import Flask, render_template, request
from test import result

app = Flask(__name__)

# Cache-like function (can use Flask-Cache for production use)
def fetch_response(question):
    return result(question)

@app.route('/', methods=['GET'])
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
    
    print("myanswer",answer)
    if isinstance(answer, dict):  # Safeguard in case `answer` isn't a dictionary
            query = answer['query']
            answer =  answer['result']
    else:
        query = ""
        answer = answer 
    return render_template('submit.html', query=query,answer=answer)

@app.route('/contact',methods = ['GET'])
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=False)
