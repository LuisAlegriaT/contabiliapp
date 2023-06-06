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
    dataEsquemasT=mysql.connection.cursor()
    dataEsquemasT.execute('SELECT datos.id_dato, datos.monto, datos.deberHaber_id, conceptos.id_Concepto FROM formatos INNER JOIN datos ON formatos.id_formato = datos.formato_id INNER JOIN conceptos ON datos.concepto_id=conceptos.id_concepto WHERE formatos.id_formato=%s',[idFormato])
    mysql.connection.commit()
    conjuntoDatos = dataEsquemasT.fetchall()

    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM formatos WHERE id_formato= %s',[idFormato])
    consulta = cur.fetchone()
    cur=mysql.connection.cursor()

    #SUMAS DE BANCOS
    sumaAbonoBa = mysql.connection.cursor()
    sumaAbonoBa.execute('SELECT SUM(datos.monto) FROM formatos INNER JOIN datos ON formatos.id_formato = datos.formato_id INNER JOIN conceptos ON datos.concepto_id=conceptos.id_concepto WHERE formatos.id_formato=%s AND datos.deberHaber_id=1 AND datos.concepto_id=2',[idFormato])
    resultado = sumaAbonoBa.fetchone()
    sumaAbonoBa=mysql.connection.cursor()

    if resultado is not None:#Comprueba si viene vacio
        sumaAbonoBanco = resultado[0]  # Acceder al valor de la suma
    else:
        print("No se encontraron resultados.")

    sumaCargoBa = mysql.connection.cursor()
    sumaCargoBa.execute('SELECT SUM(datos.monto) FROM formatos INNER JOIN datos ON formatos.id_formato = datos.formato_id INNER JOIN conceptos ON datos.concepto_id=conceptos.id_concepto WHERE formatos.id_formato=%s AND datos.deberHaber_id=2 AND datos.concepto_id=2',[idFormato])
    resultado = sumaCargoBa.fetchone()
    sumaCargoBa=mysql.connection.cursor()
    if resultado is not None:
        sumaCargoBanco = resultado[0]
    else:
        print("No se encontraron resultados.") 

    totalBanco=sumaAbonoBanco-sumaCargoBanco #RESTA DE ABONO Y CARGO
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!HACER UN INSERT EN LA TABLA TOTALES EN EL CAMPO TOTAL PONDREMOS LO QUE VALGA LA VARIABLE totalBanco!!!!!!!!!!!!!!!!!!!!!!!


    #AQUI DEBERIA INICIAR SUMA DE INVERSIONES TEMPORALES
    return render_template('vwEsquemaT.html',
                           conjuntoDatos=conjuntoDatos, 
                           consulta=consulta,
                           sumaAbonoBanco=sumaAbonoBanco,
                           sumaCargoBanco=sumaCargoBanco,
                           totalBanco=totalBanco)

if __name__ == '__main__':
    app.add_url_rule('/',view_func=index)
    app.run(debug=True, port=5005)
