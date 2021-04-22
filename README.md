
# Aplicação SMQG
![Diagrama de desenvolvimento](deploymentDiagram.png)
O servidor de aplicação consiste em três módulos:
- Cliente MQTT
- Banco de dados MYSQL
- Interface gráfica Grafana

## Cliente MQTT
O cliente MQTT foi construído em python e consiste basicamente em se inscrever em um tópico MQTT e popular o modelo MYSQL.
Sintaxe de execução:

        ``
        python3 app.py <mysql-user> <mysql-pass> <mysql-model> <mqtt-broker> <mqtt-topic>
        ```

![database model](databaseModel.png)

## Modelo do banco de dados
![modelo do banco de dados](databaseModel.png)

## Grafana
![database model](databaseModel.png)


