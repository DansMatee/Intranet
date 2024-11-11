from flask import (
    Blueprint, redirect, render_template, url_for, jsonify, current_app, g, request
)

from MySQLdb.cursors import DictCursor

# from auth import login_required, role_required
from .auth import login_required, role_required

# from __init__ import get_mysql, log_user_action
from . import get_mysql, log_user_action

import html

bp = Blueprint('mainview', __name__)

@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():

    return render_template('main/index.html')

@bp.route('/admin', methods=['GET', 'POST'])
@login_required
@role_required('ADMIN')
def admin():
    mysql = get_mysql()
    cur = mysql.connection.cursor()
    cur.execute("SELECT username, action, `desc`, ip_address, timestamp FROM logs ORDER BY timestamp DESC")
    log_entries = cur.fetchall()

    logs = [
        {
            "username": entry[0],
            "action": entry[1],
            "desc": entry[2],
            "ip_address": entry[3],
            "timestamp": entry[4].strftime('%d/%m/%Y %H:%M')
        }
        for entry in log_entries
    ]

    cur.execute("SELECT * FROM users WHERE isActive = 1")
    real_users = cur.fetchall()

    users = [
        {
            "id": entry[0],
            "username": entry[1],
            "permSet": entry[4],
            "name": entry[5] + " " + entry[6],
            "email": entry[7],
            "departmentAdmin": entry[8],
            "active": entry[3]
        }
        for entry in real_users
        if entry[0] != g.user[0]
    ]

    cur.execute("SELECT * FROM users WHERE isActive = 0")
    pending_users = cur.fetchall()
    cur.close()

    pend_users = [
        {
            "id": entry[0],
            "username": entry[1],
            "permSet": entry[4],
            "name": entry[5] + " " + entry[6],
            "email": entry[7]
        }
        for entry in pending_users
    ]

    return render_template('main/admin.html', logs=logs, users=users, pusers=pend_users)  