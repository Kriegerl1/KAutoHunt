import config.settings as set
from src.inputs import Inputs
from src.screenProcess import VerificadorTela

def iniciar_programa():
    print("Iniciando KAutoHunt...")

    inputs = Inputs()
    tela = VerificadorTela()

    inputs.set_monitor(tela)

    inputs.listen()

if __name__ == "__main__":
    iniciar_programa()
