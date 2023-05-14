from math import sqrt
import os

#Diretório onde estão armazenados os dados do MovieLensv
path = os.getcwd()
#path='D:\\Repositorios\\Projeto_recomendacao_filmes\\ml-100k'

def euclidiana(base, usuario1, usuario2):
    si = {}
    for item in base[usuario1]:
       if item in base[usuario2]: si[item] = 1

    if len(si) == 0: return 0

    soma = sum([pow(base[usuario1][item] - base[usuario2][item], 2)
                for item in base[usuario1] if item in base[usuario2]])
    return 1/(1 + sqrt(soma))

def getSimilares(base, usuario):
    similaridade = [(euclidiana(base, usuario, outro), outro)
                    for outro in base if outro != usuario]
    similaridade.sort()
    similaridade.reverse()
    return similaridade[0:30]
    
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
                
def carregaMovieLens(base_file, test_file):
    filmes = {}
    for linha in open(path + '\\ml-100k\\u.item'):
        (id, titulo) = linha.split('|')[0:2]
        filmes[id] = titulo

    base = {}
    for linha in open(path + '\\' + base_file):
        (usuario, idfilme, nota, tempo) = linha.split('\t')
        base.setdefault(usuario, {})
        base[usuario][filmes[idfilme]] = float(nota)

    test = {}
    for linha in open(path + '\\' + test_file):
        (usuario, idfilme, nota, tempo) = linha.split('\t')
        test.setdefault(usuario, {})
        test[usuario][filmes[idfilme]] = float(nota)

    return base, test
          

def calculaItensSimilares(base):
    result = {}
    for item in base:
        notas = getSimilares(base, item)
        result[item] = notas
    return result

def getRecomendacoesItens(baseUsuario, similaridadeItens, usuario):
    notasUsuario = baseUsuario[usuario]
    notas={}
    totalSimilaridade={}
    for (item, nota) in notasUsuario.items():
        for (similaridade, item2) in similaridadeItens[item]:
            if item2 in notasUsuario: continue
            notas.setdefault(item2, 0)
            notas[item2] += similaridade * nota
            totalSimilaridade.setdefault(item2,0)
            totalSimilaridade[item2] += similaridade
    rankings=[(score/totalSimilaridade[item], item) for item, score in notas.items()]
    rankings.sort()
    rankings.reverse()
    return rankings

def calcular_acuracia(base_treinamento, base_teste):
    total_predicoes = 0
    acertos = 0

    for usuario, filmes in base_teste.items():
        for id_filme, info_filme in filmes.items():
            nota_real = info_filme['nota']
            rankings = getRecomendacoesUsuario(base_treinamento, usuario)
            for _, filme in rankings:
                if filme == id_filme:
                    nota_prevista = base_treinamento[usuario][filme]['nota']
                    break
            else:
                nota_prevista = 0

            total_predicoes += 1
            if nota_prevista == nota_real:
                acertos += 1

    acuracia = acertos / total_predicoes
    return acuracia
def calculate_mae(predictions, ratings):
    errors = [abs(predictions[user_id][item_id] - rating) 
              for user_id, item_ratings in ratings.items() 
              for item_id, rating in item_ratings.items() 
              if user_id in predictions and item_id in predictions[user_id]]
    if len(errors) == 0:
        return None
    return sum(errors) / len(errors)

data = carregaMovieLens('\\ml-100k\\u1.base', '\\ml-100k\\u1.test')
base_treinamento = data[0]
base_teste = data[1]

# Fazendo predições
predictions = {}
for usuario in base_teste:
    predictions[usuario] = {}
    for filme in base_teste[usuario]:
        rankings = getRecomendacoesUsuario(base_treinamento, usuario)
        for nota, filme_predito in rankings:
            if filme_predito == filme:
                predictions[usuario][filme] = nota
                break