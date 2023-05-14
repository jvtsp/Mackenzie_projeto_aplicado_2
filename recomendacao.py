from math import sqrt
import os


#Diretório onde estão armazenados os dados do MovieLensv
diretorio_atual = os.getcwd()

# Função para calcular a similaridade entre dois usuários usando a distância Euclidiana
def euclidiana(base, usuario1, usuario2):
    # Dicionário para armazenar os itens avaliados por ambos usuários
    si = {}
    for item in base[usuario1]:
       if item in base[usuario2]: si[item] = 1

    # Se não houver itens em comum, a similaridade é zero
    if len(si) == 0: return 0

    # Calcula a soma das diferenças ao quadrado para cada item avaliado pelos dois usuários
    soma = sum([pow(base[usuario1][item] - base[usuario2][item], 2)
                for item in base[usuario1] if item in base[usuario2]])
    
    # Retorna a similaridade entre os dois usuários
    return 1/(1 + sqrt(soma))

# Função para obter uma lista de usuários similares a um dado usuário
def getSimilares(base, usuario):
    # Cria uma lista de tuplas (similaridade, usuário) para todos os usuários, exceto o usuário dado
    similaridade = [(euclidiana(base, usuario, outro), outro)
                    for outro in base if outro != usuario]
    # Ordena a lista em ordem decrescente de similaridade
    similaridade.sort()
    similaridade.reverse()
    # Retorna os 30 usuários mais similares
    return similaridade[0:30]

# Função para recomendar filmes para um dado usuário com base nos usuários mais similares
def getRecomendacoesUsuario(base, usuario):
    totais={}
    somaSimilaridade={}
    for outro in base:
        if outro == usuario: continue
        similaridade = euclidiana(base, usuario, outro)

        if similaridade <= 0: continue

        for item in base[outro]:
            if item not in base[usuario]:
                totais.setdefault(item, 0)
                totais[item] += base[outro][item] * similaridade
                somaSimilaridade.setdefault(item, 0)
                somaSimilaridade[item] += similaridade
    rankings=[(total / somaSimilaridade[item], item) for item, total in totais.items()]
    rankings.sort()
    rankings.reverse()
    return rankings[0:30]

# Função para carregar os dados do MovieLens          
def carregaMovieLens(diretorio_atual):
    filmes = {}
    for linha in open(diretorio_atual + '\\ml-100k\\u.item'):
        (id, titulo) = linha.split('|')[0:2]
        filmes[id] = titulo

    base = {}
    for linha in open(diretorio_atual + '\\ml-100k\\u.data'):
        (usuario, idfilme, nota, tempo) = linha.split('\t')
        base.setdefault(usuario, {})
        base[usuario][filmes[idfilme]] = float(nota)
    return base  
          
# Função calcula a similaridade entre cada par de filmes usando um método de similaridade do cosseno.
def calculaItensSimilares(base):
    result = {}
    for item in base:
        notas = getSimilares(base, item)
        result[item] = notas
    return result
