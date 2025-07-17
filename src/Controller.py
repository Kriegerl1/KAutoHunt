import time
import ctypes
import keyboard


""""Constantes para eventos de mouse e teclado."""
M_LEFTDOWN = 0x0002
M_LEFTUP = 0x0004
M_RIGHTDOWN = 0x0008
M_RIGHTUP = 0x0010
M_WHEEL = 0x0800

"""Fim das constantes."""
TECLAS = {
    "F1": {"vk": 0x70, "vscan": 0x3B},
    "F2": {"vk": 0x71, "vscan": 0x3C},
    "F3": {"vk": 0x72, "vscan": 0x3D},
    "F4": {"vk": 0x73, "vscan": 0x3E},
    "F5": {"vk": 0x74, "vscan": 0x3F},
    "F6": {"vk": 0x75, "vscan": 0x40},
    "F7": {"vk": 0x76, "vscan": 0x41},
    "F8": {"vk": 0x77, "vscan": 0x42},
    "F9": {"vk": 0x78, "vscan": 0x43},
    "ALT": {"vk": 0x12, "vscan": 0x38},
    "CTRL": {"vk": 0x11, "vscan": 0x1D},
    "SHIFT": {"vk": 0x10, "vscan": 0x2A},
}


class Controller:

    def RajadaDeFlechas(self):
        print("Usando Rajada de flechas...")
        KeyboardEvents.PrecionarTecla("F1")
        time.sleep(0.1)

    def AsaDeMosca(self):
        print("Teleportando...")
        KeyboardEvents.PrecionarTecla("F3")
        time.sleep(0.1)

    def MoverParaAlvo(self, x, y):
        MouseEvents.MoverMouse(x, y)
        time.sleep(0.01)

    def Atacar(self):
        MouseEvents.ClickEsquerdo()
        time.sleep(0.01)

    def AjusteInicial(self):
        """Executa o ajuste inicial de câmera e zoom no jogo."""

        def CombinarTeclas(tecla):
            keyboard.press(tecla)
            MouseEvents.ClickDireito()
            MouseEvents.ClickDireito()
            time.sleep(0.01)
            MouseEvents.ClickDireito()
            MouseEvents.ClickDireito()
            keyboard.release(tecla)
            time.sleep(0.1)

        CombinarTeclas("alt")
        CombinarTeclas("ctrl")

        for _ in range(20):
            MouseEvents.ScrollCima()

        time.sleep(0.1)


class MouseEvents:
    @staticmethod
    def ClickEsquerdo():
        ctypes.windll.user32.mouse_event(M_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(0.01)
        ctypes.windll.user32.mouse_event(M_LEFTUP, 0, 0, 0, 0)

    @staticmethod
    def ClickDireito():
        ctypes.windll.user32.mouse_event(M_RIGHTDOWN, 0, 0, 0, 0)
        time.sleep(0.01)
        ctypes.windll.user32.mouse_event(M_RIGHTUP, 0, 0, 0, 0)

    @staticmethod
    def ScrollCima(quantidade=120):
        """Rola o scroll do mouse para cima (quantidade padrão = 120)"""
        ctypes.windll.user32.mouse_event(M_WHEEL, 0, 0, quantidade, 0)
        time.sleep(0.01)

    @staticmethod
    def ScrollBaixo(quantidade=120):
        """Rola o scroll do mouse para baixo (quantidade padrão = 120)"""
        ctypes.windll.user32.mouse_event(M_WHEEL, 0, 0, -quantidade, 0)
        time.sleep(0.01)

    @staticmethod
    def MoverMouse(x, y):
        """Move o mouse para a posição (x, y)"""
        ctypes.windll.user32.SetCursorPos(x, y)
        time.sleep(0.01)


class KeyboardEvents:

    @staticmethod
    def PrecionarTecla(tecla):
        """Pressiona uma tecla específica"""
        tecla = TECLAS[tecla.upper()]
        vk = tecla["vk"]
        vscan = tecla["vscan"]

        ctypes.windll.user32.keybd_event(vk, vscan, 0, 0)
        time.sleep(0.01)
        ctypes.windll.user32.keybd_event(vk, vscan, 2, 0)
