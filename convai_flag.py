import socket

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5000))
    server_socket.listen(1)
    
    print("Servidor escuchando en el puerto 5000...")
    
    while True:
        client_socket, addr = server_socket.accept()
        with client_socket:
            data = client_socket.recv(1024)
            if data:
                is_talking = data.decode('utf-8') == 'True'
                print(f'El personaje está hablando: {is_talking}')

if __name__ == "__main__":
    start_server()
