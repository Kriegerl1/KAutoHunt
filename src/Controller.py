import pyautogui
import ctypes
import keyboard
import time
from config.settings import server

MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004


def Click():
    """Realiza um clique esquerdo do mouse na posição atual (aceito pelo Ragnarok)."""
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.01)
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def RajadaDeFlechas():
    """Ataca o mob clicando na posição atual do mouse."""
    keyboard.send("f1")


def AsaDeMosca():
    print("Teleportando...")
    keyboard.send("f3")
    LimparTentativasAntigas()


def MoverParaAlvo(x, y):
    pyautogui.moveTo(x, y)
    RajadaDeFlechas()
