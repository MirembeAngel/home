from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from data import Articles
from flaskext.mysql import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from wtforms.validators import DataRequired, Length, Email,EqualTo
from passlib.hash import sha256_crypt

app = Flask(__name__)
# Config MySQL
app.config['MySQL_HOST'] = 'localhost'
app.config['MySQL_USER'] = 'root'
app.config['MySQL_PASSWORD'] = '123456'
app.config['MySQL_DB']= 'myflaskapp'
app.config['MySQL_CUSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)

Articles = Articles()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html',articles = Articles)

@app.route('/articles/<string:id>/')
def article(id):
    return render_template('articles.html',id=id)

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1,max=50)])
    username = StringField('Username', [validators.Length(min=4,max=25)])
    email = StringField('Email', [validators.Length(min=6,max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    
    confirm = PasswordField('confirm Password')

    
@app.route('/register', methods=['GET', 'POST' ])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        Password = shad256_crypt(str(form.password.data))
        #Create cursor
        cur = mysql.connection.cursor()
        #Execute query

        cur.excute("INSERT INTO users(name, email, username, password)VALUE(%s,%s,%s)",(name, email, username, password ) )
        # Commit to DB
        mysql.connection.Commit()

        # Close connection
        cur.close()

        flask('You are now registered and can log in','success')

        return redirect(url_for('login'))
    return render_template('register.html',form=form)    

if __name__ =='__main__':
    app.Secret_key='secret123'
    app.run(debug=True)        



