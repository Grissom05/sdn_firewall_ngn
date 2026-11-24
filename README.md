# sdn_firewall_ngn
 Group project for the Next generation networks exam

Posizionati nella cartella del progetto:
cd ~/sdn_firewall


Avvia il laboratorio:
kathara lstart


Se il laboratorio è già avviato, non serve ripetere questo comando.
2. Verifica della rete di management
Dentro ctrl
Accedi al controller:
kathara connect ctrl


Verifica l'indirizzo IP:
ip addr show eth0


Devi trovare:
192.168.100.100/24


Verifica la rete:
ip route


Devi trovare:
192.168.100.0/24 dev eth0


Esci dal container:
exit


Dentro s1
Accedi allo switch:
kathara connect s1


Verifica:
ip addr show eth0


Devi trovare:
192.168.100.1/24


Esci:
exit


3. Verifica della comunicazione tra switch e controller
Dentro ctrl
kathara connect ctrl


Esegui:
ping -c 4 192.168.100.1


Devi ricevere le risposte da 192.168.100.1.

Ora verifica che il controller sia in ascolto sulla porta OpenFlow:
ss -lntp | grep 6653


Dovresti trovare una riga con LISTEN e :6653.
4. Avvio del controller OS-Ken
Sempre dentro ctrl, avvia:
/opt/ryu-venv/bin/osken-manager --ofp-tcp-listen-port 6653


Importante
 Questo comando rimane in esecuzione: non chiudere il terminale.

Per verificare lo switch, apri un secondo terminale Ubuntu.
5. Verifica della configurazione di Open vSwitch
Dentro s1
cd ~/sdn_firewall
kathara connect s1


Verifica il bridge:
ovs-vsctl show


Devi trovare:
- Bridge br0.
- Porte eth1, eth2, eth3, eth4.
- Controller tcp:192.168.100.100:6653.
Verifica il protocollo:
ovs-vsctl get bridge br0 protocols


Risultato atteso:
[OpenFlow13]


Verifica la connessione:
ovs-vsctl list Controller


Risultato atteso:
is_connected : true
status : {state=ACTIVE}


6. Verifica delle interfacce dello switch
Sempre dentro s1:
ip link show


Controlla che siano presenti:
Interfaccia	Funzione
eth0	Management
eth1	LAN1
eth2	LAN2
eth3	LAN3
eth4	EXT
br0	Bridge Open vSwitch

Controlla anche le regole OpenFlow:
ovs-ofctl -O OpenFlow13 dump-flows br0


Dovresti trovare la regola di default che invia i pacchetti al controller:
priority=0 actions=CONTROLLER:65535


7. Configurazione del file ctrl.startup
Questa è la parte che dobbiamo sistemare per evitare di avviare manualmente OS-Ken ogni volta.

Sul terminale Ubuntu host, nella cartella ~/sdn_firewall:
nano ctrl.startup


Il contenuto che vogliamo ottenere è:


ip addr add 192.168.100.100/24 dev eth0
ip link set eth0 up

/opt/ryu-venv/bin/osken-manager --ofp-tcp-listen-port 6653


Salva con CTRL+O, Invio, CTRL+X


8. Configurazione dell'ambiente Python

Le dipendenze Python del progetto sono elencate in `requirements.txt`
nella cartella principale. Dalla cartella principale del progetto, crea
e attiva l'ambiente virtuale con Python 3.15 (verificato con la versione
3.15.2) e installa le dipendenze.

Su Windows (PowerShell):

```powershell
py -3.15 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Su Linux o WSL:

```bash
python3.15 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Per uscire dall'ambiente virtuale:

```text
deactivate
```

L'ambiente `.venv` contiene le dipendenze del backend Python e non sostituisce
l'ambiente OS-Ken utilizzato dal controller nel laboratorio Kathara.
