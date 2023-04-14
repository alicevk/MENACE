import numpy as np


class Configuracao:
    """Classe para representar uma configuração do jogo da velha.

    Args:
      arr:
        Numpy array de representando o jogo. Pode ser a representação em grade
        3x3 ou em vetor linha, tanto faz.
    """

    def __init__(self, arr):
        msg = "Tua configuração deve ter 9 posições"

        self.config = np.array(arr, dtype=int)

        if len(self.config.shape) == 1:
            assert len(self.config) == 9, msg
            self.esta_encolhido = False
        else:
            assert len(self.config.ravel()) == 9, msg
            self.esta_encolhido = True

    def encolhe(self):
        """Faz com que a representação da configuração fique encolhida."""
        self.esta_encolhido = True
        self.config = self.config.ravel()
        return self.config

    def desencolhe(self):
        """Faz com que a representação da configuração fique desencolhida."""
        self.esta_encolhido = False
        self.config = self.config.reshape(3, 3)
        return self.config


if __name__ == "__main__":
    """Só para testarmos, depois deletamos isso aqui"""

    conf_lista = [0, 0, 1, 2, 0, 0, 1, 0, 0]

    conf_classe = Configuracao(conf_lista)
    print(conf_classe.encolhe())
    print(conf_classe.desencolhe())
    print(conf_classe.encolhe())
    print(conf_classe.desencolhe())
