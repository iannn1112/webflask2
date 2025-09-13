from flask import Flask, session, render_template, flash
from config import Config
from forms import TestForm

app = Flask(__name__)
app.config.from_object(Config)

visit_count = 0

# app = Flask(__name__)
# app.secret_key = os.getenv("FLASK_SECRET_pip install flaskKEY")

# class Config:
#     SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "clave_dev_segura")
#     SESSION_COOKIE_SECURE = True
#     SESSION_COOKIE_HTTPONLY = True
#     SESSION_COOKIE_SAMESITE = 'Lax'


# class TestForm (FlaskForm):
#     nombre = StringField("Nombre", validators=[DataRequired()])
#     apellido = StringField("Apellido", validators=[DataRequired()])
#     cumpleaños = DateField("Cumpleaños", validators=[DataRequired()], format="%Y-%m-%d")
#     submit = SubmitField("Enviar")

@app.after_request
def set_secure_headers(response):
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "style-src 'self' https://cdn.jsdelivr.net;"
        "script-src 'self' https://cdn.jsdelivr.net;"
        "frame-src https://www.google.com https://www.google.com.mx;"
    )
    response.headers ['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

@app.route("/faq")
def faq():
    return render_template("faq.html")

@app.route("/ubicacion")
def ubicacion():
    return render_template("ubicacion.html")

@app.route("/terminos")
def terminos():
    return render_template("terminos.html")

@app.route("/contactos")
def contactos():
    return render_template("contactos.html")

@app.route("/")
def index():
    global visit_count
    visit_count += 1
    return render_template("home.html", count=visit_count)

@app.route("/pre_test")
def pre_test():
    return "Este es mi pre-test"

@app.route('/test', methods=('GET', 'POST'))
def test():
    form = TestForm()
    if form.validate_on_submit():
        
        nombre = form. nombre.data.strip()
        apellido = form.apellido.data.strip()
        cumpleaños = form. cumpleaños.data. isoformat()

        with open("datos.txt", "a", encoding="utf-8") as f:
            f.write(f"{nombre}, {apellido}, {cumpleaños}\n")

        return render_template("resultado.html", nombre=nombre, apellido=apellido, cumple=cumpleaños)
    else:

        if form.is_submitted():
            flash("hubo un problema con el formulario, verfica los datos", "warning")
    return render_template("formulario.html", form=form)

@app.route("/result")
def result():
    return "Este es mi result"

@app.route("/counter")
def counter():
    count = session.get('count', 0) + 1
    session['count'] = count
    return f'Conteo: {count}'

if __name__ == "__main__":
    #app.run(debug=True)
    app.run()
