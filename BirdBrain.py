from RedeNeural import RedeNeural
from Matrix import Matrix
class BirdBrain(object):
	"""
	É o "cérebro" do pássaro
	""" 
	def __init__(self,inputs, ocultas, outputs, taxaDeAprendizado = 0.5):
		self.brain = RedeNeural(inputs,ocultas, outputs, taxaDeAprendizado);
		self.scoreRecorde = 0;
	def pensar(self,dados):
		"""
		Faz interface com o FeedFoward
		
		Entrada : Lista de float
		Retorno : float
		"""
		self.brain.FeedForward(dados);
		return self.brain.neuroniosSaida.info[0][0];
	def aprender(self, target):
		"""
		Faz interface com o BackPropagation
		
		Entrada : float
		Retorno : Nenhum
		"""		
		self.brain.BackPropagation([target]);
	def ajusteFino(self,scoreAtual):
		"""
		Ajusta a taxa de aprendizado da Rede Neural
		
		Entrada : int
		Retorno : Nenhum
		"""
		if(self.scoreRecorde < scoreAtual):
			self.scoreRecorde = scoreAtual; 
			self.brain.setTaxaDeAprendizado(self.brain.getTaxaDeAprendizado() * 0.75);	
	

		