import requests
import json
import csv
import time

try:
    with open('veiculos.csv', encoding='utf-8') as arquivo_referencia:

        tabela = list(csv.reader(arquivo_referencia, delimiter=','))
        
        if len(tabela) > 1:
            salvo = input('Deseja pesquisar um veículo salvo? (y/n)')
            salvo = salvo.lower()
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
    veiculo_contem = 0
except FileNotFoundError:
    file = open('veiculos.csv','w', newline='', encoding='utf-8')
    w = csv.writer(file)
    cont = 0
    salvo = 'n'
    #Define que CSV está vazio
    veiculo_contem = 3

try: 
    marca
    veiculo_contem = 0
except NameError:
    if salvo == 'y':
        print('Veículo não existe!')
    salvo = 'n'

if salvo != 'y':
    print('Bem vindo a tabela Fipe, essas são as marcas disponíveis:')
    time.sleep(2)
    marcas = requests.get('http://fipeapi.appspot.com/api/1/carros/marcas.json')
    marcas = json.loads(marcas.text)

    for i in marcas:
        print(i['id'], ' - ', i['name'])

    marca = input('Informe o número da marca desejada:')

    for i in marcas:
        if i['id']==int(marca):
            print('Você selecionou: ',i['name'])
            time.sleep(2)

    veiculos = requests.get('http://fipeapi.appspot.com/api/1/carros/veiculos/'+marca+'.json')
    veiculos = json.loads(veiculos.text)
    for i in veiculos:
        print(i['id'], ' - ', i['name'])

    veiculo = input('Informe o número do veículo desejado:')

    for i in veiculos:
        if i['id'] == veiculo:
            nome = i['name']
            print('Você selecionou: ', i['name'])
            time.sleep(2)

    versoes = requests.get('http://fipeapi.appspot.com/api/1/carros/veiculo/'+marca+'/'+veiculo+'.json')
    versoes = json.loads(versoes.text)
    for i in versoes:
        print(i['id'], ' - ', i['name'])

    versao = input('Informe a versão desejada:')

    for i in versoes:
        if i['id'] == versao:
            print('Você selecionou: ', i['name'])
            time.sleep(2)

resultado = requests.get('http://fipeapi.appspot.com/api/1/carros/veiculo/'+marca+'/'+veiculo+'/'+versao+'.json')
resultado = json.loads(resultado.text)
print(resultado['preco'])

if veiculo_contem == 3:
    veiculo_contem = 0
else:
    with open('veiculos.csv', encoding='utf-8') as arquivo_referencia:
        tabela = list(csv.reader(arquivo_referencia, delimiter=','))
        for l in tabela:
            if marca == l[2] and veiculo == l[3] and versao == l[4]:
                veiculo_contem = 1

if salvo != 'y' and veiculo_contem == 0:
    salvar = input('Salvar esse veículo? (y/n)')
    salvar = salvar.lower()
else:
    salvar = 'n'

if salvar == 'y':
    # Cria o arquivo (utilizar 'w' para sobrescrever dados e 'a' para adicionar)
    file = open('veiculos.csv', 'a', newline='', encoding='utf-8')
    w = csv.writer(file)

    if cont == 0:
        w.writerow(['ÍNDICE', 'NOME', 'MARCA', 'VEÍCULO', 'VERSÃO', 'PREÇO'])
        cont = 1
    w.writerow([cont, nome, marca, veiculo, versao, resultado['preco']])

    print('Veículo salvo com sucesso!')
