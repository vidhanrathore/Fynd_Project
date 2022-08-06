# from flask import Flask, render_template, request, session
# import cx_Oracle
# app = Flask(__name__)
# app.secret_key = "The_Hero"
#
# # -------------- Connectivity--------------------
# con = cx_Oracle.connect("hr/hr@localhost:1521/xe")
# cursor = con.cursor()


# @app.route('/login_page', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        password = request.form.get('password')
        user_name = request.form.get('name')
        cursor.execute("select my_name,password from client")
        for i in cursor:
            if user_name in i and password in i:
                session['user'] = user_name
                msg = "You are Successfully Log In"
                return render_template("loged_in.html", name=user_name, msg=msg)

        msg = "invalid username or password"
        return render_template("login_page.html", msg=msg)
    else:
        return render_template("login_page.html", msg="")


print("LOginPage")
