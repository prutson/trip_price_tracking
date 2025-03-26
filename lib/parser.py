import nest_asyncio
import asyncio
from lib.guanabara import buscar_passagens_onibus

nest_asyncio.apply()

class Parser:
    def __init__(self, entry_params):
        self.entry_params = entry_params
        self.origem= self.entry_params.origem
        self.destino= self.entry_params.destino
        self.data= self.entry_params.data
        self.passageiros= self.entry_params.passageiros

    def get_price(self):
        resultado_json = asyncio.run(buscar_passagens_onibus(
            origem= self.origem,
            destino= self.destino,
            data= self.data,
            passageiros= self.passageiros
        ))
        return resultado_json