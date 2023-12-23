import configparser
import mysql.connector
import base64
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import pyaes
from sqlalchemy import text

import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders

class crypt:
    def encrypt_aes(plain_text, master_key):
        plaintext = plain_text.encode('utf-8')
        masterkey = master_key.encode('utf-8')
        aes = pyaes.AESModeOfOperationCTR(masterkey)
        cipher_text = aes.encrypt(plaintext)
        cipher_text = base64.b64encode(cipher_text)
        return cipher_text
    
    def decrypt_aes(cipher_text, master_key):
        masterkey = master_key.encode('utf-8')
        aes = pyaes.AESModeOfOperationCTR(masterkey)
        plain_text = aes.decrypt(base64.b64decode(cipher_text))
        return plain_text.decode()
    
    def encrypt_default(plain_text):
        config = configparser.ConfigParser()
        config.read("config.ini")
        master_key_default = config.get('MASTER_KEYS','DEFAULT')
        cipher_text = crypt.encrypt_aes(plain_text=plain_text, master_key=master_key_default)
        cipher_text = cipher_text.decode()
        return cipher_text

class commons:
    def get_media(static_url):
        website_data = {
            "bg1" : "media/site/bgcover1.jpg",
            "logo_bsqr" : "media/site/logo1_sqr.png",
            "logo_wsqr" : "media/site/logo1w_sqr.png",
            "man_on_pc" : "media/svgs/man_on_pc.svg",
            "svg2": "media/svgs/3people_working.svg",
            "webp1":"media/webp/t1.webp",
            "t2":"media/webp/t2.webp",
            "t3":"media/t3.png",
            "webp3":"media/webp/t3.webp", 
            "dp1":"media/user-profile/dp1.png"
        }
        wd = dict()
        for (k,v) in website_data.items():
            x = {k: static_url+v}
            wd.update(x)
        return wd

    def get_alnum(text,rep=''):
        chx = ''
        for ch in text:
            if(ch.isalnum()):
                chx = chx + ch
            else:
                chx = chx + rep
        return chx

def get_secret():
    config = configparser.ConfigParser()
    config.read("config.ini")
    secret_enc = config.get('SECRET','secret')
    return secret_enc

class dbconn:
    def mysql(host, port=3306, username=None, password=None, database=None):
        connection_string = f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}"
        engine = create_engine(connection_string)
        conn = engine.connect()
        print("===== Mysql Database Connected =====")
        return conn
    class from_config:
        config = configparser.ConfigParser()
        config.read("config.ini")
        def mysql(server_config, masterkey_config=None, encrypt=False):
            host = dbconn.from_config.config.get(server_config,"host")
            port = dbconn.from_config.config.get(server_config,"port")
            username = dbconn.from_config.config.get(server_config,"username")
            password = dbconn.from_config.config.get(server_config,"password")
            database = dbconn.from_config.config.get(server_config,"database")
            if(encrypt):
                master_key = dbconn.from_config.config.get(masterkey_config,server_config)
                username = crypt.decrypt_aes(dbconn.from_config.config.get(server_config,"username"),master_key)
                password = crypt.decrypt_aes(dbconn.from_config.config.get(server_config,"password"),master_key)
                # Getting mysql connection object
            mysql_conn = dbconn.mysql(host=host,port=port,username=username,password=password,database=database)
            return mysql_conn

class emails:
    def send_mail(send_from, send_to, subject, cc='', bcc='', text_msg='',html_msg='', files=[],
                server="smtp.office365.com", port=587, username='ganeshm@prisoft.com', password='cHandu357$',
                use_tls=True):
        msg = MIMEMultipart('alternative')
        msg['From'] = send_from
        msg['To'] = send_to
        # msg['Date'] = formatdate(localtime=True)
        msg['Cc'] = cc
        msg['Bcc'] = bcc
        msg['Subject'] = subject

        part1 = MIMEText(text_msg, 'plain')
        part1.add_header('Content-Disposition', 'inline')

        part2 = MIMEText(html_msg, 'html')
        part2.add_header('Content-Disposition', 'inline')
        
        msg.attach(part1)
        msg.attach(part2)

        for path in files:
            part = MIMEBase('application', "octet-stream")
            with open(path, 'rb') as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename={}'.format(Path(path).name))
            msg.attach(part)

        smtp = smtplib.SMTP(server, port)
        if use_tls:
            smtp.starttls()
        smtp.login(username, password)
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.quit()

    def send_email_verification(send_to, verify_token):
        html_body = """\
        <html>
            <head></head>
            <body style="font-family: "Trebuchet MS";">
                <div class="main-wrapper">
                    <div class="mid-section">
                        <img style="max-height:50px; height:50px;" src="https://amazonx.prisoft.com/wp-content/uploads/2023/06/logo50px.png" alt="logo"/>
                        <h1> Welcome to AmazonX </h1>
                        <p>Thank you for Registering<br>
                        Please click the following link to verify your account:
                        <a href="{token}"><b>Verification Link</b></a><br><br><br>
                        If it is not you please contact support@amazonx.com</p>
                    </div>
                </div>
            </body>
        </html>
        """.format(token=verify_token)
        emails.send_mail(send_from='ganeshm@prisoft.com', send_to=send_to, subject="AmaxonX Verification Email",html_msg = html_body)

    def send_email_forgot_password(send_to, verify_token):
        html_body = """\
        <html>
            <head></head>
            <body style="font-family: "Trebuchet MS";">
                <div class="main-wrapper">
                    <div class="mid-section">
                        <img style="max-height:50px; height:50px;" src="https://amazonx.prisoft.com/wp-content/uploads/2023/06/logo50px.png" alt="logo"/>
                        <h3> Reset Your Password </h3>
                        Please click the following link to reset your account password:
                        <a href="{token}"><b>Reset Password Link</b></a><br><br><br>
                        If it is not you please contact support@amazonx.com</p>
                    </div>
                </div>
            </body>
        </html>
        """.format(token=verify_token)
        emails.send_mail(send_from='ganeshm@prisoft.com', send_to=send_to, subject="Reset Password : AmazonX",html_msg = html_body)

class formdata:
    ax_detailed_default = {
        "userid":"",
        "userpronoun":"",
        "userpronoun_others":"",
        "ax_title":"",
        "ax_date_from":"",
        "ax_date_to":"",
        "ax_emp_id":"",
        "ax_email_id":"",
        "ax_global_rank":"",
        "ax_reason_leave":"",
        "aws_specialization":"",
        "aws_skills":"",
        "aws_service_offerings":"",
        "ax_compensation":"",
        "ce_company_name":"",
        "ce_title":"",
        "ce_join_date":"",
        "ce_reason_looking":"",
        "ce_compensation":"",
        "ce_availability":"",
        "aws_endorser_name":"",
        "aws_endorser_title":"",
        "aws_endorser_email":"",
        "aws_endorser_phone_cd":"",
        "aws_endorser_phone":"",
        "aws_endorser_consent":0,
        "user_link_github":"",
        "user_link_linkedin":"",
        "user_link_portfolio":"",
        "user_link_others":"",
        "ai_workauth_us":"",
        "ai_additional_info":"",
        "ai_current_location":"",
        "ai_profile_summary":"",
        "profile_picture_path":"media/user-profile/default.png",
        "resume_path":"",
        "submit_consent":0,
        "profile_completion_percent":20,
        "section-1":0,
        "section-2":0,
        "section-3":0,
        "section-4":0,
        "section-5":0,
        "section-6":0
    }
    
    def merge_dict(main, temp, index=None):
        for (mk,mv) in main.items():
            for (tk,tv) in temp.items():
                if(mk.lower()==tk.lower()):
                    if(index==None):
                        main[mk] = tv
                    else:
                        main[mk] = tv[index]
        return main

class sql_statements:
    db_config = 'MYSQL_AX_HOSTINGER_ENC'

    def transact(sql_query):
        print(sql_query)
        conn = dbconn.from_config.mysql(sql_statements.db_config,'MASTER_KEYS',True)
        cursor = conn.execute(text(sql_query).execution_options(autocommit=True))
        conn.commit()
        conn.close()
        return cursor.rowcount

    def fetchone(sql_query):
        print(sql_query)
        conn = dbconn.from_config.mysql(sql_statements.db_config,'MASTER_KEYS',True)
        cursor = conn.execute(text(sql_query).execution_options(autocommit=True))
        if(cursor.rowcount == 0):
            conn.close()
            return False
        else:
            row = cursor.fetchone()
            conn.close()
            return row

    def init_ax_employee_detailed(uid):
        sql_initialize = f"""INSERT INTO ax_employee_detailed (UID) VALUES({uid})"""
        try:
            cursor = sql_statements.transact(sql_initialize)
        except Exception as e:
            if('Duplicate entry' in str(e)):
                print("-----> Pass Duplicate Entry Error.")
            else:
                raise Exception(str(e))
            
    def select_ax_employee_detailed(uid):
        # sql_sel=f"""SELECT * FROM u704854418_amazonx_db.ax_employee_detailed where uid={uid}"""
        sql_sel=f"""SELECT ROWID, UID, USERPRONOUN, USERPRONOUN_OTHERS, AX_TITLE, AX_DATE_FROM, AX_DATE_TO, AX_EMP_ID, AX_EMAIL_ID, 
        AX_GLOBAL_RANK, AX_REASON_LEAVE, AWS_SPECIALIZATION, AWS_SKILLS, AWS_SERVICE_OFFERINGS, AX_COMPENSATION, CE_COMPANY_NAME, 
        CE_TITLE, CE_JOIN_DATE, CE_REASON_LOOKING, CE_COMPENSATION, CE_AVAILABILITY, AWS_ENDORSER_NAME, AWS_ENDORSER_TITLE, AWS_ENDORSER_EMAIL, 
        AWS_ENDORSER_PHONE_CD, AWS_ENDORSER_PHONE, AWS_ENDORSER_CONSENT, USER_LINK_GITHUB, USER_LINK_LINKEDIN, USER_LINK_PORTFOLIO, 
        USER_LINK_OTHERS, AI_WORKAUTH_US, AI_ADDITIONAL_INFO, AI_CURRENT_LOCATION, AI_PROFILE_SUMMARY, PROFILE_PICTURE_PATH, RESUME_PATH, SUBMIT_CONSENT, 
        PROFILE_COMPLETION_PERCENT
        FROM u704854418_amazonx_db.ax_employee_detailed where uid={uid}"""
        try:
            row = sql_statements.fetchone(sql_sel)
            if(row != False):
                print(row)
                to_dict = {
                    "userid":row[1],
                    "userpronoun":row[2],
                    "userpronoun_others":row[3],
                    "ax_title":row[4],
                    "ax_date_from":str(row[5]),
                    "ax_date_to":str(row[6]),
                    "ax_emp_id":row[7],
                    "ax_email_id":row[8],
                    "ax_global_rank":row[9],
                    "ax_reason_leave":row[10],
                    "aws_specialization":row[11],
                    "aws_skills":row[12],
                    "aws_service_offerings":row[13],
                    "ax_compensation":row[14],
                    "ce_company_name":row[15],
                    "ce_title":row[16],
                    "ce_join_date":str(row[17]),
                    "ce_reason_looking":row[18],
                    "ce_compensation":row[19],
                    "ce_availability":row[20],
                    "aws_endorser_name":row[21],
                    "aws_endorser_title":row[22],
                    "aws_endorser_email":row[23],
                    "aws_endorser_phone_cd":row[24],
                    "aws_endorser_phone":row[25],
                    "aws_endorser_consent":row[26],
                    "user_link_github":row[27],
                    "user_link_linkedin":row[28],
                    "user_link_portfolio":row[29],
                    "user_link_others":row[30],
                    "ai_workauth_us":row[31],
                    "ai_additional_info":row[32],
                    "ai_current_location":row[33],
                    "ai_profile_summary":row[34],
                    "profile_picture_path":row[35],
                    "resume_path":row[36],
                    "submit_consent":row[37],
                    "profile_completion_percent":row[38],
                }
                return to_dict
            else:
                return 0
        except Exception as e:
            print(str(e))
    
    def update_ax_employee_detailed(uid, form_dict):
        f = form_dict
        sql_upt = f"""UPDATE u704854418_amazonx_db.ax_employee_detailed
        SET USERPRONOUN='{f['userpronoun']}', 
        USERPRONOUN_OTHERS='{f['userpronoun_others']}', 
        AX_TITLE='{f['ax_title']}', 
        AX_DATE_FROM='{f['ax_date_from']}', 
        AX_DATE_TO='{f['ax_date_to']}', 
        AX_EMP_ID='{f['ax_emp_id']}', 
        AX_EMAIL_ID='{f['ax_email_id']}', 
        AX_GLOBAL_RANK= '{f['ax_global_rank']}', 
        AX_REASON_LEAVE='{f['ax_reason_leave']}', 
        AWS_SPECIALIZATION='{f['aws_specialization']}', 
        AWS_SKILLS='{f['aws_skills']}', 
        AWS_SERVICE_OFFERINGS='{f['aws_service_offerings']}', 
        AX_COMPENSATION='{f['ax_compensation']}', 
        CE_COMPANY_NAME='{f['ce_company_name']}', 
        CE_TITLE='{f['ce_title']}', 
        CE_JOIN_DATE='{f['ce_join_date']}', 
        CE_REASON_LOOKING='{f['ce_reason_looking']}', 
        CE_COMPENSATION='{f['ce_compensation']}', 
        CE_AVAILABILITY='{f['ce_availability']}', 
        AWS_ENDORSER_NAME='{f['aws_endorser_name']}', 
        AWS_ENDORSER_TITLE='{f['aws_endorser_title']}', 
        AWS_ENDORSER_EMAIL='{f['aws_endorser_email']}', 
        AWS_ENDORSER_PHONE_CD='{f['aws_endorser_phone_cd']}', 
        AWS_ENDORSER_PHONE='{f['aws_endorser_phone']}', 
        AWS_ENDORSER_CONSENT='{f['aws_endorser_consent']}', 
        USER_LINK_GITHUB='{f['user_link_github']}', 
        USER_LINK_LINKEDIN='{f['user_link_linkedin']}', 
        USER_LINK_PORTFOLIO='{f['user_link_portfolio']}', 
        USER_LINK_OTHERS='{f['user_link_others']}', 
        AI_WORKAUTH_US='{f['ai_workauth_us']}', 
        AI_ADDITIONAL_INFO='{f['ai_additional_info']}', 
        AI_CURRENT_LOCATION='{f['ai_current_location']}',
        AI_PROFILE_SUMMARY= '{f['ai_profile_summary']}', 
        PROFILE_PICTURE_PATH='{f['profile_picture_path']}', 
        RESUME_PATH='{f['resume_path']}', 
        SUBMIT_CONSENT='{f['submit_consent']}', 
        PROFILE_COMPLETION_PERCENT='{f['profile_completion_percent']}'
        WHERE UID={uid};
        """
        try:
            cursor = sql_statements.transact(sql_upt)
        except Exception as e:
            if('Duplicate entry' in str(e)):
                print("-----> Pass Duplicate Entry Error.")
            else:
                raise Exception(str(e))
    
    def select_profile_public(profile_id):
        sel_public_profile = f""" select r.FULLNAME, r.useremail, r.gender, r.ENDORSER_VERIFIED,concat("+",convert(r.PHONECODE, char)," ",r.PHONE) phonenumber,
        USERPRONOUN, USERPRONOUN_OTHERS, AX_TITLE, AX_DATE_FROM, AX_DATE_TO, AX_EMP_ID, AX_EMAIL_ID, AX_GLOBAL_RANK, AX_REASON_LEAVE, 
        AWS_SPECIALIZATION, AWS_SKILLS, AWS_SERVICE_OFFERINGS, AX_COMPENSATION, 
        CE_COMPANY_NAME, CE_TITLE, CE_JOIN_DATE, CE_REASON_LOOKING, CE_COMPENSATION, CE_AVAILABILITY, 
        AWS_ENDORSER_NAME, AWS_ENDORSER_TITLE, AWS_ENDORSER_EMAIL, AWS_ENDORSER_PHONE_CD, AWS_ENDORSER_PHONE,
        USER_LINK_GITHUB, USER_LINK_LINKEDIN, USER_LINK_PORTFOLIO, USER_LINK_OTHERS, 
        AI_WORKAUTH_US, AI_ADDITIONAL_INFO, AI_CURRENT_LOCATION, AI_PROFILE_SUMMARY, PROFILE_PICTURE_PATH, RESUME_PATH, PROFILE_COMPLETION_PERCENT
        FROM ax_employee_register r
        join ax_employee_detailed d ON r.UID = d.UID 
        where r.PROFILE_ID = '{profile_id}'
        """
        try:
            conn = dbconn.from_config.mysql(sql_statements.db_config,'MASTER_KEYS',True)
            cursor = conn.execute(text(sel_public_profile))
            cols = list(cursor.keys())
            row = cursor.fetchone()
            result = dict()
            for key_index, key in enumerate(cols):
                item = {key.lower():row[key_index]}
                result.update(item)
            print(result)
            conn.close()
            return True, result
        except Exception as e:
            return False, str(e)



        