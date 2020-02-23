from Matrix import Matrix
class RedeNeural(object):
	"""
	Uma rede neural(Perceptron-multilayer) de 3 camadas
	"""
	def __init__(self,entrada, oculta, saida, taxaDeAprendizado = 0.1):
		"""
		Entrada : número de entradas, de neurônios ocultos e saidas. Podendo também variar a taxa de aprendizado
		"""
		self.__numeroNeuroniosEntrada = entrada;
		self.__numeroNeuroniosOculto = oculta;
		self.__numeroNeuroniosSaida = saida;
		self.__taxaDeAprendizado = taxaDeAprendizado;

		self.neuroniosDeEntrada = self.neuroniosOcultos = self.neuroniosSaida = [];

		

		self.pesosOculta = Matrix(oculta,entrada);
		self.pesosOculta.randomizar(0,1,0.01);
		self.pesosSaida = Matrix(saida, oculta);
		self.pesosSaida.randomizar(0,1,0.01);


		self.biasOculta = Matrix(oculta,1);
		self.biasOculta.randomizar(0,1,0.01);

		self.biasSaida = Matrix(saida,1);
		self.biasSaida.randomizar(0,1,0.01);
	
	def getTaxaDeAprendizado(self):
		return self.__taxaDeAprendizado;
		
	def setTaxaDeAprendizado(self,taxa):
		"""
		Define a taxa de aprendizado da Rede de 1% a 100%

		Entrada : float
		Retorno : Nenhum
		""" 
		if(taxa > 1):
			self.__taxaDeAprendizado = 1;
		elif(taxa <= 0):
			self.__taxaDeAprendizado = 0.01;
		else:
			self.__taxaDeAprendizado = taxa;
	@staticmethod
	def sigmoidal(valor):
		"""
		Função ativadora Sigmoidal = 1 / (1 + e ^ - valor)
		
		Entrada : Valor a ser aplicado na função
		Retorno : Resultado da aplicação
		"""
		return (1 / (1 + (2.718281828182818281828)**(-valor)));
	@staticmethod
	def derivadaSigmoidal(valor):
		"""
		Derivada da função ativadora Sigmoidal , dSigmoidal / dValor = Sigmoidal *(1 - Sigmoidal)
		
		Entrada : Valor(Resultante da aplicação à sigmoidal) a ser aplicado na função
		Retorno : Resultado da aplicação
		"""
		return valor *(1 - valor);

	@staticmethod
	def MSE(esperado, valor):
		"""
		Calculo do erro(Não é o MSE propriamente dito(Medium Square Error), mas funcionou melhor na rede)

		Entrada : O target e o valor deduzido
		Retorno : Erro calculado dadas as entradas
		"""		
		return (esperado - valor);

	def print(self):
		print("Entrada : {}\nPesos da Oculta : {}\n Oculta : {}\n Pesos da Saida : {}\n saida :{}".format(self.neuroniosDeEntrada, self.pesosOculta, self.neuroniosOcultos, self.pesosSaida, self.neuroniosSaida));

	def FeedForward(self, dados):
		"""
		Recebe as entradas e faz a classificação

		Entrada : As N entradas(float) definidas no __init__
		Retorno : Nenhum
		"""
		self.neuroniosDeEntrada = Matrix(self.__numeroNeuroniosEntrada, 1);
		self.neuroniosDeEntrada.preencher(dados);
 
		self.neuroniosOcultos =  (self.pesosOculta * self.neuroniosDeEntrada) + self.biasOculta;
		self.neuroniosOcultos = self.neuroniosOcultos.map(RedeNeural.sigmoidal);

		self.neuroniosSaida =  (self.pesosSaida * self.neuroniosOcultos) + self.biasSaida;
		self.neuroniosSaida = self.neuroniosSaida.map(RedeNeural.sigmoidal);

	def BackPropagation(self,esperado):
		"""
		Pondera as classificações e faz as correções aos pesos
		
		Entrada : Targets(float)
		Retorno : Nenhum
		"""
		es = Matrix(self.__numeroNeuroniosSaida, 1);
		for i in range(self.__numeroNeuroniosSaida):
			es.info[i][0] = self.MSE(esperado[i],self.neuroniosSaida.info[i][0]);
		deltaPesosSaida =self.neuroniosSaida.map(RedeNeural.derivadaSigmoidal).hadamart(es) * self.__taxaDeAprendizado;

		eo = self.pesosSaida.transpor() * es;
		deltaPesosOculta = 	self.neuroniosOcultos.map(RedeNeural.derivadaSigmoidal).hadamart(eo) * self.__taxaDeAprendizado;

		self.biasOculta = self.biasOculta + deltaPesosOculta;
		self.biasSaida  = self.biasSaida + deltaPesosSaida;

		self.pesosOculta = (deltaPesosOculta * self.neuroniosDeEntrada.transpor()) + self.pesosOculta; 
		self.pesosSaida =  (deltaPesosSaida * self.neuroniosOcultos.transpor()) + self.pesosSaida;
	
	def train(self, dados, esperado):
		aprendendo = True;
		while(aprendendo):
			aprendendo = False;
			for i in range(len(dados)):
				self.FeedForward(dados[i]);
				if self.MSE(esperado[i][0],self.neuroniosSaida.info[0][0])**2 > 0.005:
					aprendendo = True;
					self.BackPropagation(esperado[i]);
		print("Treinado.");


