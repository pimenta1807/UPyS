import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker


def plot_tensao(file_path, ac, dc, delimiter=';', time_format='%H:%M:%S'):
    """
    Plota as tensões e dados da bateria a partir de um arquivo CSV.

    :param file_path: Caminho para o arquivo CSV.
    :param ac: Lista de colunas de tensão a serem plotadas.
    :param dc: Lista de colunas de bateria a serem plotadas.
    :param delimiter: Delimitador do arquivo CSV.
    :param time_format: Formato da coluna de tempo.
    """
    df = pd.read_csv(file_path, delimiter=delimiter)

    df['Hora'] = pd.to_datetime(df['Hora'], format=time_format)
    vertical_line_time = pd.to_datetime('08:00:00', format='%H:%M:%S')
    df.set_index('Hora', inplace=True)

    # Plotar tensões
    plt.figure(figsize=(18, 6))

    plt.subplot(1, 3, 1)
    for coluna in ac:
        plt.plot(df.index, df[coluna], label=coluna)
    #plt.axvline(x=vertical_line_time, color='r', linestyle='--', label='Modo Teste')
    plt.title('Análise de Tensão')
    plt.xlabel('Hora')
    plt.ylabel('Tensão (V)')
    plt.legend()
    plt.grid(True)
    plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=10))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(10))  # Ajuste o intervalo para 0.2 V
    plt.xticks(rotation=45)

    # Plotar voltagem da bateria
    plt.subplot(1, 3, 2)
    #plt.axvline(x=vertical_line_time, color='r', linestyle='--', label='Modo Teste')
    plt.plot(df.index, df['Voltagem da Bateria'], label='Voltagem da Bateria')
    plt.plot(df.index, df['Temperatura'], label='Temperatura')
    plt.title('Voltagem da Bateria - Sensor')
    plt.xlabel('Hora')
    plt.ylabel('Voltagem (V) - Temperatura (°C)')
    plt.ylim(16.4, 28)
    plt.legend()
    plt.grid(True)
    plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=10))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(0.2))  # Ajuste o intervalo para 0.2 V
    plt.xticks(rotation=45)

    # Plotar carga da bateria
    plt.subplot(1, 3, 3)
    #plt.axvline(x=vertical_line_time, color='r', linestyle='--', label='Modo Teste')
    plt.plot(df.index, df['Carga da Bateria'], label='Bateria Estimada (25.2 - 20.8) - % ')
    plt.plot(df.index, df['Corrente de Saida'], label='Corrente anunciada - %')
    plt.title('Carga da Bateria + Corrente UPS')
    plt.xlabel('Hora')
    plt.ylabel('Carga (%)')
    plt.ylim(0, 100)
    plt.legend()
    plt.grid(True)
    plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=10))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(5))  # Ajuste o intervalo para 0.2 V

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

