from flask import Flask, url_for, render_template, request, session, redirect
import os
import pyshark
import asyncio
import usuario
from flask_session import Session
import math

def analisar_pacotes():
    lista_analise = []
    pacotes_protocolo = []
    pacotes_IP_origem = []
    pacotes_IP_destino = []

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Define o nome do arquivo pcap
    nome_arquivo = 'captura.pcap'
    
    # Obtém o diretório onde o script Python está localizado
    caminho_arquivo = os.path.join(os.path.dirname(os.path.realpath(__file__)), nome_arquivo)

    # Verifica se o arquivo existe
    if not os.path.exists(caminho_arquivo):
        print(f"Erro: O arquivo '{nome_arquivo}' não foi encontrado no diretório '{caminho_arquivo}'.")
        return 

    print(f"Usando arquivo pcap: {caminho_arquivo}")
    
    # Carrega o arquivo pcap com PyShark
    captura = pyshark.FileCapture(caminho_arquivo)

    # Estatísticas
    total_pacotes = 0
    pacotes_por_protocolo = {}
    pacotes_por_ip_origem = {}
    pacotes_por_ip_destino = {}

    for pacote in captura:
        Timestamp = pacote.sniff_time
        Protocolo = pacote.highest_layer

        # Atualiza estatísticas por protocolo
        if pacote.highest_layer in pacotes_por_protocolo:
            pacotes_por_protocolo[pacote.highest_layer] += 1
        else:
            pacotes_por_protocolo[pacote.highest_layer] = 1

        # Informações de IP
        if 'IP' in pacote:
            Endereço_IP_Origem = pacote.ip.src
            Endereço_IP_Destino = pacote.ip.dst

            # Atualiza estatísticas por IP de origem e destino
            if pacote.ip.src in pacotes_por_ip_origem:
                pacotes_por_ip_origem[pacote.ip.src] += 1
            else:
                pacotes_por_ip_origem[pacote.ip.src] = 1

            if pacote.ip.dst in pacotes_por_ip_destino:
                pacotes_por_ip_destino[pacote.ip.dst] += 1
            else:
                pacotes_por_ip_destino[pacote.ip.dst] = 1

        else:
            Endereço_IP_Origem = "N/A"
            Endereço_IP_Destino = "N/A"

        # Informações de transporte (TCP/UDP)
        if hasattr(pacote, 'transport_layer') and pacote.transport_layer is not None:
            Porta_Origem = pacote[pacote.transport_layer].srcport
            Porta_Destino = pacote[pacote.transport_layer].dstport
        else:
            Porta_Origem = "N/A"
            Porta_Destino = "N/A"

        # Informações de camada de enlace (Ethernet)
        if 'ETH' in pacote:
            MAC_Origem = pacote.eth.src
            MAC_Destino = pacote.eth.dst
        else:
            MAC_Origem = "N/A"
            MAC_Destino = "N/A"

        Tamanho_Pacote = pacote.length

        lista_analise.append({
            "Hora": Timestamp, 
            "IP_origem": Endereço_IP_Origem, 
            "IP_destino": Endereço_IP_Destino, 
            "Porta_origem": Porta_Origem, 
            "Porta_destino": Porta_Destino, 
            "MAC_origem": MAC_Origem, 
            "MAC_destino": MAC_Destino, 
            "Protocolo": Protocolo, 
            "Tamanho": Tamanho_Pacote
            })

    captura.close()

    # Exibe estatísticas gerais
    for protocolo, quantidade in pacotes_por_protocolo.items():
        pacotes_protocolo.append({
            "protocolo": protocolo,
            "quantidade": quantidade
        })

    for ip, quantidade in pacotes_por_ip_origem.items():
        pacotes_IP_origem.append({
            "ip": ip,
            "quantidade": quantidade
        })

    for ip, quantidade in pacotes_por_ip_destino.items():
        pacotes_IP_destino.append({
            "ip": ip,
            "quantidade": quantidade
        })

    return [lista_analise, pacotes_protocolo, pacotes_IP_origem, pacotes_IP_destino]

app = Flask(__name__)

tab = 0
tabela_completa = 0
protocolos_geral = 0
IP_origem_geral = 0
IP_destino_geral = 0

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods = ["GET", "POST"])
def main():  
    global tab
    global tabela_completa
    global protocolos_geral
    global IP_origem_geral
    global IP_destino_geral
    try:
        if request.method == "POST":
            
            if request.form.get('alternar') == 'anterior':
                tab -= 1
            elif request.form.get('alternar') == 'proximo':
                tab += 1           

            tab = tab % 4

            if request.form.get('encerrar') == 'encerrar':
                tab = 0
                tabela_completa = 0
                protocolos_geral = 0
                IP_origem_geral = 0
                IP_destino_geral = 0
                return render_template("index.html")
            else:
                if not (tabela_completa and protocolos_geral and IP_origem_geral and IP_destino_geral):
                    tabela_completa, protocolos_geral, IP_origem_geral, IP_destino_geral = analisar_pacotes()
                elif request.form.get('recarregar') == 'recarregar' or request.form.get('iniciar') == 'iniciar':
                    tabela_completa, protocolos_geral, IP_origem_geral, IP_destino_geral = analisar_pacotes()

                lista_1 = []
                lista_2 = []
    
                match int(tab):
                    case 0:
                        return render_template("index.html", analise=True, tabela=tabela_completa)
                    case 1:
                        for i in protocolos_geral:
                            lista_1.append(i["protocolo"])
                            lista_2.append(i["quantidade"])                                
                        return render_template("index.html", analise=True, lista_1=lista_1, lista_2=lista_2, grafico="protocolos")
                    case 2:
                        for i in IP_origem_geral:
                            lista_1.append(i["ip"])
                            lista_2.append(i["quantidade"])                                
                        return render_template("index.html", analise=True, lista_1=lista_1, lista_2=lista_2, grafico="IPs de origem")
                    case 3:
                        for i in IP_destino_geral: 
                            lista_1.append(i["ip"])
                            lista_2.append(i["quantidade"])                                
                        return render_template("index.html", analise=True, lista_1=lista_1, lista_2=lista_2, grafico="IPs de destino")
                return render_template("index.html")
        else:
            return render_template("index.html")
    except NameError as erro:
        return render_template("index.html", erro=erro)

@app.route("/login", methods = ["GET", "POST"])
def login():
    email = request.form.get('email')
    senha = request.form.get('senha')

    dados = usuario.login(email, senha)
    if dados['type'] != 'error':
        session['id'] = dados['id']
    else:
        session['id'] = None

    return dados

@app.route("/cadastro", methods = ["GET", "POST"])
def cadastro():
    nome = request.form.get('nome')
    cnpj = request.form.get('cnpj')
    telefone = request.form.get('telefone')
    email = request.form.get('email')
    senha = request.form.get('senha')

    if nome != '' and cnpj != '' and telefone != '' and email != '' and senha != '':
        return usuario.cadastro(nome, cnpj, telefone, email, senha)
    else:
        return {'type': 'error', 'mensagem': 'Campo(s) obrigatório(s) não preenchido(s)'}

@app.route("/validate", methods = ["GET", "POST"])
def validate():
        if len(session) < 1:
            session['id'] = None
        return usuario.validate(session['id'])

@app.route("/logout", methods = ["GET", "POST"])
def logout():
    try:
        session['id'] = None
        return {'type': 'success'}
    except:
        return {'type': 'error'}

if __name__== "__main__":
    app.run(debug=True)

    #Viado