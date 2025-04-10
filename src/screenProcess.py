from collections import deque
import os
import cv2
import numpy as np
import pygetwindow as gw
import pyautogui
import mss
import config.settings as set
import time
from math import sqrt
from keras.models import load_model
from src.controller import Controller
from src.inputs import AtivarThreadsDeCaça
from Utils.adjustProcess import AjustadorDeArea

CT = Controller()
# AA = AjustadorDeArea(f"{set.Mob}")


class VerificadorTela:
    def __init__(self):
        """Inicializa o VerificadorTela."""
        self.SqmsIgnorados = deque(maxlen=5)

        self.model = load_model(set.Model, compile=False)
        self.data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        CaminhoParaArquivoNomeMobs = os.path.join(
            os.path.dirname(__file__), "..", set.Mob
        )

        if not os.path.exists(CaminhoParaArquivoNomeMobs):
            raise FileNotFoundError(
                f"Arquivo {CaminhoParaArquivoNomeMobs} não encontrado."
            )

        with open(CaminhoParaArquivoNomeMobs, "r", encoding="utf-8") as file:
            self.classes = [line.strip().split(" ", 1)[1] for line in file]

        self.FrameAnterior = None
        self.threshold_diferenca = 5_000

    def CompararFrames(self, frame_atual):
        """ "Compara o frame atual com o anterior para verificar mudanças significativas."""
        if self.FrameAnterior is None:
            self.FrameAnterior = frame_atual
            return True

        FrameCinzaAnterior = cv2.resize(self.FrameAnterior, (0, 0), fx=0.3, fy=0.3)
        FrameCinzaAtual = cv2.resize(frame_atual, (0, 0), fx=0.3, fy=0.3)

        Diferenca = cv2.absdiff(FrameCinzaAnterior, FrameCinzaAtual)
        SomaDaDiferenca = np.sum(Diferenca)

        self.FrameAnterior = frame_atual

        return SomaDaDiferenca > self.threshold_diferenca

    def CapturarTela(self):
        """Captura apenas a área de interesse do jogo."""
        Largura = 1920
        Altura = 1080

        MargemHorizontal, MargemVertical = 350, 100

        Esquerda = MargemHorizontal
        Topo = MargemVertical
        Direita = Largura - (2 * MargemHorizontal)
        Baixo = Altura - (2 * MargemVertical)

        with mss.mss() as sct:
            monitor = {"top": Topo, "left": Esquerda, "width": Direita, "height": Baixo}
            captura = sct.grab(monitor)
            return (
                cv2.cvtColor(np.array(captura), cv2.COLOR_RGBA2BGR),
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

    def IgnorarPersonagemCentral(self, captura):
        """Define a área onde o personagem está localizado para ignorá-lo na detecção."""
        altura, largura, _ = captura.shape

        DivisaoHorizontal, DivisaoVertical = largura // 2, altura // 2

        Raio = 75

        return DivisaoHorizontal, DivisaoVertical, Raio

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

    def EncontrarContornosValidos(self, captura_preprocessada):
        Contornos, _ = cv2.findContours(
            captura_preprocessada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
        )
        ContornosValidos = [c for c in Contornos if 400 < cv2.contourArea(c) < 3000]
        return ContornosValidos

    def CalcularCentroDoPersonagem(self, captura):
        return (captura.shape[1] // 2, captura.shape[0] // 2)

    def ConfigurarCaptura(self):
        Captura, Esquerda, Topo, Direita, Baixo = self.CapturarTela()
        CapturaProcessada = self.PreProcessar(Captura)
        PersonagemX, PersonagemY = self.CalcularCentroDoPersonagem(Captura)
        ContornosValidos = self.EncontrarContornosValidos(CapturaProcessada)

        return (
            Captura,
            Esquerda,
            Topo,
            Direita,
            Baixo,
            PersonagemX,
            PersonagemY,
            ContornosValidos,
        )

    def ModoDebug(self):
        """Exibe visualmente os contornos dos mobs enquanto MODO DEBUG estiver ativo."""
        JanelaDeDebug = False

        while True:
            if set.Debug:
                (
                    Captura,
                    Esquerda,
                    Topo,
                    Direita,
                    Baixo,
                    PersonagemX,
                    PersonagemY,
                    ContonosValidos,
                ) = self.ConfigurarCaptura()

                DivisaoHorizontal, DivisaoVertical, Raio = (
                    self.IgnorarPersonagemCentral(Captura)
                )

                cv2.circle(
                    Captura,
                    (PersonagemX, PersonagemY),
                    Raio,
                    (43, 33, 33),
                    -1,
                )

                for Contorno in ContonosValidos:
                    ctn = cv2.contourArea(Contorno)
                    if not (290 < ctn < 8000):
                        continue

                    x, y, w, h, MobX, MobY, NomeDoMob, Paridade = (
                        self.DefinirCoordenadas(Captura, Contorno)
                    )

                    if Paridade < 0.8:
                        continue

                    if Esquerda <= x <= Direita and Topo <= y <= Baixo:
                        if (
                            sqrt(
                                (x - DivisaoHorizontal) ** 2
                                + (y - DivisaoVertical) ** 2
                            )
                            < Raio
                        ):
                            continue

                    Visivel = self.VerificarVisibilidadeDoAlvo(
                        Captura,
                        (PersonagemX, PersonagemY + 70),
                        (MobX, MobY + 30),
                    )

                    cor = (255, 0, 0) if Visivel else (0, 255, 0)

                    cv2.rectangle(Captura, (x, y), (x + w, y + h), cor, 2)
                    cv2.line(
                        Captura,
                        (PersonagemX, PersonagemY + 70),
                        (MobX, MobX + 30),
                        cor,
                        1,
                    )
                    cv2.putText(
                        Captura,
                        f"{NomeDoMob}: {Paridade*100:.2f}% AREA:{ctn:.2f}",
                        (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (255, 255, 255),
                        1,
                    )

                cv2.imshow("Pre-Visualizacao", Captura)
                JanelaDeDebug = True

                if cv2.waitKey(1) & 0xFF == 27:
                    set.Debug = False

            else:
                if JanelaDeDebug:
                    cv2.destroyAllWindows()
                    JanelaDeDebug = False

            time.sleep(0.1)

    def DefinirCoordenadas(self, captura, contorno):
        (x, y, w, h) = cv2.boundingRect(contorno)

        MobX, MobY = x + w // 2, y + h // 2

        SelecaoDeAlvo = captura[y : y + h, x : x + w]

        NomeDoMob, Paridade = self.VerificarCorrespondeciaDeMob(SelecaoDeAlvo)

        return x, y, w, h, MobX, MobY, NomeDoMob, Paridade

    def PodeAtacarCoordenada(self, x, y, tolerancia=40, tempo_limite=5.0):
        Agora = time.perf_counter()
        NovasCoordenadas = []

        for cx, cy, t in self.SqmsIgnorados:
            if (cx, cy) == self.CentroDaTela:
                NovasCoordenadas.append((cx, cy, t))
                continue
            if Agora - t < tempo_limite:
                NovasCoordenadas.append((cx, cy, t))
                if abs(cx - x) < tolerancia and abs(cy - y) < tolerancia:
                    return False

        self.SqmsIgnorados = NovasCoordenadas
        self.SqmsIgnorados.append((x, y, Agora))
        print(
            f"[INFO] Coordenada ({x}, {y}) registrada. Total: {len(self.SqmsIgnorados)}"
        )
        return True

    def ReprocessarTela(verificador):
        Inicio = time.time()
        MobEncontrado = False

        while time.time() - Inicio < 0.5:
            Captura, *_ = verificador.ConfigurarCaptura()

            if verificador.CompararFrames(Captura):
                Contornos = verificador.EncontrarContornosValidos(
                    verificador.PreProcessar(Captura)
                )

                for Contorno in Contornos:
                    x, y, w, h, _, _, Nome, Paridade = verificador.DefinirCoordenadas(
                        Captura, Contorno
                    )

                    if Nome.lower() == "vento da colina" and Paridade > 0.85:
                        MobEncontrado = True
                        break

            if MobEncontrado:
                return False

        if hasattr(verificador, "CentroDaTela"):
            verificador.SqmsIgnorados = [
                verificador.CentroDaTela + (time.perf_counter(),)
            ]
        else:
            verificador.SqmsIgnorados = []

        CT.AsaDeMosca()
        return True

    def Verificar(self):
        while AtivarThreadsDeCaça.is_set():
            (
                Captura,
                Esquerda,
                Topo,
                _,
                _,
                PersonagemX,
                PersonagemY,
                ContornosValidos,
            ) = self.ConfigurarCaptura()

            self.CentroDaTela = (PersonagemX, PersonagemY)
            Inicio = time.perf_counter()

            MobProcessado = False
            SemAlvos = True

            for Contorno in ContornosValidos:
                area = cv2.contourArea(Contorno)
                if not (600 < area < 3000):
                    continue

                x, y, w, h, MobX, MobY, NomeDoMob, Paridade = self.DefinirCoordenadas(
                    Captura, Contorno
                )

                MobProcessado = True

                distancia = (
                    (MobX - PersonagemX) ** 2 + (MobY - (PersonagemY + 20)) ** 2
                ) ** 0.5
                if distancia < 50:
                    continue

                if not self.PodeAtacarCoordenada(MobX, MobY):
                    continue

                if (
                    NomeDoMob == "Vento da Colina"
                    and Paridade > 0.85
                    and not self.VerificarVisibilidadeDoAlvo(
                        Captura,
                        (PersonagemX, PersonagemY + 70),
                        (MobX, MobY + 30),
                    )
                ):
                    CT.MoverParaAlvo(MobX + Esquerda, MobY + Topo)
                    CT.RajadaDeFlechas()

                    CT.Atacar()
                    self.SqmsIgnorados.append((MobX, MobY, Inicio))
                    self.ReprocessarTela()
                    return

                if self.VerificarVisibilidadeDoAlvo(
                    Captura,
                    (PersonagemX, PersonagemY + 70),
                    (MobX, MobY + 30),
                ):
                    SemAlvos = False
                    CT.MoverParaAlvo(MobX + Esquerda, MobY + Topo)
                    CT.RajadaDeFlechas()
                    time.sleep(0.1)
                    CT.Atacar()
                    self.SqmsIgnorados.append((MobX, MobY, Inicio))
                    break

            if MobProcessado and SemAlvos:
                CT.AsaDeMosca()
                return

            time.sleep(0.01)
