from flask import Flask, render_template, request
import math
import logging

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Cambia esto por una clave real

# Configura logging
logging.basicConfig(level=logging.DEBUG)

def euler_mejorado(f, x0, y0, h, n):
    resultados = []
    x = x0
    y = y0
    resultados.append((x, y))
    
    for _ in range(n):
        try:
            # Paso predictor
            y_pred = y + h * f(x, y)
            
            # Paso corrector
            y_corr = y + h * (f(x, y) + f(x + h, y_pred)) / 2
            x += h
            y = y_corr
            
            resultados.append((x, y))
        except Exception as e:
            app.logger.error(f"Error en iteración {_}: {str(e)}")
            raise ValueError(f"Error en cálculo: {str(e)}")
    
    return resultados

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Validación básica
            if not all(key in request.form for key in ['funcion', 'x0', 'y0', 'h', 'n']):
                raise ValueError("Todos los campos son requeridos")
            
            # Conversión segura
            def to_float(val):
                try:
                    return float(val)
                except ValueError:
                    raise ValueError(f"Valor numérico inválido: {val}")

            f_str = request.form['funcion'].strip()
            x0 = to_float(request.form['x0'])
            y0 = to_float(request.form['y0'])
            h = to_float(request.form['h'])
            n = int(request.form['n'])

            # Validación adicional
            if h <= 0:
                raise ValueError("El paso (h) debe ser positivo")
            if n <= 0:
                raise ValueError("El número de pasos debe ser positivo")

            # Función segura
            def f(x, y):
                allowed_names = {
                    'x': x,
                    'y': y,
                    'sin': math.sin,
                    'cos': math.cos,
                    'exp': math.exp,
                    'sqrt': math.sqrt,
                    'log': math.log,
                    'pi': math.pi,
                    'e': math.e
                }
                
                try:
                    return eval(f_str, {'__builtins__': None}, allowed_names)
                except Exception as e:
                    raise ValueError(f"Error en la función: {str(e)}. Use sólo x, y y funciones matemáticas básicas.")

            solucion = euler_mejorado(f, x0, y0, h, n)
            return render_template('index.html', 
                                solucion=solucion,
                                funcion=f_str,
                                x0=x0,
                                y0=y0,
                                h=h,
                                n=n)

        except Exception as e:
            app.logger.error(f"Error en el cálculo: {str(e)}")
            return render_template('index.html', 
                                error=f"Error: {str(e)}",
                                funcion=request.form.get('funcion', ''),
                                x0=request.form.get('x0', ''),
                                y0=request.form.get('y0', ''),
                                h=request.form.get('h', ''),
                                n=request.form.get('n', ''))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
