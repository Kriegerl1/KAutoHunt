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
        self.thread_caca = None
        self.thread_debug = None
        self.tela_monitor = None

        keyboard.add_hotkey("end", self.toggle_caca)
        keyboard.add_hotkey("home", self.toggle_debug)

    def set_monitor(self, monitor):
        self.tela_monitor = monitor

    def toggle_caca(self):
        if AtivarThreadsDeCaça.is_set():
            AtivarThreadsDeCaça.clear()
            set.ProcurandoAlvo = False
            print("[THREAD] Caça desativada.")
        else:
            AtivarThreadsDeCaça.set()
            set.ProcurandoAlvo = True
            print("[THREAD] Caça ativada.")
            self.thread_caca = threading.Thread(target=self.IniciarCaça, daemon=True)
            self.thread_caca.start()

        mostrar_status()

    def toggle_debug(self):
        if AtivarDebug.is_set():
            AtivarDebug.clear()
            set.Debug = False
            print("[THREAD] Debug desativado.")
        else:
            AtivarDebug.set()
            set.Debug = True
            print("[THREAD] Debug ativado.")
            self.thread_debug = threading.Thread(target=self.ModoDebug, daemon=True)
            self.thread_debug.start()

        mostrar_status()

    def IniciarCaça(self):
        print("Thread de caça rodando.")
        while AtivarThreadsDeCaça.is_set():
            # Aqui você chama a função de detecção de monstros
            if self.tela_monitor:
                self.tela_monitor.Verificar()
            time.sleep(0.5)
        print("Thread de caça finalizado.")

    def ModoDebug(self):
        print("Thread de debug rodando.")
        while AtivarDebug.is_set():
            if self.tela_monitor:
                self.tela_monitor.ModoDebug()
            time.sleep(0.5)
        print("Thread de debug finalizado.")

    def listen(self):
        print("Aguardando comandos (END para caça, HOME para debug)...")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Encerrando monitoramento de teclas.")
