import socket as sk
import sys

if len(sys.argv) != 4:
    print("Usage: client.py server_host server_port resource_path")
    print("Esempio: client.py localhost 8080 /index.html")
    sys.exit(1)

host = sys.argv[1]
port = int(sys.argv[2])
resource = sys.argv[3]

clientsocket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

try:
    clientsocket.connect((host, port))
    request = f"GET {resource} HTTP/1.1\r\nHost: {host}\r\n\r\n"
    clientsocket.send(request.encode())
    
    response = clientsocket.recv(4096)
    print(response.decode('utf-8'))

except Exception as e:
    print("Errore:", str(e))

finally:
    clientsocket.close()