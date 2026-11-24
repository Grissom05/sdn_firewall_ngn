
# ============================================================
# SDN-Firewall - Configurazione del Controller SDN
# ============================================================
#
# Questo modulo contiene i parametri di configurazione
# necessari al backend per comunicare con il controller SDN Ryu.
#
# ARCHITETTURA DEL SISTEMA
#
# Il progetto utilizza due ambienti distinti:
#
# 1. WSL (Ubuntu):
#    - Ospita il backend sviluppato con FastAPI.
#    - Gestisce le richieste provenienti dall'interfaccia
#      grafica e coordina le operazioni amministrative.
#
# 2. VM sdn-lab (Ubuntu):
#    - Ospita il controller SDN Ryu.
#    - Ospita Open vSwitch (OVS).
#    - Gestisce la comunicazione con gli switch attraverso
#      il protocollo OpenFlow.
#
# COMUNICAZIONE TRA BACKEND E CONTROLLER
#
# Il backend comunica con Ryu attraverso una REST API HTTP.
# Le richieste vengono inviate all'indirizzo IP della macchina
# virtuale, utilizzando la porta TCP dedicata al servizio REST.
#
# Ryu riceve le richieste, esegue le operazioni richieste
# e interagisce con gli switch Open vSwitch attraverso OpenFlow.
#
# IMPORTANTE:
# La porta REST (8080) e la porta OpenFlow (6653) hanno
# funzioni differenti:
#
# - 8080: comunicazione REST tra backend e controller.
# - 6653: comunicazione OpenFlow tra controller e switch.
#
# La porta OpenFlow non viene utilizzata direttamente dal
# backend FastAPI.
#
# ============================================================


# ------------------------------------------------------------
# INDIRIZZO IP DEL CONTROLLER RYU
# ------------------------------------------------------------
#
# Indirizzo IP della macchina virtuale sdn-lab sulla rete
# Host-Only di VirtualBox.
#
# Il backend, eseguito all'interno di WSL, utilizza questo
# indirizzo per raggiungere il controller Ryu.
#
# Indirizzo verificato attraverso test di connettività
# tra WSL e la macchina virtuale.
#
RYU_CONTROLLER_IP = "192.168.56.10" #indirizzo 


# ------------------------------------------------------------
# PORTA REST API DEL CONTROLLER
# ------------------------------------------------------------
#
# Porta TCP sulla quale Ryu espone il proprio servizio REST.
#
# Il servizio è stato avviato utilizzando l'applicazione:
# ryu.app.ofctl_rest
#
# La REST API permette al backend di interrogare il controller
# e di richiedere operazioni sugli switch OpenFlow.
#
RYU_REST_PORT = 8080


# ------------------------------------------------------------
# INDIRIZZO BASE DELLA REST API
# ------------------------------------------------------------
#
# Costruisce automaticamente l'indirizzo HTTP completo
# utilizzato dal backend per comunicare con Ryu.
#
# L'utilizzo di una variabile centralizzata evita di
# ripetere l'indirizzo IP e la porta nei diversi moduli
# del progetto.
#
# Esempio di indirizzo risultante:
# http://192.168.56.10:8080
#
# I singoli endpoint REST verranno aggiunti a questo
# indirizzo dai servizi che gestiscono le comunicazioni
# con il controller.
#
RYU_BASE_URL = f"http://{RYU_CONTROLLER_IP}:{RYU_REST_PORT}"
