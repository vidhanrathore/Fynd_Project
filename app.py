from flask import Flask, render_template, request, session
import cx_Oracle
import random
import smtplib
OTP = 'otp'
app = Flask(__name__)
app.secret_key = "The_Hero"

# -------------- Connectivity--------------------
con = cx_Oracle.connect("hr/hr@localhost:1521/xe")
cursor = con.cursor()

# ----------------Home----------------
@app.route('/')
def home():
    return render_template("login_page.html")


# ---------------login page---------------
@app.route('/login_page', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        password = request.form.get('password')
        user_name = request.form.get('name')
        cursor.execute("select my_name,password from client")
        for i in cursor:
            if user_name in i and password in i:
                session['user'] = user_name
                msg = "You are Successfully Log In"
                return render_template("loged_in.html", name=user_name, msg=msg, color="success")

        msg = "invalid username or password"
        return render_template("login_page.html", msg=msg, color="red")
    else:
        return render_template("login_page.html")


# ---------------sign-up page---------------
@app.route('/signup')
def signup():
    return render_template("signup.html")


@app.route('/reg_done', methods=['GET', 'POST'])
def reg_done():
    if request.method == 'POST':
        full_name = request.form.get('name')
        email = request.form.get('email')
        user_name = request.form.get('user_name')
        contact = request.form.get('contact')
        password = request.form.get('password')
        amount = (request.form.get('amount'))

        li = [user_name, full_name, contact, amount, email, password]
        for i in li:
            print(type(i),i)



        # OTP validations code start here.....
        global OTP
        OTP = str(random.randint(100000, 999999))
        msg = OTP + ' is your OTP.\n Enter this to verify your account '
        msg = 'Subject: OTP Verification \n' + msg
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("vidhanpython@gmail.com", "ymbjjwnawhypzssb")
        # email_id = input("Enter your email: ")
        s.sendmail("OTP", email, msg)
        return render_template('otp.html',fullname=full_name,uname=user_name,uemail=email,unumber=contact,upassword=password,uamount=amount)


        # try:
        #     # ------------Table is already Created so insert detail into it.------------
        #
        #     ins = '''insert into Client(my_name,full_name,contact,balance,email,password)
        #                                 values('{}','{}','{}','{}','{}','{}')
        #                           '''.format(user_name, full_name, contact, amount, email, password)
        #     cursor.execute(ins)
        #     con.commit()
        #     return render_template('otp.html')
        #
        # except:
        #     msg = "All ready registered with this user name"
        #     return render_template('login_page.html', msg=msg)

    # msg = "Registered Successfully.Now can Log_in"
    # return render_template('login_page.html', msg_green=msg)


# -------------OTP------------
@app.route('/otpvalidation', methods=['GET', 'POST'])
def otp_validation():

    global OTP
    if request.method == 'POST':
        user_otp = request.form.get('otp')
        full_name = request.form.get('name')
        email = request.form.get('email')
        user_name = request.form.get('user_name')
        contact = request.form.get('contact')
        password = request.form.get('password')
        amount = (request.form.get('amount'))
        print("userOTP= ", user_otp, type(user_otp), "MYOTP = ", OTP, type(OTP))
        # print(type(amount))
        li = [user_name, full_name, contact, amount, email, password]
        for i in li:
            print(type(i), i)
        if user_otp == OTP:
            try:
                # ------------Table is already Created so insert detail into it.------------

                ins = '''insert into Client(my_name,full_name,contact,balance,email,password)
                                            values('{}','{}','{}','{}','{}','{}')
                                      '''.format(user_name, full_name, contact, int(amount), email, password)
                cursor.execute(ins)
                con.commit()
                msg = "Great, You are Successfully Verified"
                return render_template("login_page.html", msg=msg, color="green")

            except Exception as e:
                print(e)
                msg = "All ready registered with this user name"
                return render_template('login_page.html', msg=msg)

        else:
            msg = "OTP is not Matched, Try Again"
            return render_template("otp.html", msg=msg, color="danger", fullname=full_name, uname=user_name, uemail=email, unumber=contact, upassword=password, uamount=amount)
    else:
        return "Pta nhi kya"


# ---------------loged_in---------------
@app.route('/loged_in')
def loged_in():
    if 'user' in session:
        user_name = session['user']
        msg = "You are Successfully Log In"
        return render_template("loged_in.html", msg=msg, name=user_name, color="info")
    else:
        msg = "Log in First"
        return render_template('login_page.html', msg_green=msg)


@app.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        user_name = request.form.get('user_name')
        email = request.form.get('email')
        cursor.execute("select email from client where my_name='{}'".format(user_name))
        # if hasnext
        pre_email = next(cursor,None)
        print(pre_email)
        if pre_email:
            if pre_email[0] == email:
                update_ins = "update client set password='{}' where my_name='{}'".format(new_password, user_name)
                print(update_ins)
                cursor.execute(update_ins)
                con.commit()
                msg = "Your Password Updated Successfully, Now you can log in"
                return render_template("login_page.html", msg=msg, color='green')

            msg = "User Name and Email Do not matched"
            return render_template("forget_password.html", msg=msg)
        else:
            msg = "User Name is not Found."
            return render_template("signup.html", msg=msg, color="danger")

    else:
        return render_template("forget_password.html", msg="")


@app.route('/cash_withdrawal', methods=['GET', 'POST'])
def cash_withdrawal():
    if 'user' in session:
        if request.method == 'POST':
            user_name = session['user']
            amount = request.form.get('cash_withdrawal')
            # password = request.form.get('password')
            ins = "select balance from client where my_name='{}'".format(user_name)
            cursor.execute(ins)
            user_balance = next(cursor)
            if user_balance[0] >= int(amount):
                #     upadte querry---------------------------------------
                new_balance = user_balance[0] - int(amount)
                update_ins = "update client set balance='{}' where my_name='{}'".format(new_balance, user_name)
                cursor.execute(update_ins)
                con.commit()
                msg = "Your amount Rs. " + amount + " is Debited successfully"
                return render_template("loged_in.html", name=user_name, msg=msg, color="danger")
            else:
                # msg = "You are not having sufficient Amount that Entered"
                msg = "Your amount is less than you entered"
                return render_template("loged_in.html", name=user_name, msg=msg, color="danger")
        else:
            return render_template("cash_withdrawal.html")
    msg = "Log in First"
    return render_template('login_page.html', msg_green=msg)


@app.route('/cash_deposit', methods=['GET', 'POST'])
def cash_deposit():
    if 'user' in session:
        if request.method == 'POST':
            user_name = session['user']
            amount = request.form.get('cash_deposit')
            # password = request.form.get('password')
            ins = "select balance from client where my_name='{}'".format(user_name)
            cursor.execute(ins)
            user_balance = next(cursor)
            #     --------------upadte querry---------------
            new_balance = user_balance[0] + int(amount)
            update_ins = "update client set balance='{}' where my_name='{}'".format(new_balance, user_name)
            cursor.execute(update_ins)
            con.commit()
            # msg = "Your amount is Deposited successfully"
            msg = "Your amount Rs. " + amount + " is Credited successfully"
            return render_template("loged_in.html", name=user_name, msg=msg, color="success")
        else:
            return render_template("cash_deposit.html")
    msg = "Log in First"
    return render_template('login_page.html', msg_green=msg)


@app.route('/mini_statement', methods=['GET', 'POST'])
def mini_statement():
    user_name = session['user']
    ins = "select balance from client where my_name='{}'".format(user_name)
    cursor.execute(ins)
    user_balance = next(cursor)
    user_balance = user_balance[0]
    # return render_template("mini_statement.html", name=user_name, amount=user_balance)
    # return render_template("loged_in.html", name=user_name, amount=user_balance, mini_statement=True)
    msg = "You are Current Balance is " + str(user_balance)
    return render_template("loged_in.html", name=user_name, msg=msg, color="info")


# @app.route('/admin', methods=['GET', 'POST'])
# def admin():
#     if 'user' in session:
#         if request.method == 'POST':
#             manager_password = request.form.get('password')
#             if manager_password == "MyATM@123":
#                 headings = ("User name", "Full Name", "Email", "Contact", "Balance")
#                 cursor.execute("select my_name,full_name,email,contact,balance from client")
#                 data = cursor
#                 return render_template("admin.html", headings=headings, data=data)
#             else:
#                 msg = "Enter Valid Password"
#                 # user_name = session['user']
#                 return render_template("admin_password.html", msg=msg)
#         else:
#             return render_template("admin_password.html")
#
#     else:
#         return render_template("login_page.html", msg="Hey! Buddy, Login First", color='warning')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'user' in session:
        if request.method == 'POST':
            manager_password = request.form.get('password')
            if manager_password == "MyATM@123":
                # headings = ("User name", "Full Name", "Email", "Contact", "Balance")
                # cursor.execute("select my_name,full_name,email,contact,balance from client")
                headings = ("Full Name","Balance")
                cursor.execute("select full_name,balance from client order by lower(full_name)")
                data = cursor
                return render_template("admin.html", headings=headings, data=data)
            else:
                msg = "Enter Valid Password"
                # user_name = session['user']
                return render_template("admin_password.html", msg=msg)
        else:
            return render_template("admin_password.html")

    else:
        return render_template("login_page.html", msg="Hey! Buddy, Login First", color='warning')



@app.route('/logout')
def logout():
    session.pop('user', None)
    return render_template('login_page.html')


if __name__ == "__main__":
    app.run(debug=True)

''' create table client(user_name varchar2(20) not null primary key,
 name varchar2(40),
 contact number,
 email varchar2(80),
 password varchar2(20),
 );'''
