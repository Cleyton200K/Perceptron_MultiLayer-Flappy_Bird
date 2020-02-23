import pygame
from BirdBrain import BirdBrain
from RedeNeural import RedeNeural
from Matrix import Matrix
from FlappyBird import *
import time
import os
import random


BASE = 510
PIPE_INICIAL = 250;
POPULACAO = 1;

def main():
	adicionarCano = False;	
	geracao = 1;
	birdBrains = [];
	birds = [];

	for i in range(POPULACAO):
		birdBrains.append(BirdBrain(3,2,1));
		birds.append(Bird(50,random.randrange(300,350)));

	removidos = [];

	fundo = Fundo(FlappyBird.LARGURA);
	chao = Base(FlappyBird.LARGURA,BASE);
	canos = [];
	numeroDeCanos =int(FlappyBird.LARGURA/300)+1;
	for i in range(numeroDeCanos):
		canos.append(Pipe(PIPE_INICIAL + i * 300));
	cano_largura = canos[0].PIPE_TOP.get_width();
	score = 0;
	window = pygame.display.set_mode((FlappyBird.LARGURA,FlappyBird.ALTURA));
	Clock = pygame.time.Clock();
	run = True;
	while (run):
		Clock.tick(30);
		for event in pygame.event.get():
			if( event. type == pygame.QUIT):
				run = False;
				pygame.quit();
				quit();


		pipe_ind = 0;
		if len(birds) > 0:
			if len(canos) > 1 and birds[0].x > canos[0].x + canos[0].PIPE_TOP.get_width():
				pipe_ind = 1;
		elif(geracao < 100):
			birdBrains = removidos;
			for i in range(POPULACAO):
				birds.append(Bird(50,350));

			removidos = [];

			canos = [];
			for i in range(numeroDeCanos):
				canos.append(Pipe(PIPE_INICIAL + i * 300));
			score = 0;
			geracao += 1;
		else:
			run = False;
			break;
		#Preve os próximo movimento e executa o movimento
		for x, bird in enumerate(birds):
			output = birdBrains[x].pensar([bird.y/150, (bird.y - canos[pipe_ind].height)/150, (bird.y- canos[pipe_ind].bottom)/150])
			if output > 0.5:
				bird.jump();
			bird.move();			

		canosRemovidos = [];
		#Faz a colisão e executa o aprendizado
		for cano in canos:
			for x,bird in enumerate(birds):	
				collided , top = cano.collide(bird);
				if collided:
					birdBrains[x].ajusteFino(score);
					if top:
						birdBrains[x].aprender(0);
					else:
						birdBrains[x].aprender(1);
					birds.pop(x);

					removidos.append(birdBrains[x]);
					birdBrains.pop(x);


				if( not cano.passed and (cano.x+cano_largura) < 0):
					cano.passed = True;
					adicionarCano = True;

			if((cano.x + cano_largura) < 0):
				canosRemovidos.append(cano);
			cano.move();

		if (adicionarCano):
			score += 1;
			canos.append(Pipe(numeroDeCanos*300 - cano_largura));
			adicionarCano = False;			
		#Remove os canos fora da tela
		for cano in canosRemovidos:
			canos.remove(cano);

		#Checa Pássaro por pássaro se tocou o solo ou saiu da tela
		for x,bird in enumerate(birds):
			if(bird.y + bird.img.get_height() >= BASE or bird.y < 0):
				birds.pop(x);
				removidos.append(birdBrains[x]);
				if(bird.y  < 0):
					birdBrains[x].aprender(0);
				else:
					birdBrains[x].aprender(1);
				birdBrains.pop(x);
			
			

		fundo.move();
		chao.move();
		draw_window(window, birds,canos,chao,fundo, score, geracao, len(birdBrains));

	print("Acabou...");

	return removidos;


if __name__ == "__main__":	
	main();
