import sys
import os
from socket import * 

serverPort = 8080
serverSocket = socket(AF_INET, SOCK_STREAM)
server_address = ('localhost', serverPort)
serverSocket.bind(server_address)
serverSocket.listen(5)
print('Il server web è attivo su porta ', serverPort)
print('URL: http://localhost:8080/')

MIME_TYPES = {
    'html': 'text/html',
    'css': 'text/css',
    'jpg': 'image/jpeg',
    'png': 'image/png'
}

while True:
    print('\nPronto...')
    connectionSocket, addr = serverSocket.accept()
    print('Connessione effettuata da ', addr)
    
    try:
        message = connectionSocket.recv(1024).decode()
        if message:
            request_line = message.split()[0]
            filename = message.split()[1]
            
            if filename == '/':
                filename = '/index.html'
            
            filepath = 'www' + filename
            print('Richiesto:', filepath)
            
            if os.path.exists(filepath) and os.path.isfile(filepath):
                with open(filepath, 'r') as f:
                    outputdata = f.read()
                
                ext = filename.split('.')[-1]
                content_type = MIME_TYPES.get(ext, 'text/plain')
                
                headers = "HTTP/1.1 200 OK\r\n"
                headers += f"Content-Type: {content_type}\r\n"
                headers += "\r\n"
                connectionSocket.send(headers.encode())
                
                connectionSocket.send(outputdata.encode())
                print('Inviato:', filepath)
            
            else:
                raise FileNotFoundError
        
    except FileNotFoundError:
        error_page = "<html><head><title>404 Not Found</title></head><body>"
        error_page += "<h1>404 - Pagina non trovata</h1>"
        error_page += "<p>La risorsa richiesta non esiste</p>"
        error_page += "</body></html>"
        
        headers = "HTTP/1.1 404 Not Found\r\n"
        headers += "Content-Type: text/html\r\n"
        headers += f"Content-Length: {len(error_page)}\r\n"
        headers += "\r\n"
        
        connectionSocket.send(headers.encode())
        connectionSocket.send(error_page.encode())
        print('Errore 404:', filename)
    
    except Exception as e:
        print('Errore:', str(e))
    
    finally:
        connectionSocket.close()