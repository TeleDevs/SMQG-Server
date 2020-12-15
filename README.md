
# SMQG Server

The architecture is a common LoRaWAN architecture implmmented with [The Things Network](https://www.thethingsnetwork.org/docs/network/architecture.html).  This repository is mainly to the application server but we keeped here all extra configurations  from the other architecture components excluding the endpoints devices.


![enter image description here](https://www.thethingsnetwork.org/docs/network/overview.png)
## Requirements

Functional requirements:
- FR.01 The system application must persist the receveived endpoint data.
- FR.02 The system application must have a graphic interface to show the statistics of the endpoint data. 

Non-functional requirements:
- NFR.01 The user must be connected to the Internet to access the application GUI (graphic user interface).

## Deployment diagram
![enter image description here](deploymentDiagram.png)


## Gateway software

|Chipset   |Repository                        |Tutorial                     |
|----------------|-------------------------------|-----------------------------|
|SX1272 and SX1276  |https://github.com/tftelkamp/single_chan_pkt_fwd                      |https://www.embarcados.com.br/lora-arduino-raspberry-pi-shield-dragino/|
|SX1301 multi-channel modem and SX1257/SX1255 RF transceivers.     |https://github.com/Lora-net/lora_gateway https://github.com/Lora-net/packet_forwarder | https://github.com/mftutui/configuracoes-gateway-ttn |
