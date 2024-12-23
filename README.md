## Introdução
Este projeto foi desenvolvido para a disciplina Computação Física e Aplicações, em conjunto com uma turma do curso de Textil e Moda. Consiste em uma aplicação que envolve microcontrolador, comunicação via rede e 
uma interface web para monitoramento e controle de dispositivos. 

Desenvolvido pensando em crianças na faixa etária de 6 a 10  anos de idade, e em seus pais, preocupados com a segurança dos pequenos ao fazer trajetos curtos como ir ao mercado, à padaria ou à escola; com nosso produto as crianças podem aprender a cada passo a ter mais independência.

A peça combina a modelagem de um colete com ajustes de uma mochila, criada em tecido de sarja com forro para garantia de uma estrutura firme para segurar os componentes e isolá-los do corpo da criança. Ou seja, possui o conforto e a estética de um acessório com praticidade para limpar, além de promover uma distribuição uniforme dos componentes na peça.

Em termos de software, ele é composto por três partes principais: um servidor web Flask, código para execução no microcontrolador (ESP32) e uma página HTML que interage com o servidor.

A principal funcionalidade consiste em enviar dados de geolocalização para o servidor, que os utiliza para marcar em um mapa e atualizar em tempo real a posição do microcontrolador. Além disso, foram incluídos 
dois LEDs à peça na altura dos ombros. Esses LEDs podem ser acionados pelo adulto que acompanha o trajeto para indicar direções que a criança deve seguir.


Materiais:
- ESP32
- GPS Neo-6M
- 2 leds
- Power Bank
	  

### 1. Servidor Web (app.py)
O servidor web, desenvolvido em Flask, é responsável por gerenciar as requisições e interagir com os dispositivos que enviam dados e ligam/desligam os LEDs. Ele possui várias rotas para realizar diferentes funções:

  - **(POST /api/coordenadas)**: Esta rota serve para receber coordenadas de latitude e longitude enviadas pelo microcontrolador; 
  - **(GET /api/latest_coordinates)**: Usada para informar as últimas coordenadas recebidas pelo servidor, permitindo que a interface web as visualize em tempo real;
  - **(POST /api/led1, POST /api/led2)**: Estas rotas permitem que a interface web envie comandos para ligar ou desligar os LEDs conectados ao microcontrolador;
  - **(GET /api/led_states)**: Criada para permitir saber o estado (ligado ou desligado) dos LEDs. Esse estado é exibido no terminal;
  - A última rota é responsável pelo acesso à página web (/).

### 2. Código do Microcontrolador (main.py)
O código do arquivo main.py é responsável por conectar o ESP32 à rede e faz a comunicação dele com o servidor.

  - **connect_wifi()**: O microcontrolador se conecta a uma rede (Wi-Fi ou móvel) utilizando credenciais fornecidas (SSID e senha).
  - **update_gps_data()**: Leitura periódica e acionamento de envio (quando obtém uma posição válida) dos dados do GPS;
  - **send_coordinates(lat, lon)**: Função responsável pelo envio das coordenadas via requisição HTTP;
  - **update_leds()**: Consulta o servidor para obter o estado dos LEDs e os aciona conforme o comando recebido.

### 3. Interface Web (index.html)
A interface web permite que o usuário visualize as coordenadas geográficas recebidas em tempo real e controle os LEDs. Ela é composta por:
  - Exibição de coordenadas: As últimas coordenadas de latitude e longitude recebidas são exibidas na tela, e a API do Google Maps é utilizada para mostrar a localização geográfica.
  - Controle dos LEDs: A interface oferece botões para ligar e desligar os LEDs.
  - Atualização em tempo real: A página web realiza uma requisição a cada 3 segundos para atualizar as coordenadas e a posição do marcador no mapa.

## Execução
1. Acesse a pasta pelo terminal e execute o comando _python app.py_
2. Na linha 14 do _main.py_ substitua NOME_DA_REDE e SENHA pelas informações da rede que será conectada ao ESP32
3. Se ESP32 e a  máquina com o servidor estiverem conectados à mesma rede, substitua ENDERECO_SERVIDOR nas linhas 45 e 58 do main.py pelo ip informado no terminal (isso foi feito para os testes iniciais). 

![IP](img/ip.png)

4. Quando o microcontrolador estiver conectado a uma rede móvel, é preciso haver um túnel para a comunicação e o servidor precisa ser deixado online. Nesse caso, a definição do endereço vai depender de como isso for feito.
5. No index.html, linha 64, substitua _CHAVE_ pela key da API do Google Maps
6. Carregue os arquivos _micropyGPS.py_ e _main.py_ na memória do ESP
7. Faça o _main.py_ executar
8. Acesse o endereço do servidor em um navegador.


### API do Maps
Foi obtida utilizando o período de teste do Google Cloud [(https://cloud.google.com/?hl=pt-BR)](https://cloud.google.com/?hl=pt-BR)


### ngrok
Serviço utilizado para a criação do túnel de comunicação entre ESP e servidor. Para isso, ele endereça o servidor e permite o acesso à interface com uma url.
Utilização:
1. Faça o download do programa [https://download.ngrok.com/windows?tab=download](https://download.ngrok.com/windows?tab=download)
2. Crie uma conta em [https://dashboard.ngrok.com/signup](https://dashboard.ngrok.com/signup)
3. Gere um token [https://dashboard.ngrok.com/get-started/your-authtoken](https://dashboard.ngrok.com/get-started/your-authtoken)
4. Executar ngrok.exe e os comandos

         ngrok config add-authtoken ESCREVA_AQUI_O_TOKEN
         ngrok http 5000
   
6. O primeiro link na linha Forwarding é o endereço do servidor e pode ser usado para acessar a interface via internet

![ngrok](img/ngrok.png)


