from flask import Flask, render_template, redirect, url_for,jsonify


from main import main

app = Flask(__name__)

terminou = True
def terminouFunc():
    global terminou
    terminou = True


@app.route('/home/')
def home():
    """
    se metodo for get
    verificar se a automação está em execução.
    return Aguarde a automação finalizar
    """
    if terminou == False:
        return redirect(url_for('aguardando'))

    return render_template('home.html')

@app.route('/ativar-automacao/', methods=['POST'])
def ativar_automacao():
    global terminou
    terminou = False
    # try:
    main()
    # except Exception:
    terminouFunc()
        # return jsonify({'status': 'ERRO!'})
    # terminouFunc()
    return jsonify({'status': 'processado'})
    # return "Automação finalizada"

@app.route('/')
def index():
    return redirect(url_for('home'))


@app.route('/aguardando/')
def aguardando():
    return render_template('aguardando.html')
    