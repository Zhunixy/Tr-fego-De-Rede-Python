from flask import Flask, url_for, render_template, request
from random import randint
import pyshark
import asyncio

lista_analise = []

Timestamp = "N/A"
Endereço_IP_Origem = "N/A"
Endereço_IP_Destino = "N/A"
Porta_Origem = "N/A"
Porta_Destino = "N/A"
MAC_Origem = "N/A"
MAC_Destino = "N/A"
Protocolo = "N/A"
Tamanho_Pacote = "N/A"

def analisar_pacotes():
    captura = pyshark.FileCapture('captura.pcap')

    for pacote in captura:
        Timestamp = {pacote.sniff_time}
        Protocolo = {pacote.highest_layer}

        # Informações de IP
        if 'IP' in pacote:
            Endereço_IP_Origem = {pacote.ip.src}
            Endereço_IP_Destino = {pacote.ip.dst}

        else:
            Endereço_IP_Origem = "N/A"
            Endereço_IP_Destino = "N/A"

        # Informações de transporte (TCP/UDP)
        if hasattr(pacote, 'transport_layer') and pacote.transport_layer is not None:
            Porta_Origem = {pacote[pacote.transport_layer].srcport}
            Porta_Destino = {pacote[pacote.transport_layer].dstport}
        else:
            Porta_Origem = "N/A"
            Porta_Destino = "N/a"

        # Informações de camada de enlace (Ethernet)
        if 'ETH' in pacote:
            MAC_Origem: {pacote.eth.src}
            MAC_Destino = {pacote.eth.dst}

        Tamanho_Pacote = {pacote.length}

        lista_analise.append({"Hora": Timestamp, "IP_origem": Endereço_IP_Origem, "IP_destino": Endereço_IP_Destino, "Porta_origem": Porta_Origem, "Porta_destino": Porta_Destino, "MAC_origem": MAC_Origem, "MAC_destino": MAC_Destino, "Protocolo": Protocolo, "Tamanho": Tamanho_Pacote})

    captura.close()
    return lista_analise

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def main():
    if request.method == "POST":
        if request.form.get('encerrar') == 'encerrar tabela':
            return render_template("index.html", tabela=0)
        else:
            tabela = analisar_pacotes()
            return render_template("index.html", tabela=tabela)
    else:
        return render_template("index.html", tabela=0)
    
    


app.run(debug=True)