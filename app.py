from flask import Flask, render_template, request, redirect, url_for, flash, \
    Response, session
from flask_bootstrap import Bootstrap
from filters import datetimeformat, file_type
from resources import get_bucket, get_buckets_list

app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'secret'
app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.filters['file_type'] = file_type

@app.route('/')
def index():
   return render_template('login.html')
@app.route('/ind')
def ind():
    return render_template('signup.html')
@app.route('/hell',methods = ['POST', 'GET'])
def hell():
   if request.method == 'POST':

         
         con = sqlite3.connect('mydatabase.db')
         uname = request.form['uname']
         pwd = request.form['pwd']
         cursorObj = con.cursor()
         cur = con.cursor()
         cursorObj = con.cursor()
         login=cursorObj.execute("SELECT * FROM signup WHERE email= ? and pwd= ?;",(uname,pwd))
         con.commit()
         if (len(login.fetchall()) > 0):
                   return render_template("index.html")
         else:
                   return render_template("login.html")
@app.route('/gol',methods = ['POST', 'GET'])
def gol():
   if request.method == 'POST':
         con = sqlite3.connect('mydatabase.db')

         def sql_insert(con):
             fname = request.form['fname']
             lname = request.form['lname']
             email = request.form['email']
             pwd = request.form['pwd']
             pwdr = request.form['pwdr']
             cursorObj = con.cursor()
             cur = con.cursor()
             cursorObj.execute("INSERT INTO signup(fname,lname,email,pwd,pwdr) VALUES('"+fname+"','"+lname+"','"+email+"','"+pwd+"','"+pwdr+"')")
             
             con.commit()
             
             
         sql_insert(con)
            
         return render_template("thankyou.html")

@app.route('/main', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        bucket = request.form['bucket']
        session['bucket'] = bucket
        return redirect(url_for('files'))
    else:
        buckets = get_buckets_list()
        return render_template("index.html", buckets=buckets)


@app.route('/files')
def files():
    my_bucket = get_bucket()
    summaries = my_bucket.objects.all()

    return render_template('files.html', my_bucket=my_bucket, files=summaries)


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']

    my_bucket = get_bucket()
    my_bucket.Object(file.filename).put(Body=file)

    flash('File uploaded successfully')
    return redirect(url_for('files'))


@app.route('/delete', methods=['POST'])
def delete():
    key = request.form['key']

    my_bucket = get_bucket()
    my_bucket.Object(key).delete()

    flash('File deleted successfully')
    return redirect(url_for('files'))


@app.route('/download', methods=['POST'])
def download():
    key = request.form['key']

    my_bucket = get_bucket()
    file_obj = my_bucket.Object(key).get()

    return Response(
        file_obj['Body'].read(),
        mimetype='text/plain',
        headers={"Content-Disposition": "attachment;filename={}".format(key)}
    )


if __name__ == "__main__":
    app.run()
