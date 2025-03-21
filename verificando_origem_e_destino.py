#biblioteca pyshark: interface Python para o Wireshark ela permite que você leia e analise arquivos de captura de rede (.pcap) diretamente no Python
import pyshark

#função para analisar os pacotes essa função será responsável por abrir o arquivo de captura e processar cada pacote
def analisar_pacotes():
    #abrindo um arquivo de captura da extensão pcap
    captura = pyshark.FileCapture('./Capturas/captura.pcap')

    #itera sobre cada pacote presente no arquivo de captura a variável pacote contém as informações de um pacote específico
    for pacote in captura:
        #imprime o número do pacote na captura cada pacote tem um número único que indica sua posição no arquivo
        print(f"Pacote {pacote.number}:")
        #imprime o protocolo de mais alto nível do pacote (por exemplo, TCP, UDP, HTTP)
        print(f"  Protocolo: {pacote.highest_layer}")
        #imprime o endereço IP de origem do pacote se o pacote não tiver uma camada IP (por exemplo, pacotes ARP), usamos pra saber quem enviou o pacote
        print(f"  Endereço IP de Origem: {pacote.ip.src if 'IP' in pacote else 'N/A'}")
        #imprime o endereço IP de destino do pacote
        print(f"  Endereço IP de Destino: {pacote.ip.dst if 'IP' in pacote else 'N/A'}")
        
        #verifica se o pacote tem uma camada de transporte (como TCP ou UDP) se tiver, imprime as portas de origem e destino
        if hasattr(pacote, 'transport_layer') and pacote.transport_layer is not None:
            print(f"  Porta de Origem: {pacote[pacote.transport_layer].srcport}")
            print(f"  Porta de Destino: {pacote[pacote.transport_layer].dstport}")
        else:
            print("  Porta de Origem: N/A")
            print("  Porta de Destino: N/A")
        
        #imprime o tamanho do pacote em bytes
        print(f"  Tamanho do Pacote: {pacote.length}")
        print("-" * 50)

    #fecha o arquivo de captura após a análise.
    captura.close()

#executa a função
analisar_pacotes()

#N/A Usamos quando for nulo