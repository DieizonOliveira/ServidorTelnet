import socket
import time
import requests
import openrouteservice
import subprocess

# --- Configurações das API Keys ---
OPENWEATHER_API_KEY = '3261a44eabac788b20668061bbbbe891'
ORS_API_KEY = '5b3ce3597851110001cf62489dc0f722464940b9a17a7d3672344e97'
EXCHANGE_API_KEY = 'a57a3d74e34293a00806b64e6f0296f2'  

# --- Função previsão do tempo ---
def buscar_previsao(cidade):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={cidade}&appid={OPENWEATHER_API_KEY}&units=metric&lang=pt_br"
    try:
        resposta = requests.get(url)
        if resposta.status_code != 200:
            return "Não foi possível obter a previsão. Verifique o nome da cidade."

        dados = resposta.json()
        previsao_texto = f"\nPrevisão para {cidade.title()}:\n"

        for i in range(0, 40, 8):
            dia = dados['list'][i]
            data_hora = dia['dt_txt'].split()[0]
            descricao = dia['weather'][0]['description']
            temp_min = dia['main']['temp_min']
            temp_max = dia['main']['temp_max']
            previsao_texto += f"{data_hora}: {descricao}, mín: {temp_min}°C, máx: {temp_max}°C\n"

        return previsao_texto

    except Exception as e:
        return f"Erro ao buscar previsão: {e}"

# --- Função cálculo distância e tempo ---
def calcular_rota(origem, destino):
    client = openrouteservice.Client(key=ORS_API_KEY)
    try:
        origem_coords = client.pelias_search(text=origem)['features'][0]['geometry']['coordinates']
        destino_coords = client.pelias_search(text=destino)['features'][0]['geometry']['coordinates']

        rota = client.directions(
            coordinates=[origem_coords, destino_coords],
            profile='driving-car',
            format='json'
        )

        distancia = rota['routes'][0]['summary']['distance'] / 1000
        duracao = rota['routes'][0]['summary']['duration'] / 60

        return f"Distância: {distancia:.2f} km\nTempo estimado: {duracao:.0f} minutos"

    except Exception as e:
        return f"Erro ao calcular rota: {e}"

# --- Função compressão PDF via Ghostscript ---
def comprimir_pdf_ghostscript(input_path, quality):
    quality_map = {
        '1': 'screen',  # baixa qualidade, maior compressão
        '2': 'ebook',   # qualidade média
        '3': 'printer'  # qualidade alta, menos compressão
    }
    q = quality_map.get(quality, 'screen')
    output_path = input_path.replace('.pdf', '_comprimido.pdf')

    gs_command = [
        'gs', '-sDEVICE=pdfwrite',
        '-dCompatibilityLevel=1.4',
        f'-dPDFSETTINGS=/{q}',
        '-dNOPAUSE', '-dQUIET', '-dBATCH',
        f'-sOutputFile={output_path}',
        input_path
    ]

    try:
        subprocess.run(gs_command, check=True)
        return f"PDF comprimido com sucesso! Arquivo salvo como:\n{output_path}"
    except Exception as e:
        return f"Erro na compressão do PDF: {e}"

# --- Função conversão de moedas usando exchangerate.host com API Key ---
def converter_moeda(origem, destino, valor):
    url = f"https://api.exchangerate.host/convert?from={origem}&to={destino}&amount={valor}&access_key={EXCHANGE_API_KEY}"
    try:
        resposta = requests.get(url)
        dados = resposta.json()
        if 'result' in dados and dados['result'] is not None:
            valor_convertido = dados['result']
            return f"{valor} {origem} = {valor_convertido:.2f} {destino}"
        else:
            return f"Erro na conversão: resposta inesperada da API.\n{dados}"
    except Exception as e:
        return f"Erro na conversão: {e}"

# --- Configuração servidor ---
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(('0.0.0.0', 8025))
servidor.listen(1)
print("Servidor aguardando conexão na porta 8025...")

cliente, endereco_cliente = servidor.accept()
print(f"Cliente conectado: {endereco_cliente}")

menu = """========= MENU DE OPERAÇÕES =======
1. Dizer olá
2. Ver hora atual
3. Previsão do tempo
4. Calcular distância e tempo entre dois locais
5. Comprimir PDF
6. Cotação e conversão de moedas
7. Encerrar comunicação

Digite sua opção:
"""

while True:
    cliente.sendall(menu.encode())
    opcao = cliente.recv(1024).decode().strip()

    if opcao == '1':
        cliente.sendall("Olá mundo!\n".encode())

    elif opcao == '2':
        cliente.sendall((time.strftime("%H:%M:%S\n")).encode())

    elif opcao == '3':
        cliente.sendall("Digite o nome da cidade: ".encode())
        cidade = cliente.recv(1024).decode().strip()
        previsao = buscar_previsao(cidade)
        cliente.sendall(previsao.encode())

    elif opcao == '4':
        cliente.sendall("Digite o ponto de origem: ".encode())
        origem = cliente.recv(1024).decode().strip()
        cliente.sendall("Digite o ponto de destino: ".encode())
        destino = cliente.recv(1024).decode().strip()
        resultado_rota = calcular_rota(origem, destino)
        cliente.sendall((resultado_rota + "\n").encode())

    elif opcao == '5':
        cliente.sendall("Digite o caminho do arquivo PDF para comprimir (ex: arquivo.pdf): ".encode())
        caminho_pdf = cliente.recv(1024).decode().strip()
        cliente.sendall("Escolha a qualidade da compressão:\n1 - Baixa\n2 - Média\n3 - Alta\nDigite o número da opção: ".encode())
        qualidade = cliente.recv(1024).decode().strip()
        resultado_comp = comprimir_pdf_ghostscript(caminho_pdf, qualidade)
        cliente.sendall((resultado_comp + "\n").encode())

    elif opcao == '6':
        moedas = ['USD', 'UYU', 'ARS', 'EUR', 'BRL']
        cliente.sendall(f"Escolha moeda de origem: {', '.join(moedas)}\n".encode())
        origem = cliente.recv(1024).decode().strip().upper()
        if origem not in moedas:
            cliente.sendall("Moeda inválida.\n".encode())
            continue

        cliente.sendall(f"Escolha moeda de destino: {', '.join(moedas)}\n".encode())
        destino = cliente.recv(1024).decode().strip().upper()
        if destino not in moedas:
            cliente.sendall("Moeda inválida.\n".encode())
            continue

        cliente.sendall("Digite o valor para converter: ".encode())
        try:
            valor = float(cliente.recv(1024).decode().strip())
        except ValueError:
            cliente.sendall("Valor inválido.\n".encode())
            continue

        resultado = converter_moeda(origem, destino, valor)
        cliente.sendall((resultado + "\n").encode())

    elif opcao == '7':
        cliente.sendall("Até breve!\n".encode())
        break

    else:
        cliente.sendall("Opção inválida. Tente novamente.\n".encode())

cliente.close()
servidor.close()
print("Servidor encerrado.")
