from flask import (
    Blueprint, redirect, render_template, url_for, jsonify, current_app, g, request
)

from MySQLdb.cursors import DictCursor

# from auth import login_required, role_required
from .auth import login_required, role_required

# from __init__ import get_mysql, log_user_action
from . import get_mysql, log_user_action

import html

bp = Blueprint('support', __name__)

@bp.route('/support', methods=['GET', 'POST'])
@login_required
@role_required('SUPPORT')
def support():
    mysql = get_mysql()
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
        SELECT l.*, u.firstname, u.lastname
        FROM links l
        JOIN users u ON l.employee_id = u.id
        WHERE l.table_id LIKE 'support-%'
        ORDER BY l.timestamp DESC
    """)
    links = cur.fetchall()

    for link in links:
        if link['timestamp']:
            link['formatted_timestamp'] = link['timestamp'].strftime('%d/%m/%Y %H:%M')
        else:
            link['formatted_timestamp'] = None

    support_1_links = [entry for entry in links if entry['table_id'] == 'support-1']
    support_2_links = [entry for entry in links if entry['table_id'] == 'support-2']
    support_3_links = [entry for entry in links if entry['table_id'] == 'support-3']
    support_4_links = [entry for entry in links if entry['table_id'] == 'support-4']

    cur.execute("""
        SELECT j.*, u.firstname, u.lastname
        FROM jobs j
        JOIN users u ON j.employee_id = u.id
        WHERE j.table_id LIKE 'support-%'
        ORDER BY j.timestamp DESC
    """)
    jobs = cur.fetchall()

    for job in jobs:
        if job['timestamp']:
            job['formatted_timestamp'] = job['timestamp'].strftime('%d/%m/%Y %H:%M')
        else:
            job['formatted_timestamp'] = None

    support_1_jobs = [entry for entry in jobs if entry['table_id'] == 'support-1']
    support_2_jobs = [entry for entry in jobs if entry['table_id'] == 'support-2']
    support_3_jobs = [entry for entry in jobs if entry['table_id'] == 'support-3']
    support_4_jobs = [entry for entry in jobs if entry['table_id'] == 'support-4']

    cur.execute("""
        SELECT n.*, u.firstname, u.lastname
        FROM notices n
        JOIN users u ON n.employee_id = u.id
        WHERE n.table_id LIKE 'support-%'
        ORDER BY n.timestamp DESC
    """)
    notices = cur.fetchall()

    for notice in notices:
        if notice['timestamp']:
            notice['formatted_timestamp'] = notice['timestamp'].strftime('%d/%m/%Y %H:%M')
        else:
            notice['formatted_timestamp'] = None

    support_1_notices = [entry for entry in notices if entry['table_id'] == 'support-1']
    support_2_notices = [entry for entry in notices if entry['table_id'] == 'support-2']
    support_3_notices = [entry for entry in notices if entry['table_id'] == 'support-3']
    support_4_notices = [entry for entry in notices if entry['table_id'] == 'support-4']

    cur.execute("SELECT * FROM users WHERE permSet = 'SUPPORT'")

    department_members = cur.fetchall()

    cur.close()

    return render_template('main/departments/support.html', 
        support_1_links=support_1_links, support_2_links=support_2_links, support_3_links=support_3_links, support_4_links=support_4_links,
        support_1_jobs=support_1_jobs, support_2_jobs=support_2_jobs, support_3_jobs=support_3_jobs, support_4_jobs=support_4_jobs,
        support_1_notices=support_1_notices, support_2_notices=support_2_notices, support_3_notices=support_3_notices, support_4_notices=support_4_notices,
        members=department_members
    )

@bp.route('/support/add_link', methods=['POST'])
@login_required
@role_required('SUPPORT')
def add_link_support():
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
                    "Created New Support Link", 
                    "User " + g.user[1] + " created new support link with ID: " + str(row_id) + " in support link section " + str(tabId) + ".")
    cur.close()


    return jsonify({"message": "Link added successfully!"}), 200

@bp.route('/support/edit_link', methods=['POST'])
@login_required
@role_required('SUPPORT')
def edit_link_support():
    data = request.get_json()
    linkId = data.get('linkId')
    linkName = html.escape(data.get('linkName'))
    linkDest = html.escape(data.get('linkDest'))

    mysql = get_mysql()
    cur = mysql.connection.cursor()
    cur.execute("UPDATE links SET link_name = %s, link_dest = %s, timestamp = NOW() WHERE id = %s", (linkName, linkDest, linkId))
    mysql.connection.commit()

    log_user_action(g.user[1], 
                    "Updated Support Link", 
                    "User " + g.user[1] + " updated support link with ID: " + str(linkId) + ", new details: Link Name: " + str(linkName) + ", Link Destination: " + str(linkDest) + ".")
    cur.close()

    return jsonify({"message": "Link updated successfully!"}), 200

@bp.route('/support/archive_link', methods=['POST'])
@login_required
@role_required('ADMIN')
def archive_link_support():
    data = request.get_json()
    linkId = data.get('linkId')

    mysql = get_mysql()
    cur = mysql.connection.cursor()
    cur.execute("UPDATE links SET archived = 1 WHERE id = %s", (linkId,))
    mysql.connection.commit()

    log_user_action(g.user[1], 
                    "Archived Support Link", 
                    "User " + g.user[1] + " archived support link with ID: " + str(linkId) + ".")
    cur.close()

    return jsonify({"message": "Link archived successfully!"}), 200

@bp.route('/support/add_job', methods=['POST'])
@login_required
@role_required('SUPPORT')
def add_job_support():
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
                    "Created New Support Job", 
                    "User " + g.user[1] + " created new support job with ID: " + str(row_id) + " in support job section " + str(tabId) + ".")
    cur.close()


    return jsonify({"message": "Job added successfully!"}), 200

@bp.route('/support/edit_job', methods=['POST'])
@login_required
@role_required('SUPPORT')
def edit_job_support():
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
                    "Updated Support Job", 
                    "User " + g.user[1] + " updated support job with ID: " + str(jobId) + ", new details: Severity: " + str(severity) + ", Job Header: " + str(jobHeader) + ", Job Description: " + str(jobDesc) +  ".")
    cur.close()


    return jsonify({"message": "Job edited successfully!"}), 200

@bp.route('/support/archive_job', methods=['POST'])
@login_required
@role_required('SUPPORT')
def archive_job_support():
    data = request.get_json()
    jobId = data.get('jobId')
    tableId = data.get('tableId')

    mysql = get_mysql()
    cur = mysql.connection.cursor()
    cur.execute("UPDATE jobs SET archived = 1, timestamp = NOW() WHERE id = %s", (jobId,))
    mysql.connection.commit()

    log_user_action(g.user[1], 
                    "Archived Support Job", 
                    "User " + g.user[1] + " archived support job with ID: " + str(jobId) + " in support job section" + str(tableId) + ".")
    cur.close()


    return jsonify({"message": "Job archived successfully!"}), 200

@bp.route('/support/add_notice', methods=['POST'])
@login_required
@role_required('SUPPORT')
def add_notice_support():
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
                    "Created New Support Notice", 
                    "User " + g.user[1] + " created new support notice with ID: " + str(row_id) + " in support notice section " + str(tabId) + ".")
    cur.close()


    return jsonify({"message": "Notice added successfully!"}), 200

@bp.route('/support/edit_notice', methods=['POST'])
@login_required
@role_required('SUPPORT')
def edit_notice_support():
    data = request.get_json()
    noticeId = data.get('noticeId')
    noticeHeader = data.get('noticeHeader')
    noticeDesc = data.get('noticeDesc')

    mysql = get_mysql()
    cur = mysql.connection.cursor()
    cur.execute("UPDATE notices SET notice_header = %s, notice_desc = %s, timestamp = NOW() WHERE id = %s", (noticeHeader, noticeDesc, noticeId))
    mysql.connection.commit()

    log_user_action(g.user[1], 
                    "Updated Support Notice", 
                    "User " + g.user[1] + " updated support notice with ID: " + str(noticeId) + ", new details: Notice Header: " + str(noticeHeader) + ", Notice Description: " + str(noticeDesc) + ".")
    cur.close()

    return jsonify({"message": "Notice updated successfully!"}), 200

@bp.route('/support/archive_notice', methods=['POST'])
@login_required
@role_required('ADMIN')
def archive_notice_support():
    data = request.get_json()
    noticeId = data.get('noticeId')

    mysql = get_mysql()
    cur = mysql.connection.cursor()
    cur.execute("UPDATE notices SET archived = 1 WHERE id = %s", (noticeId,))
    mysql.connection.commit()

    log_user_action(g.user[1], 
                    "Archived Support Notice", 
                    "User " + g.user[1] + " archived support notice with ID: " + str(noticeId) + ".")
    cur.close()

    return jsonify({"message": "Notice archived successfully!"}), 200

@bp.route('/support/get_severities')
@login_required
@role_required('SUPPORT')
def get_severities_support():
    mysql = get_mysql()
    cur = mysql.connection.cursor()
    query = '''
    SELECT job_severity, COUNT(*) as count
    FROM jobs
    WHERE table_id LIKE 'support-%'
    GROUP BY job_severity
    '''
    cur.execute(query)
    
    results = cur.fetchall()

    severity_data = {severity: count for severity, count in results}

    cur.close()
    return jsonify(severity_data)