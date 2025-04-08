import time
import ctypes
import keyboard
import pyautogui
from config.settings import server

MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_WHEEL = 0x0800


class Controller:
    def ClickEsquerdo(self):
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(0.01)
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    def ClickDireito(self):
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
        time.sleep(0.01)
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)

    def ScrollCima(self, quantidade=120):
        """Rola o scroll do mouse para cima (quantidade padrão = 120)"""
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_WHEEL, 0, 0, quantidade, 0)
        time.sleep(0.01)

    def ScrollBaixo(self, quantidade=120):
        """Rola o scroll do mouse para baixo (quantidade padrão = 120)"""
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_WHEEL, 0, 0, -quantidade, 0)
        time.sleep(0.01)

    def RajadaDeFlechas(self):
        keyboard.send("f1")

    def AsaDeMosca(self):
        print("Teleportando...")
        keyboard.send("f3")

    def MoverParaAlvo(self, x, y):
        pyautogui.moveTo(x, y)
        self.RajadaDeFlechas()
        self.ClickEsquerdo()
        time.sleep(0.01)

    def AjusteInicial(self):
        """Executa o ajuste inicial de câmera e zoom no jogo."""

        def UsarTecla(tecla):
            keyboard.press(tecla)
            self.ClickDireito()
            self.ClickDireito()
            time.sleep(0.01)
            self.ClickDireito()
            self.ClickDireito()
            keyboard.release(tecla)
            time.sleep(0.1)

        UsarTecla("alt")
        UsarTecla("ctrl")

        for _ in range(20):
            self.ScrollCima()

        time.sleep(0.1)
