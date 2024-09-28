import time
import re
import os


# Buscando a tensão que os nobreaks considerem 0% e 100% de carga
VB0 = 22.0
VB100 = 25.2

def is_valid_command(command):
    # Define os padrões para os comandos
    patterns = [
        r'^T$',          # Teste de Bateria (10 segundos)
        r'^TL$',         # Testa a bateria até estado baixo e retorna para rede
        r'^T\d+$',       # Testa a bateria por <n> minutos
        r'^Q$',          # Desabilita beep extra inicial em caso de falha AC
        r'^S\d+$',       # Desliga o nobreak em <n> segundos
        r'^S\d+R\d+$',   # Desliga o nobreak em <n> minutos e religa em <m> minutos
        r'^C$',          # Cancela o desligamento programado
        r'^CT$',         # Cancela o teste de bateria
    ]
    
    # Verifica se o comando corresponde a algum dos padrões
    for pattern in patterns:
        if re.match(pattern, command):
            return True
    return False

def process_ups_info(info):
    company_name = info[:15].strip()
    ups_model = info[16:26].strip()
    version = info[27:37].strip()
    return company_name, ups_model, version

def process_rating(rating):
    rating_values = rating.split()
    if len(rating_values) == 4:
        rated_voltage, rated_current, battery_voltage, frequency = rating_values
        return rated_voltage, battery_voltage, frequency
    else:
        print("Resposta de classificação do NoBreak está em um formato inesperado.")

def est_battery_capacity(voltage):
    remaing_capacity = (voltage - VB0) / (VB100 - VB0) * 100
    return min(max(remaing_capacity, 0), 100)

def print_commands():

    print("""Comandos disponíveis:
Q1       - Leitura de dados.
T        - Teste de Bateria (10 segundos.
TL       - Testa a bateria até estado baixo e retorna para rede.
T<n>     - Testa a bateria por <n> minutos.
Q        - Desabilita beep extra inicial em caso de falha AC.
S<n>     - Desliga o nobreak em <n> segundos.
S<n>R<m> - Desliga o nobreak em <n> minutos e religa em <m> minutos.
C        - Cancela o desligamento programado.
CT       - Cancela o teste de bateria.
""")

def process_data(data):
    values = data.split()
    values[0] = values[0].replace("(", "")
    values[5] = float(values[5])
    bits = list(values[7])
    grid = "Bateria" if bits[0] == "1" else "Rede"
    remaing_capacity = est_battery_capacity(values[5])
    remaing_capacity = format(remaing_capacity, '.2f')

    # Caso algum campo tenha retornado um valor não suportado.
    values = [v if v != '@' else 'N/A' for v in values]

    print("Pressione qualquer tecla para sair.\n")
    print(f"Última leitura:      {time.strftime('%H:%M:%S')}")
    print(f"Tensão de Entrada:   {int(float(values[0]))} V")
    print(f"Tensão de Falha:     {int(float(values[1]))} V")
    print(f"Tensão de Saída:     {int(float(values[2]))} V")
    print(f"Corrente de Saída:   {int(values[3])} %")
    print(f"Frequência de Saída: {int(float(values[4]))} Hz")
    print(f"Voltagem da Bateria: {values[5]} V")
    print(f"Carga da Bateria:    {'Carregando' if values[5] > 25.6 and grid == 'Rede' else str(remaing_capacity) + ' %'}")
    print(f"Temperatura:         {values[6]} °C")
    print(f"Modo:                {grid}")
    print(f"Status da Bateria:   {'Baixa' if bits[1] == '1' else 'Com Carga'}")
    print(f"Modo de Teste:       {'Sim' if bits[5] == '1' else 'Não'}")
    print(f"Bypass:              {'Ativado' if bits[2] == '1' else 'Desativado'}")
    print(f"Estado do NoBreak:   {'Em falha' if bits[3] == '1' else 'OK'}")
    print(f"Tipo de NoBreak:     {'Online' if bits[4] == '0' else 'Offline'}")
    print(f"Desligamento:        {'Ativo' if bits[6] == '1' else 'Desativado'}")
    print(f"Buzzer (Apito):      {'Ativo' if bits[7] == '1' else 'Desativado'}")


def log_data(data, name):

    values = data.split()
    values[0] = values[0].replace("(", "")
    values[5] = float(values[5])
    bits = list(values[7])
    grid = "Bateria" if bits[0] == "1" else "Rede"
    remaing_capacity = est_battery_capacity(values[5])
    remaing_capacity = format(remaing_capacity, '.2f')

    header = "Hora;Tensão de Entrada;Tensão de Falha;Tensão de Saída;Corrente de Saída;Voltagem da Bateria;Carga da Bateria;Temperatura;Modo;Status da Bateria;Estado do NoBreak\n"
    csv_data = f"{time.strftime('%H:%M:%S')};{int(float(values[0]))};{int(float(values[1]))};{int(float(values[2]))};{int(values[3])};{values[5]};{remaing_capacity};{values[6]};{grid};{'Baixa' if bits[1] == '1' else 'Com Carga'};{'Em falha' if bits[3] == '1' else 'OK'}\n"

    file_path = f"{name}.csv"
    
    # Verifica se o arquivo existe
    file_exists = os.path.isfile(file_path)
    
    # Verifica se o arquivo está vazio
    file_is_empty = os.path.getsize(file_path) == 0 if file_exists else True
    
    # Abre o arquivo no modo de anexar
    with open(file_path, "a") as f:
        # Adiciona o cabeçalho se o arquivo não existir ou estiver vazio
        if not file_exists or file_is_empty:
            f.write(header)
        
        # Escreve os dados no arquivo
        f.write(csv_data)