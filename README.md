# Progetto di Programmazione di Reti: Web Server Statico

**Autore**: Chierici Alessandro

## Descrizione del Progetto

Questo progetto consiste nell'implementazione di un web server HTTP minimale utilizzando la libreria `socket` di Python. Il server è in grado di gestire richieste `GET`, servire un sito web statico composto da più pagine HTML e fogli di stile CSS, e gestire correttamente gli errori più comuni come le risorse non trovate (404).

Per accedere al sito, aprire un qualsiasi browser web e navigare all'indirizzo `http://localhost:8080`.

## Dettagli Tecnici

### Server (`server.py`)
Il server è costruito utilizzando un socket TCP (`AF_INET`, `SOCK_STREAM`). Si mette in ascolto sulla porta `8080` dell'interfaccia (`localhost`).

Il ciclo principale del server attende le connessioni in entrata. Per ogni connessione:
1.  Accetta la richiesta e legge il messaggio HTTP inviato dal client (fino a 1024 bytes).
2.  Estrae il percorso del file (es. `/`, `/about.html`).
3.  Controlla se il file esiste nella cartella `www/`.
4.  Se il file esiste costruisce una risposta `HTTP/1.1 200 OK` con gli header corretti (`Content-Type`) e invia il contenuto del file, mentre Se il file non esiste costruisce e invia una risposta `HTTP/1.1 404 Not Found` con una semplice pagina di errore.
5.  La connessione con il client viene chiusa.

### Sito Web (`www/`)
Il sito è composto da 3 pagine HTML collegate tra loro (`index.html`, `about.html`, `contacts.html`) e un foglio di stile comune (`style.css`) che definisce l'aspetto grafico.

## Funzionalità Implementate

Oltre ai requisiti minimi (server funzionante, gestione corretta di ACK/timeout, invio/cattura pacchetti, ecc.) vengono soddisfatte diverse estensioni opzionali.

### Estensioni Implementate

* **Gestione MIME Types**: Il server rileva l'estensione del file richiesto e imposta l'header `Content-Type` appropriato (es. `text/html`, `text/css`, `image/jpeg`). Questo garantisce che il browser interpreti correttamente ogni risorsa.
* **Logging delle Richieste**: Ogni richiesta ricevuta viene registrata in un file `server.log`, includendo data, ora, indirizzo IP del client e risorsa richiesta. Gli errori 404 vengono registrati come `WARNING` per una facile identificazione.
* **Animazioni e Layout**: Il sito utilizza semplici animazioni CSS (`@keyframes`) per rendere più dinamica la visualizzazione dei titoli e un layout base centrato e flessibile (`max-width: 800px`) per una migliore leggibilità su diversi schermi.
