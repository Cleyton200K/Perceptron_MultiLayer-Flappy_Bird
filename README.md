# Flappy_Bird_Perceptron_MultiLayer
# Introdução
Um experimento comum é o aprendizado de máquina com algoritmos genéticos no jogo Flappy Bird, então como experimento, quis testar utilizando somente o BackPropagation, uma ideia simples, tocou o cano superior(ou voou para fora da tela) não deve pular e caso toque no cano inferior(ou no solo) deve pular, e a cada ponto de Score a taxa de aprendizado é reduzida em 25%(com intuito de tornar as mudanças mais sutis, e a porcentagem de mudança é arbitrária).

# Metodologia
Projeto realizado em python 3.7, utilizando a biblioteca PyGame e o código do jogo foi modificado a partir de :https://github.com/techwithtim/NEAT-Flappy-Bird, o restante implementado do zero.

# Instruções
Basta executar Main.py

Principais Modificações(Main.py):

Alterar tamanho da População(Variável Global POPULACAO)

Alterar velocidade(na função main) : FlappyBird.setVELOCIDADE(valor) ->   valor maior que 0

Alterar Largura da janela(na função main) : FlappyBird.setLARGURA(valor) ->   valor maior que 500

Alterar GAP entre os canos(na função main) : FlappyBird.setGAP(valor) ->   valor maior que 0, e menor que a Altura da Janela(550 pixels)
