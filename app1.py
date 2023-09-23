from flask import Flask, render_template, url_for, redirect, request, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
# MYSQL CONNECTION
app.config["MYSQL_HOST"] = "localhost" #host name
app.config["MYSQL_USER"] = "root" #database root name
app.config["MYSQL_PASSWORD"] = "12345" #my database passwordr̥
app.config["MYSQL_DB"] = "imdb" # my data base name
app.config["MYSQL_CURSORCLASS"] = "DictCursor" #data receving in a dict format
mysql = MySQL(app)


# Loading Home Page
@app.route("/")
def home():
    con = mysql.connection.cursor()
    sql = "SELECT * FROM IMDB"
    con.execute(sql)
    res = con.fetchall()
    return render_template('admin.html', datas=res)

#USER page
@app.route("/User")
def userhome():
    con = mysql.connection.cursor()
    sql = "SELECT * FROM IMDB"
    con.execute(sql)
    res = con.fetchall()
    return render_template("User.html", datas=res)

# New User
@app.route("/addUsers", methods=['GET', 'POST'])
def addUsers():
    if request.method == 'POST':
        movie_name = request.form['movie_name']
        imdb_score = request.form['imdb_score']
        director = request.form['director']
        genre = request.form['genre']
        popularity = request.form['popularity']
        con = mysql.connection.cursor()
        sql = "insert into imdb(MOVIE_NAME, IMDB_SCORE, DIRECTOR, GENRE, POPULARITY) value (%s,%s,%s,%s,%s)"
        con.execute(sql, [movie_name, imdb_score, director, genre, popularity])
        mysql.connection.commit()
        con.close()
        flash('IMDB Details Added')
        return redirect(url_for("home"))
    return render_template("add.html")


# update User
@app.route("/editUser/<string:id>", methods=['GET', 'POST'])
def editUser(id):
    con = mysql.connection.cursor()
    if request.method == 'POST':
        movie_name = request.form['movie_name']
        director = request.form['director']
        imdb_score = request.form['imdb_score']
        genre = request.form['genre']
        popularity = request.form['popularity']
        con = mysql.connection.cursor()
        sql = "update imdb set MOVIE_NAME=%s,DIRECTOR=%s,IMDB_SCORE=%s, GENRE=%s, POPULARITY=%s where ID=%s"
        con.execute(sql, [movie_name, director, imdb_score, genre, popularity, id])
        mysql.connection.commit()
        con.close()
        flash('IMDB Detail Updated')
        return redirect(url_for("home"))


    sql = "select * from imdb where ID=%s"
    con.execute(sql, [id])
    res = con.fetchone()
    return render_template("update.html", datas=res)


# Delete data
@app.route("/delete/<string:id>", methods=['GET', 'POST'])
def delete(id):
    con = mysql.connection.cursor()
    sql = "delete from imdb where (ID = %s) "
    # abc= str(id)
    con.execute("delete from imdb where ID = %s", [id])
    mysql.connection.commit()
    con.close()
    flash('IMDB Details Deleted')
    return redirect(url_for("home"))

#SEARCH page
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    con = mysql.connection.cursor()
    sql = "SELECT * FROM IMDB WHERE GENRE LIKE %s"
    con.execute(sql, ['%' + query + '%',])
    results = con.fetchall()
    con.close()
    return render_template('search.html', results=results)

if (__name__ == '__main__'):
    app.secret_key = "abc123"
    app.run(debug=True)






