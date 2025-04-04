import config.settings as set
import threading
import time
from src.Screen_Process import VerificadorTela
from src.input_monitor import Inputs

Vt = VerificadorTela()
In = Inputs()


def iniciar_programa():
    print("Iniciando KAutoHunt...")

    print("Iniciando monitoramento de teclas...")
    threading.Thread(target=In.IniciarCaça, daemon=True).start()
    threading.Thread(target=In.ModoDebug, daemon=True).start()

    print("Iniciando bot de detecção de mobs...")
    threading.Thread(target=Vt.Verificar, daemon=True).start()
    threading.Thread(target=Vt.ModoDebug, daemon=True).start()

    while True:
        time.sleep(5)


if __name__ == "__main__":
    iniciar_programa()
