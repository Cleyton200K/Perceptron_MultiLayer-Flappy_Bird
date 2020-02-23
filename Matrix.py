from random import randrange
class Matrix(object):
	"""
	Define uma matriz N x M, e oferece operações básicas para a Rede
	"""
	def __init__(self, linhas, colunas):
		self.info = [];
		for i in range(linhas):
			self.info.append([]);
			for j in range(colunas):
				self.info[i].append(0);

		self.__linhas = linhas;
		self.__colunas = colunas;

	def preencher(self, dados):
		"""
		Recebe um vetor(V m.n ou menor) é insere os valores neles contidos(Na ordem de linha por linha)

		Entrada : Vetor com os n.m dados 
		Retorno : Nenhum
		"""
		if(len(dados) > self.__linhas*self.__colunas):
			raise Exception("Quantidade de dados extrapola a dimensão da Matriz");
		for i in range(len(dados)):			
			self.info[i//self.__colunas][i%self.__colunas] = dados[i];
	


	def getLinhas(self):
		"""
		Retorna o número de linhas definidas na Matriz

		Entrada : Nenhuma
		Retorno : Número de linhas
		"""
		return self.__linhas;

	def map(self,funcao):
		"""
		Como a função map do Python, aplica uma função passada no parâmetro a cada valor da matriz

		Entrada : Função a ser aplicada 
		Retorno : Matriz Cópia com a função aplicada
		"""
		tempMatrix = Matrix(self.__linhas, self.__colunas);
		for i in range(self.__linhas):
			for j in range(self.__colunas):
				tempMatrix.info[i][j] = funcao(self.info[i][j]);
		return tempMatrix;

	def transpor(self):
		"""
		Transpoem a Matriz
		
		Entrada : Nenhuma
		Retorno : Matriz Cópia Transposta
		"""
		tempInfo = [];
		for i in range(self.__colunas):
			tempInfo.append([]);
			for j in range(self.__linhas):
				tempInfo[i].append(self.info[j][i]);

		tempMatrix = Matrix(self.__colunas, self.__linhas);
		tempMatrix.info = tempInfo;
		return tempMatrix;

		tempInfo;
	def randomizar(self, inicio, fim, passos = 1):
		"""
		Cada valor da matriz é definido dentro intervalo de entrada randomicamente

		Entrada : Valor inicial , Final e unitário
		Retorno : Matriz Cópia com os valores randômicos aplicados
		""" 
		for i in range(self.__linhas):
			for j in range(self.__colunas):
				self.info[i][j] = randrange(inicio * 100, fim* 100,passos * 100)/100;
	def hadamart(self, matrixB):
		tempMatrix = Matrix(self.__linhas, self.__colunas);
		if(self.__linhas == matrixB.getLinhas() and self.__colunas == matrixB.getColunas()):
			for i in range(self.__linhas):
				for j in range(self.__colunas):
					tempMatrix.info[i][j] = self.info[i][j] * matrixB.info[i][j];
		return tempMatrix;

	

	def normalizar(self):
		"""
		Define o máximo e o mínimo e muda a escala de [mínimo , máximo] para [-1 , 1]

		Entrada : Nenhuma
		Retorno : Matriz Cópia normalizada
		"""
		maximo = minimo = self.info[0][0];
		for i in range(self.__linhas):
			for j in range(self.__colunas):
				if(self.info[i][j] > maximo):
					maximo = self.info[i][j];
				elif(self.info[i][j] < minimo):
					minimo = self.info[i][j];
		
		tempMatrix = Matrix(self.__linhas,self.__colunas);
		media = (maximo - minimo)/2;
		for i in range(self.__linhas):
			for j in range(self.__colunas):
				tempMatrix.info[i][j] = (self.info[i][j] - minimo - media)/ media;
		return tempMatrix;

	def getColunas(self):
		"""
		Retorna o número de colunas definidas na Matriz

		Entrada : Nenhuma
		Retorno : Número de colunas
		"""
		return self.__colunas;

	def getInformacao(self):
		"""
		Retorna a matriz(não a própria Matrix)
		
		Entrada : Nenhuma
		Retorno : O Atributo "info"
		"""

		return self.info;


	#Métodos Especiais	
	def __sub__(self, matrixB):
		"""
		Subtração  entre matrizes( matrixA[m x n] - matrixB[m x n] )

		Entrada : Matrix a direita do operador
		Retorno : MatrixC[m x n] Resultante da operação
		"""
		if(self.__colunas == matrixB.getColunas() and self.__linhas == matrixB.getLinhas()):
			matrixC = Matrix(self.__linhas, self.__colunas);
			for i in range(self.__linhas):
				for j in range(self.__colunas):
					matrixC.info[i][j] = self.info[i][j] - matrixB.getInformacao()[i][j];
			return matrixC;
		else:
			raise Exception("É impossivel somar matrizes NÃO quadradas identicas");

	

	def __add__(self, matrixB):
		"""
		Adição  entre matrizes( matrixA[m x n] + matrixB[m x n] )

		Entrada : Matrix a direita do operador
		Retorno : MatrixC[m x n] Resultante da operação
		"""
		if(self.__colunas == matrixB.getColunas() and self.__linhas == matrixB.getLinhas()):
			matrixC = Matrix(self.__linhas, self.__colunas);
			for i in range(self.__linhas):
				for j in range(self.__colunas):
					matrixC.info[i][j] = self.info[i][j] + matrixB.getInformacao()[i][j];
			return matrixC;
		else:
			raise Exception("É impossivel somar matrizes NÃO quadradas identicas");

	
	def __mul__(self, matrixB):
		"""
		multiplicação  entre matrizes( matrixA[m x n] - matrixB[n x k] )

		Entrada : Matrix a direita do operador
		Retorno : MatrixC[m x k] Resultante da operação

		multiplicação entre matriz e escalar(sempre a direita)

		Entrada : Escalar(float) a direita(somente) do operador
		Retorno : MatrixC[m x n] 
		"""
		if type(matrixB) is float:
			matrixC = Matrix(self.__linhas, self.__colunas);
			for i in range(self.__linhas):
				for j in range(self.__colunas):
					matrixC.info[i][j] = self.info[i][j] * matrixB;
			return matrixC;
		elif(self.__colunas == matrixB.getLinhas()):
			matrixC = Matrix(self.__linhas, matrixB.getColunas());
			currentColumn = 0;
			for i in range(self.__linhas):
				for j in range(matrixB.getColunas()):
					for k in range(self.__colunas):
						matrixC.info[i][j] += self.info[i][k] * matrixB.info[k][j];
			return matrixC;
		else:	
			raise Exception("É impossivel multiplicar matrizes sem a relação Ai == Bj");

	def __str__(self):
		"""
		Formata a informação e retorna
		"""
		retorno = "";
		for i in range(self.__linhas):
			retorno = "{}\n{}".format(retorno,self.info[i]);
		return retorno;



