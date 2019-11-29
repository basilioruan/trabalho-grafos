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

    def __init__(self, ID, prof, mat, Turma):
        self.ID = ID
        self.professor = prof
        self.materia = mat
        self.turma = Turma
        self.cor = 0
    
    def imprimir(self):
        return (str(self.ID) + " " + str(self.professor) + " " + str(self.materia) + " " + str(self.turma) + " " + str(self.cor))

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

    def __init__(self):
        self.listaAdj = {}
        self.vertices = {}
        self.ID = 0
    
    def adicionaVertice(self, professor, materia, turma):
        v = Vertice(self.ID, professor, materia, turma)
        self.vertices[self.ID] = v
        self.listaAdj[self.ID] = Lista()
        self.ID+=1

    def adicionaAresta(self, IDV1, IDV2):
        #Grafo nao-direcionado
        self.listaAdj[IDV1].adicionaVertice(IDV2)
        #self.listaAdj[IDV2].adicionaVertice(IDV1)

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

'''Funcao que extrai os valores do arquivo e cria o grafo atraves de uma lista de adjacencia'''
def leGrafo():
    grafo = ListaAdjacencia()
    planilha = pd.read_excel("Escola_C.xlsx")
    colunas = planilha.columns
    qtdLinhas = int(planilha.index.stop)
    for linha in range (qtdLinhas):
        for aulas in range (int(planilha[colunas[3]][linha])):
            grafo.adicionaVertice(planilha[colunas[2]][linha], planilha[colunas[0]][linha], planilha[colunas[1]][linha])
    
    for i in range (grafo.numeroVertices()):
        for j in range (grafo.numeroVertices()):
            if(i != j and grafo.verificaConflito(i, j) == True):
                grafo.adicionaAresta(i, j)

    grafo.imprime()

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
  
