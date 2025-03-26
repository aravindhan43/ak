import os
import random
from datetime import date
import re
import PyPDF2
from urllib import request
import pymysql
from PyPDF2 import PdfFileReader
import smtplib, ssl
from flask import Flask, render_template, flash, request, session, current_app, send_from_directory
from werkzeug.utils import redirect, secure_filename


port = 587
smtp_server = "smtp.gmail.com"
sender_email = "serverkey2018@gmail.com"
password ="extazee2018"

# ps = PorterStemmer()
app = Flask(__name__, static_folder="static")
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

################################################################### HOME
@app.route("/")
def homepage():
    return render_template('index.html')
@app.route("/about")
def about_us():
    return render_template('about.html')
#########################################################
@app.route("/admin")
def admin_home():
    return render_template('admin.html')
@app.route("/contact")
def contact():
    return render_template('contact.html')


@app.route("/contact_1",methods = ['GET', 'POST'])
def contact_1():
    if request.method == 'POST':
        name = request.form['textfield']
        contact = request.form['textfield2']
        email = request.form['textfield3']
        comment=request.form['textarea']
        message=name+"\n"+contact+"\n"+email+"\n"+comment
        # context = ssl.create_default_context()
        # email1="arunextazee@gmail.com"
        # with smtplib.SMTP(smtp_server, port) as server:
        #     server.ehlo()  # Can be omitted
        #     server.starttls(context=context)
        #     server.ehlo()  # Can be omitted
        #     server.login(sender_email, password)
        #     server.sendmail(sender_email, email1, message)
    #return render_template('contact.html',data="Mail send Successfully ")
    return render_template('contact.html')

@app.route("/admin_home")
def admin():
    return render_template('admin_home.html')



@app.route("/admin_company")
def admin_company():
    conn = pymysql.connect(user='root', password='', host='localhost', database='python_job_search_portal',
                           charset='utf8')
    cursor = conn.cursor()
    cursor.execute("SELECT cname,contact,email,address,city,state,website FROM company_details")
    data=cursor.fetchall()
    cursor.close()
    return render_template('admin_company.html',items=data)

@app.route("/admin_job")
def admin_job():
    conn = pymysql.connect(user='root', password='', host='localhost', database='python_job_search_portal',
                           charset='utf8')
    cursor1 = conn.cursor()
    cursor1.execute("SELECT job_title,job_type,company_website,date,skills_required,city,state FROM job_details")
    data=cursor1.fetchall()
    cursor1.close()
    return render_template('admin_job.html',items=data)


@app.route("/admin_applicants")
def admin_applicants():
    conn = pymysql.connect(user='root', password='', host='localhost', database='python_job_search_portal',
                           charset='utf8')
    cursor1 = conn.cursor()
    cursor1.execute("SELECT applicant_name,contact,email,dob,experience,address,city,state FROM user_details")
    data=cursor1.fetchall()
    cursor1.close()
    return render_template('admin_applicants.html',items=data)

@app.route("/admin_login", methods = ['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['pass'] == 'admin':
            return render_template('admin_home.html',error=error)
        else:
            return render_template('admin.html', error=error)
    return render_template('admin.html', error=error)
########################################################
@app.route("/company")
def company():
    return render_template('company.html')

@app.route("/company_posted_job")
def company_posted_job():
    conn = pymysql.connect(user='root', password='', host='localhost', database='python_job_search_portal',charset='utf8')
    cm=session['company']
    cursor = conn.cursor()
    cursor.execute("SELECT id,job_title,job_type,company_website,date,skills_required,city,state FROM job_details where report='"+cm+"'")
    data=cursor.fetchall()
    tmp=[]
    i=0
    for xx in data:
        i=i+1
        id=xx[0]
        job_title=xx[1]
        job_type=xx[2]
        company_website=xx[3]
        date=xx[4]
        skills_required=xx[5]
        city=xx[6]
        state=xx[7]
        tmp.append([i,job_title,job_type,company_website,date,skills_required,city,state])

    return render_template('company_posted_job.html',items=tmp)



@app.route("/company_applicant_profile")
def company_applicant_profile():
    conn = pymysql.connect(user='root', password='', host='localhost', database='python_job_search_portal',
                           charset='utf8')
    cursor = conn.cursor()
    company=session['company']
    cursor.execute("SELECT id,uname,cdate,report FROM user_apply where cid='"+str(company)+"'")
    data=cursor.fetchall()
    tmp = []
    i = 0
    for xx in data:
        i = i + 1
        id = xx[0]
        uname = xx[1]
        cdate = xx[2]
        report = xx[3]

        tmp.append([i, uname, cdate, report])

    return render_template('company_applicant_profile.html',items=tmp)

@app.route("/company_register")
def company_register():
    return render_template('company_registration.html')

@app.route("/company_register1",methods = ['GET', 'POST'])
def company_register1():
    conn = pymysql.connect(user='root', password='', host='localhost', database='python_job_search_portal',
                           charset='utf8')
    if request.method == 'POST':
        cname = request.form['cname']
        contact = request.form['contact']
        email = request.form['email']
        address = request.form['address']
        city = request.form['district']
        state = request.form['countrya']
        country = request.form['state']
        website = request.form['website']
        password = request.form['password']
        cpass = request.form['cpass']
        if password==cpass:
            cursor = conn.cursor()
            cursor.execute("SELECT max(id)+1 FROM   company_details")
            maxid = cursor.fetchone()[0]
            if maxid is None:
                maxid=1
            cursor = conn.cursor()
            cursor.execute("insert into company_details values('"+str(maxid) + "','"+cname + "','"+contact+"','"+email+"','"+address+"','"+city+"','"+state+"','"+country+"','"+website+"','"+password+"')")
            conn.commit()
        else:
            d=0
        return render_template('company.html')

@app.route("/company_login",methods = ['GET', 'POST'])
def student_login():
    conn = pymysql.connect(user='root', password='', host='localhost', database='python_job_search_portal',
                           charset='utf8')
    if request.method == 'POST':
        n = request.form['uname']
        g = request.form['pass']

        cursor1 = conn.cursor()
        cursor1.execute("SELECT * from company_details where email='" + str(n) + "' and password='" + str(g) + "'")
        #data = cursor.fetchone()
        myresult = cursor1.fetchall()
        print(myresult)

        cursor1.close()
        if (len(myresult)==0):
            return render_template('company.html')
        else:
            a1 = "";
            for x in myresult:
                print(x)
                a1 = x
            d = (a1[1])
            print(d)
            session['company'] = d
            session['uname'] =n
            print(n)
            return render_template('company_home.html',sid=n)
    return render_template('company.html')

@app.route("/user")
def user():
    return render_template('user.html')

@app.route("/user_register")
def user_register():
    data=['-select-','India','Pakistan']
    return render_template('user_register.html',items=data)

@app.route("/user_reg")
def user_reg():
    data=['-select-','India','Pakistan']
    return render_template('user_register.html',items=data)

@app.route("/user_register_1/<string:filename>",methods = ['GET', 'POST'])
def user_register_1(filename):
    if request.method == 'POST':
        applicant_name = request.form['applicant_name']
        return  filename
    return filename

@app.route("/user_register1",methods = ['GET', 'POST'])
def user_register1():
    conn = pymysql.connect(user='root', password='', host='localhost', database='python_job_search_portal',
                           charset='utf8')
    if request.method == 'POST':
        applicant_name = request.form['applicant_name']
        contact = request.form['contact']
        email = request.form['email']
        dob = request.form['dob']
        qualification = request.form['qualification']
        experience = request.form['experience']
        address = request.form['address']
        city = request.form['district']
        state = request.form['countrya']
        country = request.form['state']
        password = request.form['password']
        cpass = request.form['cpass']
        if password==cpass:
            if 'file' not in request.files:
                flash('No file Part')
                return redirect(request.url)
            file= request.files['file']
            print(file)
            f = request.files['file']
            f.save(os.path.join("static/uploads/", secure_filename(f.filename)))

            cursor = conn.cursor()
            cursor.execute("SELECT max(id)+1 FROM   user_details")
            maxid = cursor.fetchone()[0]
            if maxid is None:
                maxid=1
            maxid=1
            cursor.close()
            cursor1 = conn.cursor()
            cursor1.execute("insert into user_details values('"+str(maxid) + "','"+str(applicant_name) + "','"+str(contact)+"','"+str(email)+"','"+str(dob)+"','"+str(qualification)+"','"+str(experience)+"','"+str(address)+"','"+str(city)+"','"+str(state)+"','"+str(password)+"','0','"+str(country)+"','"+f.filename+"')")
            conn.commit()
            cursor1.close()
            return render_template('user.html')
        else:
            return render_template('user_register.html')

@app.route("/user_login",methods = ['GET', 'POST'])
def user_login():
    conn = pymysql.connect(user='root', password='', host='localhost', database='python_job_search_portal',
                           charset='utf8')
    if request.method == 'POST':
        n = request.form['uname']
        g = request.form['pass']
        n1=str(g)
        g1=str(g)
        cursor = conn.cursor()
        cursor.execute("SELECT * from user_details where email='" + n + "' and password='" + str(g) + "'")
        data = cursor.fetchone()
        conn.commit()
       # cursor.close()
        if data is None:
            return render_template("user.html", data='Username or Password is wrong')
        else:
            session['uname'] =n
            #print(n)
            return render_template('user_home.html',sid=n)
    return render_template('user.html')
################################################################### COMPANY

@app.route("/company_home")
def company_home():
    return render_template('company_home.html')

@app.route("/company_new_job")
def company_new_job():
    return render_template('company_new_job.html')

@app.route("/company_new_job1",methods = ['GET', 'POST'])
def company_new_job1():
    conn = pymysql.connect(user='root', password='', host='localhost', database='python_job_search_portal',
                           charset='utf8')
    if request.method == 'POST':
        job_title = request.form['job_title']
        job_type = request.form['job_type']
        company_website = request.form['company_website']
        date = request.form['date']
        skills_required = request.form['skills_required']
        country=request.form['state']
        city = request.form['district']
        state = request.form['countrya']
        d=session['company']
        cursor = conn.cursor()
        cursor.execute("SELECT max(id)+1 FROM   job_details")
        maxid = cursor.fetchone()[0]
        if maxid is None:
            maxid=1
        cursor = conn.cursor()
        cursor.execute("insert into job_details values('"+str(maxid) + "','"+job_title + "','"+job_type+"','"+company_website+"','"+date+"','"+skills_required+"','"+city+"','"+state+"','"+country+"','"+d+"')")
        conn.commit()
        cursor.close()
        return render_template('company_home.html')

##################### USER
@app.route("/user_home")
def user_home():
    return render_template('user_home.html')

@app.route("/user_jobs")
def user_jobs():
    conn = pymysql.connect(user='root', password='', host='localhost', database='python_job_search_portal',
                           charset='utf8')
    cur = conn.cursor()
    cur.execute("SELECT distinct city,state FROM job_details")
    data = cur.fetchall()

    return render_template('user_jobs.html',data=data)

@app.route("/user_applied",methods = ['GET', 'POST'])
def user_applied():
    conn = pymysql.connect(user='root', password='', host='localhost', database='python_job_search_portal',
                           charset='utf8')
    uname =session['uname']
    cursor = conn.cursor()
    cursor.execute("select id,cid,cdate from user_apply where uname='"+uname+"'")
    i=0
    tmp=[]
    dd=cursor.fetchall()
    for xx in dd:
        i=i+1
        tmp.append([i,xx[1],xx[2]])
    return render_template('user_applied.html',items=tmp)

@app.route("/user_forgot")
def user_forgot():
    return render_template('user_forgot.html')

@app.route("/user_forgot1",methods = ['GET', 'POST'])
def user_forgot1():
    conn = pymysql.connect(user='root', password='', host='localhost', database='python_job_search_portal',
                           charset='utf8')
    if request.method == 'POST':
        email = request.form['uname']
        print(email)
        session['email']=email
        cursor = conn.cursor()
        cursor.execute("SELECT * from user_details where email='" + email + "'")
        data = cursor.fetchone()
        if data is None:
            return 'Data Not Found'
        else:
            r=random.randrange(1000, 9999)
            message = """\
            Subject: Forgot Password

            OTP :"""+str(r)
            context = ssl.create_default_context()
            with smtplib.SMTP(smtp_server, port) as server:
                server.ehlo()  # Can be omitted
                server.starttls(context=context)
                server.ehlo()  # Can be omitted
                server.login(sender_email, password)
                server.sendmail(sender_email, email, message)
            cursor = conn.cursor()
            cursor.execute('update user_details set report=%s WHERE email = %s', (r, email))
            conn.commit()
            session['email'] = email
            session['otp'] = r
    return render_template('user_forgot2.html',data=email)


@app.route("/user_forgot3",methods = ['GET', 'POST'])
def user_forgot3():
    if request.method == 'POST':
        otp = int(request.form['otp'])
        otp1= int(session['otp'])
        print(otp,otp1)
        if otp==otp1:
            print("ss")
            return render_template('user_forgot3.html')
        else:
            print("mnnn")
            return render_template('user_forgot.html')


@app.route("/user_forgot4",methods = ['GET', 'POST'])
def user_forgot4():
    conn = pymysql.connect(user='root', password='', host='localhost', database='python_job_search_portal',
                           charset='utf8')
    if request.method == 'POST':
        p1 = request.form['p1']
        p2= request.form['p2']
        email=session['email']
        if p1==p2:
            f=0
            cursor = conn.cursor()
            cursor.execute('update user_details set password=%s WHERE email = %s', (p1, email))
            conn.commit()
            return render_template('user.html')
        else:
            return render_template('user_forgot3.html')



@app.route('/user_job_s',methods = ['GET', 'POST'])
def user_file_recei_s():
    conn = pymysql.connect(user='root', password='', host='localhost', database='python_job_search_portal',
                           charset='utf8')
    if request.method == 'POST':
        cur = conn.cursor()
        cur.execute("SELECT distinct city,state FROM job_details")
        data = cur.fetchall()
        job_title = request.form['job_title']
        city = request.form['district']
        state = request.form['countrya']
        cursor = conn.cursor()
        cursor.execute("SELECT id,job_title,job_type,company_website,date,skills_required,city,state FROM job_details where job_title='"+job_title+"' and city='"+city+"' and state='"+state+"' ")
        hh=cursor.fetchall()
        tmp=[]
        i=0
        print(hh)
        for xx in hh:
            i = i + 1
            id = xx[0]
            job_title = xx[1]
            job_type = xx[2]
            company_website = xx[3]
            date = xx[4]
            skills_required = xx[5]
            city = xx[6]
            state = xx[7]
            tmp.append([i, job_title, job_type, company_website, date, skills_required, city, state,id])


        return render_template('user_jobs.html', items=tmp,data=data)
@app.route('/student_college2/<string:filename>', methods=['GET','POST'])
def user_file_recei1(filename):
    conn = pymysql.connect(user='root', password='', host='localhost', database='python_job_search_portal',
                           charset='utf8')
    data=[]
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM job_details where id='"+filename+"'")
    data=cursor.fetchall()
    for x in data:
        print(x)
        a1=x

    d=(a1[9])

    session['cname']=d
    session['cid']=filename
    if request.method == 'POST':
        f=filename
        return render_template('user_jobs1.html', items=data)
    return render_template('user_jobs1.html', items=data)


@app.route('/user_review/<string:filename>', methods=['GET','POST'])
def student_college_review(filename):
    conn = pymysql.connect(user='root', password='', host='localhost', database='python_job_search_portal',
                           charset='utf8')
    data=[]
    cursor = conn.cursor()
    cursor.execute("SELECT user,cdate,commends FROM user_review where cid='"+filename+"'")
    data=cursor.fetchall()
    session['cid']=filename
    if request.method == 'POST':
        f=filename

        return render_template('user_review.html', items=data)
    return render_template('user_review.html', items=data)


@app.route("/user_review1",methods = ['GET', 'POST'])
def student_college_review1():
    conn = pymysql.connect(user='root', password='', host='localhost', database='python_job_search_portal',
                           charset='utf8')
    if request.method == 'POST':
        today = date.today()
        cdate = today.strftime("%d-%m-%Y")
        commends = request.form['textfield']
        user =session['uname']
        cid =session['cid']


        cursor = conn.cursor()
        cursor.execute("SELECT max(id)+1 FROM   user_review")
        maxid = cursor.fetchone()[0]
        if maxid is None:
            maxid=1
        cursor1 = conn.cursor()
        cursor1.execute("insert into user_review values('"+str(maxid) + "','"+cid+"','"+user+"','"+commends+"','"+cdate+"','0','0')")
        conn.commit()
        ###########################
        p1 = session['cid']
        cursor = conn.cursor()
        cursor.execute("select user,cdate,commends from user_review where cid='"+p1+"'")
    return render_template('user_review.html',items=cursor.fetchall())



@app.route("/user_apply",methods = ['GET', 'POST'])
def user_apply():
    conn = pymysql.connect(user='root', password='', host='localhost', database='python_job_search_portal',
                           charset='utf8')
    if request.method == 'POST':
        today = date.today()
        cdate = today.strftime("%d-%m-%Y")
        cid =session['cid']
        uname =session['uname']
        d=session['cname']
        if 'file' not in request.files:
            flash('No file Part')
            return redirect(request.url)
        file= request.files['file']
        print(file)
        f = request.files['file']
        f.save(os.path.join("static/uploads/", secure_filename(f.filename)))
        cursor = conn.cursor()
        cursor.execute("SELECT max(id)+1 FROM   user_apply")
        maxid = cursor.fetchone()[0]
        if maxid is None:
            maxid=1
        cursor1 = conn.cursor()
        cursor1.execute("insert into user_apply values('"+str(maxid) + "','"+str(d)+"','"+uname+"','"+cdate+"','0','"+f.filename+"')")
        conn.commit()
        ###########################
        cursor2 = conn.cursor()
        cursor2.execute("select id,cid,cdate from user_apply where uname='"+uname+"'")
        tmp=[]
        i=0
        dd=cursor2.fetchall()
        for xx in dd:
            i=i+1
            tmp.append([i,xx[1],xx[2]])
        return render_template('user_applied.html',items=tmp)
    return render_template('user_applied.html')

@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    print(filename)
    uploads = os.path.join(current_app.root_path, "static\\uploads\\")
    print(uploads)
    f=filename
    uploads = os.path.join(current_app.root_path, "static/uploads")
    return send_from_directory(uploads, filename)
    # return send_from_directory(directory=uploads,path=uploads, filename=filename,as_attachment=True)
##########################
@app.route("/company_matching_profile")
def company_matching_profile():
    conn = pymysql.connect(user='root', password='', host='localhost', database='python_job_search_portal',
                           charset='utf8')
    cm = session['company']
    cursor = conn.cursor()
    cursor.execute("SELECT skills_required FROM job_details where report='" + cm + "'")
    data = cursor.fetchall()
    sample=data
    result_data=list()
    #print(data)
    #print(data[0])
    for x in data:

        try:
            wordList = x[0].split()
        except:
            wordList =x


        for y in wordList:
            #print(y)

            cursor1 = conn.cursor()
            cursor1.execute("SELECT email,report FROM user_details")
            user_data = cursor1.fetchall()

            user_email= tuple()
            user_emaily = list(user_email)

            for z in user_data:
                username=z[0]
                resume=z[1]

                res=read_pdf(y,resume)
                #print(x, username,res)
                if(res=="success"):
                    user_emaily.append([username,x])
                    #print(resume)
                    result_data.append([username,y,resume])

                #print(user_emaily)

    return render_template('company_matching_profile.html',data=(result_data),data1=sample)
######################

def read_pdf(key,file):
    sss=os.path.join("static/uploads/", secure_filename(file))
    print(sss)
    pdf_document = sss#secure_filename(file)
    read_data=''
    with open(pdf_document, "rb") as filehandle:
        pdf = PdfFileReader(filehandle)
        info = pdf.getDocumentInfo()
        pages = pdf.getNumPages()

        #print(info)
        #print("number of pages: %i" % pages)
        for i in range(pages):
            #print(i)
            page1 = pdf.getPage(i)
            read_data+=page1.extractText()
        ss=read_data.lower()
        #print(key,ss)
        if key in ss:
            return('success')
        else:
             return('failed')







@app.route('/user_profile',methods = ['GET', 'POST'])
def user_profile():
    conn = pymysql.connect(user='root', password='', host='localhost', database='python_job_search_portal',
                           charset='utf8')
    uname=session['uname']
    print(uname)
    cursor2 = conn.cursor()
    cursor2.execute("select applicant_name,contact,email,dob,qualification,experience,address,report,password from user_details where email='" + uname + "'")

    return render_template('user_profile.html',data=cursor2.fetchall())

@app.route("/user_profile1",methods = ['GET', 'POST'])
def user_profile1():
    conn = pymysql.connect(user='root', password='', host='localhost', database='python_job_search_portal',
                           charset='utf8')
    if request.method == 'POST':
        applicant_name = request.form['applicant_name']
        contact = request.form['contact']
        email = request.form['email']
        dob = request.form['dob']
        qualification = request.form['qualification']
        experience = request.form['experience']
        address = request.form['address']


        password = request.form['password']

        if password==password:
            if 'file' not in request.files:
                flash('No file Part')
                return redirect(request.url)
            file= request.files['file']

            f = request.files['file']
            dd=file.filename
            print("file", dd)
            qry = "update  user_details set applicant_name='" + str(applicant_name) + "',contact='" + str(
                contact) + "',email='" + str(email) + "',dob='" + str(dob) + "',qualification='" + str(
                qualification) + "',experience='" + str(experience) + "',address='" + str(
                address) + "',password='" + str(
                password) + "' where email='" + email + "'"

            if(len(dd)!=0):
                f.save(os.path.join("static/uploads/", secure_filename(f.filename)))
                qry = "update  user_details set applicant_name='" + str(applicant_name) + "',contact='" + str(
                    contact) + "',email='" + str(email) + "',dob='" + str(dob) + "',qualification='" + str(
                    qualification) + "',experience='" + str(experience) + "',address='" + str(
                    address) + "',password='" + str(
                    password) + "',report='" + f.filename + "' where email='" + email + "'"



            cursor1 = conn.cursor()
            #print(qry)
            cursor1.execute(qry)
            conn.commit()
            cursor1.close()
            return user_profile()
        else:
            return user_profile()
    return user_profile()

######################################
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)