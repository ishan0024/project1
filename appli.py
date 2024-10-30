from flask import Flask, session, redirect, url_for, request

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # You need to set a secret key for session encryption

@app.route('/')
def index():
    # Retrieve the number from the session, or set it to 0 if not present
    number = session.get('number', 0)
    return f'The number in the session is: {number}'

@app.route('/set_number', methods=['POST'])
def set_number():
    # Get the number from the form data and save it in the session
    number = request.form['number']
    session['number'] = int(number)
    return redirect(url_for('index'))

@app.route('/increment')
def increment():
    # Increment the number in the session
    session['number'] = session.get('number', 0) + 1
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)