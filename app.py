from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session management

# In-memory data storage (use a database in production)
users = []


# Route for Signup Page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_data = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "password": request.form['password'],
            "confirm_password": request.form['confirm_password'],
            "email_id": request.form['email_id'],
            "phone_no": request.form['phone_no'],
            "manager_name": request.form['manager_name']
        }

        # Basic validation
        if user_data['password'] != user_data['confirm_password']:
            return "Passwords do not match", 400

        # Check if the email already exists
        if any(user['email_id'] == user_data['email_id'] for user in users):
            return "Email already registered", 400

        # Save user data (In real-world applications, save to a database)
        users.append(user_data)
        return redirect(url_for('login'))

    return render_template('signup.html')


# API to fetch all users (Admin or Manager API)
@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify(users)


# Route for Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email_id']
        password = request.form['password']

        # Validate the credentials
        user = next((u for u in users if u['email_id'] == email and u['password'] == password), None)

        if user:
            session['user'] = user
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials", 400

    return render_template('login.html')


# Route for Dashboard (after login)
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    return render_template('dashboard.html', users=users)


# Logout Route
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
