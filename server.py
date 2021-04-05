from flask import Flask, render_template, request, session, redirect, jsonify, flash
import data_handler as dh
import password_salter as ps

app = Flask(__name__)

app.secret_key = "123213"


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method ==  'POST':
        username = request.form['emailInput']
        password = ps.hash_password(request.form['passwordInput'])
        isTaken = dh.check_if_taken(username)
        if isTaken:
            flash('Username already exists, please choose another one!')
            return redirect('/registration')
        print(isTaken)
        dh.save_registered_user(username, password)        
        flash('Successful registration. Log in to continue.')
        return redirect('/login')    
    return render_template('registration.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["user"]
        password = request.form["password"]        
        try:
            hashed_password = dh.get_hashed_password(username)['password']
        except:
            flash('Wrong username or password.')
            return redirect('/login') 
        print(hashed_password)
        if ps.verify_password(request.form["password"], hashed_password):
            session['user'] = username
            return redirect('/')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
