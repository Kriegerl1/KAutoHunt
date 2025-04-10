import keyboard
import time
import config.settings as set
from src.controller import Controller
import threading

CT = Controller()

AtivarThreadsDeCaça = threading.Event()
AtivarDebug = threading.Event()


def mostrar_status():
    print(
        f"[STATUS] Caça: {'ON' if set.ProcurandoAlvo else 'OFF'} | Debug: {'ON' if set.Debug else 'OFF'}"
    )


class Inputs:
    def __init__(self):
        self.thread_caca = None
        self.thread_debug = None
        self.tela_monitor = None
        self.executando_caca = False
        self.executando_debug = False

        keyboard.add_hotkey("end", self.toggle_caca)
        keyboard.add_hotkey("home", self.toggle_debug)

    def set_monitor(self, monitor):
        self.tela_monitor = monitor

    def toggle_caca(self):
        if AtivarThreadsDeCaça.is_set():
            # Desativa caça
            AtivarThreadsDeCaça.clear()
            set.ProcurandoAlvo = False
            print("[THREAD] Caça desativada.")
        else:
            # Garante que não há thread anterior rodando
            if self.thread_caca is not None and self.thread_caca.is_alive():
                print("[INFO] Aguardando thread anterior encerrar...")
                AtivarThreadsDeCaça.clear()
                self.thread_caca.join(timeout=2)

            # Ativa caça
            AtivarThreadsDeCaça.set()
            set.ProcurandoAlvo = True
            CT.AjusteInicial()

            print("[THREAD] Caça ativada.")

            self.thread_caca = threading.Thread(target=self.IniciarCaça, daemon=True)
            self.thread_caca.start()

        mostrar_status()

    def toggle_debug(self):
        if AtivarDebug.is_set():
            # Desativa debug
            AtivarDebug.clear()
            set.Debug = False
            print("[THREAD] Debug desativado.")
        else:
            # Ativa debug
            AtivarDebug.set()
            set.Debug = True
            print("[THREAD] Debug ativado.")

            if self.thread_debug is None or not self.thread_debug.is_alive():
                self.thread_debug = threading.Thread(target=self.ModoDebug, daemon=True)
                self.thread_debug.start()
            else:
                print("[AVISO] A thread de debug já está rodando!")

        mostrar_status()

    def IniciarCaça(self):
        if self.executando_caca:
            print("[AVISO] A thread de caça já está em execução.")
            return
        self.executando_caca = True

        print("Thread de caça rodando.")
        while AtivarThreadsDeCaça.is_set():
            if self.tela_monitor:
                self.tela_monitor.Verificar()
            time.sleep(0.5)

        print("Thread de caça finalizado.")
        self.executando_caca = False

    def ModoDebug(self):
        if self.executando_debug:
            print("[AVISO] A thread de debug já está em execução.")
            return
        self.executando_debug = True

        print("Thread de debug rodando.")
        while AtivarDebug.is_set():
            if self.tela_monitor:
                self.tela_monitor.ModoDebug()
            time.sleep(0.5)

        print("Thread de debug finalizado.")
        self.executando_debug = False

    def listen(self):
        print("Aguardando comandos (END para caça, HOME para debug)...")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Encerrando monitoramento de teclas.")
