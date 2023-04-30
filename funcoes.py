import numpy as np
from functools import partial


# todas as operações para gerar configurações simétricas. Não sei se está
# correto e completo!
ALL_SYMMETRY_OP = [
    lambda x: x,
    np.rot90,
    partial(np.rot90, k=2),
    partial(np.rot90, k=3),
    np.fliplr,
    np.flipud,
    lambda x: np.fliplr(np.rot90(x)),
    lambda x: np.flipud(np.rot90(x)),
]


class Configuracao:
    """Classe para representar uma configuração do jogo da velha.

    Args:
      arr:
        Numpy array de representando o jogo. Pode ser a representação em grade
        3x3 ou em vetor linha, tanto faz.
    """

    def __init__(self, arr):
        self.config = np.array(arr, dtype=int)

        msg = "Tua configuração deve ter 9 posições"
        assert len(self.config.ravel() == 9), msg
        self.config = self.config.reshape(3, 3)
        self.esta_encolhido = False

    def __repr__(self):
        return self.config.reshape(3, 3).__str__()

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

    def symmetry_set(self):
        """Gera o conjunto de simetrias."""
        symmetries = set()
        self.desencolhe()
        for op in ALL_SYMMETRY_OP:
            id_ = "".join(str(num) for num in op(self.config).ravel())
            symmetries.add(id_)
        return symmetries

    def get_symmetry_id(self):
        """O ID oficial da config. é a string da primeira posição do sorted."""
        return sorted(self.symmetry_set())[0]


if __name__ == "__main__":
    """Só para testarmos, depois deletamos isso aqui"""

    from pprint import pprint

    conf_lista = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    conf_lista = [1, 0, 0, 1, 1, 1, 0, 0, 0]

    jogo = Configuracao(conf_lista)

    print()

    simetrias = jogo.symmetry_set()
    for s in simetrias:
        print(np.array(list(s), dtype=int).reshape(3, 3))
        print()
    pprint(simetrias)
    print(jogo.get_symmetry_id())
