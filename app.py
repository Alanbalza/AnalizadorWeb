from flask import Flask, render_template, request
from analizador import analizar_codigo

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        codigo = request.form['codigo']
        resultado_lexico, resultado_sintactico, totales = analizar_codigo(codigo)
        return render_template('index.html', codigo=codigo, resultado_lexico=resultado_lexico, resultado_sintactico=resultado_sintactico, totales=totales)
    return render_template('index.html', codigo='', resultado_lexico=[], resultado_sintactico='', totales={})

if __name__ == '__main__':
    app.run(debug=True)
