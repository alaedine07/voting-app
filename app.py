from flask import Flask,render_template,request,abort,flash,redirect
from wtforms import Form,StringField,validators
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask_debugtoolbar import DebugToolbarExtension
#APP_CONFIG
app = Flask(__name__)
toolbar = DebugToolbarExtension(app)
app.secret_key='*******'
#MYSQL_CONFIG
app.config['MYSQL_HOST'] = '******'
app.config['MYSQL_USER'] = '*******'
app.config['MYSQL_PASSWORD'] = '*******'
app.config['MYSQL_DB'] = '******'
#init mysql
mysql = MySQL(app)
#register_form_class
class RegistrationForm(Form):
    teacher_first_name = StringField('teacher_first_name', [validators.length(min=2, max=30)])
    teacher_last_name = StringField('teacher_last_name', [validators.length(min=2, max=30)])
    subject = StringField('subject', [validators.length(min=3, max=20)])
    institution = StringField('institution', [validators.length(min=3, max=50)])
#routes
@app.route('/search', methods=['GET', 'POST'])
def search():
    #handling the search system
    if request.method == 'POST' and 'find' in request.form: 
        teacher = request.form["find"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM teachers WHERE first_name = %s", (teacher,))
        details = cur.fetchall()
        return render_template("search.html", details = details)
        cur.close()
    #handling the rating system
    if request.method == 'POST' and 'rating' in request.form:
        rate = request.form["rating"]
        print(rate)
    return render_template("search.html")    
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        #getting data from form
        FirstName = form.teacher_first_name.data
        LastName = form.teacher_last_name.data
        Subject = form.subject.data
        Institution = form.institution.data
        #adding to database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO teachers (first_name,last_name,subject,institution) VALUES (%s,%s,%s,%s)", (FirstName,LastName,Subject,Institution))
        mysql.connection.commit()
        cur.close()
        flash("teacher has been added")
    return render_template('register.html', form = form)
if __name__ == "__main__":
    app.run(debug=True)    