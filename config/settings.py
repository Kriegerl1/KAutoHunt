import threading
import clr
import sys
import os

settings = None


class Settings:
    def CarregarCaminhos(self, model=None, arquivoDeMobs=None, mobsAlvo=None):
        if model is None:
            model = r"C:\Users\Leo_Rodrigues\source\repos\Python\KAutoHunt\assets\Maps\default.h5"
        if arquivoDeMobs is None:
            arquivoDeMobs = r"C:\Users\Leo_Rodrigues\source\repos\Python\KAutoHunt\assets\Maps\default.txt"
        if mobsAlvo is not None and hasattr(mobsAlvo, "__iter__"):
            mobsAlvo = list(mobsAlvo)

        self.Model = model
        self.ArquivoDeMobs = arquivoDeMobs
        self.MobsAlvo = mobsAlvo

        print(f"Modelo: {self.Model}")
        print(f"ArquivoDeMobs: {self.ArquivoDeMobs}")
        print(f"MobsAlvo: {self.MobsAlvo}")

        return self.Model, self.ArquivoDeMobs, self.MobsAlvo


settings = Settings()
