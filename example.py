
from itertools import combinations
import nltk
from nltk.tokenize import sent_tokenize, RegexpTokenizer
from nltk.stem.snowball import RussianStemmer
import networkx as nx

def similarity(s1, s2):
    if not len(s1) or not len(s2):
        return 0.0
    return len(s1.intersection(s2))/(1.0 * (len(s1) + len(s2)))

# Выдает список предложений отсортированных по значимости
def textrank(text):
    sentences = sent_tokenize(text)
    tokenizer = RegexpTokenizer(r'\w+')
    lmtzr = RussianStemmer()
    words = [set(lmtzr.stem(word) for word in tokenizer.tokenize(sentence.lower()))
             for sentence in sentences] 	 
    pairs = combinations(range(len(sentences)), 2)
    scores = [(i, j, similarity(words[i], words[j])) for i, j in pairs]
    scores = filter(lambda x: x[2], scores)
    g = nx.Graph()
    g.add_weighted_edges_from(scores)
    pr = nx.pagerank(g)
    return sorted(((i, pr[i], s) for i, s in enumerate(sentences) if i in pr), key=lambda x: pr[x[0]], reverse=True)

# Сокращает текст до нескольких наиболее важных предложений
def sumextract(text, n=5):
    tr = textrank(text)
    top_n = sorted(tr[:n])
    return ' '.join(x[2] for x in top_n)

text='''Регулятор конфиденциальности Европейского Союза направил в Facebook предварительное распоряжение приостановить передачу данных в США о своих пользователях из Евросоюза, сообщил в среду WSJ, что представляет собой операционную и юридическую проблему для компании, которая может создать прецедент для других компаний-техгигантов. Это означает, что действие «стандартных договорных условий» (Standard Contractual Clauses, SCC), используемых тысячами европейских компаний для передачи данных, теперь приближается к отмене. Ник Клегг, руководитель отдела политики и коммуникаций Facebook, подтвердил, что SCC больше не может на практике использоваться для трансфера данных ЕС-США. Решение было давно предсказано многими сторонниками конфиденциальности после того, как Европейский суд постановил, что США не заслуживают доверия для передачи персональных данных. «Надзорные органы должны приостановить или запретить передачу персональных данных в третью страну, если они считают, что стандартные положения о защите данных не выполняются или не могут быть соблюдены в этой стране и что защита данных, требуемая законодательством ЕС, не может быть обеспечена другими средствами », — заявил в июле Высший суд Европы.'''

print(sumextract(text, 2))



