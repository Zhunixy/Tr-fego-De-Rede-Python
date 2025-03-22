import pyshark  # Importa a biblioteca pyshark, que é uma interface Python para o Wireshark (ferramenta de captura de pacotes).
import json  # Importa a biblioteca json, que permite trabalhar com dados em formato JSON.

def decodificar_payload(payload):  # Define a função decodificar_payload que recebe um parâmetro 'payload'.
    try:
        return bytes.fromhex(payload).decode('utf-8', errors='replace')  # Tenta converter o payload de hexadecimal para bytes e depois para string UTF-8, substituindo caracteres inválidos.
    except ValueError:  # Caso ocorra um erro na conversão, como se o payload não for um hexadecimal válido.
        return payload  # Retorna o payload original caso o erro aconteça (caso não seja hexadecimal ou não possa ser decodificado como UTF-8).

def analisar_pacotes():  # Define a função principal que vai analisar os pacotes de rede.
    caminho_pcap = './Capturas/captura.pcap'  # Define o caminho do arquivo .pcap (arquivo de captura de pacotes).
    captura = pyshark.FileCapture(caminho_pcap)  # Abre o arquivo .pcap com pyshark para começar a captura dos pacotes.
    dados = []  # Cria uma lista vazia onde serão armazenados os dados dos pacotes.

    for pacote in captura:  # Inicia um loop para iterar por cada pacote na captura.
        try:
            if hasattr(pacote, 'transport_layer') and pacote.transport_layer is not None:  # Verifica se o pacote tem a camada de transporte e se não é None.
                # Verifica se o pacote tem um campo 'data' com um 'data' aninhado dentro dele e tenta decodificar.
                payload_decodificado = decodificar_payload(
                    pacote.data.data  # Pega os dados brutos do pacote e passa para a função 'decodificar_payload'.
                ) if hasattr(pacote, 'data') and hasattr(pacote.data, 'data') else "N/A"  # Se não houver dados, define o payload como "N/A".

                dados.append({  # Adiciona as informações do pacote na lista 'dados'.
                    "numero": pacote.number,  # Adiciona o número do pacote na lista.
                    "protocolo": pacote.highest_layer,  # Adiciona o nome do protocolo da camada mais alta do pacote.
                    "ip_origem": pacote.ip.src if 'IP' in pacote else "N/A",  # Se o pacote tiver camada IP, pega o IP de origem, caso contrário, coloca "N/A".
                    "ip_destino": pacote.ip.dst if 'IP' in pacote else "N/A",  # Se o pacote tiver camada IP, pega o IP de destino, caso contrário, coloca "N/A".
                    "porta_origem": pacote[pacote.transport_layer].srcport,  # Pega a porta de origem da camada de transporte do pacote.
                    "porta_destino": pacote[pacote.transport_layer].dstport,  # Pega a porta de destino da camada de transporte do pacote.
                    "tamanho": pacote.length,  # Pega o tamanho total do pacote.
                    "payload": payload_decodificado  # Adiciona o payload decodificado ou "N/A" caso não seja possível decodificar.
                })

        except Exception as e:  # Se ocorrer qualquer erro dentro do bloco try.
            print(f"Erro ao processar pacote: {str(e)}")  # Exibe uma mensagem de erro com a descrição do erro.
            continue  # Continua o loop com o próximo pacote, ignorando o pacote que causou o erro.
            
    captura.close()  # Fecha a captura de pacotes após o loop de pacotes.
    return dados  # Retorna a lista de dados coletados dos pacotes.






## PARA CONEXÃO COM O FLASK

if __name__ == '__main__':
    dados = analisar_pacotes()
    print(json.dumps(dados))