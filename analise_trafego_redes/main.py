from flask import Flask, url_for, render_template, request
import os
import pyshark
import asyncio

lista_analise = []
pacotes_protocolo = []
pacotes_IP_origem = []
pacotes_IP_destino = []

def analisar_pacotes():
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
    print("\nEstatísticas Gerais:")
    print(f"Total de Pacotes: {total_pacotes}")
    print("Pacotes por Protocolo:")
    for protocolo, quantidade in pacotes_por_protocolo.items():
        print(f"  {protocolo}: {quantidade}")
        pacotes_protocolo.append({
            "protocolo": protocolo,
            "quantidade": quantidade
        })

    print("Pacotes por IP de Origem:")
    for ip, quantidade in pacotes_por_ip_origem.items():
        print(f"  {ip}: {quantidade}")
        pacotes_IP_origem.append({
            "ip": ip,
            "quantidade": quantidade
        })

    print("Pacotes por IP de Destino:")
    for ip, quantidade in pacotes_por_ip_destino.items():
        print(f"  {ip}: {quantidade}")
        pacotes_IP_destino.append({
            "ip": ip,
            "quantidade": quantidade
        })

    return [lista_analise, pacotes_protocolo, pacotes_IP_origem, pacotes_IP_destino]

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def main():
    if request.method == "POST":
        if request.form.get('encerrar') == 'encerrar tabela':
            return render_template("index.html", tabela=0)
        else:
            try:
                tabela = analisar_pacotes()[0]
                protocolos_geral = analisar_pacotes()[1]
                IP_origem_geral = analisar_pacotes()[2]
                IP_destino_geral = analisar_pacotes()[3]
                return render_template("index.html", tabela=tabela, protocolos_geral=protocolos_geral, IP_origem_geral=IP_origem_geral, IP_destino_geral=IP_destino_geral)
            except:

                return render_template("index.html", erro=1)
    else:
        return render_template("index.html", tabela=0)

app.run(debug=True)