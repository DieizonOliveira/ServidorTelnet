Servidor Telnet Multifuncional - Projeto ADS
Descrição do Projeto
Este projeto consiste em um servidor Telnet desenvolvido em Python, que disponibiliza uma interface simples para realizar diversas operações úteis via conexão remota. O servidor aceita conexões TCP na porta 8025 e oferece um menu interativo para o usuário executar comandos variados.

O objetivo é fornecer uma ferramenta prática para aprendizado e aplicação de conceitos de redes, APIs externas e manipulação de arquivos, integrando funcionalidades reais do mundo moderno em uma interface de linha de comando acessível via Telnet.

Funcionalidades Disponíveis
O servidor Telnet disponibiliza as seguintes opções:

Dizer olá
Retorna uma saudação simples ("Olá mundo!").

Ver hora atual
Exibe a hora atual do servidor.

Previsão do tempo
Consulta a previsão meteorológica para uma cidade informada, exibindo a previsão para os próximos 5 dias (com intervalos de 24 horas).

Calcular distância e tempo entre dois locais
Utiliza uma API de roteamento para calcular a distância em quilômetros e o tempo estimado de viagem entre dois endereços ou pontos informados.

Comprimir PDF
Recebe o caminho de um arquivo PDF e permite comprimi-lo em três níveis de qualidade diferentes (baixa, média e alta), usando o Ghostscript para reduzir o tamanho do arquivo sem perder muita qualidade.

Cotação e conversão de moedas
Permite consultar a cotação atual entre diferentes moedas (dólar, peso uruguaio, peso argentino, euro e real) e converter valores entre elas, utilizando a API exchangerate.host.

Encerrar comunicação
Finaliza a conexão com o cliente e encerra o servidor.

Tecnologias e APIs Utilizadas
Linguagem e Ferramentas
Python 3.12 — Linguagem principal do servidor e lógica do programa.

Socket TCP — Para comunicação via rede usando o protocolo Telnet.

Ghostscript — Utilizado para compressão de arquivos PDF via linha de comando.

APIs Externas
OpenWeatherMap
API de dados meteorológicos para previsão do tempo.
Documentação: https://openweathermap.org/api
Uso: Obtém dados de previsão estendida para a cidade solicitada.

OpenRouteService
API para cálculo de rotas, distância e duração entre dois locais geográficos.
Documentação: https://openrouteservice.org/dev/#/api-docs
Uso: Calcula trajetos e tempos estimados de deslocamento de carro.

Exchangerate.host
API de câmbio e conversão de moedas (gratuita, requer API Key).
Documentação: https://exchangerate.host/#/
Uso: Fornece taxas de câmbio atualizadas para diversas moedas e realiza conversões monetárias.

Como Usar
Executar o servidor:
Rode o script servidor_telnet.py no terminal:

bash
Copiar
Editar
python servidor_telnet.py
Conectar via Telnet:
Use um cliente Telnet para se conectar na máquina e porta do servidor, por exemplo:

bash
Copiar
Editar
telnet localhost 8025
Interagir com o menu:
Digite a opção desejada e siga as instruções fornecidas pelo servidor.

Comprimir PDF:
Informe o caminho completo do arquivo PDF existente na máquina onde o servidor está rodando e escolha o nível de compressão.

Conversão de moedas:
Escolha as moedas de origem e destino dentre as disponíveis, informe o valor e aguarde o resultado.

Encerrar:
Use a opção 7 para fechar a conexão com o servidor.

Requisitos
Python 3.6 ou superior.

Biblioteca requests instalada (pip install requests).

Biblioteca openrouteservice instalada (pip install openrouteservice).

Ghostscript instalado e disponível no PATH do sistema (gs).

API Keys para OpenWeatherMap, OpenRouteService e Exchangerate.host configuradas no código.

Pontos de Expansão
Este servidor pode ser expandido para incluir mais funcionalidades, tais como:

Integração com mais APIs (ex: notícias, transporte público, câmbio com outras moedas).

Autenticação de usuários.

Interface gráfica via web para facilitar o uso.

Funcionalidades de agenda e alarmes.

Logs e monitoramento das conexões.

