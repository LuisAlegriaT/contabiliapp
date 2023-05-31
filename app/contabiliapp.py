from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Bienvenido al curso de Codigo Facilito YAZ"

@app.route('/holaMundo')
def hola_mundo():
    return "Hola Mundo"

if __name__ == '__main__':
    app.add_url_rule('/',view_func=index)
    app.run(debug=True, port=5000)
