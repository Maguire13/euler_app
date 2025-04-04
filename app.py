from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        app.logger.error(f"Error loading template: {str(e)}")
        return "Error loading page", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

def euler_mejorado(f, x0, y0, h, n):
    """
    Método de Euler Mejorado (Heun) para resolver EDOs.

    Args:
        f: Función de la EDO dy/dx = f(x, y).
        x0: Valor inicial de x.
        y0: Valor inicial de y.
        h: Tamaño del paso.
        n: Número de pasos.

    Returns:
        Una lista de tuplas (x, y) con los resultados.
    """
    resultados = [(x0, y0)]
    x = x0
    y = y0
    for _ in range(n):
        # Predictor (Euler estándar)
        y_pred = y + h * f(x, y)
        # Corrector (Heun)
        y = y + h * (f(x, y) + f(x + h, y_pred)) / 2
        x += h
        resultados.append((x, y))
    return resultados

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            f_str = request.form['funcion']
            x0 = float(request.form['x0'])
            y0 = float(request.form['y0'])
            h = float(request.form['h'])
            n = int(request.form['n'])

            # Definir la función f(x, y) a partir del string
            def f(x, y):
                return eval(f_str)

            # Calcular solución
            solucion = euler_mejorado(f, x0, y0, h, n)

            return render_template('index.html',
                                 solucion=solucion,
                                 funcion=f_str,
                                 x0=x0,
                                 y0=y0,
                                 h=h,
                                 n=n)
        except Exception as e:
            error = f"Error: {str(e)}"
            return render_template('index.html', error=error)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
