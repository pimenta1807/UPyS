import time


# Buscando a tensão que os nobreaks considerem 0% e 100% de carga
VB0 = 22.0
VB100 = 25.2


def process_ups_info(info):
    company_name = info[:15].strip()
    ups_model = info[16:26].strip()
    version = info[27:37].strip()
    return company_name, ups_model, version

def process_rating(rating):
    valores_rating = rating.split()
    if len(valores_rating) == 4:
        tensao_nominal, corrente_nominal, tensao_bateria, frequencia = valores_rating
        return tensao_nominal, tensao_bateria, frequencia
    else:
        print("Resposta de classificação do NoBreak está em um formato inesperado.")

def est_battery_capacity(voltagem):
    remaing_capacity = (voltagem - VB0) / (VB100 - VB0) * 100
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
I        - Informações do Nobreak.
F        - Classificação do Nobreak.""")

def processar_dados(dados):
    valores = dados.split()
    valores[0] = valores[0].replace("(", "")
    valores[5] = float(valores[5])
    bits = list(valores[7])
    grid = "Bateria" if bits[0] == "1" else "Rede"
    remaing_capacity = est_battery_capacity(valores[5])
    remaing_capacity = format(remaing_capacity, '.2f')

    # Caso algum campo tenha retornado um valor não suportado.
    valores = [v if v != '@' else 'N/A' for v in valores]

    print("\033[H\033[J")
    print("Pressione qualquer tecla para sair.\n")
    print(f"Última leitura:      {time.strftime('%H:%M:%S')}")
    print(f"Tensão de Entrada:   {int(float(valores[0]))} V")
    print(f"Tensão de Falha:     {int(float(valores[1]))} V")
    print(f"Tensão de Saída:     {int(float(valores[2]))} V")
    print(f"Corrente de Saída:   {int(valores[3])} %")
    print(f"Frequência de Saída: {int(float(valores[4]))} Hz")
    print(f"Voltagem da Bateria: {valores[5]} V")
    print(f"Carga da Bateria:    {'Carregando' if valores[5] > 25.6 and grid == 'Rede' else str(remaing_capacity) + ' %'}")
    print(f"Temperatura:         {valores[6]} °C")
    print(f"Modo:                {grid}")
    print(f"Status da Bateria:   {'Baixa' if bits[1] == '1' else 'Com Carga'}")
    print(f"Modo de Teste:       {'Sim' if bits[5] == '1' else 'Não'}")
    print(f"Bypass:              {'Ativado' if bits[2] == '1' else 'Desativado'}")
    print(f"Estado do NoBreak:   {'Em falha' if bits[3] == '1' else 'OK'}")
    print(f"Tipo de NoBreak:     {'Online' if bits[4] == '0' else 'Offline'}")
    print(f"Desligamento:        {'Ativo' if bits[6] == '1' else 'Desativado'}")
    print(f"Buzzer (Apito):      {'Ativo' if bits[7] == '1' else 'Desativado'}")