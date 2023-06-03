from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/vw_insertDatos')
def vwInsertDatos():
    return render_template('vwInsertDatos.html')


@app.route('/vw_esquemaT')
def vwEsquemaT():
    return render_template('vwEsquemaT.html')








if __name__ == '__main__':
    app.add_url_rule('/',view_func=index)
    app.run(debug=True, port=5005)
