import cv2
import numpy as np
import pygetwindow as gw
import pyautogui
import mss
import config.settings as set
import time
from src.Controller import MoverParaAlvo, AsaDeMosca, GuardarItems
from keras.models import load_model
from math import sqrt


class VerificadorTela:
    def __init__(self, model_path="keras_model.h5", classes_file="mob.txt"):
        self.model = load_model(model_path, compile=False)
        self.data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        self.mobs_fixos = {}  # Dicionário de mobs fixados

        with open(classes_file, "r", encoding="utf-8") as file:
            self.classes = [line.strip().split(" ", 1)[1] for line in file]

        self.frame_anterior = None
        self.threshold_diferenca = 10_000

    def CompararFrames(self, frame_atual):
        if self.frame_anterior is None:
            self.frame_anterior = frame_atual
            return True

        # cinza_anterior = cv2.cvtColor(self.frame_anterior, cv2.COLOR_BGRA2GRAY)
        # cinza_atual = cv2.cvtColor(frame_atual, cv2.COLOR_BGRA2GRAY)

        cinza_anterior = cv2.resize(self.frame_anterior, (0, 0), fx=0.7, fy=0.7)
        cinza_atual = cv2.resize(frame_atual, (0, 0), fx=0.7, fy=0.7)

        diferenca = cv2.absdiff(cinza_anterior, cinza_atual)
        soma_diferenca = np.sum(diferenca)

        self.frame_anterior = frame_atual

        return soma_diferenca > self.threshold_diferenca

    def CapturarTela(self):
        """Captura apenas a área de interesse do jogo."""
        Largura = 1920
        Altura = 1080

        MargemHorizontal, MargemVertical = 190, 60

        Esquerda = MargemHorizontal
        Topo = MargemVertical
        Direita = Largura - (2 * MargemHorizontal)
        Baixo = Altura - (2 * MargemVertical)

        with mss.mss() as sct:
            monitor = {"top": Topo, "left": Esquerda, "width": Direita, "height": Baixo}
            captura = sct.grab(monitor)
            return (
                cv2.cvtColor(np.array(captura), cv2.COLOR_RGB2BGR),
                Esquerda,
                Topo,
                Direita,
                Baixo,
            )

    def PreProcessar(self, captura):
        """Aplica filtros para realçar os contornos dos mobs."""

        captura = cv2.GaussianBlur(captura, (3, 3), 0)

        captura = cv2.Canny(captura, threshold1=50, threshold2=150)

        kernel = np.ones((2, 2), np.uint8)

        captura = cv2.dilate(captura, kernel, iterations=1)

        captura = cv2.erode(captura, kernel, iterations=1)

        return captura

    def detectar_area_util(self, captura):
        """Define a área útil para detecção de mobs."""

        altura, largura, _ = captura.shape

        MargemHorizontal, MargemVertical = 150, 80  # Ajuste conforme necessário
        return (
            MargemHorizontal,
            MargemVertical,
            largura - MargemHorizontal,
            altura - MargemVertical,
        )

    def IgnorarPersonagemCentral(self, captura):
        """Define a área onde o personagem está localizado para ignorá-lo na detecção."""
        altura, largura, _ = captura.shape

        DivisaoHorizontal, DivisaoVertical = largura // 2, altura // 2

        Raio = 75

        return DivisaoHorizontal, DivisaoVertical, Raio

    def IgnorarPonteiroMouse(self, captura):
        """Ignora o cursor do mouse na detecção."""
        mouse_x, mouse_y = pyautogui.position()
        # Definição do ponteiro em formato de triângulo
        tamanho = 29  # Tamanho do ponteiro
        ponteiro = np.array(
            [
                [
                    (mouse_x, mouse_y),
                    (mouse_x + tamanho, mouse_y + tamanho // 2),
                    (mouse_x, mouse_y + tamanho),
                ]
            ],
            dtype=np.int32,
        )

        # Desenha o contorno e preenche o ponteiro
        cv2.polylines(
            captura, [ponteiro], isClosed=True, color=(43, 33, 33), thickness=2
        )
        cv2.fillPoly(captura, [ponteiro], color=(43, 33, 33))
        return captura

    def VerificarCorrespondeciaDeMob(self, sprite):
        """Classifica o mob detectado usando o modelo treinado."""
        sprite = cv2.resize(sprite, (224, 224)).astype(np.float32) / 255.0

        self.data[0] = sprite

        prediction = self.model.predict(self.data, verbose=0)

        index = np.argmax(prediction)

        return self.classes[index], prediction[0][index]

    def DefinirParede(self, region):
        """Verifica se a região é uma parede, analisando a média de cores."""
        return np.all(np.mean(region, axis=(0, 1)) < [30, 30, 30])

    def VerificarVisibilidadeDoAlvo(
        self, Captura, PontoInicial, PontoFinal, TamanhoAreaVerificacao=10
    ):
        """Verifica se há parede entre dois pontos."""

        # Move o PontoInicial 15 pixels para baixo
        PontoInicial = (PontoInicial[0], PontoInicial[1])

        # Cria 50 pontos entre PontoInicial e PontoFinal
        PontosEntreOsPontos = np.linspace(
            PontoInicial, PontoFinal, num=30, dtype=np.int32
        )

        for X, Y in PontosEntreOsPontos:
            if 0 <= X < Captura.shape[1] and 0 <= Y < Captura.shape[0]:
                AreaParaVerificacao = Captura[
                    max(0, Y - TamanhoAreaVerificacao) : Y + TamanhoAreaVerificacao,
                    max(0, X - TamanhoAreaVerificacao) : X + TamanhoAreaVerificacao,
                ]
                if self.DefinirParede(AreaParaVerificacao):
                    return True  # Obstáculo encontrado

        return False  # Nenhum obstáculo encontrado

    def gerenciar_mobs_fixos(
        self,
        mob_id,
        confianca,
        EsquerdaDaSelecao,
        TopoDaSelecao,
        DireitaDaSelecao,
        BaixoDaSelecao,
        personagem,
        captura,
    ):
        """Gerencia os mobs fixos, adicionando ou removendo conforme necessário."""
        limite_movimento = 50
        if mob_id in self.mobs_fixos:
            self.mobs_fixos[mob_id]["posicao"] = (
                EsquerdaDaSelecao,
                TopoDaSelecao,
                DireitaDaSelecao,
                BaixoDaSelecao,
            )
            self.mobs_fixos[mob_id]["linha_visivel"] = (
                not self.VerificarVisibilidadeDoAlvo(
                    captura,
                    personagem,
                    (
                        EsquerdaDaSelecao + DireitaDaSelecao // 2,
                        TopoDaSelecao + BaixoDaSelecao // 2,
                    ),
                )
            )
        elif confianca >= 0.91:
            for fixo_id, fixo_data in self.mobs_fixos.items():
                fx, fy, _, _ = fixo_data["posicao"]
                if (
                    sqrt((EsquerdaDaSelecao - fx) ** 2 + (TopoDaSelecao - fy) ** 2)
                    < limite_movimento
                ):
                    return
            self.mobs_fixos[mob_id] = {
                "Paridade": confianca,
                "posicao": (
                    EsquerdaDaSelecao,
                    TopoDaSelecao,
                    DireitaDaSelecao,
                    BaixoDaSelecao,
                ),
                "linha_visivel": True,
            }
        elif (
            confianca < 0.30
            and mob_id in self.mobs_fixos
            and not self.mobs_fixos[mob_id]["linha_visivel"]
        ):
            del self.mobs_fixos[mob_id]

    def EncontrarContornosValidos(self, captura_preprocessada):
        contours, _ = cv2.findContours(
            captura_preprocessada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
        )
        contornos_validos = [c for c in contours if 400 < cv2.contourArea(c) < 3000]
        return contornos_validos

    def CalcularCentroDoPersonagem(self, captura):
        return (captura.shape[1] // 2, captura.shape[0] // 2)

    def ModoDebug(self):
        """Exibe visualmente os contornos dos mobs enquanto MODO DEBUG estiver ativo."""
        janela_aberta = False

        while True:
            if set.Debug:
                captura, Esquerda, Topo, Direita, Baixo = self.CapturarTela()
                captura_preprocessada = self.PreProcessar(captura)
                PersonagemX, PersonagemY = self.CalcularCentroDoPersonagem(captura)
                contornos_validos = self.EncontrarContornosValidos(
                    captura_preprocessada
                )
                DivisaoHorizontal, DivisaoVertical, Raio = (
                    self.IgnorarPersonagemCentral(captura)
                )

                for contorno in contornos_validos:
                    (x, y, w, h) = cv2.boundingRect(contorno)
                    centro_x, centro_y = x + w // 2, y + h // 2

                    SelecaoDeAlvo = captura[y : y + h, x : x + w]

                    NomeDoMob, Paridade = self.VerificarCorrespondeciaDeMob(
                        SelecaoDeAlvo
                    )
                    if Paridade > 0.7:
                        if Esquerda <= x <= Direita and Topo <= y <= Baixo:
                            if (
                                sqrt(
                                    (x - DivisaoHorizontal) ** 2
                                    + (y - DivisaoVertical) ** 2
                                )
                                < Raio
                            ):
                                continue

                        visivel = self.VerificarVisibilidadeDoAlvo(
                            captura, (PersonagemX, PersonagemY), (centro_x, centro_y)
                        )

                        cor = (255, 255, 255) if visivel else (0, 255, 0)

                        cv2.rectangle(captura, (x, y), (x + w, y + h), cor, 2)
                        cv2.line(
                            captura,
                            (PersonagemX, PersonagemY + 40),
                            (centro_x, centro_y - 10),
                            cor,
                            1,
                        )
                        cv2.putText(
                            captura,
                            f"{NomeDoMob}: {Paridade*100:.2f}%",
                            (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8,
                            (255, 255, 255),
                            1,
                        )

                cv2.imshow("Pre-Visualizacao", captura)

            janela_aberta = True

            if cv2.waitKey(1) & 0xFF == 27:
                set.Debug = False
        else:
            if janela_aberta:
                cv2.destroyAllWindows()
                janela_aberta = False
            time.sleep(0.1)

    def Verificar(self):
        """Loop principal do bot."""
        while True:
            captura, Esquerda, Topo, Direita, Baixo = self.CapturarTela()

            captura_preprocessada = self.PreProcessar(captura)

            PersonagemX, PersonagemY = self.CalcularCentroDoPersonagem(captura)

            if not self.CompararFrames(captura):
                continue

            DivisaoHorizontal, DivisaoVertical, Raio = self.IgnorarPersonagemCentral(
                captura
            )
            contornos_validos = self.EncontrarContornosValidos(captura_preprocessada)
            if set.ProcurandoAlvo:

                for contorno in contornos_validos:
                    if 600 < cv2.contourArea(contorno) < 16000:

                        MobEncontrado = False

                        x, y, w, h = cv2.boundingRect(contorno)

                        centro_x, centro_y = x + w // 2, y + h // 2

                        SelecaoDeAlvo = captura[y : y + h, x : x + w]

                        NomeDoMob, Paridade = self.VerificarCorrespondeciaDeMob(
                            SelecaoDeAlvo
                        )

                        if (
                            Paridade > 0.9
                            and NomeDoMob == "Les"
                            and not self.VerificarVisibilidadeDoAlvo(
                                captura,
                                (PersonagemX, PersonagemY),
                                (centro_x, centro_y),
                            )
                        ):
                            MoverParaAlvo(centro_x + Esquerda, centro_y + Topo)