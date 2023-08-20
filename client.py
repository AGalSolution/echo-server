import socket
import argparse

def main():
    parser = argparse.ArgumentParser(description="Client per inviare messaggi al server")
    parser.add_argument("-p", "--port", type=int, required=True, help="Porta del server")
    args = parser.parse_args()

    host = '127.0.0.1'  # Indirizzo IP del server
    port = args.port

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connetti il client al server
        client_socket.connect((host, port))
        print(f"Connesso al server {host}:{port}")

        while True:
            message = input("Inserisci il messaggio da inviare (digita '.quit' per uscire): ")

            # Invia il messaggio al server
            client_socket.send(message.encode('utf-8'))

            # Esci dal loop se l'utente ha inserito ".quit"
            if message == '.quit':
                break

            # Ricevi la risposta dal server
            response = client_socket.recv(1024).decode('utf-8')
            print("Risposta dal server:", response)

    except Exception as e:
        print(f"Errore: {e}")
    finally:
        client_socket.close()
        print("Connessione chiusa.")

if __name__ == "__main__":
    main()

