from flask import Flask, render_template, request, redirect, url_for, session , jsonify
import mysql.connector
import bcrypt

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="helloSatish@123",
    database="encryption_app"
)

cursor = db.cursor()

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.json['email']  # Get JSON data
    password = request.json['password'].encode('utf-8')

    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if user:
        db_password = user[3].encode('utf-8')
        if bcrypt.checkpw(password, db_password):
            session['user'] = user[1]
            return jsonify({'status': 'success', 'message': 'Login successful! Redirecting...'})
        else:
            return jsonify({'status': 'error', 'message': 'Invalid password. Please try again.'})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid email. Please try again.'})

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password'].encode('utf-8')

    # Hash the password
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

    # Store user in database
    try:
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", 
                       (name, email, hashed_password))
        db.commit()
        return redirect(url_for('login_page'))
    except mysql.connector.IntegrityError:
        return "Email already exists, <a href='/'>try again</a>."

@app.route('/home')
def home():
    if 'user' in session:
        return render_template('home.html', user=session['user'])  # Pass user to the template
    else:
        return redirect(url_for('login_page'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login_page'))

if __name__ == "__main__":
    app.run(debug=True)
