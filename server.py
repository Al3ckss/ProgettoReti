import sys
import os
import logging
from socket import *

# Impostazioni server
serverPort = 8080
serverSocket = socket(AF_INET, SOCK_STREAM)
server_address = ('localhost', serverPort)
serverSocket.bind(server_address)
serverSocket.listen(5)
print('Server web attivo su http://localhost:8080/')

# Logging base su file
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s %(message)s')

# MIME Types per i vari file
MIME_TYPES = {
    'html': 'text/html',
    'css': 'text/css',
    'js': 'application/javascript',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif',
    'ico': 'image/x-icon'
}

def get_content_type(filename):
    # Restituisce il MIME type corretto in base all'estensione del file
    ext = filename.split('.')[-1]
    return MIME_TYPES.get(ext, 'application/octet-stream')

def serve_file(filepath):
    # Legge il file richiesto dal client
    # Se è immagine/risorsa binaria passa a modalità binaria ('rb')
    ext = filepath.split('.')[-1]
    mode = 'rb' if ext in ['jpg', 'jpeg', 'png', 'gif', 'ico'] else 'r'

    with open(filepath, mode) as f:
        return f.read()

while True:
    print('\nIn attesa di richieste...')
    connectionSocket, addr = serverSocket.accept()
    print('Connessione da:', addr)

    try:
        # Riceve il messaggio HTTP dal client (browser)
        message = connectionSocket.recv(1024).decode()
        if not message:
            continue

        parts = message.split()
        if len(parts) < 2:
            continue

        filename = parts[1]
        if filename == '/':
            filename = '/index.html'

        filepath = 'www' + filename
        print('Richiesta:', filename)
        logging.info(f"{addr} -> {filename}")

        # Gestione file esistente
        if os.path.exists(filepath) and os.path.isfile(filepath):
            content_type = get_content_type(filename)
            content = serve_file(filepath)

            # Costruisce l'intestazione della risposta HTTP (con 200 OK)
            header = "HTTP/1.1 200 OK\r\n"
            header += f"Content-Type: {content_type}\r\n\r\n"

            # Se il contenuto è una stringa codifica in bytes
            if isinstance(content, str):
                content = content.encode()

            # Invio di intestazione e contenuto
            connectionSocket.send(header.encode() + content)
            print('Inviato:', filename)

        # Gestione file non trovato, invio pagina 404
        else:
            error_page = """
            <html><head><title>404 Not Found</title></head>
            <body><h1>404 Not Found</h1>
            <p>La risorsa richiesta non esiste</p></body></html>
            """
            response = "HTTP/1.1 404 Not Found\r\n"
            response += "Content-Type: text/html\r\n\r\n"
            response += error_page

            connectionSocket.send(response.encode())
            print('Errore 404:', filename)
            logging.warning(f"404 Not Found -> {filename}")

    except Exception as e:
        print('Errore:', str(e))
        logging.error(f"Errore: {str(e)}")

    finally:
        connectionSocket.close()
