<h2 align="center"> MENACE: Caixas de fósforo que aprendem </h2>
<p align="justify">
Estamos em busca dos melhores jogadores do Jogo da Velha que possam desafiar o nosso grande campeão, o MENACE, uma caixinha de fósforo com habilidade super especiais de aprendizado de máquina. Queremos competir com os mais diversos jogadores e aprimorar cada vez mais as habilidades do MENACE, e aí:  </p>

<h3 align='center'> <i> "Vocês acham que conseguem ganhar contra uma caixinha de fósforo"? </i> </h3>


<p align="center"><img src="https://github.com/alicevk/MENACE/assets/106678040/f52ddf3b-f538-4edc-816c-7ae54e6d9732" height="300"></p>
<h5 align="center"> Figura 1. Combate entre as caixinhas de fósforo, MENACE, com o jogador humano. [Fonte: Autoral] </h5>


## MENACE - Resumo

<p align="justify">
O MENACE (Matchbox Educable Noughts and Crosses Engine) consiste em um conjunto de caixas de fósforo em que cada uma representa uma possível configuração do tabuleiro do jogo da velha. Dentro de cada caixa há um conjunto de miçangas coloridas representando possíveis movimentos. </p>
<p align="justify"> Inicialmente, as caixas de fósforo são preenchidas com número igual de miçangas que  correspondem a cada jogada. Quando o MENACE joga uma partida de jogo da velha, ele consulta a caixa  correspondente à configuração atual do tabuleiro e seleciona aleatoriamente uma miçanga  dessa caixa. A miçanga selecionada determina a jogada do MENACE. Após o jogo, o  MENACE recebe um feedback na forma de vitória, derrota ou empate. </p>
<p align="justify"> Essa capacidade de receber feedback demonstra a super habilidade do MENACE: o aprendizado de máquina. Por meio do resultado do seu confronto com o MENACE, conseguimos atribuir valores positivos, negativos ou neutro que comutam em um processo de aprendizado para o MENACE que fica cada vez mais estrategista quando você joga com ele. E aí, estão preparados para enfrentar esse desafio? </p>
<p align="justify"> Neste repositório estamos apresentando uma versão de implementação do MENACE para o Ciência Aberta do CNPEM! </p>


## Instalação

```sh
pip install pygame numpy matplotlib
```


## Alguns cuidados antes de rodar o MENACE:
	
Confira se você tem as bibliotecas pygame e numpy instaladas antes de tentar abrir!
	
Foi implementada uma trava para o jogo não ser fechado sem querer/fora de hora por jogadores em eventos! Por isso, Alt + F4 não vai fechar a tela! Tome cuidado com isso! O único jeito de sair da tela fullscreen e fechar a janela é digitando o Konami code!!!! (↑↑↓↓←→←→BA)

OBS: A interface gráfica não foi otimizada para o sistema Windows, por isso tome cuidado extra nessa plataforma! Caso o código acima não funcione, utilize o Gerenciador de Tarefas do Windows.

## Como fazer para rodar?

Basta executar o `main.py` usando o Python. Certifique-se que está no ambiente virtual onde instalou o pygame e numpy, do contrário vai dar erro.

```sh
python main.py
```