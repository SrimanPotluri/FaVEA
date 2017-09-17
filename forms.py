# pythonspot.com
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import os.path
import Main
 
# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
 
class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])

 
@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)
 
    print form.errors
    if request.method == 'POST':
        name=request.form['name']
        #password=request.form['password']
        #email=request.form['email']

        #complete_path = os.path.abspath(name)
        #print complete_path
        Main.main("/Users/sriman/PycharmProjects/FaceRecognition1/Videos/Speech2.mp4")

        if form.validate():
            # Save the comment here.
            with open('output.txt', 'r') as myfile:
                data = myfile.read().replace('/n'," ")

            flash(data)

        else:
            flash('Error: All the form fields are required. ')
 
    return render_template('hello.html', form=form)

if __name__ == "__main__":
    app.run(port=int("5100"))

