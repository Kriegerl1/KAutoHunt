import pygetwindow as gw
import pyautogui
import threading
import keyboard
import time
import os
import cv2
import numpy as np
from PIL import ImageGrab

print("Abra o 4r e defina a tecla de inicio para 'END'...(Pressione Enter para continuar)")

# Aguarda o pressionamento da tecla Enter para continuar
keyboard.wait("Enter")

# Dicionário de imagens
Dicionario_Mobs = {
    "Les": [
        r"C:\Users\himat.DESKTOP-HKHTJQB\source\repos\Python\Aimbot python\Mobs\Les\LesFrente.bmp",
        r"C:\Users\himat.DESKTOP-HKHTJQB\source\repos\Python\Aimbot python\Mobs\Les\LesCosta.bmp",
    ]
}

# Sprite de morte
Dicionario_Mobs_morte = {
    "Les": [
        r"C:\Users\himat.DESKTOP-HKHTJQB\source\repos\Python\Aimbot python\Mobs\Les\LesMorte.bmp",
    ]
}

# Filtra apenas imagens que realmente existem
Dicionario_Mobs = {
    nome_mob: [img for img in mob_imgs if os.path.exists(img)]
    for nome_mob, mob_imgs in Dicionario_Mobs.items()
}

# Verifica se há imagens válidas
if not Dicionario_Mobs:
    print("Nenhuma imagem válida foi encontrada. Verifique os caminhos dos arquivos.")
    exit()
else:
    print("Imagens carregadas com sucesso.")

caçando = False  # Estado da caça
hora = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def espelhar_imagem(img_path):
    """ Gera uma versão espelhada da imagem e a salva temporariamente. """
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)  # Lê a imagem sem alterar transparência
    img_espelhada = cv2.flip(img, 1)  # Espelha a imagem horizontalmente

    # Salva temporariamente para ser usada pelo PyAutoGUI
    caminho_espelhado = img_path.replace(".bmp", "_espelhado.bmp")
    cv2.imwrite(caminho_espelhado, img_espelhada)
    return caminho_espelhado  # Retorna o caminho da imagem espelhada


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
                            # Tenta encontrar a imagem original
                            localizacao = pyautogui.locateOnScreen(img, confidence=0.6)
                        except pyautogui.ImageNotFoundException:
                            localizacao = None  # Se der erro, simplesmente ignora

                        if not localizacao:
                            try:
                                localizacao = pyautogui.locateOnScreen(img_espelhada, confidence=0.6)
                            except pyautogui.ImageNotFoundException:
                                localizacao = None  # Se não achar a espelhada, ignora

                        # Se encontrou o mob, processa a mira
                        if localizacao:
                            x_mira, y_mira = pyautogui.center(localizacao)
                            # Move o mouse até o mob
                            pyautogui.moveTo(x_mira, y_mira)
                            centralizar_mouse()
                            Mob_Encontrado = True
                            break  # Para a busca quando encontrar um mob

                        if Mob_Encontrado:
                            print(f"Mob: {nome_mob} encontrado em X={x_mira}, Y={y_mira} | {hora}")
                            break

            except Exception as e:
                print(f"Erro inesperado: {e}")

            time.sleep(0.05)  # Pequena pausa para evitar consumo excessivo de CPU



def centralizar_mouse():
    """ Centraliza o mouse na tela """
    largura_tela, altura_tela = pyautogui.size()
    pyautogui.moveTo(largura_tela / 2, altura_tela / 2, duration=0.1)


def monitorar_teclas():
    """ Função para ativar/desativar a caça ao pressionar 'END' """
    global caçando
    print("Pressione 'END' para iniciar o AimBot 2.0...")
    while True:
        keyboard.wait("end")
        caçando = not caçando
        print("Caça ativada!" if caçando else "Caça desativada!")
        time.sleep(0.1)  # Pequena pausa para evitar múltiplos acionamentos


def iniciar_programa():
    """ Inicia as threads do programa """
    threading.Thread(target=monitorar_tela, daemon=True).start()
    threading.Thread(target=monitorar_teclas, daemon=True).start()

    while True:
        time.sleep(1)


if __name__ == "__main__":
    iniciar_programa()
