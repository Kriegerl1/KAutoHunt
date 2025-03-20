import keyboard
import time
from PIL import Image
import threading
import os
import pygetwindow as gw
import win32api
import win32con
import pyautogui  # Certifique-se de que o pyautogui está importado corretamente

print("Pressione 'F4' para testar...")

# Aguarda a primeira pressão da tecla F4 para continuar
keyboard.wait("f4")
print("Tecla 'F4' detectada!")

# Definição das cores do padrão quadriculado
cor1 = (255, 255, 255)  # Branco
cor2 = (204, 204, 204)  # Cinza claro

# Tamanho do bloco quadriculado
TAMANHO_PADRAO = 8

# Lista de imagens para buscar (verifica se os arquivos existem)
imagens = [
    r"C:\Users\himat.DESKTOP-HKHTJQB\source\repos\Aimbot python\lesFrente2.png",
    r"C:\Users\himat.DESKTOP-HKHTJQB\source\repos\Aimbot python\lesCostas2.png"
]

# Filtra apenas imagens existentes
imagens = [img for img in imagens if os.path.exists(img)]
if not imagens:
    print("Nenhuma imagem encontrada. Verifique os caminhos dos arquivos.")
    exit()

# Verifica se um bloco segue o padrão quadriculado
def is_quadriculado(pixels, x, y, largura, altura):
    for i in range(TAMANHO_PADRAO):
        for j in range(TAMANHO_PADRAO):
            if (x + i) >= largura or (y + j) >= altura:
                return False  # Sai dos limites da imagem
            
            cor_pixel = pixels[x + i, y + j]
            if cor_pixel != cor1 and cor_pixel != cor2:
                return False  # Se houver uma cor diferente, não é um padrão quadriculado
    return True

caçando = False  # Estado da caça

# Função para capturar e processar a tela
def monitorar_tela():
    global caçando

    while True:
        if caçando:
            try:
                # Encontra a janela "LegionBR | Gepard Shield 3.0"
                janela = gw.getWindowsWithTitle("LegionBR | Gepard Shield 3.0")
                if janela:
                    janela = janela[0]
                    janela.activate()  # Ativa a janela
                    janela.restore()  # Restaura a janela se estiver minimizada

                # Captura a tela inteira
                screenshot = pyautogui.screenshot()  # Captura usando pyautogui
                screenshot = screenshot.convert("RGB")  # Garante formato RGB

                # Obtém os pixels da tela
                pixels = screenshot.load()
                largura, altura = screenshot.size

                # Processa a imagem para remover o padrão quadriculado de toda a tela
                for i in range(0, largura, TAMANHO_PADRAO):  
                    for j in range(0, altura, TAMANHO_PADRAO):
                        if is_quadriculado(pixels, i, j, largura, altura):
                            for a in range(TAMANHO_PADRAO):
                                for b in range(TAMANHO_PADRAO):
                                    if (i + a) < largura and (j + b) < altura:
                                        pixels[i + a, j + b] = (33, 33, 43)  # Cor neutra

                # Salva a imagem para depuração (opcional)
                screenshot.save("modified_screenshot.png")

                # Busca apenas um sprite por vez
                sprite_encontrada = None
                for img in imagens:
                    localizacao = pyautogui.locateOnScreen(img, confidence=0.5)  # Localiza sprite usando pyautogui
                    if localizacao:
                        sprite_encontrada = (img, localizacao)
                        break  # Sai do loop assim que encontrar um sprite

            except Exception as e:
                print(f"Erro: {e}")
                sprite_encontrada = None

            if sprite_encontrada:
                img, Mira = sprite_encontrada
                x_mira, y_mira = pyautogui.center(Mira)  # Obtém o centro do sprite

                print(f"Sprite encontrada: {img} - Coordenadas: X={x_mira}, Y={y_mira}")

                # Substituindo o pyautogui.moveTo com win32api
                mover_mouse(x_mira, y_mira)  # Mover o mouse usando win32api
            else:
                print("Nenhuma sprite encontrada.")

            time.sleep(0.1)  # Pausa para evitar processamento excessivo

def coordenadas_validas(x, y):
    # Obtém a largura e altura da tela
    largura_tela, altura_tela = pyautogui.size()
    
    # Verifica se as coordenadas estão dentro dos limites da tela
    return 0 <= x <= largura_tela and 0 <= y <= altura_tela

def mover_mouse(x, y):
    if coordenadas_validas(x, y):  # Verifica se as coordenadas são válidas
        win32api.SetCursorPos((x, y))  # Mover o mouse usando win32api
    else:
        print(f"Coordenadas inválidas: X={x}, Y={y}. O mouse não será movido.")

def click_mouse():
    # Clique do mouse (botão esquerdo)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

# Função para escutar a tecla 'F4' para ativar/desativar a caça
def monitorar_teclas():
    global caçando

    print("Monitorando teclas...")

    while True:
        keyboard.wait("f4")  # Aguarda até F4 ser pressionado
        caçando = not caçando
        print("Caça ativada!" if caçando else "Caça desativada!")
        time.sleep(0.5)  # Evita ativações múltiplas seguidas

# Criando threads para rodar as funções simultaneamente
def iniciar_programa():
    # Criação de uma thread para monitorar a captura de tela
    monitorar_thread = threading.Thread(target=monitorar_tela, daemon=True)
    monitorar_thread.start()

    # Criação de uma thread para monitorar as teclas
    monitorar_teclas_thread = threading.Thread(target=monitorar_teclas, daemon=True)
    monitorar_teclas_thread.start()

    # Mantém o programa em execução
    while True:
        time.sleep(1)

if __name__ == "__main__":
    iniciar_programa()
