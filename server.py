import socket
import redis

def main():
    host = '0.0.0.0'
    port = 7070

    # Connessione al server Redis
    redis_host = 'redis-server'
    redis_port = 6379
    redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"In attesa di connessioni su {host}:{port}...")

        client_socket, client_address = server_socket.accept()
        print(f"Connessione accettata da {client_address[0]}:{client_address[1]}")

        counter = 0

        while True:
            data = client_socket.recv(1024).decode('utf-8')

            if data == ".quit":
                print("Server sta chiudendo...")
                with open('counter.txt','w') as counter_log:
                	counter_log.write(f'last count is {counter}')
                break

            # Incrementa la variabile nel server Redis
            counter = redis_client.incr('message_counter')

            # Invia la risposta con il contatore al client
            response = f"ECHO: {data} (Contatore: {counter})"
            client_socket.send(response.encode('utf-8'))
    except Exception as e:
        print(f"Errore: {e}")
    finally:
        client_socket.close()
        server_socket.close()
        print("Server chiuso.")

if __name__ == "__main__":
    main()

