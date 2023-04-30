import numpy as np
from functools import partial


# todas as operações para gerar configurações simétricas. Não sei se está
# correto e completo!
ALL_SYMMETRY_OP = {
    "id": lambda x: x,
    "rot90": np.rot90,
    "rot180": partial(np.rot90, k=2),
    # "rot270": partial(np.rot90, k=3),  # precisa desse?
    "flipv": np.fliplr,
    "fliph": np.flipud,
    "flipds": lambda x: np.fliplr(np.rot90(x)),
    "flipdp": lambda x: np.flipud(np.rot90(x)),
}

# Operaçãos inversas
ALL_SYMMETRY_OP_INV = {
    "id": lambda x: x,
    "rot90": partial(np.rot90, k=-1),
    "rot180": partial(np.rot90, k=-2),
    # "rot270": partial(np.rot90, k=-3),
    "flipv": np.fliplr,
    "fliph": np.flipud,
    "flipds": lambda x: np.fliplr(np.rot90(x)),
    "flipdp": lambda x: np.flipud(np.rot90(x)),
}


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

    def symmetry_dict(self):
        """Gera o conjunto de simetrias."""
        if not hasattr(self, "symmetries"):
            symmetries = {}
            self.desencolhe()
            for name, op in ALL_SYMMETRY_OP.items():
                id_ = "".join(str(num) for num in op(self.config).ravel())
                symmetries[name] = id_
            self.symmetries = symmetries
        return self.symmetries

    def get_symmetry_id(self):
        """O ID oficial da config. é a string da primeira posição do sorted."""
        self.symmetry_dict()
        self.id_ = sorted(self.symmetries.values())[0]
        self.op_name = [
            name
            for name in self.symmetries
            if self.symmetries[name] == self.id_
        ][0]
        return self.id_

    def symmetry_map(self):
        """Computa o mapa de simetria. Números iguais representam mesma jogada."""
        self.symmetry_dict()
        mapa = (np.arange(9) + 1).reshape(3, 3)

        base = self.symmetries["id"]

        if base == self.symmetries["fliph"]:
            mapa[2, :] = mapa[0, :]
        if base == self.symmetries["flipv"]:
            mapa[:, 2] = mapa[:, 0]
        if base == self.symmetries["flipdp"]:
            mapa[1, 0] = mapa[0, 1]
            mapa[2, 0] = mapa[0, 2]
            mapa[2, 1] = mapa[1, 2]
        if base == self.symmetries["flipds"]:
            mapa[1, 2] = mapa[0, 1]
            mapa[2, 2] = mapa[0, 0]
            mapa[2, 1] = mapa[1, 0]
        if base == self.symmetries["rot90"]:
            mapa[0, 0] = mapa[0, 2] = mapa[2, 0] = mapa[2, 2] = 1
            mapa[0, 1] = mapa[1, 0] = mapa[1, 2] = mapa[2, 1] = 2
        if base == self.symmetries["rot180"]:
            mapa[2, 1] = mapa[0, 1]
            mapa[1, 2] = mapa[1, 0]
            mapa[2, 2] = mapa[0, 0]
            mapa[2, 0] = mapa[0, 2]

        # jogadas proibidas tem número -1
        logic = self.config > 0
        mapa[logic] = -1

        return mapa


if __name__ == "__main__":
    """Só para testarmos, depois deletamos isso aqui"""

    from pprint import pprint

    conf_lista = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    conf_lista = [1, 0, 0, 0, 0, 0, 0, 0, 0]
    conf_lista = [0, 1, 0, 0, 0, 0, 0, 0, 0]
    conf_lista = [0, 0, 1, 0, 0, 0, 0, 0, 0]
    conf_lista = [0, 0, 0, 1, 0, 0, 0, 0, 0]
    conf_lista = [0, 0, 0, 0, 1, 0, 0, 0, 0]
    conf_lista = [0, 0, 0, 0, 0, 1, 0, 0, 0]
    conf_lista = [0, 0, 0, 0, 0, 0, 1, 0, 0]
    conf_lista = [0, 0, 0, 0, 0, 0, 0, 1, 0]
    conf_lista = [0, 0, 0, 0, 0, 0, 0, 0, 1]
    conf_lista = [1, 0, 2, 0, 0, 0, 0, 0, 0]
    conf_lista = [0, 1, 0, 0, 0, 0, 0, 2, 0]
    conf_lista = [0, 0, 1, 0, 0, 0, 2, 0, 0]
    conf_lista = [0, 2, 0, 2, 1, 1, 0, 1, 0]

    jogo = Configuracao(conf_lista)

    # teste simetrias
    print("Simetrias")
    print()
    simetrias = jogo.symmetry_dict()
    for nome, s in simetrias.items():
        print(np.array(list(s), dtype=int).reshape(3, 3))
        print()
    pprint(simetrias)
    print()
    print("ID do jogo:", jogo.get_symmetry_id())

    # testando os operadores. Se estiver tudo certo não é pra printar nada
    for name in ALL_SYMMETRY_OP:
        conf = jogo.config
        op = ALL_SYMMETRY_OP[name](conf)
        treat = ALL_SYMMETRY_OP_INV[name](op)
        if not np.all(np.equal(conf, treat)):
            print(name)
            print(conf)
            print()
            print(treat)
            print()

    print()
    print(jogo.config)
    print(jogo.symmetry_map())
