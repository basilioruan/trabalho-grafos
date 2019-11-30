'''
Template de resposta em Python
GCC218 - 2019/02
Trabalho final da disciplina de algoritmos em grafos 
Professor: Mayron Cesar
Grupo: Rafaela Custodio, 14, 201720376 
       Ruan Basilio, 14, 201720089
Data: 07/11/2019 
'''

'''Bibliotecas utilizadas'''
import pandas as pd
#from pyexcel_xlsx import get_data


'''Classe auxiliar de uma lista para a lista de adjacencia'''
class Lista:
    inicio = None
    fim = None
    
    def adicionaVertice(self, ID):
        if(self.inicio == None):
            self.inicio = Noh(ID)
            self.fim = self.inicio
            return

        novo = Noh(ID)
        self.fim.proximo = novo
        self.fim = novo

'''Classe auxiliar a classe lista para armazenar um no'''
class Noh:
    ID = None
    proximo = None
    relacao = None
    def __init__(self, ID):
        self.ID = ID

'''Classe vertice
        Feita para armazenar informacoes do vertice nome, se ja foi visitado, pais
        tempo de descoberta e fechamento'''
class Vertice:
    ID = None
    professor = None
    materia = None
    turma = None
    cor = None
    grau = None

    def __init__(self, ID, prof, mat, Turma):
        self.ID = ID
        self.professor = prof
        self.materia = mat
        self.turma = Turma
        self.cor = -1
        self.grau = 0
    
    def imprimir(self):
        return (str(self.ID) + " " + str(self.professor) + " " + str(self.materia) + " " + str(self.turma) + " " + str(self.cor) + " " + str(self.grau))

'''Classe lista de adjacencia
        Classe da estrutura principal, possui um dicionario de vertices e uma lista propriamente dita
        o atributo tempo foi colocado aqui para ser global na estrutura toda
        por ser a classe principal, nela estao os metodos que adicionam vertices e arestas
        e metodos auxiliares para se obter as ligacoes de um vertice
        os metodos estao todos com nomes sugestivos'''
class ListaAdjacencia:
    listaAdj = None
    vertices = None
    ID = 0
    maiorGrau = None
    inicial = None

    def __init__(self):
        self.listaAdj = {}
        self.vertices = {}
        self.ID = 0
        self.maiorGrau = 0
        self.inical = None
    
    def adicionaVertice(self, professor, materia, turma):
        v = Vertice(self.ID, professor, materia, turma)
        self.vertices[self.ID] = v
        self.listaAdj[self.ID] = Lista()
        self.ID+=1

    def adicionaAresta(self, IDV1, IDV2):
        #Grafo nao-direcionado
        self.listaAdj[IDV1].adicionaVertice(IDV2)
        #self.listaAdj[IDV2].adicionaVertice(IDV1)
    
    def ajustaGrau(self):
        for v in self.listaAdj:
            self.vertices[v].grau = len(self.getVizinhos(v))

    '''Metodo para imprimir o grafo, apenas para debug'''
    def imprime(self):
        for elemento in self.listaAdj:
            print (self.vertices[elemento].imprimir() + " " + str(self.getVizinhos(elemento)) + "\n")
    
    def saoVizinhos(self, v1, v2):
        if(v1 not in self.listaAdj):
            return False
        if(v2 not in self.listaAdj):
            return False
        if(v2 not in self.listaAdj[v1]):
            return False
        return True

    def getVizinhos(self, v):
        vizinhos = []
        listaVizinhos = self.listaAdj[v]
        viz = listaVizinhos.inicio
        while(viz != None):
            vizinhos.append(viz.ID)
            viz = viz.proximo
        return vizinhos

    def numeroVertices(self):
        return self.ID

    def verificaConflito(self, ID1, ID2):
        if(self.vertices[ID1].professor == self.vertices[ID2].professor):
            return True
        elif(self.vertices[ID1].turma == self.vertices[ID2].turma):
            return True
        else:
            return False
    
    def getInicial(self):
        for v in self.listaAdj:
            grauVertice = len(self.getVizinhos(v))
            if(grauVertice > self.maiorGrau):
                self.maiorGrau = grauVertice
                inicial = self.vertices[v]
        return inicial
    def zeraCor(self):
        for v in self.listaAdj:
            self.vertices[v].cor = -1


def Ingenua(grafo):
    listaAdj = grafo.listaAdj
    vertices = grafo.vertices
    k = 0

    for v in listaAdj:
        available = []
        for i in range (k):
            available.append(True)

        for vizinho in grafo.getVizinhos(v):
            if(vertices[vizinho].cor != -1):
                available[vertices[vizinho].cor] = False
        c = 0
        while (c < k and available[c] == False):
            c+=1
        if(c < k):
            vertices[v].cor = c
        else:
            vertices[v].cor = k
            k+=1
    return k 

def DSATUR(grafo):
    listaAdj = grafo.listaAdj
    vertices = grafo.vertices
    cores = 0
    verticeAtual = grafo.getInicial()
    for v in listaAdj:
        coresVizinhos = []
        #print(verticeAtual.imprimir())
        for vizinhos in grafo.getVizinhos(verticeAtual.ID):
            if(vertices[vizinhos].cor != -1 and vertices[vizinhos].cor not in coresVizinhos):
                coresVizinhos.append(vertices[vizinhos].cor)
        if(len(coresVizinhos) == cores):
            cores+=1
            verticeAtual.cor = cores
        else:
            for i in range (cores):
                if(i not in coresVizinhos):
                    verticeAtual.cor = i
                    break
        verticeAtual = grauSaturacao(grafo, verticeAtual)
        
    return cores

def grauSaturacao(grafo, atual):
    maxDeegre = 0
    verticeCandidato = []
    lista = []
    for v in grafo.listaAdj:
        if(grafo.vertices[v].cor == -1):
            for vizinho in grafo.getVizinhos(v):
                if(grafo.vertices[vizinho].cor != -1 and grafo.vertices[vizinho].cor not in lista):
                    lista.append(grafo.vertices[vizinho].cor)
            if(len(lista) > maxDeegre):
                maxDeegre = len(lista)
                verticeCandidato = []
                verticeCandidato.append(grafo.vertices[v])
            elif(len(lista) == maxDeegre):
                verticeCandidato.append(grafo.vertices[v])
            lista = []
    if(len(verticeCandidato) == 1):
        return verticeCandidato[0]
    else:
        grauMaior = 0
        posicao = 0
        for i in range (len(verticeCandidato)):
            if(verticeCandidato[i].grau > grauMaior):
                grauMaior = verticeCandidato[i].grau
                posicao = i
        #print("TAMANHO VETOR: ", len(verticeCandidato), "VALOR POSICAO: ", posicao)
        if(len(verticeCandidato) == 0):
            return None
        return verticeCandidato[posicao]


'''Funcao que extrai os valores do arquivo e cria o grafo atraves de uma lista de adjacencia'''
def leGrafo():
    grafo = ListaAdjacencia()
    planilha = pd.read_excel("Escola_A.xlsx")
    colunas = planilha.columns
    qtdLinhas = int(planilha.index.stop)
    for linha in range (qtdLinhas):
        for aulas in range (int(planilha[colunas[3]][linha])):
            grafo.adicionaVertice(planilha[colunas[2]][linha], planilha[colunas[0]][linha], planilha[colunas[1]][linha])
    
    for i in range (grafo.numeroVertices()):
        for j in range (grafo.numeroVertices()):
            if(i != j and grafo.verificaConflito(i, j) == True):
                grafo.adicionaAresta(i, j)
    grafo.ajustaGrau()

    #grafo.imprime()
    print("Escola A total cores (Ingenua): ", Ingenua(grafo))
    grafo.zeraCor()
    print("Escola A total cores (DSATUR): ", DSATUR(grafo))
    #grafo.imprime()

    '''f = open("ativ1_instance.txt")
    qtd = int(f.readline())
    for i in range (qtd):
        linha = f.readline()
        aux = linha.split(" ")
        tam = len(aux)
        grafo.adicionaVertice(aux[0].rstrip())
        for j in range (1, tam):
            if(aux[j] != '-'):
                grafo.adicionaAresta(aux[0], aux[j].rstrip())
    f.close()'''
      
leGrafo()
  
