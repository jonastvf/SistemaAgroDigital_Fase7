import math
import os
import csv

cultures = ['milho', 'laranja']
products = {'milho': 'Fosfato Monoamônico', 'laranja': 'Diclorofenoxiacético'}
productsQtd = {'Fosfato Monoamônico': 5, 'Diclorofenoxiacético': 0.15}
formats = {'milho': 'retangulo', 'laranja': 'triangulo'}
streets = {'milho': 1, 'laranja': 2}
spaceBetweenStreets = 1
calculatedPlantingAreas = []

logo = welcomeMessage = '''___________                        _________      .__          __  .__                      
\_   _____/____ _______  _____    /   _____/ ____ |  |  __ ___/  |_|__| ____   ____   ______
 |    __) \__  \\_  __ \/     \   \_____  \ /  _ \|  | |  |  \   __\  |/  _ \ /    \ /  ___/
 |     \   / __ \|  | \/  Y Y  \  /        (  <_> )  |_|  |  /|  | |  (  <_> )   |  \\___ \ 
 \___  /  (____  /__|  |__|_|  / /_______  /\____/|____/____/ |__| |__|\____/|___|  /____  >
     \/        \/            \/          \/                                       \/     \/ 
'''
active = True
phase = 0
currentCulture = ''
currentArea = 0

def resetCurrentStatus():
    global currentCulture, currentArea
    currentCulture = ''
    currentArea = 0

def setCurrentStatus(culture, area):
    global currentCulture, currentArea
    currentCulture = culture
    currentArea = area


def showInvalidInput():
    print('Entrada inválida! Tente novamente.')

def clearTerminal():
    system = os.name
    if system == 'nt':
        os.system('cls')
        return
    os.system('clear')

def calcAreaAvailable(area, figure, streetSize, spaceBetweenStreets):
    if figure == 'retangulo':
        totalStreetSize = streetSize + spaceBetweenStreets
        streetQdt = math.floor(area / totalStreetSize)
        areaOccupiedByStreets = streetQdt * streetSize
        areaAvailable = area - areaOccupiedByStreets
        return {'plantingArea': areaAvailable, 'numberOfStreets': streetQdt}

    if figure == 'triangulo':
        base = math.sqrt(2 * area)
        height = base / 2
        totalArea = (base * height) / 2
        totalStreetSize = streetSize + spaceBetweenStreets
        streetsQtd = math.floor(height / totalStreetSize)
        areaAvailable = totalArea - (streetsQtd * streetSize * base / totalArea)
        return {'plantingArea': areaAvailable, 'numberOfStreets': streetsQtd}

def onInit():
    clearTerminal()
    print (welcomeMessage + '\n')
    print('Bem vindo a Tech Farm Solutions!')
    print('Vamos planejar um plantio eficiente?')
    print('Tecle enter para começar.')
    input()

def getCultureIndex():
    userInput = 0
    try:
        print('Digite 1 para milho ou 2 para laranja ou digite 0 para sair.')
        userInput = int(input('Selecione uma cultura: '))
    except Exception as e:
        showInvalidInput()
        return -1
    
    return userInput

def getTotalArea():
    totalArea = 0
    try:
        print('Digite a área total disponível para plantio em metros quadrados ou digite 0 para sair')
        userInput = int(input('Area total: '))
        totalArea = userInput
    except Exception as e:
        showInvalidInput()
        return -1
    return totalArea

def getProductQtd(product, area):
    productMultiplier = productsQtd[product]
    return area * productMultiplier

def setCalculatedPlantingArea(index = -1):
    global calculatedPlantingAreas, currentCulture, currentArea, formats, streets, spaceBetweenStreets
    streetSize = streets[currentCulture]
    currentFormat = formats[currentCulture]
    calc = calcAreaAvailable(currentArea, currentFormat, streetSize, spaceBetweenStreets)
    newData = {
            'culture': currentCulture, 
            'totalArea': currentArea,
            'plantingArea': round(calc['plantingArea'], 2) ,
            'numberOfStreets': calc['numberOfStreets'],
            'product': products[currentCulture],
            'productQtd': round(getProductQtd(products[currentCulture], calc['plantingArea']), 2)
        }

    if index == -1:
        calculatedPlantingAreas.append(newData)
        return
    
    calculatedPlantingAreas[index] = newData

def showResult(data):
    result = f'''
Cultura: {data['culture']}
area total: {data['totalArea']}
area disponível para plantio: {data['plantingArea']}
quantidade de ruas: {data['numberOfStreets']}
aplicação do produto: {data['product']}
quantidade de produto necessário: {data['productQtd']}
'''
    print(result)

def getNewOption():
    option = 0
    try:
        userInput = int(input('\nDigite 1 para inserir um novo registro\nDigite 2 para exibir os dados\nDigite 3 para editar um registro\nDigite 4 para exportar os dados para um arquivo CSV\nDigite 5 para deletar um registro\nDigite 0 para sair\n'))
        option = userInput
    except Exception as e:
        showInvalidInput
        return -1
    return option

def showResumedData():
    if len(calculatedPlantingAreas) == 0: return
    count = 1
    for i in calculatedPlantingAreas:
        option = i
        print(f"Opção {count} - Cultura: {option['culture']}, area total: {option['totalArea']}")
        count += 1

def getCalculatedPlantingAreaIndex(mode = "editar"):
    option = 0
    try:
        userInput = int(input(f"Digite a opção que deseja {mode} ou digite 0 para sair: "))
        option = userInput
    except Exception as e:
        showInvalidInput()
        return -1
    
    return option

def exportData():
    global calculatedPlantingAreas
    fileName = 'dados.csv'

    with open(fileName, mode='w', newline='', encoding='utf-8') as file:
        columnNames = calculatedPlantingAreas[0].keys()
        writer = csv.DictWriter(file, fieldnames=columnNames)
        writer.writeheader()
        writer.writerows(calculatedPlantingAreas)

    print(f"Dados exportados com sucesso!\n Verifique o arquivo dados.csv")

while active:
    match phase:
        case 0:
            onInit()
            phase = 1
        case 1:
            userInput = getCultureIndex()
            if userInput == -1: continue
            if not userInput :
                active = False
                continue
            if userInput not in [i + 1 for i, _ in enumerate(cultures)]:
                showInvalidInput()
                continue
            currentCulture = cultures[userInput - 1]
            phase = 2
        case 2:
            userInput = getTotalArea()
            if userInput == -1: continue
            if userInput == 0:
                active = False
                continue
            currentArea = userInput
            currentIndex = len(calculatedPlantingAreas) - 1
            setCalculatedPlantingArea()
            currentIndex = len(calculatedPlantingAreas) - 1
            print(f"==================> Index: {len(calculatedPlantingAreas)}")
            showResult(calculatedPlantingAreas[currentIndex])
            resetCurrentStatus()
            phase = 3
        case 3:
            userInput = getNewOption()
            if userInput == -1: continue
            if userInput == 0:
                active = False
                continue
            if userInput == 1:
                clearTerminal()
                phase = 1
                continue
            if userInput == 2:
                clearTerminal()
                for i in calculatedPlantingAreas:
                    showResult(i)
                continue
            if userInput == 3:
                clearTerminal()
                showResumedData()
                userInput = getCalculatedPlantingAreaIndex()
                if userInput == -1: continue
                if userInput == 0:
                    active = False
                    continue
                if userInput < 0 or userInput > len(calculatedPlantingAreas):
                    showInvalidInput()
                    continue
                index = userInput - 1

                # Get culture
                culture = getCultureIndex()
                if culture == -1: continue
                if not culture :
                    active = False
                    continue
                if culture not in [i + 1 for i, _ in enumerate(cultures)]:
                    showInvalidInput()
                    continue
                currentCulture = cultures[culture - 1]

                # Get area
                area = getTotalArea()
                if area == -1: continue
                if area == 0:
                    active = False
                    continue
                currentArea = area

                # Calculate data and show results
                setCalculatedPlantingArea(index)
                showResult(calculatedPlantingAreas[index])
                resetCurrentStatus()
            if userInput == 4: phase = 4

            if userInput == 5: phase = 5
        case 4:
            clearTerminal()
            exportData()
            print('Tecle enter para continuar')
            input()
            phase = 3
        case 5:
            clearTerminal()
            showResumedData()
            userInput = getCalculatedPlantingAreaIndex("deletar")
            if userInput == -1: continue
            if userInput == 0:
                active = False
                continue
            if userInput < 0 or userInput > len(calculatedPlantingAreas):
                showInvalidInput()
                continue
            index = userInput - 1

            removed = calculatedPlantingAreas.pop(index)
            print("\nDados removidos com sucesso.")
            showResult(removed)
            print("\nTecle enter para continuar")
            input()
            clearTerminal()
            phase = 3

            


