import serial
import serial.tools.list_ports
import time
import protocols.megatech as megatech
#import msvcrt


# Configuração da porta serial
BAUD_RATE = 2800

def clear_screen():
    print("\033[H\033[J")

def search_for_serial_port():
    ports = serial.tools.list_ports.comports()
    available_ports = [port.device for port in ports]
    return available_ports

def start_serial_connection():

    ports = search_for_serial_port()
    for port in ports:
        try:
            ser = serial.Serial(port, BAUD_RATE, timeout=1)
            if ser.is_open:
                print(f"Conexão com porta {port} estabelecida.\n")
                return ser
        except serial.SerialException:
            print(f"Sem conexão na porta {port}.")
    return None # Caso nenhuma porta serial esteja disponível

def send_command(ser, command):
    command = command.strip() + '\r'    # Adiciona <cr> ao comando
    ser.write(command.encode('utf-8'))  # Envia o comando codificado.
    time.sleep(0.1)                     # Aguarda um tempo para a resposta
    answer = ser.readline().decode('utf-8').strip()
    if answer == command: 
        print("Comando invalido recebido pelo NoBreak.")
        return None
    return answer


def main():

    ser = start_serial_connection
    if not ser:
        print("Nenhuma porta serial disponível.")
        return
    
    print("Verificação do modelos de Nobreak...")

    # Megatec https://networkupstools.org/protocols/megatec.html
    who_is = send_command(ser, "I") # Megatech UPS Information Command
    if who_is:
        print("Protocolo Megatech Encontrado.")
        company_name, ups_model, version = megatech.process_ups_info(who_is)
        tensao_nominal, tensao_bateria, frequencia = send_command(ser, "F") # Megatech UPS Rating Command
        while True:
            print(f"Nome da empresa: {company_name} - Modelo: {ups_model} - Versão: {version}")
            print(f"Tensão Nominal: {tensao_nominal}V - Tensão da Bateria: {tensao_bateria}V - Frequência: {frequencia}Hz\n\n")
            megatech.print_commands()
            input = "Digite o comando desejado: "
            send_command(ser, input)
            time.sleep(10)
            clear_screen()
    

        

if __name__ == "__main__":
    main()