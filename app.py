from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from psycopg2 import connect

app = Flask(__name__)
ENV = 'dev'
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost/Elegance'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(55), unique=True)
    dealer = db.Column(db.String(50))
    rating = db.Column(db.Integer)
    service = db.Column(db.String(60))
    comments = db.Column(db.Text())

    def __init__(self,customer,dealer,rating,service,comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.service = service
        self.comments = comments

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/submit',methods =['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        service = request.form['service']
        comments = request.form['comments']
        #print(customer,dealer,rating,service,comments)
        if customer == '' or dealer == '':
            return render_template('homepage.html', message='Fill Required Fields.')
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer,dealer,rating,service,comments)
            db.session.add(data)
            db.session.commit()
            return render_template('success.html', message='successfully submitted.')
        return render_template('homepage.html', message='Your Feedback Was Submitted.')
if __name__ == '__main__':
    app.run()