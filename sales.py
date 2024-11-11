from flask import (
    Blueprint, redirect, render_template, url_for, jsonify, current_app, g, request
)

from MySQLdb.cursors import DictCursor

# from auth import login_required, role_required
from .auth import login_required, role_required

# from __init__ import get_mysql, log_user_action
from . import get_mysql, log_user_action

import html

bp = Blueprint('sales', __name__)

@bp.route('/sales', methods=['GET', 'POST'])
@login_required
@role_required('SALES')
def sales():
    mysql = get_mysql()
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
        SELECT l.*, u.firstname, u.lastname
        FROM links l
        JOIN users u ON l.employee_id = u.id
        WHERE l.table_id LIKE 'sales-%'
        ORDER BY l.timestamp DESC
    """)
    links = cur.fetchall()

    for link in links:
        if link['timestamp']:
            link['formatted_timestamp'] = link['timestamp'].strftime('%d/%m/%Y %H:%M')
        else:
            link['formatted_timestamp'] = None

    sales_1_links = [entry for entry in links if entry['table_id'] == 'sales-1']
    sales_2_links = [entry for entry in links if entry['table_id'] == 'sales-2']
    sales_3_links = [entry for entry in links if entry['table_id'] == 'sales-3']
    sales_4_links = [entry for entry in links if entry['table_id'] == 'sales-4']

    cur.execute("""
        SELECT j.*, u.firstname, u.lastname
        FROM jobs j
        JOIN users u ON j.employee_id = u.id
        WHERE j.table_id LIKE 'sales-%'
        ORDER BY j.timestamp DESC
    """)
    jobs = cur.fetchall()

    for job in jobs:
        if job['timestamp']:
            job['formatted_timestamp'] = job['timestamp'].strftime('%d/%m/%Y %H:%M')
        else:
            job['formatted_timestamp'] = None

    sales_1_jobs = [entry for entry in jobs if entry['table_id'] == 'sales-1']
    sales_2_jobs = [entry for entry in jobs if entry['table_id'] == 'sales-2']
    sales_3_jobs = [entry for entry in jobs if entry['table_id'] == 'sales-3']
    sales_4_jobs = [entry for entry in jobs if entry['table_id'] == 'sales-4']

    cur.execute("""
        SELECT n.*, u.firstname, u.lastname
        FROM notices n
        JOIN users u ON n.employee_id = u.id
        WHERE n.table_id LIKE 'sales-%'
        ORDER BY n.timestamp DESC
    """)
    notices = cur.fetchall()

    for notice in notices:
        if notice['timestamp']:
            notice['formatted_timestamp'] = notice['timestamp'].strftime('%d/%m/%Y %H:%M')
        else:
            notice['formatted_timestamp'] = None

    sales_1_notices = [entry for entry in notices if entry['table_id'] == 'sales-1']
    sales_2_notices = [entry for entry in notices if entry['table_id'] == 'sales-2']
    sales_3_notices = [entry for entry in notices if entry['table_id'] == 'sales-3']
    sales_4_notices = [entry for entry in notices if entry['table_id'] == 'sales-4']

    cur.execute("SELECT * FROM users WHERE permSet = 'SALES'")

    department_members = cur.fetchall()

    cur.close()

    return render_template('main/departments/sales.html', 
        sales_1_links=sales_1_links, sales_2_links=sales_2_links, sales_3_links=sales_3_links, sales_4_links=sales_4_links,
        sales_1_jobs=sales_1_jobs, sales_2_jobs=sales_2_jobs, sales_3_jobs=sales_3_jobs, sales_4_jobs=sales_4_jobs,
        sales_1_notices=sales_1_notices, sales_2_notices=sales_2_notices, sales_3_notices=sales_3_notices, sales_4_notices=sales_4_notices,
        members=department_members
    )

@bp.route('/sales/add_link', methods=['POST'])
@login_required
@role_required('SALES')
def add_link_sales():
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
                    "Created New Sales Link", 
                    "User " + g.user[1] + " created new sales link with ID: " + str(row_id) + " in sales link section " + str(tabId) + ".")
    cur.close()


    return jsonify({"message": "Link added successfully!"}), 200

@bp.route('/sales/edit_link', methods=['POST'])
@login_required
@role_required('SALES')
def edit_link_sales():
    data = request.get_json()
    linkId = data.get('linkId')
    linkName = html.escape(data.get('linkName'))
    linkDest = html.escape(data.get('linkDest'))

    mysql = get_mysql()
    cur = mysql.connection.cursor()
    cur.execute("UPDATE links SET link_name = %s, link_dest = %s, timestamp = NOW() WHERE id = %s", (linkName, linkDest, linkId))
    mysql.connection.commit()

    log_user_action(g.user[1], 
                    "Updated Sales Link", 
                    "User " + g.user[1] + " updated sales link with ID: " + str(linkId) + ", new details: Link Name: " + str(linkName) + ", Link Destination: " + str(linkDest) + ".")
    cur.close()

    return jsonify({"message": "Link updated successfully!"}), 200

@bp.route('/sales/archive_link', methods=['POST'])
@login_required
@role_required('ADMIN')
def archive_link_sales():
    data = request.get_json()
    linkId = data.get('linkId')

    mysql = get_mysql()
    cur = mysql.connection.cursor()
    cur.execute("UPDATE links SET archived = 1 WHERE id = %s", (linkId,))
    mysql.connection.commit()

    log_user_action(g.user[1], 
                    "Archived Sales Link", 
                    "User " + g.user[1] + " archived sales link with ID: " + str(linkId) + ".")
    cur.close()

    return jsonify({"message": "Link archived successfully!"}), 200

@bp.route('/sales/add_job', methods=['POST'])
@login_required
@role_required('SALES')
def add_job_sales():
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
                    "Created New Sales Job", 
                    "User " + g.user[1] + " created new sales job with ID: " + str(row_id) + " in sales job section " + str(tabId) + ".")
    cur.close()


    return jsonify({"message": "Job added successfully!"}), 200

@bp.route('/sales/edit_job', methods=['POST'])
@login_required
@role_required('SALES')
def edit_job_sales():
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
                    "Updated Sales Job", 
                    "User " + g.user[1] + " updated sales job with ID: " + str(jobId) + ", new details: Severity: " + str(severity) + ", Job Header: " + str(jobHeader) + ", Job Description: " + str(jobDesc) +  ".")
    cur.close()


    return jsonify({"message": "Job edited successfully!"}), 200

@bp.route('/sales/archive_job', methods=['POST'])
@login_required
@role_required('SALES')
def archive_job_sales():
    data = request.get_json()
    jobId = data.get('jobId')
    tableId = data.get('tableId')

    mysql = get_mysql()
    cur = mysql.connection.cursor()
    cur.execute("UPDATE jobs SET archived = 1, timestamp = NOW() WHERE id = %s", (jobId,))
    mysql.connection.commit()

    log_user_action(g.user[1], 
                    "Archived Sales Job", 
                    "User " + g.user[1] + " archived sales job with ID: " + str(jobId) + " in sales job section" + str(tableId) + ".")
    cur.close()


    return jsonify({"message": "Job archived successfully!"}), 200

@bp.route('/sales/add_notice', methods=['POST'])
@login_required
@role_required('SALES')
def add_notice_sales():
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
                    "Created New Sales Notice", 
                    "User " + g.user[1] + " created new sales notice with ID: " + str(row_id) + " in sales notice section " + str(tabId) + ".")
    cur.close()


    return jsonify({"message": "Notice added successfully!"}), 200

@bp.route('/sales/edit_notice', methods=['POST'])
@login_required
@role_required('SALES')
def edit_notice_sales():
    data = request.get_json()
    noticeId = data.get('noticeId')
    noticeHeader = data.get('noticeHeader')
    noticeDesc = data.get('noticeDesc')

    mysql = get_mysql()
    cur = mysql.connection.cursor()
    cur.execute("UPDATE notices SET notice_header = %s, notice_desc = %s, timestamp = NOW() WHERE id = %s", (noticeHeader, noticeDesc, noticeId))
    mysql.connection.commit()

    log_user_action(g.user[1], 
                    "Updated Sales Notice", 
                    "User " + g.user[1] + " updated sales notice with ID: " + str(noticeId) + ", new details: Notice Header: " + str(noticeHeader) + ", Notice Description: " + str(noticeDesc) + ".")
    cur.close()

    return jsonify({"message": "Notice updated successfully!"}), 200

@bp.route('/sales/archive_notice', methods=['POST'])
@login_required
@role_required('ADMIN')
def archive_notice_sales():
    data = request.get_json()
    noticeId = data.get('noticeId')

    mysql = get_mysql()
    cur = mysql.connection.cursor()
    cur.execute("UPDATE notices SET archived = 1 WHERE id = %s", (noticeId,))
    mysql.connection.commit()

    log_user_action(g.user[1], 
                    "Archived Sales Notice", 
                    "User " + g.user[1] + " archived sales notice with ID: " + str(noticeId) + ".")
    cur.close()

    return jsonify({"message": "Notice archived successfully!"}), 200

@bp.route('/sales/get_severities')
@login_required
@role_required('SALES')
def get_severities_sales():
    mysql = get_mysql()
    cur = mysql.connection.cursor()
    query = '''
    SELECT job_severity, COUNT(*) as count
    FROM jobs
    WHERE table_id LIKE 'sales-%'
    GROUP BY job_severity
    '''
    cur.execute(query)
    
    results = cur.fetchall()

    severity_data = {severity: count for severity, count in results}

    cur.close()
    return jsonify(severity_data)