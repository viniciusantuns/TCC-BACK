import socket


def obter_endereco_ip():
    try:
        # Obtém o nome da máquina
        hostname = socket.gethostname()

        # Obtém o endereço IP associado ao nome da máquina
        endereco_ip = socket.gethostbyname(hostname)

        return endereco_ip
    except Exception as e:
        print(f"Erro ao obter o endereço IP: {e}")
        return None


# Chama a função para obter o endereço IP
endereco_ip = obter_endereco_ip()

if endereco_ip:
    print(f"Endereço IP da máquina: {endereco_ip}")
else:
    print("Não foi possível obter o endereço IP.")