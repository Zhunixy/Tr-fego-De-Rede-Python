from flask import Flask, url_for, render_template, request
from random import randint

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def main():
    if request.method == "POST":
        if request.form.get('encerrar') == 'encerrar tabela':
            return render_template("index.html", texto="boiolas", tabela=0)
        else:
            tabela = [ 
                {"Hora": randint(0, 100000), "IP_origem": randint(0, 100000), "IP_destino": randint(0, 100000), "Porta_origem": randint(0, 100000), "Porta_destino": randint(0, 100000), "Protocolo": randint(0, 100000), "Tamanho": randint(0, 100000), "Status": randint(0, 100000)},
                {"Hora": randint(0, 100000), "IP_origem": randint(0, 100000), "IP_destino": randint(0, 100000), "Porta_origem": randint(0, 100000), "Porta_destino": randint(0, 100000), "Protocolo": randint(0, 100000), "Tamanho": randint(0, 100000), "Status": randint(0, 100000)},
                {"Hora": randint(0, 100000), "IP_origem": randint(0, 100000), "IP_destino": randint(0, 100000), "Porta_origem": randint(0, 100000), "Porta_destino": randint(0, 100000), "Protocolo": randint(0, 100000), "Tamanho": randint(0, 100000), "Status": randint(0, 100000)},
                {"Hora": randint(0, 100000), "IP_origem": randint(0, 100000), "IP_destino": randint(0, 100000), "Porta_origem": randint(0, 100000), "Porta_destino": randint(0, 100000), "Protocolo": randint(0, 100000), "Tamanho": randint(0, 100000), "Status": randint(0, 100000)},
                {"Hora": randint(0, 100000), "IP_origem": randint(0, 100000), "IP_destino": randint(0, 100000), "Porta_origem": randint(0, 100000), "Porta_destino": randint(0, 100000), "Protocolo": randint(0, 100000), "Tamanho": randint(0, 100000), "Status": randint(0, 100000)},
                {"Hora": randint(0, 100000), "IP_origem": randint(0, 100000), "IP_destino": randint(0, 100000), "Porta_origem": randint(0, 100000), "Porta_destino": randint(0, 100000), "Protocolo": randint(0, 100000), "Tamanho": randint(0, 100000), "Status": randint(0, 100000)},
                {"Hora": randint(0, 100000), "IP_origem": randint(0, 100000), "IP_destino": randint(0, 100000), "Porta_origem": randint(0, 100000), "Porta_destino": randint(0, 100000), "Protocolo": randint(0, 100000), "Tamanho": randint(0, 100000), "Status": randint(0, 100000)},
                {"Hora": randint(0, 100000), "IP_origem": randint(0, 100000), "IP_destino": randint(0, 100000), "Porta_origem": randint(0, 100000), "Porta_destino": randint(0, 100000), "Protocolo": randint(0, 100000), "Tamanho": randint(0, 100000), "Status": randint(0, 100000)},
                {"Hora": randint(0, 100000), "IP_origem": randint(0, 100000), "IP_destino": randint(0, 100000), "Porta_origem": randint(0, 100000), "Porta_destino": randint(0, 100000), "Protocolo": randint(0, 100000), "Tamanho": randint(0, 100000), "Status": randint(0, 100000)},
                {"Hora": randint(0, 100000), "IP_origem": randint(0, 100000), "IP_destino": randint(0, 100000), "Porta_origem": randint(0, 100000), "Porta_destino": randint(0, 100000), "Protocolo": randint(0, 100000), "Tamanho": randint(0, 100000), "Status": randint(0, 100000)} 
                ]
            return render_template("index.html", texto="boiolas", tabela=tabela)
    else:
        return render_template("index.html", texto="boiolas", tabela=0)
    


@app.route("/sobre", methods = ["GET", "POST"])
def main():
    return"<div>pintos e bolas</div>"
    


app.run(debug=True)