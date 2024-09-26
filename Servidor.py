import socket
import threading
import json

mutex = threading.Lock() 

def info_servidor(): #Solicita ao usuário o IP e a porta do servidor. 

    host = '0.0.0.0'
    port = 61624

    return host, int(port)

def iniciar_servidor(host, port): #Inicializa o servidor e começa a escutar conexões.

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp.bind((host, port))
    tcp.listen(8)

    print(f"Servidor iniciado no IP {host} e porta {port}.")

    return tcp

def handle_client(con, cliente): #Loop principal da interação do servidor com o cliente.

    print(f'Conectado a: {cliente}')

    try:

        while True:

            info = con.recv(1024).decode('utf-8', errors='replace')

            if not info:

                break

            if info == 'exit':

                print("Comando de encerramento recebido. Encerrando a conexão com o cliente...")
                con.sendall(str.encode('Conexão encerrada pelo cliente.'))

                break

            if processar_solicitacao(con, info):

                con.sendall(str.encode('True'))
                
            else:

                con.sendall(str.encode('False'))
                print(f'Trecho {info} indisponível\n')

            print(f'{cliente} enviou a informação: {info}')

    except Exception as e:

        print(f'Erro com {cliente}: {e}')

    finally:

        print(f'Conexão com {cliente} encerrada')
        con.close()

def processar_solicitacao(con, info): #Processa a solicitação do cliente, verifica e atualiza a disponibilidade dos trechos.

    #Formatando a infomação enviada pelo client.
    info = info.lower()
    origem,destino = info.split('>')
    origem = origem.strip()
    destino = destino.strip()

    with mutex:    

        with open('Voos.json', 'r', encoding='utf-8') as json_file:
            trechos_disponiveis = json.load(json_file)

        for trecho in trechos_disponiveis:

            if origem == trecho['Origem'] and destino == trecho['Destino']:

                if trecho['Vagas'] > 0:

                    con.sendall(str.encode('True'))
                    con.settimeout(30)
                    resp = con.recv(1024).decode('utf-8')

                    if resp == 'S':

                        trecho['Vagas'] -= 1

                        with open('Voos.json', 'w', encoding='utf-8') as json_file:
                                
                                json.dump(trechos_disponiveis, json_file, ensure_ascii=False, indent=4)

                        return True
                    
                    else:

                        return False
                    
        return False
 

def aceitar_conexoes(tcp): #Aceita conexões de clientes e cria uma nova thread para cada um.

    while True:

        con, cliente = tcp.accept()
        client_thread = threading.Thread(target=handle_client, args=(con, cliente))
        client_thread.start()


def main(): # Função principal que coordena a execução do servidor

    host, port = info_servidor()
    tcp = iniciar_servidor(host, port)
    aceitar_conexoes(tcp)

if __name__ == '__main__':
    main()