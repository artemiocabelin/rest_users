from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector

app = Flask(__name__)
app.secret_key = 'Secret'
mysql = MySQLConnector(app,'super_friends')

@app.route('/')
def index():
    return redirect('/users')

@app.route('/users')
def users():
    select_query = "SELECT *,DATE_FORMAT(created_at, '%M %D %Y') AS date_created FROM users"
    user_data = mysql.query_db(select_query)
    return  render_template('index.html', index_users = user_data)


# Creates new users
@app.route('/users/new')
def add_new():
    return render_template('create.html')

@app.route('/users/create', methods=['POST'])
def create_new():
    form = request.form
    insert_query = "INSERT INTO users (first_name, last_name, email, created_at) VALUES (:first_name, :last_name, :email, NOW())"
    query_data = {
        'first_name' : form['first_name'],
        'last_name' : form['last_name'],
        'email'     : form['email']
    }
    new_user = mysql.query_db(insert_query, query_data)
    return redirect('/users')

# Show a User
@app.route('/users/<user_id>')
def show_user(user_id):
    user = mysql.query_db("SELECT *,DATE_FORMAT(created_at, '%M %D %Y') AS date_created FROM users WHERE id = :id", {'id':user_id})
    return render_template('show.html', user = user)

# Delete a user
@app.route('/users/<user_id>/delete')
def delete_user(user_id):
    user = mysql.query_db("DELETE FROM users WHERE id = :id", {'id':user_id})
    return redirect('/users')

# Edit a user
@app.route('/users/<user_id>/edit')
def edit_user(user_id):
    user = mysql.query_db("SELECT *,DATE_FORMAT(created_at, '%M %D %Y') AS date_created FROM users WHERE id = :id", {'id':user_id})
    return render_template('edit.html', user=user)

@app.route('/users/<user_id>/update', methods=['POST'])
def update_user(user_id):
    form = request.form
    update_query = 'UPDATE users SET first_name = :first_name, last_name = :last_name, email = :email WHERE id = :id'
    query_data = {
        'id'         :  user_id,
        'first_name' :  form['first_name'],
        'last_name'  :  form['last_name'],
        'email' :  form['email']
    }
    user = mysql.query_db(update_query,query_data)
    return redirect('/users')

app.run(debug=True)