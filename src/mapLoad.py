import os
import zipfile


class MapLoader:
    @staticmethod
    def CarregarMapa(nome_zip):
        nome_base = os.path.splitext(nome_zip)[0]

        zip_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "assets", "Zimap", nome_zip)
        )

        destino = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "assets", "Maps")
        )
        os.makedirs(destino, exist_ok=True)

        Model = os.path.join(destino, f"{nome_base}.h5")
        Nome = os.path.join(destino, f"{nome_base}.txt")

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            with zip_ref.open("keras_model.h5") as model_file:
                with open(Model, "wb") as f_out:
                    f_out.write(model_file.read())

            with zip_ref.open("labels.txt") as txt_file:
                with open(Nome, "wb") as f_out:
                    f_out.write(txt_file.read())

        return Model, Nome
