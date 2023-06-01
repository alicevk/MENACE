from files.api import Jogador, simulacao, plot
from pprint import pprint
import numpy as np

if __name__ == '__main__':

    num_jogos = 1000

    player1 = Jogador(1)
    # player2 = Jogador(2, reforco_vitoria=0, reforco_derrota=0)

    player3 = Jogador(1, reforco_vitoria=0, reforco_derrota=0)
    player4 = Jogador(2)

    # player1, player2, vitorias1, vitorias2, empates12 = simulacao(
    #     player1, player2, num_jogos
    # )

    # player3, player4, vitorias3, vitorias4, empates34 = simulacao(
    #     player3, player4, num_jogos
    # )

    num_jogos = 10000

    player1, player4, vitorias1b, vitorias4b, empates14 = simulacao(
        player1, player4, num_jogos
    )

    print()
    pprint(player1.brain)
    print("---")
    pprint(player4.brain)

    plot_name = "simulacao3"
    plot(vitorias1b, vitorias4b, empates14, plot_name, show=True)

