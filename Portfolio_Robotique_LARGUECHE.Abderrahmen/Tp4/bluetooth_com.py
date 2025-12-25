import serial
import threading

# --- CONFIGURATION ---
# Sur Windows : 'COM1', 'COM3', etc.
# Sur Linux/Mac : '/dev/ttyUSB0', '/dev/ttyACM0', etc.
SERIAL_PORT = 'COM9'
BAUD_RATE = 38400


def reception_thread(ser):
    """
    Fonction qui tourne en arrière-plan pour écouter les messages entrant en permanence.
    """
    while True:
        try:
            # S'il y a des données dans le buffer
            if ser.in_waiting > 0:
                # On lit la ligne (reçoit des bytes)
                data_bytes = ser.readline()

                # On décode les bytes en string (souvent utf-8 ou ascii)
                try:
                    data_str = data_bytes.decode('utf-8').strip()
                    if data_str:
                        print(f"\n[REÇU] : {data_str}")
                        # On réaffiche le prompt pour que ce soit joli
                        print("Votre message : ", end='', flush=True)
                except UnicodeDecodeError:
                    print(f"\n[REÇU (Brut)] : {data_bytes}")

        except serial.SerialException:
            print("\nErreur de connexion pendant la lecture.")
            break
        except Exception as e:
            print(f"\nErreur inattendue : {e}")
            break


try:
    # Initialisation du port série
    print(f"Tentative de connexion à {SERIAL_PORT}...")
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Connecté avec succès à {BAUD_RATE} baud.")

    # Démarrage du thread d'écoute
    # daemon=True signifie que le thread mourra quand le programme principal s'arrêtera
    thread = threading.Thread(target=reception_thread, args=(ser,), daemon=True)
    thread.start()

    print("Vous pouvez taper vos messages ci-dessous (CTRL+C pour quitter).")
    print("-" * 50)

    # Boucle principale pour l'ENVOI
    while True:
        # Input bloquant (attend que l'utilisateur tape Entrée)
        user_input = input("Votre message : ")

        if user_input.lower() == 'exit':
            break

        # Envoi des données
        # On ajoute souvent \n (nouvelle ligne) pour que l'autre côté sache que le message est fini
        message_to_send = user_input + '\n'
        ser.write(message_to_send.encode('utf-8'))

except serial.SerialException as e:
    print(f"Erreur : Impossible d'ouvrir le port {SERIAL_PORT}. Vérifiez qu'il n'est pas utilisé ailleurs.")
    print(f"Détails : {e}")
except KeyboardInterrupt:
    print("\nArrêt du programme demandé par l'utilisateur.")
finally:
    # Fermeture propre
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Port série fermé.")
