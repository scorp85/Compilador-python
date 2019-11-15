# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 14:38:35 2019

@author: vitor
"""
from pyparsing import *

filename = "programa.cfz"
#-------Keywords
programa, car, intt, retorne, leia, escreva, novalinha, se, entao, senao, enquanto, execute = map(Keyword,"programa car int retorne leia escreva novalinha se entao senao enquanto execute".split())
#-------Operadores
mul, div, mod, mais, menos, maior, maiorIgual, menor, menorIgual, igual, diferente, e, ou, assing, interroga, colon, negac= map(Keyword,"* / % + - > >= < <= == != e ou = ? : !".split())
#-------Declaração dos terminais
intconst = Word(nums)                   #palavra contendo uma simples sequencia de numeros
id = Word(alphas+"_", alphanums+"_").setName("id")    #palavras iniciadas com letras ou underline, e contendo letras, underline ou numeros no corpo
tipo = (intt | car)
constString = dblQuotedString.setName("constString")
carconst = Word(alphas, max=1)

#usando função foward para usar recursão
declFuncVar = Forward()
declVar = Forward()
listaParametrosCont = Forward()
bloco = Forward()
listaDeclVar = Forward()
listaComando = Forward()
comando = Forward()
assignExpr = Forward()
condExpr = Forward()
orExpr = Forward()
andExpr = Forward()
eqExpr = Forward()
desigExpr = Forward()
addExpr = Forward()
mulExpr = Forward()

expr = assignExpr

listExpr = Group(delimitedList(assignExpr, delim=',')).setName("listExpr")

primExpr = Group(id + Optional(nestedExpr("(", ")", content=listExpr) | nestedExpr("[", "]", content=expr) | '(' + ')')
            | carconst
            | intconst
            | nestedExpr("(", ")", content=expr)).setName("primExpr")

lValueExpr = Group(id + Optional(nestedExpr("[", "]", content=expr))).setName("LValueExpr")

unExpr = Group(Optional(menos | negac) + primExpr).setName("unExpr")

mulExpr << Group(Optional(mulExpr + (mul | div | mod)) + unExpr).setName("mulExpr")

addExpr << Group(Optional(addExpr + (mais | menos)) + mulExpr).setName("addExpr")

desigExpr << Group(Optional(desigExpr + (maior | maiorIgual | menor | menorIgual)) + addExpr).setName("desigExpr")

eqExpr << Group(Optional(eqExpr + (igual | diferente)) + desigExpr).setName("eqExpr")

andExpr << Group(Optional(andExpr + e) + eqExpr).setName("andExpr")

orExpr << Group(Optional(orExpr + ou) + andExpr).setName("orExpr")

condExpr << Group(orExpr + Optional(interroga + expr + colon + condExpr)).setName("condExpr")

assignExpr = Group(condExpr | (lValueExpr + assing + assignExpr)).setName("assignExpr")

vp = Word(alphas, max=1)

comando << Group(vp
           | Group(retorne + expr + vp).setName("retorne")
           | Group(leia + lValueExpr + vp).setName("leia")
           | Group(escreva + expr + vp).setName("escrevaExpr")
           | Group(escreva + '"' + constString + '"' + vp).setName("escreva")
           | Group(novalinha).setName("novalinha")
           | Group(se + nestedExpr("(", ")", content=expr) + entao + comando).setName("se")
           | Group(se + nestedExpr("(", ")", content=expr) + entao + comando + senao + comando).setName("seSenao")
           | Group(enquanto + nestedExpr("(", ")", content=expr) + execute + comando).setName("enquanto")
           | bloco).setName("comando")

listaComando << Group(comando + Optional(listaComando)).setName("listaComando")

listaDeclVar << Group(Optional(tipo + id + Optional(nestedExpr('[', ']', content=intconst)) + declVar + vp + listaDeclVar)).setName("listaDeclVar")

bloco << Group(nestedExpr('{', '}', content=(listaDeclVar + Optional(listaComando)))).setName("bloco")

listaParametrosCont << Group(delimitedList((tipo + id + Optional('[' + ']')), delim=',')).setName("listaParametrosCont")

listaParametros = Optional(listaParametrosCont)

declFunc = Group(nestedExpr('(', ')', content=listaParametros) + bloco).setName("declFunc")

declVar << Group(Optional(',' + id + Optional(nestedExpr('[', ']', content=intconst)) + declVar)).setName("declVar")

declProg = Group(programa + bloco).setName("declProg")

declFuncVar << Group(Optional(delimitedList((tipo + id + Optional(nestedExpr('[', ']', content=intconst)) + declVar), delim=';')) | (tipo + id + declFunc + declFuncVar)).setName("declFuncVar")

padrao = Group(declFuncVar + declProg).setName("programa")
padrao.ignore(cStyleComment)

try:
  padrao.validate()
except:
  print("Erro de recursão") 

print(padrao.parseFile(filename, parseAll=True))