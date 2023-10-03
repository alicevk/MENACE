# MENACE: Caixas de fósforo que aprendem </h1>

Estamos em busca dos melhores jogadores de Jogo da Velha que possam desafiar o nosso **grande campeão**, o MENACE, uma caixinha de fósforo com habilidades super especiais de **aprendizado de máquina**. Queremos competir com os mais diversos jogadores e aprimorar cada vez mais as habilidades do MENACE!!! E aí?

<p align='center' style='font-size:120%'> VOCÊ ACHA QUE CONSEGUE GANHAR JOGANDO CONTRA UMA CAIXINHA DE FÓSFORO? </p>

<p align="center"><img src="https://github.com/alicevk/MENACE/assets/106678040/f52ddf3b-f538-4edc-816c-7ae54e6d9732" height="300"></p>


## O que é o MENACE e como ele funciona?

O MENACE (Matchbox Educable Noughts and Crosses Engine) consiste em um conjunto de caixas de fósforo, no qual cada uma representa uma possível configuração do tabuleiro do jogo da velha. Dentro de cada caixa há um conjunto de miçangas coloridas, representando todos possíveis movimentos que o MENACE pode realizar.

Inicialmente, as caixas de fósforo são preenchidas com número igual das miçangas que  correspondem a cada jogada. Cada vez que o MENACE joga uma partida de jogo da velha, ele consulta a caixa  correspondente à configuração atual do tabuleiro e seleciona aleatoriamente uma miçanga  dessa caixa. A miçanga selecionada determina a jogada que ele irá realizar. Isso ocorre sucessivamente até o final da partida.

Após o final do jogo, o  MENACE recebe um feedback na forma de vitória, derrota ou empate. Dependendo desse feedback, em cada caixinha o MENACE recebe mais miçangas iguais à que foi sorteada (caso suas jogadas tenham sido boas o suficiente), ou então perde algumas miçangas dessa cor (caso ele não tenha um bom desempenho).

Essa capacidade de receber um feedback demonstra a super habilidade do MENACE: o aprendizado de máquina. Por meio do resultado do seu confronto com o MENACE, conseguimos atribuir valores positivos, negativos ou neutros que comutam em um processo de aprendizado para que o MENACE fique cada vez mais estrategista quando você joga com ele.

**E aí, está preparado para enfrentar esse desafio?**


## Como instalar o MENACE?

Para poder jogar contra o MENACE do seu próprio computador, tudo que você precisa fazer é clonar este repositório!

O código do jogo foi escrito em Python, utilizando de algumas bibliotecas para realizar diferentes funções. Para que seja possível rodar o MENACE sem se deparar com problemas, instale essas bibliotecas utilizando o comando abaixo no terminal:

```sh
pip install pygame numpy matplotlib
```


## Como fazer para rodar?

Basta executar o arquivo [`main.py`](./main.py) usando o Python. Certifique-se que está no ambiente virtual onde instalou o pygame e numpy, do contrário pode ocorrer algum erro. Com o terminal aberto na pasta deste repositório, utilize o comando:

```sh
python main.py
```

## Alguns cuidados antes de rodar o MENACE:
	
* Confira se você tem as bibliotecas `pygame` e `numpy` instaladas antes de tentar abrir qualquer arquivo!
	
* Foi implementada uma trava para o jogo não ser fechado sem querer/fora de hora por jogadores em eventos! Por isso, a combinação Alt + F4 não vai fechar a tela! Tome cuidado com isso! O único jeito de sair da tela fullscreen e fechar a janela é digitando o Konami code!!!! ( ↑ ↑ ↓ ↓ ← → ← → B A )

**OBS:** A interface gráfica não foi otimizada para o sistema Windows, por isso tome cuidado extra nessa plataforma! Caso o código acima não funcione, utilize o Gerenciador de Tarefas do Windows.