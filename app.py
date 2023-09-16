import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template,request,redirect

with open('config.json','r') as json_file:
    parse = json.load(json_file)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = parse['database-uri']
db = SQLAlchemy(app)

class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)

    def __repr__(self) -> str:
        return f'{self.title} - {self.desc}'

@app.route('/')
def home():
    data = Contact.query.all()
    return render_template('index.html', data=data)

@app.route('/add-ct', methods=['GET','POST'])
def add_contact():
    if request.method == 'POST':
        name=request.form['name']
        phone=request.form['phone']
        email=request.form['email']
        address=request.form['address']
        sendTodb = Contact(name=name, phone=phone, email=email, address=address)
        db.session.add(sendTodb)
        db.session.commit()
        return redirect('/')
    return render_template('add.html')

@app.route('/update/<string:sno>', methods=['GET','POST'])
def update_contact(sno):
    if request.method=='POST':
            name=request.form['name']
            phone=request.form['phone']
            email=request.form['email']
            address=request.form['address']
            data = Contact.query.filter_by(sno=sno).first()
            data.name = name
            data.phone = phone
            data.email = email
            data.address = address
            db.session.commit()
            return redirect('/')
    data = Contact.query.filter_by(sno=sno).first()
    return render_template('update.html',data=data, sno=sno)

@app.route('/delete/<int:sno>', methods=["GET","POST"])
def delete_contact(sno):
    data = Contact.query.filter_by(sno=sno).first()
    db.session.delete(data)
    db.session.commit()
    return redirect('/')

@app.route('/search', methods=['GET', 'POST'])
def search_contact():
    if request.method == 'POST':
        search_query = request.form['search']
        contacts = Contact.query.filter(
            (Contact.name.contains(search_query)) |
            (Contact.email.contains(search_query)) |
            (Contact.address.contains(search_query)) |
            (Contact.phone.contains(search_query)) 
        ).all()
        return render_template('search.html', contacts=contacts, search_query=search_query)
    return render_template('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)