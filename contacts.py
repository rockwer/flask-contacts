from flask import Flask, jsonify, request, render_template
from models import Contact
from forms import AddContactForm
from flask_mongoengine import MongoEngine
from flask_wtf.csrf import CSRFProtect
from mongoengine import *
from datetime import date

app = Flask(__name__)
app.config.from_pyfile('the-config.cfg')
app.debug = True
app.secret_key = '23sdf8794sdfua90f0a'
csrf = CSRFProtect(app)
mongo = MongoEngine(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contacts/', methods=['GET'])
def all_contacts():
    contacts = Contact.objects.all()
    contacts_output = []
    for contact in contacts:
        contacts_output.append({'id': str(contact.id), 'name': contact.name, 'phone': contact.phone, 'email': contact.email, 'registration_date': contact.registration_date})
    return jsonify({'contacts': contacts_output})
    
if __name__ == '__main__':
    app.run(debug=True)

@app.route('/contacts/<username>', methods=['GET'])
def get_contact(username):
    try:
        contacts = Contact.objects.filter(name = username)
        contacts_output = []
        for contact in contacts:
            contacts_output.append({'id': str(contact.id), 'name': contact.name, 'phone': contact.phone, 'email': contact.email, 'registration_date': contact.registration_date})
        return jsonify({'contacts': contacts_output})
    except Contact.DoesNotExist:
        return jsonify({'error': 'no contact with this name'})

@csrf.exempt
@app.route('/api/add-contact/', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        connect(mongo)
        new_contact = Contact()
        new_contact.name = request.form.get('name')
        new_contact.phone = request.form.get('phone')
        new_contact.email = request.form.get('email')
        new_contact.registration_date = str(date.today())
        new_contact.save()
        return jsonify({'error': 'succesful'})
    
if __name__ == '__main__':
    app.run(debug=True)

@app.route('/add-contact/', methods=['GET', 'POST'])
def add_contact_form():
    form = AddContactForm()
    if request.method == 'POST' and form.validate_on_submit():
        connect(mongo)
        new_contact = Contact()
        new_contact.name = form.name.data
        new_contact.phone = form.phone.data
        new_contact.email = form.email.data
        new_contact.registration_date = str(date.today())
        new_contact.save()
        return 'Contact added'
    return render_template("add_contact.html", form=form)
    
if __name__ == '__main__':
    app.run(debug=True)
    
@app.route('/delete/<id>', methods=['GET'])
def delete_contact(id):
    try:
        contacts = Contact.objects.get(id = id).delete()
        return jsonify({'status': 'deleted'})
    except Contact.DoesNotExist:
        return jsonify({'error': 'no contact with this id'})
    
if __name__ == '__main__':
    app.run(debug=True)