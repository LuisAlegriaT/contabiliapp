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
    cur1=mysql.connection.cursor()
    cur1.execute('SELECT * FROM conceptos')
    consulta1 = cur1.fetchall()
    cur2=mysql.connection.cursor()
    cur2.execute('SELECT * FROM deberhaber')
    consulta2 = cur2.fetchall()
    cur3=mysql.connection.cursor()
    cur3.execute('SELECT * FROM datos JOIN conceptos ON datos.concepto_id = conceptos.id_concepto JOIN deberhaber ON datos.deberHaber_id = deberhaber.id_deberHaber WHERE formato_id= %s',[idFormato])
    consulta3 = cur3.fetchall()
    return render_template('vwInsertDatos.html',consulta=consulta,conceptos=consulta1, deberhaber=consulta2, idFormato=idFormato, datos= consulta3)

@app.route('/vw_insertData/<idFormato>',methods=['POST'])
def vwInsertData(idFormato):
    if request.method == ('POST'):
        monto = request.form['monto']
        print(monto)
        Concepto = request.form['Concepto']
        print(Concepto)
        tipo = request.form['tipo']
        print(tipo)
        cur1=mysql.connection.cursor()
        cur1.execute('INSERT INTO datos(monto,concepto_id,deberHaber_id,formato_id) values(%s,%s,%s, %s)',[monto,Concepto,tipo,idFormato])
        mysql.connection.commit()
        return redirect(url_for('vwInsertDatos',idFormato=idFormato)) 


@app.route('/vw_esquemaT/<idFormato>')
def vwEsquemaT(idFormato):
    cursor1=mysql.connection.cursor()
    cursor1.execute('SELECT datos.id_dato, datos.monto, conceptos.tipoConcepto, datos.concepto_id,datos.deberHaber_id FROM formatos INNER JOIN datos ON formatos.id_formato = datos.formato_id INNER JOIN conceptos ON datos.concepto_id=conceptos.id_concepto WHERE formatos.id_formato=%s ',[idFormato])
    mysql.connection.commit()
    cursores = cursor1.fetchone()
    

    if cursores[2] == 'Bancos':
        Bancos = cursores[2]
        cursores1=mysql.connection.cursor()
        cursores1.execute('SELECT datos.monto, datos.id_dato FROM datos INNER JOIN conceptos ON datos.concepto_id=conceptos.id_concepto WHERE conceptos.tipoConcepto=%s AND datos.deberHaber_id = %s AND datos.formato_id = %s',[Bancos, 1, idFormato])
        mysql.connection.commit()  
        cursor1 = cursores1.fetchall()

        cursores2=mysql.connection.cursor()
        cursores2.execute('SELECT datos.monto, datos.id_dato FROM datos INNER JOIN conceptos ON datos.concepto_id=conceptos.id_concepto WHERE conceptos.tipoConcepto=%s AND datos.deberHaber_id = %s AND datos.formato_id = %s',[Bancos,2, idFormato])
        mysql.connection.commit()  
        cursor2 = cursores2.fetchall()
   
    
    
    return render_template('vwEsquemaT.html', consulta1=Bancos, cursor1=cursor1, cursor2=cursor2, )

if __name__ == '__main__':
    app.add_url_rule('/',view_func=index)
    app.run(debug=True, port=5005)
