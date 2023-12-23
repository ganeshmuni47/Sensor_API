from flask import Flask, render_template, request, redirect, session, url_for, jsonify, abort
# from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import secrets
import os, sys
from utils import dbconn, emails, crypt, sql_statements, formdata, commons
import utils
from sqlalchemy.util import deprecations
deprecations.SILENCE_UBER_WARNING = True

app = Flask(__name__)
app.secret_key = utils.get_secret()
static_path = os.path.abspath("./static")
app.config['UPLOAD_FOLDER'] = os.path.join(static_path, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
max_upload_size = 5 #in MB
print(app.config['UPLOAD_FOLDER'])
server_name = 'localhost'

#-----------------------------------------#
#   User Defined Functions
#-----------------------------------------#

def make_token():
    return secrets.token_urlsafe(16)

def get_filepath(uid, type='resume', filename='xxx.xxx', format=['xxx.xxx']):
    filename_ext = filename.split('.')[1]
    if(filename_ext not in format):
        errors1 = f"Error, File Extension({filename_ext}) not allowed for {type}."
        errors2 = "None"
        return errors1, errors2
    else:
        uidx = 'userid'+str(uid)
        uidx_enc = crypt.encrypt_default(uidx)
        uidx_mod = ''.join(e for e in uidx_enc if e.isalnum())
        uidx_path = f'/userdata/{uidx_mod}/{type}/'
        file_dir = app.config['UPLOAD_FOLDER']+uidx_path
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
            print(f"New Directories Created: {file_dir}")
        file_path_full = file_dir + filename
        file_path_upload = f'uploads{uidx_path}{filename}'
        return file_path_full, file_path_upload

#-----------------------------------------#
#   Webpage Routes 
#-----------------------------------------#

@app.route('/')
def index():
    wd = commons.get_media(url_for('static',filename='', _external=True))
    return render_template('home.html', wd=wd)

@app.route('/about')
def about():
    wd = commons.get_media(url_for('static',filename='', _external=True))
    return render_template('about.html',wd=wd)

@app.route('/services')
def services():
    wd = commons.get_media(url_for('static',filename='', _external=True))
    return render_template('services.html',wd=wd)

@app.route('/registration', methods=["GET", "POST"])
def registration():
    user_type = request.args.get('user')
    # ------------ Recuiter Registration ----------- #
    if(user_type=='recruiter'):
        if(request.method == 'POST'):
            if(request.form.get('registration_recruiter')):
                fname = request.form['fname']
                email = request.form['email']
                phonecode = request.form['phonecode']
                phone = request.form['phone']
                company_name = request.form['company_name']
                company_website = request.form['company_website']
                company_size = request.form['company_size']
                password = request.form['password']
                confirm_password = request.form['confirm_password']
                if(password != confirm_password):
                    return render_template('registration.html',user='recruiter',error="Passwords did not match!")
                else:
                    password_enc = crypt.encrypt_default(password)
                    print(password, password_enc)
                sql_get_ai = """SELECT `AUTO_INCREMENT` FROM information_schema.tables WHERE table_name='ax_recruiter_register'"""
                row = sql_statements.fetchone(sql_get_ai)
                next_uid = row[0]
                profile_id = commons.get_alnum(email.split('@')[0])+'-'+ commons.get_alnum(crypt.encrypt_default("ax"+str(next_uid)).lower())
                reg_token = make_token().lower()
                verify_link = f"{url_for('index', _external=True)}verification?user=recruiter&email={email}&regtoken={reg_token}"
                sql_insert_reg = f"""INSERT INTO ax_recruiter_register
                    (FULLNAME, USEREMAIL, PHONECODE, PHONE, PASSWD, COMPANY_NAME, COMPANY_WEBSITE, COMPANY_SIZE, VERIFY_TOKEN, PROFILE_ID)
                    VALUES('{fname.strip().upper()}', '{email.lower()}', {phonecode}, '{phone}', '{password_enc}', '{company_name}','{company_website}','{company_size}', '{reg_token}','{profile_id}')"""
                try:
                    sql_statements.transact(sql_insert_reg)
                    # send verification mail
                    emails.send_email_verification(email, verify_link)
                    return render_template('registration.html', user='recruiter', success="Registration Pending.", success_msg = "Verification Link sent to Registered Email.")
                except Exception as e:
                    if("Duplicate entry" in str(e)):
                        sql_sel_verified = f"SELECT VERIFIED FROM ax_recruiter_register WHERE USEREMAIL='{email}'"
                        row = sql_statements.fetchone(sql_sel_verified)
                        verified = row[0]
                        if(verified==1):
                            return render_template('login.html', user='recruiter', error="Email Already Registered and Verified.", error_msg='Please Login to Continue.')
                        else:
                            print("Duplicate Entry. Re-Create Token")
                            reg_token = make_token().lower()
                            verify_link = f"{url_for('index', _external=True)}verification?user=recruiter&email={email}&regtoken={reg_token}"
                            print(verify_link)
                            sql_upt_token = f"UPDATE ax_recruiter_register SET VERIFY_TOKEN='{reg_token}' WHERE USEREMAIL='{email}'"
                            sql_statements.transact(sql_upt_token)
                            # send verification mail #
                            emails.send_email_verification(email, verify_link)
                            return render_template('registration.html', user='recruiter', error="Email Already Registered But Not Verified", error_msg="Verification Link again sent to Registered Email.")
                    else:
                        return render_template('registration.html',user='recruiter', error="Unable to Process Your Request Now", error_msg='Please try after some time.')
            else:
                return render_template('registration.html', user_type = user_type)
        else:        
            return render_template('registration.html', user_type = user_type)
        
    else:
        user_type = "ex_employee"
        if(request.method == 'POST'):
            if(request.form.get('registration')):
                fname = request.form['fname']
                email = request.form['email']
                phonecode = request.form['phonecode']
                phone = request.form['phone']
                password = request.form['password']
                confirm_password = request.form['confirm_password']
                gender = request.form['gender']
                if(password != confirm_password):
                    return render_template('registration.html', error="Passwords did not match!")
                else:
                    password_enc = crypt.encrypt_default(password)
                    print(password, password_enc)
                sql_get_ai = """SELECT `AUTO_INCREMENT` FROM information_schema.tables WHERE table_name='ax_employee_register'"""
                row = sql_statements.fetchone(sql_get_ai)
                next_uid = row[0]
                profile_id = commons.get_alnum(email.split('@')[0])+'-'+ commons.get_alnum(crypt.encrypt_default("ax"+str(next_uid)).lower())
                reg_token = make_token().lower()
                verify_link = f"{url_for('index', _external=True)}verification?email={email}&regtoken={reg_token}"
                sql_insert_reg = f"""INSERT INTO ax_employee_register
                    (FULLNAME, USEREMAIL, PHONECODE, PHONE, PASSWD, GENDER, VERIFY_TOKEN, REGISTER_TYPE, PROFILE_ID)
                    VALUES('{fname.upper()}', '{email.lower()}', {phonecode}, '{phone}', '{password_enc}', '{gender}', '{reg_token}', 'EMPLOYEE', '{profile_id}')"""
                try:
                    sql_statements.transact(sql_insert_reg)
                    # send verification mail
                    emails.send_email_verification(email, verify_link)
                    return render_template('registration.html', success="Registration Pending.", success_msg = "Verification Link sent to Registered Email.")
                except Exception as e:
                    if("Duplicate entry" in str(e)):
                        sql_sel_verified = f"SELECT VERIFIED FROM u704854418_amazonx_db.ax_employee_register WHERE USEREMAIL='{email}'"
                        row = sql_statements.fetchone(sql_sel_verified)
                        verified = row[0]
                        if(verified==1):
                            return render_template('login.html',error="Email Already Registered and Verified.", error_msg='Please Login to Continue.')
                        else:
                            print("Duplicate Entry. Re-Create Token")
                            reg_token = make_token().lower()
                            verify_link = f"{url_for('index', _external=True)}verification?email={email}&regtoken={reg_token}"
                            print(verify_link)
                            sql_upt_token = f"UPDATE u704854418_amazonx_db.ax_employee_register SET VERIFY_TOKEN='{reg_token}' WHERE USEREMAIL='{email}'"
                            sql_statements.transact(sql_upt_token)
                            # send verification mail #
                            emails.send_email_verification(email, verify_link)
                            return render_template('registration.html',error="Email Already Registered But Not Verified", error_msg="Verification Link again sent to Registered Email.")
                    else:
                        return render_template('registration.html',error="Unable to Process Your Request Now",error_msg='Please try after some time.')
        else:        
            return render_template('registration.html')

@app.route('/verification', methods=["GET", "POST"])
def verification():
    user_type = request.args.get('user')
    if(user_type == 'recruiter'):
        if(request.method=='GET'):
            ## User Email Verification Process ##
            if(request.args.get('email') and request.args.get('regtoken')):
                vemail = request.args.get('email')
                vregtoken = request.args.get('regtoken')
                print("[info]", vemail, vregtoken)
                try:
                    sql_sel_token = f"SELECT VERIFY_TOKEN, VERIFIED FROM ax_recruiter_register WHERE USEREMAIL='{vemail}'"
                    sql_upt_reg = f"UPDATE ax_recruiter_register SET VERIFIED=1, VERIFY_TOKEN=NULL WHERE USEREMAIL='{vemail}'"
                    row = sql_statements.fetchone(sql_sel_token)
                    print(row)
                    if(row==False):
                        return render_template('registration.html',user='recruiter',error="User not Registered. Please Register.")
                    else:
                        if(row[1]==0):
                            if(vregtoken==row[0]):
                                sql_statements.transact(sql_upt_reg)
                                # return redirect(url_for('login',user='recruiter'))
                                return render_template('login.html', user='recruiter', success="Registration Complete. Please Log In to Continue.")                            
                            else:
                                return render_template('registration.html', user='recruiter', error="Invalid Token. Please Re-register.")
                        if(row[1]==1):
                            return render_template('login.html', user='recruiter', success="Registration Already Complete. Please Log In to Continue.")
                except Exception as e:
                    print(str(e))
                    return render_template('login.html', user='recruiter', error="Unable to Process Request Now.")
            else:
                abort(404)
        else:
            abort(404)
    else:
        if(request.method=='GET'):
            ## User Email Verification Process ##
            if(request.args.get('email') and request.args.get('regtoken')):
                vemail = request.args.get('email')
                vregtoken = request.args.get('regtoken')
                print("[info]", vemail, vregtoken)
                try:
                    sql_sel_token = f"SELECT VERIFY_TOKEN, VERIFIED FROM ax_employee_register WHERE USEREMAIL='{vemail}'"
                    sql_upt_reg = f"UPDATE ax_employee_register SET VERIFIED=1, VERIFY_TOKEN=NULL WHERE USEREMAIL='{vemail}'"
                    row = sql_statements.fetchone(sql_sel_token)
                    if(row==False):
                        return render_template('registration.html',error="User not Registered. Please Register.")
                    else:
                        if(row[1]==0):
                            if(vregtoken==row[0]):
                                sql_statements.transact(sql_upt_reg)
                                return render_template('login.html',success="Registration Complete. Please Log In to Continue.")                            
                            else:
                                return render_template('registration.html',error="Invalid Token. Please Re-register.")
                        if(row[1]==1):
                            return render_template('login.html',success="Registration Already Complete. Please Log In to Continue.")
                except Exception as e:
                    print(str(e))
                    return render_template('login.html',error="Unable to Process Request Now.")
            else:
                abort(404)
        else:
            abort(404)

@app.route('/login', methods=["GET", "POST"])
def login():
    if(session.get('userid') or session.get('recruiterid')):
        session.pop('userid',None)
        session.pop('recruiterid',None)
    # ---------- Recruiter Login ----------- #
    user_type = request.args.get('user')
    if(user_type=='recruiter'):
        if(request.method=='POST'):
            if(request.form['lusername'] and request.form['lpassword']):
                lusername = request.form['lusername']
                lpassword = request.form['lpassword']
                lpassword_enc = crypt.encrypt_default(lpassword)
                # print(lusername,lpassword_enc)
                try:
                    sql_sel_user = f"SELECT UID,PASSWD,VERIFIED,FULLNAME,PROFILE_ID FROM ax_recruiter_register WHERE USEREMAIL='{lusername}'"
                    row = sql_statements.fetchone(sql_sel_user)
                    if(row != False):
                        if(row[1]==lpassword_enc):
                            # Password Matched !
                            if(row[2]==1):
                                # User Verified. Login Success !
                                session['username'] = lusername
                                session['recruiterid'] = row[0]
                                session['userfname'] = row[3]
                                session['profile_id'] = row[4]
                                return redirect(url_for('dashboard', user_type='recruiter',profile_id=session['profile_id']))
                            else:
                                return render_template('login.html',user='recruiter',error="User's Email Not Verified. Please Verify.")
                        else:
                            return render_template('login.html',user='recruiter',error="Login Failed. Invalid Password.")
                    else:
                        return render_template('login.html',user='recruiter',error="User Not Found. Please Register.")
                except Exception as e:
                    print(str(e))
                    return render_template('login.html',user='recruiter',error="Error: Unable To Process Your Request Now.")
            else:
                return render_template('login.html',user_type=user_type)
        else:
            return render_template('login.html',user_type=user_type)
    else:
        # ---------- Employee Login ----------- #
        user_type = "ex_employee"
        if(request.method=='POST'):
            if(request.form['lusername'] and request.form['lpassword']):
                lusername = request.form['lusername']
                lpassword = request.form['lpassword']
                lpassword_enc = crypt.encrypt_default(lpassword)
                # print(lusername,lpassword_enc)
                try:
                    sql_sel_user = f"SELECT UID,PASSWD,VERIFIED,FULLNAME,PROFILE_ID FROM ax_employee_register WHERE USEREMAIL='{lusername}'"
                    row = sql_statements.fetchone(sql_sel_user)
                    print(row) # number of columns
                    if(row):
                        if(row[1]==lpassword_enc):
                            # Password Matched !
                            if(row[2]==1):
                                # User Verified. Login Success !
                                session['username'] = lusername
                                session['userid'] = row[0]
                                session['userfname'] = row[3]
                                session['profile_id'] = row[4]
                                user_data = sql_statements.select_ax_employee_detailed(session['userid'])
                                if(user_data == 0):
                                    print("-----> user data not available. Initialize Database")
                                    sql_statements.init_ax_employee_detailed(session['userid'])
                                    session['user_detailed'] = formdata.ax_detailed_default
                                    session['user_detailed']['userid'] = session['userid']
                                    return redirect(url_for('edit_profile'))
                                    # return render_template('profile.html',ud = session['user_detailed'])
                                else:
                                    print("-----> user data available")
                                    session['user_detailed'] = formdata.merge_dict(formdata.ax_detailed_default, user_data)
                                    # print(session['user_detailed'])
                                    if(session['user_detailed']['profile_completion_percent'] == 100):
                                        return redirect(url_for('profile',profile_id=session['profile_id']))
                                    else:
                                        return redirect(url_for('edit_profile'))
                                    # return render_template('profile.html',ud=session['user_detailed'])
                            else:
                                return render_template('login.html',error="User's Email Not Verified. Please Verify.")
                        else:
                            return render_template('login.html',error="Login Failed. Invalid Password.")
                    else:
                        return render_template('login.html',error="User Not Found. Please Register.")
                except Exception as e:
                    print(str(e))
                    return render_template('login.html',error="Error: Unable To Process Your Request Now.")
        else:
            return render_template('login.html', user_type=user_type)

@app.route('/profile/<profile_id>')
def profile(profile_id):
    if(session.get('userid')):
        flag, result  = sql_statements.select_profile_public(profile_id=profile_id)
        if(flag):
            if(session.get('userid')): 
                if(session['username'] == result['useremail']):
                    return render_template('profile.html', ud=result, account='me')
            else:
                return render_template('profile.html', ud=result, account='other')
        else:
            abort(404)
    else:
        return redirect(url_for('login'))
    
@app.route('/edit_profile', methods=["GET", "POST"])
def edit_profile():
    if(session.get('userid')):
        print(f"#========= Edit Profile Session : UID : {session['userid']} ===========#")
        # print(session['user_detailed'])
        # session['user_detailed'] = formdata.ax_detailed_default
        if(request.method=="POST"):
            print("#== Method POST ==#")
            # sql_statements.init_ax_employee_detailed(session['userid'])
            if(request.form.get('section-1')):
                print("#==== Section 1 ====#")
                form_dict = request.form.to_dict(flat=False)
                # print(form_dict)
                merged = formdata.merge_dict(session['user_detailed'], form_dict, 0)
                session['user_detailed'] = merged
                # sql_statements.update_ax_employee_detailed(session['userid'],merged)
            if(request.form.get('section-2')):
                print("#==== Section 2 ====#")
                form_dict = request.form.to_dict(flat=False)
                merged = formdata.merge_dict(session['user_detailed'], form_dict, 0)
                session['user_detailed'] = merged
                # sql_statements.update_ax_employee_detailed(session['userid'],merged)    
            if(request.form.get('section-3')):
                print("#==== Section 3 ====#")
                form_dict = request.form.to_dict(flat=False)
                merged = formdata.merge_dict(session['user_detailed'], form_dict, 0)
                session['user_detailed'] = merged
                # sql_statements.update_ax_employee_detailed(session['userid'],merged)
            if(request.form.get('section-4')):
                print("#==== Section 4 ====#")
                form_dict = request.form.to_dict(flat=False)
                merged = formdata.merge_dict(session['user_detailed'], form_dict, 0)
                session['user_detailed'] = merged
                # sql_statements.update_ax_employee_detailed(session['userid'],merged)
            if(request.form.get('section-5')):
                print("#==== Section 5 ====#")
                form_dict = request.form.to_dict(flat=False)
                merged = formdata.merge_dict(session['user_detailed'], form_dict, 0)
                session['user_detailed'] = merged
                if(request.files.get('resume_path')):
                    print("----> resume_path")
                    f_resume_format = ['doc', 'docx', 'pdf']
                    f_resume = request.files['resume_path']
                    f_resume_path,f_resume_link = get_filepath(session['userid'],type='resume',filename=f_resume.filename, format=f_resume_format)
                    if(f_resume_path.split(',')[0]=='Error'):
                        return render_template('edit_profile.html', upload_error=f_resume_path, ud = session['user_detailed'])
                    else:    
                        f_resume.save(f_resume_path)
                        file_size = round((os.stat(f_resume_path).st_size / (1024*1024)),2)
                        if(file_size <= max_upload_size):
                            session['user_detailed']['resume_path'] = f_resume_link
                        else:
                            if os.path.exists(f_resume_path):
                                os.remove(f_resume_path)
                            return render_template('edit_profile.html', upload_error=f"File Size Exceeds the limit of {max_upload_size}MB", ud = session['user_detailed'])
                if(request.files.get('profile_picture_path')):
                    print("----> profile_picture_path")
                    f_photo_format = ['jpg', 'png']
                    f_photo = request.files['profile_picture_path']
                    f_photo_path, f_photo_link = get_filepath(session['userid'],type='profile_pic',filename=f_photo.filename, format=f_photo_format)
                    if(f_photo_path.split(',')[0]=='Error'):
                        return render_template('edit_profile.html', upload_error=f_photo_path, ud = session['user_detailed'])
                    else:    
                        f_photo.save(f_photo_path)
                        file_size = round((os.stat(f_photo_path).st_size / (1024*1024)),2)
                        if(file_size <= max_upload_size):
                            session['user_detailed']['profile_picture_path'] = f_photo_link
                        else:
                            if os.path.exists(f_photo_path):
                                os.remove(f_photo_path)
                            return render_template('edit_profile.html', upload_error=f"File Size Exceeds the limit of {max_upload_size}MB", ud = session['user_detailed'])
            if(request.form.get('section-6')):
                print("#==== Section 6 ====#")
                form_dict = request.form.to_dict(flat=False)
                merged = formdata.merge_dict(session['user_detailed'], form_dict, 0)
                session['user_detailed'] = merged
                # sql_statements.update_ax_employee_detailed(session['userid'],merged)
            print("#========= Updating Database =========#")
            if(session['user_detailed']['profile_completion_percent'] != 100):
                session['user_detailed']['profile_completion_percent'] = int(20) + (int(session['user_detailed']['section-1'])
                + int(session['user_detailed']['section-2']) + int(session['user_detailed']['section-3']) +int(session['user_detailed']['section-4'])
                + int(session['user_detailed']['section-5']) + int(session['user_detailed']['section-6']))

            # print(session['user_detailed'])
            sql_statements.update_ax_employee_detailed(session['userid'],session['user_detailed'])
            return render_template('edit_profile.html', ud=session['user_detailed'])
        else:
            return render_template('edit_profile.html', ud=session['user_detailed'])
    else:
        return redirect(url_for('login'))

@app.route('/dashboard/<user_type>/<profile_id>', methods=["GET", "POST"])
def dashboard(user_type,profile_id):
    if(user_type=='recruiter' and session.get('recruiterid')):
        return "recruiter dashboard"
    if(user_type=='ex_employee' and session.get('userid')):
        return "recruiter dashboard"
    else:
        return redirect(url_for('login'))

@app.route('/forgot_password', methods=["GET", "POST"])
def forgot_password():
    user_type = request.args.get('user')
    # ------------ Recuiter Forgot Password ----------- #
    if(user_type=='recruiter'):
        print("Recruiter Forgot Password")
        if(request.method == "POST"):
            if(request.form.get('forgot_password')):
                fpusername = request.form.get('fpusername').lower()
                verify_token = make_token().lower()
                sql_query = f"""UPDATE ax_recruiter_register SET FORGOT_TOKEN = '{verify_token}' WHERE USEREMAIL='{fpusername}'"""
                try:
                    row = sql_statements.transact(sql_query)
                    if(row==0):
                        return render_template('forgot_password.html',user=user_type,error="User Not Found. Please Register!")
                    verify_link = f"{url_for('index', _external=True)}forgot_password?email={fpusername}&fptoken={verify_token}"
                    print(verify_link)
                    emails.send_email_forgot_password(fpusername, verify_link)
                    return render_template('forgot_password.html',user=user_type,success="Reset password link sent to Email")
                except Exception as e:
                    print(str(e))
                    return render_template('forgot_password.html',user=user_type,error="Unable to Process Request at the moment.")

            if(request.form.get('reset_password')):
                fppassword = request.form.get('fppassword')
                fpconfirm = request.form.get('fpconfirm')
                if(fppassword != fpconfirm):
                    return render_template('forgot_password.html',user=user_type, page='reset_password', error='Entered passwords did not match!')
                else:
                    try:
                        if(session.get('fpusername') and session.get('forgot_token')):
                            password_enc = crypt.encrypt_default(fppassword)
                            sql_query = f"UPDATE ax_recruiter_register SET FORGOT_TOKEN=NULL, PASSWD='{password_enc}' WHERE USEREMAIL='{session['fpusername']}' AND FORGOT_TOKEN ='{session['forgot_token']}'"
                            update_rowcount = sql_statements.transact(sql_query)
                            if(update_rowcount == 0):
                                return render_template('forgot_password.html',user=user_type,page='forgot_password', error='Token expired or no found! Please Resend.')
                            else:
                                session.pop('fpusername')
                                session.pop('forgot_token')
                                return render_template('login.html',user=user_type, success = 'Password Reset Successful! Please Login to Continue.')
                    except Exception as e:
                        print(str(e))
                        return render_template('forgot_password.html',user=user_type,page='forgot_password', error='Unable to process request at the moment.')
                
        elif(request.method == "GET"):
            if(request.args.get('email') and request.args.get('fptoken')):
                vemail = request.args.get('email')
                vfptoken = request.args.get('fptoken')
                print("[info]", vemail, vfptoken)
                try:
                    if(len(vfptoken)>10):
                        sql_query = f"SELECT FORGOT_TOKEN FROM ax_recruiter_register WHERE USEREMAIL='{vemail}'"
                        row = sql_statements.fetchone(sql_query)
                        if(row):
                            forgot_token = row[0]
                            if(forgot_token == vfptoken):
                                session['forgot_token'] = vfptoken
                                session['fpusername'] = vemail
                                return render_template('forgot_password.html', page='reset_password')
                        else:
                            return render_template('forgot_password.html',user=user_type, page='forgot_password', error='Token expired or no found!')
                    else:
                        abort(404)
                except Exception as e:
                    print(str(e))
                    return render_template('login.html',user=user_type, error="Unable to Process Request Now.")
            else:
                return render_template('forgot_password.html',user=user_type, page='forgot_password')
        else:
            return render_template('forgot_password.html',user=user_type, page='forgot_password')
    else:
        # ------------ Forgot Password for Ex- Employee ------------ # 
        user_type = "ex_employee"
        if(request.method == "POST"):
            if(request.form.get('forgot_password')):
                fpusername = request.form.get('fpusername').lower()
                verify_token = make_token().lower()
                sql_query = f"""UPDATE ax_employee_register SET FORGOT_TOKEN = '{verify_token}' WHERE USEREMAIL='{fpusername}'"""
                try:
                    row = sql_statements.transact(sql_query)
                    if(row==0):
                        return render_template('forgot_password.html',error="User Not Found. Please Register!")
                    verify_link = f"{url_for('index', _external=True)}forgot_password?email={fpusername}&fptoken={verify_token}"
                    print("verify_link",verify_link)
                    emails.send_email_forgot_password(fpusername, verify_link)
                    return render_template('forgot_password.html',success="Reset password link sent to Email")
                except Exception as e:
                    print(str(e))
                    return render_template('forgot_password.html',error="Unable to Process Request at the moment.")

            if(request.form.get('reset_password')):
                fppassword = request.form.get('fppassword')
                fpconfirm = request.form.get('fpconfirm')
                if(fppassword != fpconfirm):
                    return render_template('forgot_password.html',page='reset_password', error='Entered passwords did not match!')
                else:
                    try:
                        if(session.get('fpusername') and session.get('forgot_token')):
                            password_enc = crypt.encrypt_default(fppassword)
                            sql_query = f"UPDATE ax_employee_register SET FORGOT_TOKEN=NULL, PASSWD='{password_enc}' WHERE USEREMAIL='{session['fpusername']}' AND FORGOT_TOKEN ='{session['forgot_token']}'"
                            update_rowcount = sql_statements.transact(sql_query)
                            if(update_rowcount == 0):
                                return render_template('forgot_password.html',page='forgot_password', error='Token expired or no found! Please Resend.')
                            else:
                                session.pop('fpusername')
                                session.pop('forgot_token')
                                return render_template('login.html', success = 'Password Reset Successful! Please Login to Continue.')
                    except Exception as e:
                        print(str(e))
                        return render_template('forgot_password.html',page='forgot_password', error='Unable to process request at the moment.')           
        
        elif(request.method == "GET"):
            if(request.args.get('email') and request.args.get('fptoken')):
                vemail = request.args.get('email')
                vfptoken = request.args.get('fptoken')
                print("[info]", vemail, vfptoken)
                try:
                    if(len(vfptoken)>10):
                        sql_query = f"SELECT FORGOT_TOKEN FROM ax_employee_register WHERE USEREMAIL='{vemail}'"
                        row = sql_statements.fetchone(sql_query)
                        if(row):
                            forgot_token = row[0]
                            if(forgot_token == vfptoken):
                                session['forgot_token'] = vfptoken
                                session['fpusername'] = vemail
                                return render_template('forgot_password.html',page='reset_password')
                        else:
                            return render_template('forgot_password.html',page='forgot_password', error='Token expired or no found!')
                    else:
                        abort(404)
                except Exception as e:
                    print(str(e))
                    return render_template('login.html',error="Unable to Process Request Now.")
            else:
                return render_template('forgot_password.html', page='forgot_password')
        else:
            return render_template('forgot_password.html', page='forgot_password')

@app.route('/logout')
def logout():
    session.pop('userid',None)
    session.pop('user_detailed',None)
    session.pop('userfname',None)
    session.pop('username',None)
    return redirect('login')

@app.route('/show_image')
def show_image():
    img_file_path = session['user_detailed'].get('profile_picture_path', None)
    img_file_path = app.config['UPLOAD_FOLDER']+'\default.png'
    print(img_file_path)
    return render_template('show_image.html', user_image = img_file_path)

@app.route('/info/<page>')
def info(page):
    wd = commons.get_media(url_for('static',filename='', _external=True))
    if(page=='privacy_policy'):
        return render_template('info.html', wd=wd, page=page)
    elif((page=='terms_of_use')):
        return render_template('info.html', wd=wd, page=page)
    else:
        return redirect(url_for('index'))
if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0', port=8000)
