import functools

from flask import (
    Blueprint, g, redirect, render_template, url_for, request, session, jsonify
)

from werkzeug.security import generate_password_hash, check_password_hash

# from __init__ import get_mysql, log_user_action
from . import get_mysql, log_user_action

bp = Blueprint('auth', __name__)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view

def role_required(role):
    def decorator(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if g.user and (g.user[4] == role or g.user[4] == 'ADMIN'):
                return view(**kwargs)
            
            return redirect(url_for('mainview.index'))
        return wrapped_view
    return decorator

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form_type = request.form.get('form_type')

        if form_type == 'login':
            username = request.form.get('username')
            password = request.form.get('password')
            mysql = get_mysql()
            cur = mysql.connection.cursor()
            error = None

            cur.execute("SELECT * FROM users WHERE username = %s", [username])
            user = cur.fetchone()
            cur.close()

            if user is None:
                error = 'Incorrect username.'
            elif not check_password_hash(user[2], password):
                error = 'Incorrect password.'
            
            if error is None:
                if user[3] == 0:
                    return redirect(url_for('auth.activate'))
                else:
                    session.clear()
                    session['user_id'] = user[0]
                    return redirect(url_for('mainview.index'))



    return render_template('auth/login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        form_type = request.form.get('form_type')

        if form_type == 'register':
            username = request.form.get('username')
            password = generate_password_hash(request.form.get('password'))
            repeatpassword = request.form.get('repeatpassword')
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            email = request.form.get('email')

            mysql = get_mysql()
            cur = mysql.connection.cursor()
            error = None

            if not username:
                error = 'Username is required.'
            elif not password:
                error = 'Password is required.'
            elif not check_password_hash(password, repeatpassword):
                error = 'Passwords do not match.'

            if error is None:
                x = cur.execute("SELECT * FROM users WHERE username = (%s)", (username,))

                if int(x) > 0:
                    error = f"User {username} is already registered."
                else:
                    cur.execute("INSERT INTO users (username, password, firstname, lastname, email) VALUES (%s, %s, %s, %s, %s)", (username, password, firstname, lastname, email))
                    mysql.connection.commit()
                    cur.close()

                    return redirect(url_for("auth.login"))

    return render_template('auth/register.html')

@bp.route('/activate')
def activate():
    return render_template('auth/activate.html')

@bp.route('/activate_user', methods=['POST'])
@login_required
@role_required('ADMIN')
def activate_user():
    data = request.get_json()
    uid = data.get('id')
    
    mysql = get_mysql()
    cur = mysql.connection.cursor()

    cur.execute("UPDATE users SET isActive = 1 WHERE id = %s", [uid])
    cur.connection.commit()
    cur.close()

    log_user_action(g.user[1], "Activated User", "User " + str(g.user[1]) + " activated account id: " + str(uid) + ".")

    return jsonify({"message": "User activated successfully!"}), 200

@bp.route('/update_user', methods=['POST'])
@login_required
@role_required('ADMIN')
def update_user():
    data = request.get_json()
    uid = data.get('id')
    permSet = data.get('permSet')
    dptAdmin = data.get('dptAdmin')
    isActive = data.get('isActive')

    mysql = get_mysql()
    cur = mysql.connection.cursor()

    cur.execute("UPDATE users SET isActive = %s, permSet = %s, departmentAdmin = %s WHERE id = %s", [isActive, permSet, dptAdmin, uid])
    cur.connection.commit()
    cur.close()

    log_user_action(g.user[1], "Updated User", 
                    "User " + str(g.user[1]) + " updated account id: " + str(uid) + ", new account settings: Is Active: " + str(isActive) + ", Permissions: " + str(permSet) + ", Department Admin: "
                      + str(dptAdmin) + ".")

    return jsonify({"message": "User updated successfully!"}), 200


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('mainview.index'))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        mysql = get_mysql()
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE id = %s", [user_id,])
        g.user = cur.fetchone()
        cur.close()