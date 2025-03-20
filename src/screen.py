import pygetwindow as gw
import pyautogui
import time
import numpy as np
import cv2
from PIL import ImageGrab
from control import centralizar_mouse, espelhar_imagem
from utils import carregar_imagens

Dicionario_Mobs = carregar_imagens()
caçando = False  # Estado da caça

def monitorar_tela():
    global caçando

    while True:
        if caçando:
            try:
                # Ativa a janela do jogo
                janela = gw.getWindowsWithTitle("LegionBR | Gepard Shield 3.0")
                if janela:
                    janela = janela[0]
                    janela.activate()
                    janela.restore()

                # Captura a tela
                screenshot = ImageGrab.grab()
                tela = np.array(screenshot)

                Mob_Encontrado = None

                # Itera por todos os mobs e suas imagens
                for nome_mob, imagens in Dicionario_Mobs.items():
                    for img in imagens:
                        img_espelhada = espelhar_imagem(img)  # Gera a versão espelhada

                        try:
                            localizacao = pyautogui.locateOnScreen(img, confidence=0.6)
                        except pyautogui.ImageNotFoundException:
                            localizacao = None

                        if not localizacao:
                            try:
                                localizacao = pyautogui.locateOnScreen(img_espelhada, confidence=0.6)
                            except pyautogui.ImageNotFoundException:
                                localizacao = None

                        # Se encontrou o mob, processa a mira
                        if localizacao:
                            x_mira, y_mira = pyautogui.center(localizacao)
                            pyautogui.moveTo(x_mira, y_mira)
                            centralizar_mouse()
                            Mob_Encontrado = True
                            print(f"Mob: {nome_mob} encontrado em X={x_mira}, Y={y_mira}")
                            break

            except Exception as e:
                print(f"Erro inesperado: {e}")

            time.sleep(0.05)  # Pequena pausa para evitar consumo excessivo de CPU
