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
import time
import timeit


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
        Feita para armazenar informacoes do vertice'''
class Vertice:
    ID = None
    professor = None
    materia = None
    turma = None
    cor = None
    grau = None
    restricoes = None
    preferencias = None
    preferenciasNaoAtendidas = None

    def __init__(self, ID, prof, mat, Turma):
        self.ID = ID
        self.professor = prof
        self.materia = mat
        self.turma = Turma
        self.cor = -1
        self.grau = 0
        self.restricoes = []
        self.preferencias = []
        self.preferenciasNaoAtendidas = 0
    
    def imprimir(self):
        return (str(self.ID) + " " + str(self.professor) + " " + str(self.materia) + " " + str(self.turma) + " " + str(self.preferencias) + "\n")

'''Classe lista de adjacencia
        Classe da estrutura principal, possui um dicionario de vertices e uma lista propriamente dita
        o atributo ID indica a numeração do vértice, totalPreferencias indica o número de todas as
        preferências dos professores, horarios indica o número de horários disponíveis da escola,
        preferenciasAtendidas é um vetor que indica as preferencias que foram atendidas, cores indica
        o número total de cores utilizadas na coloração, naoColoridos indica a quantidade de vértices 
        não coloridos, os atributos segunda à sexta indica os horários (cores) disponiveis nos respectivos
        dias. Os métodos estão todos com nomes sugestivos'''
class ListaAdjacencia:
    listaAdj = None
    vertices = None
    ID = 0
    totalPreferencias = None
    horarios = None
    preferenciasAtendidas = None
    cores = None
    naoColoridos = None
    segunda = None
    terca = None
    quarta = None
    quinta = None
    sexta = None

    def __init__(self):
        self.listaAdj = {}
        self.vertices = {}
        self.ID = 0
        self.totalPreferencias = 0
        self.horarios = 0
        self.segunda = None
        self.terca = None
        self.quarta = None
        self.quinta = None
        self.sexta = None
        self.preferenciasAtendidas = []
        self.cores = None
    
    def adicionaVertice(self, professor, materia, turma):
        v = Vertice(self.ID, professor, materia, turma)
        self.vertices[self.ID] = v
        self.listaAdj[self.ID] = Lista()
        self.ID+=1

    def adicionaAresta(self, IDV1, IDV2):
        #Grafo nao-direcionado
        self.listaAdj[IDV1].adicionaVertice(IDV2)
    
    def ajustaGrau(self):
        for v in self.listaAdj:
            self.vertices[v].grau = len(self.getVizinhos(v))

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
        maiorGrau = 0
        for v in self.listaAdj:
            grauVertice = len(self.getVizinhos(v))
            if(grauVertice > maiorGrau):
                maiorGrau = grauVertice
                inicial = self.vertices[v]
        return inicial

    def resetar(self):
        for v in self.listaAdj:
            self.vertices[v].cor = -1
        self.preferenciasAtendidas = []

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
    
    def preferenciasProfessor(self, preferencias):
        qtdLinhas = int(preferencias.index.stop)
        self.totalPreferencias = qtdLinhas
        for i in range(qtdLinhas):
            professor = preferencias["Professor:"][i]
            dia = preferencias["Dia da semana:"][i]
            horario = str(preferencias["Horário:"][i])
            for elemento in self.listaAdj:
                if(self.vertices[elemento].professor == professor):
                    if(dia == "Segunda" and self.segunda[horario] not in self.vertices[elemento].restricoes):
                        self.vertices[elemento].preferencias.append(self.segunda[horario])
                    elif(dia == "Terça" and self.terca[horario] not in self.vertices[elemento].restricoes):
                        self.vertices[elemento].preferencias.append(self.terca[horario])
                    elif(dia == "Quarta" and self.quarta[horario] not in self.vertices[elemento].restricoes):
                        self.vertices[elemento].preferencias.append(self.quarta[horario])
                    elif(dia == "Quinta" and self.quinta[horario] not in self.vertices[elemento].restricoes):
                        self.vertices[elemento].preferencias.append(self.quinta[horario])
                    elif(dia == "Sexta" and self.sexta[horario] not in self.vertices[elemento].restricoes):
                        self.vertices[elemento].preferencias .append(self.sexta[horario])
                    self.vertices[elemento].preferenciasNaoAtendidas += 1

    def verificaColoracao(self):
        cont = 0
        for elemento in self.listaAdj:
            if(self.vertices[elemento].cor == -1):
                cont+=1
        self.naoColoridos = cont
        return cont
    
    def verificaPreferencias(self):
        return (len(self.preferenciasAtendidas)/self.totalPreferencias)

'''Algortimo DSATUR priorizando preferencias, nesse algoritmo prioriza a tentativa de colorir
    o vértice com alguma cor (horário) de sua preferência'''
def DSATURpreferencial(grafo):
    listaAdj = grafo.listaAdj
    vertices = grafo.vertices
    horarios = grafo.horarios
    flagPreferencia = False
    cores = []
    verticeAtual = grafo.getInicial()
    for v in listaAdj:
        coresVizinhos = []
        for vizinhos in grafo.getVizinhos(verticeAtual.ID):
            if(vertices[vizinhos].cor != -1 and vertices[vizinhos].cor not in coresVizinhos):
                coresVizinhos.append(vertices[vizinhos].cor)
        for corPreferencial in verticeAtual.preferencias:
            if(corPreferencial not in coresVizinhos and corPreferencial not in verticeAtual.restricoes):
                verticeAtual.cor = corPreferencial
                verticeAtual.preferenciasNaoAtendidas -= 1
                if(corPreferencial not in grafo.preferenciasAtendidas):
                    grafo.preferenciasAtendidas.append(corPreferencial)
                flagPreferencia = True
                if(corPreferencial not in cores):
                    cores.append(corPreferencial)
        if(flagPreferencia == False):
            for i in range (horarios*5):
                if(i not in coresVizinhos and i not in verticeAtual.restricoes):
                    verticeAtual.cor = i
                    if(i not in cores):
                        cores.append(i)
                    break
        flagPreferencia = False
        verticeAtual = grauSaturacao(grafo, verticeAtual)
    
    grafo.cores = len(cores)
    return len(cores)

'''Algortimo DSATUR sem preferencias, nesse algoritmo não há priorização na tentativa de colorir
    o vértice com alguma cor (horário) de sua preferência, atribui-se uma cor e caso seja de sua
    preferência, é contabilizada'''
def DSATUR(grafo):
    listaAdj = grafo.listaAdj
    vertices = grafo.vertices
    horarios = grafo.horarios
    cores = []
    verticeAtual = grafo.getInicial()
    for v in listaAdj:
        coresVizinhos = []
        for vizinhos in grafo.getVizinhos(verticeAtual.ID):
            if(vertices[vizinhos].cor != -1 and vertices[vizinhos].cor not in coresVizinhos):
                coresVizinhos.append(vertices[vizinhos].cor)
        for i in range (horarios*5):
            if(i not in coresVizinhos and i not in verticeAtual.restricoes):
                if(i in verticeAtual.preferencias and i not in grafo.preferenciasAtendidas):
                    grafo.preferenciasAtendidas.append(i)
                    verticeAtual.preferenciasNaoAtendidas -= 1
                verticeAtual.cor = i
                if(i not in cores):
                    cores.append(i)
                break
        verticeAtual = grauSaturacao(grafo, verticeAtual)
        
    grafo.cores = len(cores)
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

def obterResultado(grafo):
    '''Executando DSATUR com preferencia'''
    totalCoresPref = DSATURpreferencial(grafo)
    totalNaoColoridosPref = grafo.verificaColoracao()
    totalPrefAtendidasPref = grafo.verificaPreferencias()

    '''Resetando as cores'''
    grafo.resetar()

    '''Executando DSATUR sem preferencia'''
    totalCoresSemPref = DSATUR(grafo)
    totalNaoColoridosSemPref = grafo.verificaColoracao()
    totalPrefAtendidasSemPref = grafo.verificaPreferencias()

    '''Comparando resultados'''
    if(totalCoresPref < totalCoresSemPref):
        grafo.cores = str(totalCoresPref)
        grafo.naoColoridos = str(totalNaoColoridosPref)
        print("Quantidade de cores: " + str(totalCoresPref))
        print("Vértices não coloridos: " + str(totalNaoColoridosPref))
        print("Preferencias atendidas sobre o total de preferências: " + str(totalPrefAtendidasPref))
    else:
        if(totalNaoColoridosPref < totalNaoColoridosSemPref):
            grafo.cores = str(totalCoresPref)
            grafo.naoColoridos = str(totalNaoColoridosPref)
            print("Quantidade de cores: " + str(totalCoresPref))
            print("Vértices não coloridos: " + str(totalNaoColoridosPref))
            print("Preferencias atendidas sobre o total de preferências: " + str(totalPrefAtendidasPref)) 
        elif(totalNaoColoridosPref == totalNaoColoridosSemPref):
            if(totalPrefAtendidasPref > totalPrefAtendidasSemPref):
                grafo.cores = str(totalCoresPref)
                grafo.naoColoridos = str(totalNaoColoridosPref)
                print("Quantidade de cores: " + str(totalCoresPref))
                print("Vértices não coloridos: " + str(totalNaoColoridosPref))
                print("Preferencias atendidas sobre o total de preferências: " + str(totalPrefAtendidasPref))
            else:
                grafo.cores = str(totalCoresSemPref)
                grafo.naoColoridos = str(totalNaoColoridosSemPref)
                print("Quantidade de cores: " + str(totalCoresSemPref))
                print("Vértices não coloridos: " + str(totalNaoColoridosSemPref))
                print("Preferencias atendidas sobre o total de preferências: " + str(totalPrefAtendidasSemPref)) 
        else:
            grafo.cores = str(totalCoresSemPref)
            grafo.naoColoridos = str(totalNaoColoridosSemPref)
            print("Quantidade de cores: " + str(totalCoresSemPref))
            print("Vértices não coloridos: " + str(totalNaoColoridosSemPref))
            print("Preferencias atendidas sobre o total de preferências: " + str(totalPrefAtendidasSemPref)) 

    

'''Funcao que extrai os valores do arquivo e cria o grafo atraves de uma lista de adjacencia'''
def leGrafo(nomeExcel):
    grafo = ListaAdjacencia()

    '''Lendo os dados do grafo'''
    planilha = pd.read_excel(nomeExcel, sheet_name=0)
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
    sheetConfig = pd.read_excel(nomeExcel, sheet_name = 1)
    configuracao = []
    sheetLinhas = int(sheetConfig.index.stop)
    sheetColunas = sheetConfig.columns
    for i in range (0, sheetLinhas):
       configuracao.append(str(sheetConfig["Horários de Inicio de aulas a cada dia."][i]))

    '''Criar matriz de cores'''
    grafo.criaListaCores(configuracao)

    '''Lendo restricoes da turma'''
    restricoesTurma = pd.read_excel(nomeExcel, sheet_name = 3)
    if(not restricoesTurma.empty):
        grafo.restricoesTurma(restricoesTurma)

    '''Lendo restricoes dos professores'''
    restricoesProfessor = pd.read_excel(nomeExcel, sheet_name = 2)
    if(not restricoesProfessor.empty):
        grafo.restricoesProfessor(restricoesProfessor)
    
    '''Lendo preferencias dos professores'''
    preferenciasProfessor = pd.read_excel(nomeExcel, sheet_name = 4)
    if(not preferenciasProfessor.empty):
        grafo.preferenciasProfessor(preferenciasProfessor)
    
    return grafo
    #obterResultado(grafo, int(preferenciasProfessor.index.stop))
    
      
def main():

    print("Escola A:")
    escolaA = leGrafo("Escola_A.xlsx")
    inicio = timeit.default_timer()
    obterResultado(escolaA)
    fim = timeit.default_timer()
    tempoA = fim - inicio
    print()

    print("Escola B:")
    escolaB = leGrafo("Escola_B.xlsx")
    inicio = timeit.default_timer()
    obterResultado(escolaB)
    fim = timeit.default_timer()
    tempoB = fim - inicio
    print()

    print("Escola C:")
    escolaC = leGrafo("Escola_C.xlsx")
    inicio = timeit.default_timer()
    obterResultado(escolaC)
    fim = timeit.default_timer()
    tempoC = fim - inicio
    print()

    print("Escola D:")
    escolaD = leGrafo("Escola_D.xlsx")
    inicio = timeit.default_timer()
    obterResultado(escolaD)
    fim = timeit.default_timer()
    tempoD = fim - inicio

    arquivo = open('Resultado.txt', 'w')
    arquivo.write('Resultados:' + '\n' + '\n')
    arquivo.write('Quantidade de horarios utilizados (Cores):' + '\n' + '\n')
    arquivo.write('Escola A: ' + str(escolaA.cores) + '\n' + '\n')
    arquivo.write('Escola B: ' + str(escolaB.cores) + '\n' + '\n')
    arquivo.write('Escola C: ' + str(escolaC.cores) + '\n' + '\n')
    arquivo.write('Escola D: ' + str(escolaD.cores) + '\n' + '\n')

    arquivo.write('Tempo para cada iteração do algortimo (em segundos):' + '\n' + '\n')
    arquivo.write('Escola A: ' + str(tempoA) + '\n' + '\n')
    arquivo.write('Escola B: ' + str(tempoB) + '\n' + '\n')
    arquivo.write('Escola C: ' + str(tempoC) + '\n' + '\n')
    arquivo.write('Escola D: ' + str(tempoD) + '\n' + '\n')

    arquivo.write('Quantidade de vértices não coloridos:' + '\n' + '\n')
    arquivo.write('Escola A: ' + str(escolaA.naoColoridos) + '\n' + '\n')
    arquivo.write('Escola B: ' + str(escolaB.naoColoridos) + '\n' + '\n')
    arquivo.write('Escola C: ' + str(escolaC.naoColoridos) + '\n' + '\n')
    arquivo.write('Escola D: ' + str(escolaD.naoColoridos) + '\n' + '\n')

main()  