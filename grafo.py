'''
Template de resposta em Python
GCC218 - 2019/02
Trabalho final da disciplina de algoritmos em grafos 
Professor: Mayron Cesar
Grupo: Liliana Sabato Teodoro, 14, 201810021 
       Rafaela Custodio, 14, 201720376 
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
    restricoes = None

    def __init__(self, ID, prof, mat, Turma):
        self.ID = ID
        self.professor = prof
        self.materia = mat
        self.turma = Turma
        self.cor = -1
        self.grau = 0
        self.restricoes = []
    
    def imprimir(self):
        return (str(self.ID) + " " + str(self.professor) + " " + str(self.materia) + " " + str(self.turma) + " " + str(self.cor) + " " + str(self.grau) +
        " " + str(self.restricoes))

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
    horarios = None
    segunda = None
    terca = None
    quarta = None
    quinta = None
    sexta = None

    def __init__(self):
        self.listaAdj = {}
        self.vertices = {}
        self.ID = 0
        self.maiorGrau = 0
        self.horarios = 0
        self.segunda = None
        self.terca = None
        self.quarta = None
        self.quinta = None
        self.sexta = None
    
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
            print (self.vertices[elemento].imprimir() + "\n")
    
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

    def criaListaCores(self, configuracao):
        self.horarios = len(configuracao)
        self.segunda = {}
        self.segunda[configuracao[0]] = 0
        for i in range(1, len(configuracao)):
            self.segunda[configuracao[i]] = i * 5
        
        self.terca = {}
        self.terca[configuracao[0]] = 1
        cont = 1
        for i in range(1, len(configuracao)):
            self.terca[configuracao[i]] = cont + 5
            cont+=5
        

        self.quarta = {}
        self.quarta[configuracao[0]] = 2
        cont = 2
        for i in range(1, len(configuracao)):
            self.quarta[configuracao[i]] = cont + 5
            cont+=5

        self.quinta = {}
        self.quinta[configuracao[0]] = 3
        cont = 3
        for i in range(1, len(configuracao)):
            self.quinta[configuracao[i]] = cont + 5
            cont+=5
        
        self.sexta = {}
        self.sexta[configuracao[0]] = 4
        cont = 4
        for i in range(1, len(configuracao)):
            self.sexta[configuracao[i]] = cont + 5
            cont+=5
    
    '''Carregando as restricoes da turma'''
    def restricoesTurma(self, restricaoTurma):
        qtdLinhas = int(restricaoTurma.index.stop)
        for i in range(qtdLinhas):
            turma = restricaoTurma["Turma"][i]
            dia = restricaoTurma["Dia da semana"][i]
            horario = str(restricaoTurma["Horário da restrição"][i])
            for elemento in self.listaAdj:
                if(self.vertices[elemento].turma == turma):
                    if(dia == "Segunda"):
                        self.vertices[elemento].restricoes.append(self.segunda[horario])
                    elif(dia == "Terça"):
                        self.vertices[elemento].restricoes.append(self.terca[horario])
                    elif(dia == "Quarta"):
                        self.vertices[elemento].restricoes.append(self.quarta[horario])
                    elif(dia == "Quinta"):
                        self.vertices[elemento].restricoes.append(self.quinta[horario])
                    elif(dia == "Sexta"):
                        self.vertices[elemento].restricoes.append(self.sexta[horario])
    
    '''Carregando as restricoes dos professores'''
    def restricoesProfessor(self, restricaoProfessor):
        qtdLinhas = int(restricaoProfessor.index.stop)
        for i in range(qtdLinhas):
            professor = restricaoProfessor["Professor:"][i]
            dia = restricaoProfessor["Dia da semana da restrição:"][i]
            horario = str(restricaoProfessor["Restrição de Horário:"][i])
            for elemento in self.listaAdj:
                if(self.vertices[elemento].professor == professor):
                    if(dia == "Segunda" and self.segunda[horario] not in self.vertices[elemento].restricoes):
                        self.vertices[elemento].restricoes.append(self.segunda[horario])
                    elif(dia == "Terça" and self.terca[horario] not in self.vertices[elemento].restricoes):
                        self.vertices[elemento].restricoes.append(self.terca[horario])
                    elif(dia == "Quarta" and self.quarta[horario] not in self.vertices[elemento].restricoes):
                        self.vertices[elemento].restricoes.append(self.quarta[horario])
                    elif(dia == "Quinta" and self.quinta[horario] not in self.vertices[elemento].restricoes):
                        self.vertices[elemento].restricoes.append(self.quinta[horario])
                    elif(dia == "Sexta" and self.sexta[horario] not in self.vertices[elemento].restricoes):
                        self.vertices[elemento].restricoes.append(self.sexta[horario])
        #self.imprime()

    '''Verificação se existe vértices sem cor'''
    def verificaColoracao(self):
        cont = 0
        for elemento in self.listaAdj:
            if(self.vertices[elemento].cor == -1):
                cont+=1
        return cont

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
    horarios = grafo.horarios
    cores = []
    verticeAtual = grafo.getInicial()
    for v in listaAdj:
        coresVizinhos = []
        #print(verticeAtual.imprimir())
        for vizinhos in grafo.getVizinhos(verticeAtual.ID):
            if(vertices[vizinhos].cor != -1 and vertices[vizinhos].cor not in coresVizinhos):
                coresVizinhos.append(vertices[vizinhos].cor)
        for i in range (horarios*5):
            if(i not in coresVizinhos and i not in verticeAtual.restricoes):
                verticeAtual.cor = i
                if(i not in cores):
                    cores.append(i)
                break
        '''if(len(coresVizinhos) == cores):
            verticeAtual.cor = cores
            cores+=1
        else:
            for i in range (cores):
                if(i not in coresVizinhos):
                    verticeAtual.cor = i
                    break'''
        verticeAtual = grauSaturacao(grafo, verticeAtual)
        
    return len(cores)

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
    elif(len(verticeCandidato) == 0):
            return None
    else:
        grauMaior = 0
        posicao = 0
        for i in range (len(verticeCandidato)):
            if(verticeCandidato[i].grau > grauMaior):
                grauMaior = verticeCandidato[i].grau
                posicao = i
        return verticeCandidato[posicao]


'''Funcao que extrai os valores do arquivo e cria o grafo atraves de uma lista de adjacencia'''
def leGrafo():
    grafo = ListaAdjacencia()

    '''Lendo os dados do grafo'''
    planilha = pd.read_excel("Escola_A.xlsx", sheet_name=0)
    colunas = planilha.columns
    qtdLinhas = int(planilha.index.stop)
    for linha in range (qtdLinhas):
        for aulas in range (int(planilha[colunas[3]][linha])):
            grafo.adicionaVertice(planilha[colunas[2]][linha], planilha[colunas[0]][linha], planilha[colunas[1]][linha])
    
    '''Fazendo ligacoes de conflito'''
    for i in range (grafo.numeroVertices()):
        for j in range (grafo.numeroVertices()):
            if(i != j and grafo.verificaConflito(i, j) == True):
                grafo.adicionaAresta(i, j)
    grafo.ajustaGrau()

    '''Lendo configuracoes'''
    sheetConfig = pd.read_excel("Escola_A.xlsx", sheet_name=1)
    configuracao = []
    sheetLinhas = int(sheetConfig.index.stop)
    sheetColunas = sheetConfig.columns
    for i in range (0, sheetLinhas):
       configuracao.append(str(sheetConfig["Horários de Inicio de aulas a cada dia."][i]))

    '''Criar matriz de cores'''
    grafo.criaListaCores(configuracao)

    '''Lendo restricoes da turma'''
    restricoesTurma = pd.read_excel("Escola_A.xlsx", sheet_name=3)
    if(not restricoesTurma.empty):
        grafo.restricoesTurma(restricoesTurma)

    '''Lendo restricoes dos professores'''
    restricoesProfessor = pd.read_excel("Escola_A.xlsx", sheet_name=2)
    if(not restricoesProfessor.empty):
        grafo.restricoesProfessor(restricoesProfessor)

    print("Escola A total cores (DSATUR): ", DSATUR(grafo))
    print("Vértices não coloridos: " + str(grafo.verificaColoracao()))
      
leGrafo()
  
