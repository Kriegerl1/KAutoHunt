import keyboard
import time
import config.settings as set
import threading

AtivarThreadsDeCaça = threading.Event()
AtivarDebug = threading.Event()


def mostrar_status():
    print(
        f"[STATUS] Caça: {'ON' if set.ProcurandoAlvo else 'OFF'} | Debug: {'ON' if set.Debug else 'OFF'}"
    )


class Inputs:
    def __init__(self):
        keyboard.add_hotkey("end", self.toggle_caca)
        keyboard.add_hotkey("home", self.toggle_debug)

    def toggle_caca(self):
        if AtivarThreadsDeCaça.is_set():
            AtivarThreadsDeCaça.clear()
            set.ProcurandoAlvo = False
        else:
            AtivarThreadsDeCaça.set()
            set.ProcurandoAlvo = True

        mostrar_status()

    def toggle_debug(self):
        if AtivarDebug.is_set():
            AtivarDebug.clear()
            set.Debug = False
        else:
            AtivarDebug.set()
            set.Debug = True

        mostrar_status()

    def IniciarCaça(self):
        print("Hotkey 'END' pronta para ativar/desativar caça.")
        while True:
            time.sleep(1)

    def ModoDebug(self):
        print("Hotkey 'HOME' pronta para ativar/desativar debug.")
        while True:
            time.sleep(1)
