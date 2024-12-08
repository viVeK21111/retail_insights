from flask import Flask, render_template, request,jsonify
from test import result
from translate import translate
import MySQLdb


app = Flask(__name__)

# Configure database connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'vivek123'
app.config['MYSQL_DB'] = 'k_tshirts'

# Initialize database connection
db = MySQLdb.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    passwd=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB']
)
cursor = db.cursor()


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
    
    print("answer is : ",answer)
    if isinstance(answer, dict):  # Safeguard in case `answer` isn't a dictionary
            query = answer['query']
            answer =  answer['result']
    else:
        query = question
        if(len(answer)>300):
         answer = answer[-328:-61]
    return render_template('submit.html', query=query,answer=answer)

@app.route('/translate', methods=['POST'])
def api_translate():
    data = request.get_json()
    text = data['text']
    translated_text = translate(text)
    print("translated ",translated_text)
    return jsonify({"transtext":translated_text})

@app.route('/contact',methods = ['GET'])
def contact():
    return render_template('contact.html')


@app.route('/submitcontact', methods=['POST'])
def submit_contact():
    # Get form data
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    
    # Insert into database
    query = "INSERT INTO feedback (name, email, message) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, email, message))
    db.commit()
    
    return "Message Submitted Successfully!\n We will contact you soon."

if __name__ == '__main__':
    app.run(debug=True)

