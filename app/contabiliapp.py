from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    titles={
        'title':'ContabiliApp',
        'indexText':'Bienvenido a CONTABILIAPP'
    }
    return render_template('indexTemplate.html',titles=titles)

@app.route('/holaMundo')
def hola_mundo():
    return "Hola Mundo"

if __name__ == '__main__':
    app.add_url_rule('/',view_func=index)
    app.run(debug=True, port=5005)
