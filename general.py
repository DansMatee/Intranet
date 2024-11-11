from flask import (
    Blueprint, redirect, render_template, url_for, jsonify, current_app, g, request
)

from MySQLdb.cursors import DictCursor

# from auth import login_required, role_required
from .auth import login_required, role_required

# from __init__ import get_mysql, log_user_action
from . import get_mysql, log_user_action

import html

bp = Blueprint('general', __name__)

@bp.route('/general', methods=['GET', 'POST'])
@login_required
@role_required('GENERAL')
def general():
    mysql = get_mysql()
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
        SELECT l.*, u.firstname, u.lastname
        FROM links l
        JOIN users u ON l.employee_id = u.id
        WHERE l.table_id LIKE 'general-%'
        ORDER BY l.timestamp DESC
    """)
    links = cur.fetchall()

    for link in links:
        if link['timestamp']:
            link['formatted_timestamp'] = link['timestamp'].strftime('%d/%m/%Y %H:%M')
        else:
            link['formatted_timestamp'] = None

    general_1_links = [entry for entry in links if entry['table_id'] == 'general-1']
    general_2_links = [entry for entry in links if entry['table_id'] == 'general-2']
    general_3_links = [entry for entry in links if entry['table_id'] == 'general-3']
    general_4_links = [entry for entry in links if entry['table_id'] == 'general-4']

    cur.execute("""
        SELECT j.*, u.firstname, u.lastname
        FROM jobs j
        JOIN users u ON j.employee_id = u.id
        WHERE j.table_id LIKE 'general-%'
        ORDER BY j.timestamp DESC
    """)
    jobs = cur.fetchall()

    for job in jobs:
        if job['timestamp']:
            job['formatted_timestamp'] = job['timestamp'].strftime('%d/%m/%Y %H:%M')
        else:
            job['formatted_timestamp'] = None

    general_1_jobs = [entry for entry in jobs if entry['table_id'] == 'general-1']
    general_2_jobs = [entry for entry in jobs if entry['table_id'] == 'general-2']
    general_3_jobs = [entry for entry in jobs if entry['table_id'] == 'general-3']
    general_4_jobs = [entry for entry in jobs if entry['table_id'] == 'general-4']

    cur.execute("""
        SELECT n.*, u.firstname, u.lastname
        FROM notices n
        JOIN users u ON n.employee_id = u.id
        WHERE n.table_id LIKE 'general-%'
        ORDER BY n.timestamp DESC
    """)
    notices = cur.fetchall()

    for notice in notices:
        if notice['timestamp']:
            notice['formatted_timestamp'] = notice['timestamp'].strftime('%d/%m/%Y %H:%M')
        else:
            notice['formatted_timestamp'] = None

    general_1_notices = [entry for entry in notices if entry['table_id'] == 'general-1']
    general_2_notices = [entry for entry in notices if entry['table_id'] == 'general-2']
    general_3_notices = [entry for entry in notices if entry['table_id'] == 'general-3']
    general_4_notices = [entry for entry in notices if entry['table_id'] == 'general-4']

    cur.execute("SELECT * FROM users WHERE permSet = 'GENERAL'")

    department_members = cur.fetchall()

    cur.close()

    return render_template('main/departments/general.html', 
        general_1_links=general_1_links, general_2_links=general_2_links, general_3_links=general_3_links, general_4_links=general_4_links,
        general_1_jobs=general_1_jobs, general_2_jobs=general_2_jobs, general_3_jobs=general_3_jobs, general_4_jobs=general_4_jobs,
        general_1_notices=general_1_notices, general_2_notices=general_2_notices, general_3_notices=general_3_notices, general_4_notices=general_4_notices,
        members=department_members
    )

@bp.route('/general/add_link', methods=['POST'])
@login_required
@role_required('GENERAL')
def add_link_general():
    data = request.get_json()
    tabId = data.get('tableId')
    linkName = html.escape(data.get('linkName'))
    linkDest = html.escape(data.get('linkDest'))

    if not isinstance(tabId, str):
        return jsonify({"error": "Not a string"}), 400
    if not isinstance(linkName, str):
        return jsonify({"error": "Not a string"}), 400
    if not isinstance(linkDest, str):
        return jsonify({"error": "Not a string"}), 400

    mysql = get_mysql()
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO links (table_id, link_name, link_dest, employee_id) VALUES (%s, %s, %s, %s)", (tabId, linkName, linkDest, g.user[0]))
    mysql.connection.commit()
    row_id = cur.lastrowid

    log_user_action(g.user[1], 
                    "Created New General Link", 
                    "User " + g.user[1] + " created new general link with ID: " + str(row_id) + " in general link section " + str(tabId) + ".")
    cur.close()


    return jsonify({"message": "Link added successfully!"}), 200

@bp.route('/general/edit_link', methods=['POST'])
@login_required
@role_required('GENERAL')
def edit_link_general():
    data = request.get_json()
    linkId = data.get('linkId')
    linkName = html.escape(data.get('linkName'))
    linkDest = html.escape(data.get('linkDest'))

    mysql = get_mysql()
    cur = mysql.connection.cursor()
    cur.execute("UPDATE links SET link_name = %s, link_dest = %s, timestamp = NOW() WHERE id = %s", (linkName, linkDest, linkId))
    mysql.connection.commit()

    log_user_action(g.user[1], 
                    "Updated General Link", 
                    "User " + g.user[1] + " updated general link with ID: " + str(linkId) + ", new details: Link Name: " + str(linkName) + ", Link Destination: " + str(linkDest) + ".")
    cur.close()

    return jsonify({"message": "Link updated successfully!"}), 200

@bp.route('/general/archive_link', methods=['POST'])
@login_required
@role_required('ADMIN')
def archive_link_general():
    data = request.get_json()
    linkId = data.get('linkId')

    mysql = get_mysql()
    cur = mysql.connection.cursor()
    cur.execute("UPDATE links SET archived = 1 WHERE id = %s", (linkId,))
    mysql.connection.commit()

    log_user_action(g.user[1], 
                    "Archived General Link", 
                    "User " + g.user[1] + " archived general link with ID: " + str(linkId) + ".")
    cur.close()

    return jsonify({"message": "Link archived successfully!"}), 200

@bp.route('/general/add_job', methods=['POST'])
@login_required
@role_required('GENERAL')
def add_job_general():
    data = request.get_json()
    tabId = data.get('tableId')
    jobNumber = data.get('jobNumber')
    severity = data.get('severity')
    jobHeader = data.get('jobHeader')
    jobDesc = data.get('jobDesc')

    mysql = get_mysql()
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO jobs (table_id, job_number, job_severity, job_header, job_desc, employee_id) VALUES (%s, %s, %s, %s, %s, %s)", (tabId, jobNumber, severity, jobHeader, jobDesc, g.user[0]))
    mysql.connection.commit()
    row_id = cur.lastrowid

    log_user_action(g.user[1], 
                    "Created New General Job", 
                    "User " + g.user[1] + " created new general job with ID: " + str(row_id) + " in general job section " + str(tabId) + ".")
    cur.close()


    return jsonify({"message": "Job added successfully!"}), 200

@bp.route('/general/edit_job', methods=['POST'])
@login_required
@role_required('GENERAL')
def edit_job_general():
    data = request.get_json()
    jobId = data.get('jobId')
    severity = data.get('severity')
    jobHeader = data.get('jobHeader')
    jobDesc = data.get('jobDesc')

    mysql = get_mysql()
    cur = mysql.connection.cursor()
    cur.execute("UPDATE jobs SET job_severity = %s, job_header = %s, job_desc = %s, timestamp = NOW() WHERE id = %s", (severity, jobHeader, jobDesc, jobId))
    mysql.connection.commit()

    log_user_action(g.user[1], 
                    "Updated General Job", 
                    "User " + g.user[1] + " updated general job with ID: " + str(jobId) + ", new details: Severity: " + str(severity) + ", Job Header: " + str(jobHeader) + ", Job Description: " + str(jobDesc) +  ".")
    cur.close()


    return jsonify({"message": "Job edited successfully!"}), 200

@bp.route('/general/archive_job', methods=['POST'])
@login_required
@role_required('GENERAL')
def archive_job_general():
    data = request.get_json()
    jobId = data.get('jobId')
    tableId = data.get('tableId')

    mysql = get_mysql()
    cur = mysql.connection.cursor()
    cur.execute("UPDATE jobs SET archived = 1, timestamp = NOW() WHERE id = %s", (jobId,))
    mysql.connection.commit()

    log_user_action(g.user[1], 
                    "Archived General Job", 
                    "User " + g.user[1] + " archived general job with ID: " + str(jobId) + " in general job section" + str(tableId) + ".")
    cur.close()


    return jsonify({"message": "Job archived successfully!"}), 200

@bp.route('/general/add_notice', methods=['POST'])
@login_required
@role_required('GENERAL')
def add_notice_general():
    data = request.get_json()
    tabId = data.get('tableId')
    noticeHeader = data.get('noticeHeader')
    noticeDesc = data.get('noticeDesc')

    mysql = get_mysql()
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO notices (table_id, notice_header, notice_desc, employee_id) VALUES (%s, %s, %s, %s)", (tabId, noticeHeader, noticeDesc, g.user[0]))
    mysql.connection.commit()
    row_id = cur.lastrowid

    log_user_action(g.user[1], 
                    "Created New General Notice", 
                    "User " + g.user[1] + " created new general notice with ID: " + str(row_id) + " in general notice section " + str(tabId) + ".")
    cur.close()


    return jsonify({"message": "Notice added successfully!"}), 200

@bp.route('/general/edit_notice', methods=['POST'])
@login_required
@role_required('GENERAL')
def edit_notice_general():
    data = request.get_json()
    noticeId = data.get('noticeId')
    noticeHeader = data.get('noticeHeader')
    noticeDesc = data.get('noticeDesc')

    mysql = get_mysql()
    cur = mysql.connection.cursor()
    cur.execute("UPDATE notices SET notice_header = %s, notice_desc = %s, timestamp = NOW() WHERE id = %s", (noticeHeader, noticeDesc, noticeId))
    mysql.connection.commit()

    log_user_action(g.user[1], 
                    "Updated General Notice", 
                    "User " + g.user[1] + " updated general notice with ID: " + str(noticeId) + ", new details: Notice Header: " + str(noticeHeader) + ", Notice Description: " + str(noticeDesc) + ".")
    cur.close()

    return jsonify({"message": "Notice updated successfully!"}), 200

@bp.route('/general/archive_notice', methods=['POST'])
@login_required
@role_required('ADMIN')
def archive_notice_general():
    data = request.get_json()
    noticeId = data.get('noticeId')

    mysql = get_mysql()
    cur = mysql.connection.cursor()
    cur.execute("UPDATE notices SET archived = 1 WHERE id = %s", (noticeId,))
    mysql.connection.commit()

    log_user_action(g.user[1], 
                    "Archived General Notice", 
                    "User " + g.user[1] + " archived general notice with ID: " + str(noticeId) + ".")
    cur.close()

    return jsonify({"message": "Notice archived successfully!"}), 200

@bp.route('/general/get_severities')
@login_required
@role_required('GENERAL')
def get_severities_general():
    mysql = get_mysql()
    cur = mysql.connection.cursor()
    query = '''
    SELECT job_severity, COUNT(*) as count
    FROM jobs
    WHERE table_id LIKE 'general-%'
    GROUP BY job_severity
    '''
    cur.execute(query)
    
    results = cur.fetchall()

    severity_data = {severity: count for severity, count in results}

    cur.close()
    return jsonify(severity_data)