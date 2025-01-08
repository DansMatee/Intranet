from flask import Flask, request
from flask_mysqldb import MySQL

mysql = MySQL()

def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY='DEV',
        MYSQL_HOST='LOCALHOST',
        MYSQL_USER='USER',
        MYSQL_PASSWORD='PASSWORD',
        MYSQL_DB='intranet'
    )

    mysql.init_app(app)

    # import auth
    from . import auth
    app.register_blueprint(auth.bp)

    # import mainview
    from . import mainview
    app.register_blueprint(mainview.bp)

    # import support
    from . import support
    app.register_blueprint(support.bp)

    # import tanks
    from . import tanks
    app.register_blueprint(tanks.bp)

    # import general
    from . import general
    app.register_blueprint(general.bp)

    # import sales
    from . import sales
    app.register_blueprint(sales.bp)

    return app

def get_mysql():
    return mysql

def log_user_action(username, action, desc):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO logs (username, action, `desc`, ip_address) VALUES (%s, %s, %s, %s)", (username, action, desc, request.remote_addr))
    mysql.connection.commit()
    cur.close()