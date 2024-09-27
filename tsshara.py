import serial
import time
#import msvcrt

# Configuração da porta serial
porta_serial = 'COM3'  # Defina a porta serial correta
baud_rate = 9600  # Defina a taxa de baud do seu NoBreak

# Sequência hexadecimal para enviar
hex_string_info = "49 0D"
bytes_to_send_info = bytes.fromhex(hex_string_info)

hex_string_rating = "46 0D"
bytes_to_send_rating = bytes.fromhex(hex_string_rating)



# Inicializar a conexão serial
ser = serial.Serial(porta_serial, baud_rate, timeout=1)

# Verificar se a porta serial está aberta
if ser.is_open:
    print(f"Conexão com {porta_serial} estabelecida.\n")

    # Enviar a sequência de bytes
    print("Requisitando informações do NoBreak...")
    ser.write(bytes_to_send_info)
    time.sleep(0.1)
    nobreak = ser.readline().decode('utf-8').strip()
    print("NoBreak respondeu nosso oi!:", nobreak, "\n")

    print("Requisitando informações de classificação do NoBreak...")
    ser.write(bytes_to_send_rating)
    time.sleep(0.1)
    rating = ser.readline().decode('utf-8').strip()
    if rating == '':
        rating = "Não foram encontradas informações de classificação."
    else:
        # Processar a resposta de classificação
        valores_rating = rating.split()
        if len(valores_rating) == 4:
            tensao_nominal = valores_rating[0]
            corrente_nominal = valores_rating[1]
            tensao_bateria = valores_rating[2]
            frequencia = valores_rating[3]

            print("Informações de Classificação do NoBreak:")
            print(f"Tensão Nominal: {tensao_nominal} V - Corrente Nominal: {corrente_nominal} % - Tensão da Bateria: {tensao_bateria} V - Frequência: {frequencia} Hz")        
        else:
            print("Resposta de classificação do NoBreak está em um formato inesperado.")

    input("Pressione Enter para continuar...")
    print("\n")
    #if nobreak == "#TS SHARA 230727 Senoid  18 V01030500F":
    if nobreak == "#TS -222  231016 Senoid  18 V010101058":
        print("Solicitando dados...\n")
        # Sequência hexadecimal para enviar
        hex_string = "51 31 0D"
        bytes_to_send = bytes.fromhex(hex_string)
        print("Aguarde...\n")
        time.sleep(3)
        
        try:
            while True:
                estimativa_carga = 0

                hora_leitura = time.strftime("%H:%M:%S")
                # Enviar a sequência de bytes
                ser.write(bytes_to_send)

                # Aguardar um breve período de tempo para permitir que o NoBreak responda
                time.sleep(0.1)
                # Ler a resposta do NoBreak
                dados = ser.readline().decode('utf-8').strip()
                valores = dados.split()

                # Antes de imprimir, vamos remover o ( do primeiro valor
                valores[0] = valores[0].replace("(", "")
                # Passamos a voltagem das baterias pra float para evitar de fazer a conversão toda vez que precisarmos
                valores[5] = float(valores[5])
                # Vamos fazer também a representação do valor 7.
                bits = list(valores[7])
                rede_eletrica = "Bateria" if bits[0] == "1" else "Rede"
                status_bateria = "Baixa" if bits[1] == "1" else "Com Carga"
                bypass = "Ativado" if bits[2] == "1" else "Desativado"
                ups_check = "Em falha" if bits[3] == "1" else "OK"
                ups_type = "Online" if bits[4] == "0" else "Offline"
                test_mode = "Sim" if bits[5] == "1" else "Não"
                shutdown = "Ativo" if bits[6] == "1" else "Desativado"
                buzzer = "Ativo" if bits[7] == "1" else "Desativado"

                # Vamos também estimar a carga da bateria baseasdo na tensão.   
                # Voltagem que representa 0% de carga
                voltagem_zero = 22.0
                # Voltagem que representa 100% de carga
                voltagem_cem = 25.2
                # Calcula a estimativa de carga
                estimativa_carga = (valores[5] - voltagem_zero) / (voltagem_cem - voltagem_zero) * 100
                # Limita a estimativa de carga entre 0 e 100
                estimativa_carga = format(estimativa_carga, '.2f')
                if float(estimativa_carga) > 100:
                    estimativa_carga = 100

                #limpar a tela antes de imprimir, está aqui pra garantir que as informações já foram obtidas e calculadas.
                print("\033[H\033[J")

                print("Pressione qualquer tecla para sair.\n")
                print(f"Última leitura:      ", hora_leitura)
                print(f"Tensão de Entrada:   ", int(float(valores[0])), "V")
                print(f"Tensão de Falha:     ", int(float(valores[1])), "V")
                print(f"Tensão de Saída:     ", int(float(valores[2])), "V")
                print(f"Corrente de Saída:   ", int((valores[3])), "%")
                print(f"Frequência de Saída: ", int(float(valores[4])), "Hz")
                print(f"Voltagem da Bateria: ", valores[5], "V")
                print(f"Carga da Bateria:    ", "Carregando" if valores[5]> 25.6 and rede_eletrica == "Rede" else str(estimativa_carga) + " %")
                print(f"Temperatura:         ", valores[6], "°C")
                print(f"Modo:                ", rede_eletrica)
                print(f"Status da Bateria:   ", status_bateria)
                print(f"Modo de Teste:       ", test_mode)
                print(f"Bypass:              ", bypass)
                print(f"Estado do NoBreak:   ", ups_check)
                print(f"Tipo de NoBreak:     ", ups_type)
                print(f"Desligamento:        ", shutdown)
                print(f"Buzzer (Apito):      ", buzzer)




            # Aguardar 5 segundos antes de solicitar os dados novamente
            time.sleep(1.8)
            pass
        except KeyboardInterrupt:
            print("\nSaindo...")

    # Fechar a conexão serial
    ser.close()
    print("\nConexão com a porta serial fechada.")
else:
    print(f"Erro ao abrir {porta_serial}. Verifique se a porta está disponível e tente novamente.")

