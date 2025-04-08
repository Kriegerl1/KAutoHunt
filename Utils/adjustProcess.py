import json
import os
from collections import defaultdict
import statistics


class AjustadorDeArea:
    def __init__(self, nome_mapa):
        self.arquivo = f"{nome_mapa} - adjust_raw.json"
        self.dados = defaultdict(list)

        if os.path.exists(self.arquivo):
            with open(self.arquivo, "r") as f:
                try:
                    carregado = json.load(f)
                    for nome, lista in carregado.items():
                        self.dados[nome] = list(lista)
                except Exception:
                    pass


    def CapturarAreaDoMob(self, nome_mob, area):
        areas = self.dados[nome_mob]
        
        if len(areas) >= 5:  # só aplica a checagem se já tem dados suficientes
            media = sum(areas) / len(areas)
            desvio_max = media * 0.5  # permite variação de 50% pra mais ou menos

            if not (media - desvio_max <= area <= media + desvio_max):
                print(f"[DESCARTADO] Área {area} fora do intervalo esperado para {nome_mob} (média: {media})")
                return  # ignora essa leitura

        self.dados[nome_mob].append(area)
        print(f"[ACEITO] Área {area} registrada para {nome_mob}")


    def Salvar(self):
        # Salva as listas brutas
        with open(self.arquivo, "w") as f:
            json.dump(self.dados, f, indent=4)

        # Gera arquivo de médias separado
        medias = {
            nome: round(sum(areas) / len(areas), 2)
            for nome, areas in self.dados.items()
            if areas
        }
        with open(self.arquivo.replace("_raw.json", "_medias.json"), "w") as f:
            json.dump(medias, f, indent=4)

    def CalcularMediaArea(self, nome_mob):
        try:
            areas = self.dados.get(nome_mob, [])
            if not areas:
                return None
            return round(sum(areas) / len(areas), 2)
        except Exception:
            return None
