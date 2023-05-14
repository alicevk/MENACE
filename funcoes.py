import numpy as np
from itertools import product
from functools import partial
from random import choices, choice
from pprint import pprint
from matplotlib import pyplot as plt


ALL_SYMMETRY_OP = {
    "id": lambda x: x,
    "rot90": np.rot90,
    "flipv": np.fliplr,
    "fliph": np.flipud,
    "flipds": lambda x: np.fliplr(np.rot90(x)),
    "flipdp": lambda x: np.flipud(np.rot90(x)),
}

# Operaçãos inversas
ALL_SYMMETRY_OP_INV = {
    "id": lambda x: x,
    "rot90": partial(np.rot90, k=-1),
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
        3x3 ou em vetor linha, tanto faz. Pode ser também a representação em
        string da configuração.
    """

    def __init__(self, arr="000000000"):
        if isinstance(arr, str):
            self.config = np.array(list(arr), dtype=int)
        else:
            self.config = np.array(arr, dtype=int)

        msg = "Tua configuração deve ter 9 posições"
        assert len(self.config.ravel() == 9), msg
        self.config = self.config.reshape(3, 3)
        self.esta_encolhido = False
        self.lista = list(self.config.ravel())

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

        # jogadas proibidas tem número -1
        logic = self.config > 0
        mapa[logic] = -1

        return mapa

    def create_choice_dict(self, initial_value=2):
        # tem que converter para a posição padrão antes
        self.get_symmetry_id()
        conf = Configuracao(self.id_)
        mapa = conf.symmetry_map()
        choice_dict = {v: initial_value for v in set(mapa[mapa > 0])}
        return choice_dict

    def check_vitoria(self, jogador):
        """Checa se jogador ganhou."""
        self.desencolhe()
        logic = self.config == jogador
        if (
            3 in logic.sum(axis=0)
            or 3 in logic.sum(axis=1)
            or np.trace(logic) == 3
            or np.trace(np.fliplr(logic)) == 3
        ):
            return True
        else:
            return False


class Jogador:
    """Cria um agente jogador de jogo da velha."""

    def __init__(self, player_num=1, valor_inicial=2):
        self.player_num = player_num
        self.valor_inicial = valor_inicial
        self.cria_dicionario_jogadas()
        self.fim_de_jogo = False
        self.jogadas = []

    def cria_dicionario_jogadas(self):
        """Cria dicionário de todas as jogadas possíveis do jogador.

        Lista apenas jogos onde mais de uma escolha pode ser feita.

        Condições:
        + Jogador 1 é quem começa a jogar
        + Jogos já ganhos não são listados
        """

        if self.player_num == 1:
            diff = 0
        else:
            diff = 1

        jogos = {
            jogo.get_symmetry_id(): jogo.create_choice_dict(self.valor_inicial)
            for jogo in map(Configuracao, product([0, 1, 2], repeat=9))
            if jogo.lista.count(1) - jogo.lista.count(2) == diff
            and not (jogo.check_vitoria(1) or jogo.check_vitoria(2))
            and not jogo.lista.count(0) in [0, 1]
        }

        self.brain = jogos

    def realizar_jogada(self, config, verbose=False):
        id_ = config.get_symmetry_id()

        if id_.count("0") == 1:
            # apenas uma jogada a ser feita, não temos escolha
            config_up = Configuracao(id_.replace("0", str(self.player_num)))

        else:
            dicionario = self.brain[id_]
            posicoes = list(dicionario.keys())
            chance = list(dicionario.values())

            # se uma caixa está sem missangas, temos que resetá-la
            if sum(chance) <= 0:
                for k in dicionario:
                    dicionario[k] = self.valor_inicial
                chance = list(dicionario.values())

            # escolhe jogada
            try:
                casa_escolhida = choices(posicoes, weights=chance)[0]
            except ValueError:
                breakpoint()

            config_up = Configuracao(id_)
            mapa = config_up.symmetry_map()

            if verbose:
                print(config)
                print(ALL_SYMMETRY_OP_INV[config.op_name](mapa))
                print(casa_escolhida)
                print(dicionario)
                print(config.op_name)
                print()

            index = choice(np.where(mapa.ravel() == casa_escolhida)[0])

            lista = config_up.lista.copy()
            lista[index] = self.player_num
            array = np.array(lista).reshape(3,3)
            array = ALL_SYMMETRY_OP_INV[config.op_name](array)
            config_up = Configuracao(array)

            # registra jogo feito
            self.jogadas.append([dicionario, casa_escolhida])

        return config_up

    def atualizar_vitoria(self):
        """Atualiza os dicionários de escolha em caso de vitória."""
        for dicionario, casa_escolhida in self.jogadas:
            dicionario[casa_escolhida] += 3
        self.jogadas = []

    def atualizar_derrota(self):
        """Atualiza os dicionários de escolha em caso de derrota."""
        for dicionario, casa_escolhida in self.jogadas:
            dicionario[casa_escolhida] -= 1
        self.jogadas = []



jogadores = [Jogador(1), Jogador(2)]
num_jogos = 10000
placar = [0,0,0]

vitorias1 = [0]
vitorias2 = [0]
empates = [0]

for _ in range(num_jogos):
    config = Configuracao()
    jogador_da_vez = False

    while (
        (not config.check_vitoria(1))
        and (not config.check_vitoria(2))
        and (config.get_symmetry_id().count("0") > 0)
    ):
        config = jogadores[jogador_da_vez].realizar_jogada(config, False)
        jogador_da_vez = not jogador_da_vez

    if config.check_vitoria(1):
        jogadores[0].atualizar_vitoria()
        jogadores[1].atualizar_derrota()
        placar[0] += 1
        vitorias1.append(vitorias1[-1] + 1)
        vitorias2.append(vitorias2[-1])
        empates.append(empates[-1])

    elif config.check_vitoria(2):
        jogadores[1].atualizar_vitoria()
        jogadores[0].atualizar_derrota()
        placar[1] += 1
        vitorias2.append(vitorias2[-1] + 1)
        vitorias1.append(vitorias1[-1])
        empates.append(empates[-1])

    else:
        placar[2] += 1
        vitorias1.append(vitorias1[-1])
        vitorias2.append(vitorias2[-1])
        empates.append(empates[-1] + 1)

jog1 = jogadores[0]
pprint(jog1.brain)

jog2 = jogadores[1]
pprint(jog2.brain)



fig, axe = plt.subplots(
    ncols=1,
    nrows=1,
    figsize=(5, 5),
    dpi=150,
)

x = list(range(1, num_jogos+ 1))

axe.plot(x, vitorias1[1:], label="Vitórias 1")
axe.plot(x, vitorias2[1:], label="Vitórias 2")
axe.plot(x, empates[1:], label="Empates")

axe.set_xlabel("Jogo")
axe.set_ylabel("Quantidade")

fig.legend()

fig.savefig(
    "simulacao_2.png",
    dpi=150,
    bbox_inches='tight',
    pad_inches=2e-2,
)

plt.show()

plt.close(fig)
