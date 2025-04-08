from PIL import Image
import os

TAMANHO_FINAL = 244
COR_DE_FUNDO = (255, 0, 0)  # preto


def redimensionar_e_preencher(imagem: Image.Image) -> Image.Image:
    # Calcula novo tamanho proporcional com o lado maior = 244
    original_width, original_height = imagem.size
    if original_width > original_height:
        nova_largura = TAMANHO_FINAL
        nova_altura = int((TAMANHO_FINAL / original_width) * original_height)
    else:
        nova_altura = TAMANHO_FINAL
        nova_largura = int((TAMANHO_FINAL / original_height) * original_width)

    imagem = imagem.resize((nova_largura, nova_altura), Image.Resampling.LANCZOS)

    # Cria nova imagem quadrada e centraliza a redimensionada
    nova_imagem = Image.new("RGB", (TAMANHO_FINAL, TAMANHO_FINAL), COR_DE_FUNDO)
    pos_x = (TAMANHO_FINAL - nova_largura) // 2
    pos_y = (TAMANHO_FINAL - nova_altura) // 2
    nova_imagem.paste(imagem, (pos_x, pos_y))

    return nova_imagem


for arquivo in os.listdir("."):
    if arquivo.lower().endswith(".bmp"):
        try:
            print(f"Processando: {arquivo}")
            imagem = Image.open(arquivo)

            # Redimensiona proporcionalmente com preenchimento
            imagem_redimensionada = redimensionar_e_preencher(imagem)

            nome_base = os.path.splitext(arquivo)[0]
            redimensionado_nome = f"{nome_base}_244.bmp"
            imagem_redimensionada.save(redimensionado_nome)

            # Espelho a imagem redimensionada
            espelho = imagem_redimensionada.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            espelho_nome = f"{nome_base}_244_espelho.bmp"
            espelho.save(espelho_nome)

        except Exception as e:
            print(f"Erro ao processar {arquivo}: {e}")
