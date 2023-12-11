import pandas as pd
import pywhatkit as kit
import datetime
import phonenumbers
import time
import random

# Función para validar un número de teléfono
def validar_numero(numero):
    try:
        parsed_numero = phonenumbers.parse(numero, None)
        return phonenumbers.is_valid_number(parsed_numero)
    except phonenumbers.phonenumberutil.NumberParseException:
        return False

# Lee el archivo CSV con los mensajes, números de teléfono y nombres
df = pd.read_csv('datos.csv')  # Reemplaza 'datos.csv' con tu archivo CSV
df['Numero'] = df['Numero'].astype(str)

# Lista para almacenar los números a los que se enviaron los mensajes
numeros_enviados = []
# Lista para almacenar los números de teléfono inválidos
numeros_invalidos = []

# Itera a través de cada fila del DataFrame
for index, row in df.iterrows():
    mensaje = row['Mensaje']
    numero = row['Numero']

    if validar_numero(numero):
        try:
            hora_actual = datetime.datetime.now()
            hora_envio = hora_actual.hour

            kit.sendwhatmsg(numero, mensaje, hora_envio, hora_actual.minute + 1)
            print(f"Mensaje enviado a {numero}: {mensaje}")
            numeros_enviados.append(numero)

            # Genera un retraso aleatorio entre 20 y 60 segundos
            retraso = random.randint(20, 60)
            time.sleep(retraso)
        except Exception as e:
            print(f"Error al enviar mensaje a {numero}: {str(e)}")
            numeros_invalidos.append(numero)
    else:
        numeros_invalidos.append(numero)
        print(f"Número de teléfono inválido: {numero}. Mensaje no enviado.")

# Generar reporte de números inválidos
if numeros_invalidos:
    print("\n----- Reporte de Números Inválidos -----")
    for num in numeros_invalidos:
        print(f"Número de teléfono inválido: {num}")
else:
    print("\nTodos los mensajes fueron enviados con éxito.")

# Puedes hacer lo que necesites con las listas numeros_enviados y numeros_invalidos
# Por ejemplo, guardarlos en archivos, enviar notificaciones, etc.
