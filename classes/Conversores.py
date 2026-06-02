from datetime import datetime   

class Conversores:

    @staticmethod
    def converte_data(data: str, hora: str = '00:00') -> str:
        """Converte string de data e hora em formato datetime"""
        data_hora = f"{data} {hora}"
        data_formato = "%d/%m/%Y %H:%M"
        data_completa = datetime.strptime(data_hora, data_formato)
        data_completa_str = data_completa.strftime("%Y-%m-%d %H:%M:%S")
        return data_completa_str

    @staticmethod
    def converte_float(string: str) -> float:
        new_string = string.replace(",", ".")
        return float(new_string)

    @staticmethod
    def converte_dinheiro(string: str) -> float:
        new_string = string.replace("R$", "")
        new_string = new_string.replace(",", ".")
        return float(new_string)

    @staticmethod
    def remove_newline(string: str) -> str:
        return string.replace("\n", "")
    
    @staticmethod
    def remove_espaco(string: str) -> str:
        return string.replace(" ", "")