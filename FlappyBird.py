import pygame
import time
import os
import random
pygame.font.init();




BIRD_IMGS = [pygame.image.load(os.path.join("imgs","bird1.png")), pygame.image.load(os.path.join("imgs","bird2.png")), pygame.image.load(os.path.join("imgs","bird3.png"))];
PIPE_IMG = pygame.image.load(os.path.join("imgs","pipe.png"));
BASE_IMG = pygame.image.load(os.path.join("imgs", "base.png"));
BACKGROUND_IMG = (pygame.image.load(os.path.join("imgs","bg.png")));
FONT = pygame.font.SysFont("comicsans",50);

class FlappyBird(object):
	"""
	Define e possibilita as alterações de velocidades Espaçamento entre Pipes
	"""
	VELOCIDADE = 6;
	LARGURA = 800;
	ALTURA = 550;
	GAP = 120;
	
	@staticmethod
	def setGAP(valor):
		"""
		Altera o GAP da classe de controle e a Pipe

		Entrada : int
		Retorno : Nenhum
		"""
		if(valor > 0 and valor < FlappyBird.ALTURA):
			FlappyBird.GAP = int(valor);
			Pipe.GAP = int(valor);
			
	@staticmethod
	def setLARGURA(valor):
		"""
		Muda a Largura da Janela se maior 500 pixels

		Entrada : valor(int) da largura em pixels
		Retorno : Nenhum
		"""

		if(valor > 500):
			FlappyBird.LARGURA = valor;
		else:
			print("Largura inválida.");
	@staticmethod
	def setVELOCIDADE(valor):
		"""
		Muda a velocidade do Controlador e de todos elementos da tela

		Entrada : valor(int) 
		Retorno : Nenhum
		"""
		if(valor > 0 ):
			FlappyBird.VELOCIDADE = valor;
			Bird.ANIMATION_TIME = valor;
			Pipe.VEL = valor;
			Base.VEL = valor;
			Fundo.VEL = valor+1;
	


class Bird(object):
	IMGS = BIRD_IMGS;
	MAX_ROTATION = 30;
	ROTATION_VEL = 20;
	ANIMATION_TIME = FlappyBird.VELOCIDADE;

	def __init__ (self, x, y):
		"""Posição inicial do Pássaro é descrita pelos eixos inseridos X e Y."""
		self.x = x;
		self.y = y;
		self.tilt = 0;
		self.tick_count = 0;
		self.vel = 0;
		self.height = self.y;
		self.img_count = 0;
		self.img = self.IMGS[0];
	def jump(self):
		self.vel = -8.5;
		self.tick_count = 0;
		if(self.tilt < 10):
			self.tilt += self.MAX_ROTATION;
		self.height = self.y;

	def move(self):
		self.tick_count += 1;

		d = self.vel * self.tick_count + 1.5 * (self.tick_count**2);
		if( d >= 16):
			d = 16; 
		elif (d < 0):
			d-= 2;

		self.y = self.y + d;
		if(d < 0 or self.y < ( self.height +50)):
			if self.tilt < self.MAX_ROTATION:
				self.tilt - self.MAX_ROTATION;
		else:
			if(self.tilt > -90):
				self.tilt -= self.ROTATION_VEL;

	def draw(self, win):
		self.img_count +=1;

		if(self.img_count <  (self.ANIMATION_TIME)):
			self.img = self.IMGS[0];
		elif(self.img_count < (self.ANIMATION_TIME * 2)):
			self.img = self.IMGS[1];
		elif(self.img_count < (self.ANIMATION_TIME * 3)):
			self.img = self.IMGS[2];
		elif(self.img_count < (self.ANIMATION_TIME * 4)):
			self.img = self.IMGS[1];
		elif(self.img_count == (self.ANIMATION_TIME * 4 + 1)):
			self.img = self.IMGS[0];
			self.img_count = 0;

		if(self.tilt <= -80):
			self.img = self.IMGS[1];
			self.img_count =self.ANIMATION_TIME * 2;

		rotated_image = pygame.transform.rotate(self.img, self.tilt);
		new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x,self.y)).center);
		win.blit(rotated_image, new_rect.topleft);
	def get_mask(self):
		return pygame.mask.from_surface(self.img);

class Pipe(object):
	"""
	Estrutura de canos
	"""
	GAP = FlappyBird.GAP;
	VEL = FlappyBird.VELOCIDADE;
	def __init__(self,x):
		self.x = x;
		self.height = 0;
		self.gap = 120;

		self.top = 0;
		self.bottom = 0;
		self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True);
		self.PIPE_BOTTOM = PIPE_IMG;

		self.passed = False;
		self.set_height();

	def set_height(self):
		self.height =random.randrange(120,330);
		self.top = self.height - self.PIPE_TOP.get_height();
		self.bottom = self.height + self.GAP;

	def move(self):
		self.x -= self.VEL;

	def draw(self,win):
		win.blit(self.PIPE_TOP,(self.x, self.top));
		win.blit(self.PIPE_BOTTOM,(self.x, self.bottom))

	def collide(self, bird):
		"""
		Checa colisão entre pássaro e a estrutura

		Entrada : Pássaro
		Retorno : (Bool) Se Colidiu, (Bool) Se colidiu com Top
		"""
		bird_mask = bird.get_mask();
		top_mask = pygame.mask.from_surface(self.PIPE_TOP);
		bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM);

		top_offset = (self.x - bird.x, self.top - round(bird.y));
		bottom_offset = (self.x -bird.x, self.bottom - round(bird.y));

		bottom_point = bird_mask.overlap(bottom_mask, bottom_offset);
		top_point = bird_mask.overlap(top_mask, top_offset);

		if top_point or bottom_point:
			return True, top_point;

		return False,False;

class Base(object):
	"""
	Base animada
	"""
	VEL = 	FlappyBird.VELOCIDADE;
	WIDTH = BASE_IMG.get_width();
	WIDTH_BACKGROUND = BACKGROUND_IMG.get_width();
	IMG = BASE_IMG;

	def __init__(self,x,y):
		self.y = y;
		self.x = int(x/self.WIDTH) + 2;
		self.__blocos = [];
		for i in range(self.x):
			self.__blocos.append(self.WIDTH * i);

	def move (self):
		for i in range(self.x):
			self.__blocos[i] -= self.VEL;
		for i in range(self.x):
			if(self.__blocos[i]+self.WIDTH < 0):
				self.__blocos[i] = self.__blocos[i-1]+self.WIDTH;
	def draw(self, win):
		for i in range(self.x):
			win.blit(self.IMG,(self.__blocos[i],self.y));


class Fundo(object):
	"""
	Fundo animado
	"""
	VEL = 	FlappyBird.VELOCIDADE + 1;
	WIDTH = BACKGROUND_IMG.get_width();
	IMG = BACKGROUND_IMG;

	def __init__(self,x, y= 0):
		self.y = y;
		self.x = int(x/self.WIDTH) + 2;
		self.__papeisDeParedes = [];
		for i in range(self.x):
			self.__papeisDeParedes.append(self.WIDTH * i);

	def move (self):
		for i in range(self.x):
			self.__papeisDeParedes[i] -= self.VEL;
		for i in range(self.x):
			if(self.__papeisDeParedes[i]+self.WIDTH < 0):
				self.__papeisDeParedes[i] = self.__papeisDeParedes[i-1]+self.WIDTH;

	def draw(self, win):
		for i in range(self.x):
			win.blit(self.IMG,(self.__papeisDeParedes[i],0));


def draw_window(win,birds, pipes,base,fundo, score, GEN,populacao):
	"""
	Desenha os elementos na tela

	Entrada : Janela, lista de pássaros, lista de Pipes , base, fundo, Geração Atual(int), População(int)
	Retorno : Nenhum
	"""
	fundo.draw(win);

	for pipe in pipes:
		pipe.draw(win);

	base.draw(win);

	for bird in birds:
		bird.draw(win);

	text1 = FONT.render("Score : " + str(score),1,(255,255,255));
	text2 = FONT.render("Geração : " + str(GEN),1,(255,255,255));
	text3 = FONT.render("População : " + str(populacao),1,(255,255,255));

	win.blit(text1, (FlappyBird.LARGURA -10 - text1.get_width(), 10))
	win.blit(text2, (10, 10))
	win.blit(text3, (10, 40))

	pygame.display.update();

