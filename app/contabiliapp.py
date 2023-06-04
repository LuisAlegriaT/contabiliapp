from colorama import Cursor
from flask import Flask, render_template, request ,redirect,url_for,flash 
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= ''
app.config['MYSQL_DB']= 'dbcontabiliapp'
mysql= MySQL(app)
app.secret_key='mysecretkey'

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/vw_insertFormatos',methods=['POST'])
def vwInsertFormatos():
    if request.method == ('POST'):
        formato = request.form['formato']
        print(formato)
        cur=mysql.connection.cursor()
        cur.execute('INSERT INTO formatos(nombre)values(%s)',[formato])
        mysql.connection.commit()

        cursos=mysql.connection.cursor()
        cursos.execute('SELECT * FROM formatos WHERE nombre= %s',[formato])
        consulta = cursos.fetchall()
        print(consulta)
        return render_template('Become.html', Formato= consulta)


@app.route('/vw_insertDatos/<idFormato>')
def vwInsertDatos(idFormato):
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM formatos WHERE id_formato= %s',[idFormato])
    consulta = cur.fetchall()
    return render_template('vwInsertDatos.html',consulta=consulta)


@app.route('/vw_esquemaT')
def vwEsquemaT():
    return render_template('vwEsquemaT.html')








if __name__ == '__main__':
    app.add_url_rule('/',view_func=index)
    app.run(debug=True, port=5005)
