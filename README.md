
# SMQG Server

The architecture is a common LoRaWAN architecture implmmented with [The Things Network](https://www.thethingsnetwork.org/docs/network/architecture.html).  This repository is mainly to the application server but we keeped here all extra configurations  from the other architecture components excluding the endpoints devices.


![enter image description here](https://www.thethingsnetwork.org/docs/network/overview.png)
## Requirements

Functional requirements:
- FR.01 The system must persist the receveived endpoint data.
- FR.02 The system must have a graphic interface to show the statistics of the endpoint data. 

Non-functional requirements:
- NFR.01 The persistence must be implemented with MySQL.
- NFR.02 The graphic interface must be implemented with Grafana.
- NFR.03 The gateway must be implemented with Raspberry PI 3.
