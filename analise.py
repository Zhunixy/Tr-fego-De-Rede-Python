import pyshark

def analisar_pacotes():
    captura = pyshark.FileCapture('captura.pcap')
    
    # Estatísticas
    total_pacotes = 0
    pacotes_por_protocolo = {}
    pacotes_por_ip_origem = {}
    pacotes_por_ip_destino = {}

    for pacote in captura:
        total_pacotes += 1
        print(f"Pacote {pacote.number}:")
        print(f"  Timestamp: {pacote.sniff_time}")
        print(f"  Protocolo: {pacote.highest_layer}")

        # Atualiza estatísticas por protocolo
        if pacote.highest_layer in pacotes_por_protocolo:
            pacotes_por_protocolo[pacote.highest_layer] += 1
        else:
            pacotes_por_protocolo[pacote.highest_layer] = 1

        # Informações de IP
        if 'IP' in pacote:
            print(f"  Endereço IP de Origem: {pacote.ip.src}")
            print(f"  Endereço IP de Destino: {pacote.ip.dst}")

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
            print("  Endereço IP de Origem: N/A")
            print("  Endereço IP de Destino: N/A")

        # Informações de transporte (TCP/UDP)
        if hasattr(pacote, 'transport_layer') and pacote.transport_layer is not None:
            print(f"  Porta de Origem: {pacote[pacote.transport_layer].srcport}")
            print(f"  Porta de Destino: {pacote[pacote.transport_layer].dstport}")
        else:
            print("  Porta de Origem: N/A")
            print("  Porta de Destino: N/A")

        # Informações de camada de enlace (Ethernet)
        if 'ETH' in pacote:
            print(f"  MAC de Origem: {pacote.eth.src}")
            print(f"  MAC de Destino: {pacote.eth.dst}")

        # Informações de payload (HTTP, DNS, etc.)
        if 'HTTP' in pacote:
            print(f"  Método HTTP: {pacote.http.request_method if 'request_method' in pacote.http else 'N/A'}")
            print(f"  Host: {pacote.http.host if 'host' in pacote.http else 'N/A'}")
            print(f"  URI: {pacote.http.request_uri if 'request_uri' in pacote.http else 'N/A'}")

        if 'DNS' in pacote:
            print(f"  Consulta DNS: {pacote.dns.qry_name if 'qry_name' in pacote.dns else 'N/A'}")

        print(f"  Tamanho do Pacote: {pacote.length}")
        print("-" * 50)

    captura.close()

    # Exibe estatísticas gerais
    print("\nEstatísticas Gerais:")
    print(f"Total de Pacotes: {total_pacotes}")
    print("Pacotes por Protocolo:")
    for protocolo, quantidade in pacotes_por_protocolo.items():
        print(f"  {protocolo}: {quantidade}")
    print("Pacotes por IP de Origem:")
    for ip, quantidade in pacotes_por_ip_origem.items():
        print(f"  {ip}: {quantidade}")
    print("Pacotes por IP de Destino:")
    for ip, quantidade in pacotes_por_ip_destino.items():
        print(f"  {ip}: {quantidade}")

analisar_pacotes()