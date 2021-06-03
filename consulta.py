import requests
import json
import csv

# 1. abrir o arquivo
with open('veiculos.csv', encoding='utf-8') as arquivo_referencia:

    # 2. ler a tabela
    tabela = list(csv.reader(arquivo_referencia, delimiter=','))
    
    if len(tabela) > 1:
        salvo = input('Deseja pesquisar um veículo salvo? (y/n)')
    else:
        salvo = 'n'
        
    cont = 0
    for l in tabela:
        indice = l[0]
        tabela_nome = l[1]
        tabela_marca = l[2]
        tabela_veiculo = l[3]
        tabela_versao = l[4]
        tabela_preco = l[5]
        if cont != 0 and salvo == 'y':
            print(indice, ' - ','Modelo: ', tabela_nome, ' Versão: ', tabela_versao)
        cont = cont + 1

    if salvo == 'y':
        escolhido = input('Escolha o veículo:')
        for l in tabela:
            if escolhido == l[0]:
                marca = l[2]
                veiculo = l[3]
                versao = l[4]

if salvo != 'y':
    print('Bem vindo a tabela Fipe, essas são as marcas disponíveis:')
    marcas = requests.get('http://fipeapi.appspot.com/api/1/carros/marcas.json')
    marcas = json.loads(marcas.text)

    for i in marcas:
        print(i['id'], ' - ', i['name'])

    marca = input('Informe o número da marca desejada:')

    for i in marcas:
        if i['id']==int(marca):
            print('Você selecionou: ',i['name'])

    veiculos = requests.get('http://fipeapi.appspot.com/api/1/carros/veiculos/'+marca+'.json')
    veiculos = json.loads(veiculos.text)
    for i in veiculos:
        print(i['id'], ' - ', i['name'])

    veiculo = input('Informe o número do veículo desejado:')

    for i in veiculos:
        if i['id'] == veiculo:
            nome = i['name']
            print('Você selecionou: ', i['name'])

    versoes = requests.get('http://fipeapi.appspot.com/api/1/carros/veiculo/'+marca+'/'+veiculo+'.json')
    versoes = json.loads(versoes.text)
    for i in versoes:
        print(i['id'], ' - ', i['name'])

    versao = input('Informe a versão desejada:')

    for i in versoes:
        if i['id'] == versao:
            print('Você selecionou: ', i['name'])

resultado = requests.get('http://fipeapi.appspot.com/api/1/carros/veiculo/'+marca+'/'+veiculo+'/'+versao+'.json')
resultado = json.loads(resultado.text)
print(resultado['preco'])

if salvo == 'n':
    salvar = input('Salvar esse veículo? (y/n)')
else:
    salvar = 'n'

if salvar == 'y':
    # 1. cria o arquivo (utilizar 'w' para sobrescrever dados e 'a' para adicionar)
    file = open('veiculos.csv', 'a', newline='', encoding='utf-8')

    # 2. cria o objeto de gravação
    w = csv.writer(file)

    # 3. grava as linhas
    w.writerow([cont, nome, marca, veiculo, versao, resultado['preco']])

    print('Veículo salvo com sucesso!')
