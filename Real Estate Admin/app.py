from flask import Flask,render_template,url_for,redirect,request,flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# Mysql connection
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "root"
app.config['MYSQL_DB'] = "realestate"
app.config['MYSQL_CURSORCLASS'] = "DictCursor"
mysql = MySQL(app)

# Loading Home Page
@app.route("/")
def home():
    con= mysql.connection.cursor()
    sql="SELECT ID,NAME,MOBILE FROM AGENT"
    con.execute(sql)
    res = con.fetchall()
    return render_template("home.html",datas = res )

# agent sales Report
@app.route("/salesreport",methods=['GET','POST'])
def salesreport():
    if request.method=='POST':
        id =request.form['id']
        cursor= mysql.connection.cursor()
        sql_select_query = """SELECT S.DEAL_NO,S.PID,P.NAME,P.TYPE,P.AREA,P.PRICE,P.AGENT_ID,S.DEAL_DATE FROM PROPERTY P,SALES S WHERE P.PID = S.PID AND AGENT_ID = %s"""
        cursor.execute(sql_select_query, (id,))
        res = cursor.fetchall()
        if res is None:
            return "No data Available!"
        else:
            return render_template("result_sales.html",datas = res)
    return render_template("salesreport.html")

#area wise Report
@app.route("/areareport",methods=['GET','POST'])
def areareport():
    if request.method=='POST':
        area =request.form['area']
        cursor= mysql.connection.cursor()
        sql_select_query = """SELECT PID,AGENT_ID,NAME,OWNER_MOBILE,PRICE,TYPE,AREA FROM PROPERTY WHERE STATUS ="CLOSED" AND AREA = %s"""
        cursor.execute(sql_select_query, (area,))
        res = cursor.fetchall()
        if res is None:
            return "No data Available!"
        else:
            return render_template("result_area.html",datas = res)
    return render_template("areareport.html")

#area wise Report
@app.route("/filter_report",methods=['GET','POST'])
def filter_report():
    if request.method=='POST':
        id =request.form['id']
        area =request.form['area']
        type = request.form['type']
        status = request.form['status']
        cursor= mysql.connection.cursor()
        sql_select_query = """SELECT PID,AGENT_ID,NAME,OWNER_MOBILE,PRICE,AREA,ZIP_CODE FROM PROPERTY WHERE STATUS = %s AND AREA = %s AND AGENT_ID = %s AND TYPE = %s"""
        cursor.execute(sql_select_query, (status,area,id,type,))
        res = cursor.fetchall()
        if res is None:
            return "No data Available!"
        else:
            return render_template("Filter_result.html",datas = res)
    return render_template("filter_report.html")

@app.route("/property_info",methods=['GET','POST'])
def property_info():
    if request.method=='POST':
        id =request.form['id']
        cursor= mysql.connection.cursor()
        sql_select_query = """SELECT * FROM PROPERTY NATURAL JOIN FEATURES WHERE PID = %s"""
        cursor.execute(sql_select_query, (id,))
        res = cursor.fetchall()
        if res is None:
            return "No data Available!"
        else:
            return render_template("property_result.html",datas = res)
    return render_template("property_info.html")






if(__name__=='__main__'):
    app.secret_key="abc123"
    app.run(debug=True)
