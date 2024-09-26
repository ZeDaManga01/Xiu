import socket

def info_servidor(): #Solicita ao usuário o IP e a porta do servidor.

    host = 'localhost'
    port = 61624
    
    return host, int(port)

def conetar_servidor(host, port): #Conecta ao servidor TCP com o endereço fornecido.

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server = (host, port)
    tcp.connect(server)
    print(f"Conectado ao servidor {host}:{port}. Pressione Ctrl+X para sair.")
    return tcp

def enviar_msg(tcp, info): #Envia uma solicitação ao servidor e recebe a resposta.
   
    tcp.sendall(info.encode('utf-8'))
    return tcp.recv(1024).decode('utf-8')
    

def processar_comprar(tcp): #Gerencia o processo de compra do trecho.

    try:

        resp = input('Trecho disponível!\n\nDeseja Comprar?\nS ou N\n')
        tcp.sendall(resp.encode('utf-8'))
        compra_resultado = tcp.recv(1024).decode('utf-8')
        
        if compra_resultado == 'True':

            print('Compra realizada\n')

        else:

            print('Compra não realizada\n')

    except Exception as e:

        print(f'A conexão foi encerrada, Erro:{e}')

def handle_interaction(tcp): #Loop principal de interação com o servidor.

    info = "a"
    
    while info != '\x18':  # Ctrl+X para sair

        info = input('Informe o trecho do voo\n')

        if info == 'exit':

            print('Conexão com o servidor encerrada')
            tcp.close()

            break
        
        disp_info = enviar_msg(tcp, info)

        if disp_info == 'True':

            processar_comprar(tcp)

        else:

            print('Trecho indisponível\n')

def main(): #Função principal que orquestra a execução do cliente. 

    host, port = info_servidor()
    tcp = conetar_servidor(host, port)
    handle_interaction(tcp)
    tcp.close()

if __name__ == '__main__':
    main()