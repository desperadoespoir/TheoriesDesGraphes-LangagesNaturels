######################################################################
# Auteurs  : Sanyan Obossou Ema-Wo  -  1780896
#            Billy Bouchard         -  1850477
#            Gnaga Dogbeda Georges  -  1870143
# Version Python: 3.6 (32-bits)
######################################################################
from graph import Graph
from graph import Node
from graph import Arc
from djikstra import djikstra
import re
import os.path
from six.moves import reduce
from six.moves import input


def readNodeLine(line):
    ######################################################################
    # This function read a line of the style "1,2\n" and returns
    # a node object from it
    ######################################################################
    firstNumber = True
    nodeid = ""
    hasStation = ""
    for char in line:
        if char == ",":
            firstNumber = False
            continue
        if firstNumber:
            nodeid += char
        if not(firstNumber):
            hasStation += char
    nodeid = int(nodeid)
    hasStation = hasStation == '1\n'
    return Node(nodeid, hasStation)


def readArcLine(line, graph):
    ######################################################################
    # this function read a line of format : "1,4,7\n" and return an arc
    # object out of it. It needs a group of preexisting node to work
    ######################################################################
    variables = ["", "", ""]
    current = 0
    for char in line:
        if char == ',':
            current += 1
            continue
        variables[current] += char
    node1 = int(variables[0])
    node2 = int(variables[1])
    time = int(variables[2])
    return Arc(time, graph[node1], graph[node2])


def creerGraph(nomFichier):
    ######################################################################
    # This function read a file and generate a graph from it
    ######################################################################
    graph = Graph()
    fichier = open(nomFichier, "r")
    line = fichier.readline()
    while line != '\n':
        graph << readNodeLine(line)
        line = fichier.readline()
    line = fichier.readline()
    while line != '':
        graph << readArcLine(line, graph)
        line = fichier.readline()
    return graph


def lireGraph(graph):
    ######################################################################
    # This function print a formated string to look like the graph
    ######################################################################
    print("")
    print(20 * "=", "  AFFICHAGE DU GRAPHE DE LA CARTE  ", 20 * "=")
    text = ''
    for nodeId, node in graph.nodes.items():
        text += '(noeud, ' + str(nodeId) + ', ('
        i = False
        for arc in node.arcs:
            if i:
                text += ', '
            else:
                i = True
            text += "(" + str(arc.node1.id if arc.node1.id !=
                              nodeId else arc.node2.id) + ', ' + str(arc.time) + ')'
        text += '))\n'
    print(text)


def plusCourtChemin(graph, startNodeId, endNodeId, vehiculeType):
    ######################################################################
    # Algorithm to select the best company and if the stealing
    # should be done
    ######################################################################
    print("")
    print(10 * "=", " RESULTAT DU PLUS COURT CHEMIN SECURITAIRE OBTENU ", 10 * "=")

    if vehiculeType == "voiture":
        solution = djikstra(graph, startNodeId, endNodeId, 5)
        company = "Cheap Car"
        if solution == []:
            solution = djikstra(graph, startNodeId, endNodeId, 3)
            company = "Super Car"
            if solution == []:
                return "ne pas faire le braquage"
    elif vehiculeType == "pick-up":
        solution = djikstra(graph, startNodeId, endNodeId, 7)
        company = "Cheap Car"
        if solution == []:
            solution = djikstra(graph, startNodeId, endNodeId, 4)
            company = "Super Car"
            if solution == []:
                return "ne pas faire le braquage"
    elif vehiculeType == "fourgon":
        solution = djikstra(graph, startNodeId, endNodeId, 8)
        company = "Cheap Car"
        if solution == []:
            solution = djikstra(graph, startNodeId, endNodeId, 6)
            company = "Super Car"
            if solution == []:
                return "ne pas faire le braquage"
    solution = map(lambda x: str(x.id) + "->", solution)
    answer = "il faut passer par : \n\t\t" + \
        reduce(lambda x, y: x + y, solution)
    answer = re.sub(r'->$', '', answer)
    answer += "\navec" + (" une " if vehiculeType == "voiture" else " un ") + \
        vehiculeType + " de " + company
    return answer


# Text menu to be printed.
def printMenu():
    print("")
    print(35 * "-", "MENU", 35 * "-")
    print("Choisir l'option à excecuter : \n ")
    print("\t 1 pour Mettre à jour la carte")
    print("\t 2 pour Déterminer le plus court chemin sécuritaire")
    print("\t 3 pour Quitter")
    print(76 * "-")


# List of towns to be printed.
def printTowns():
    print("\nListe des villes canadiennes accessibles :")
    print("1 - Montréal         11 - Saskatoon ")
    print("2 - Québec           12 - Calgary")
    print("3 - Ottawa           13 - Vancouver")
    print("4 - Toronto          14 - Edmonton")
    print("5 - Halifax          15 - Fort McMurray")
    print("6 - Sept-Iles        16 - Churchill")
    print("7 - Thunder Bay      17 - Prince George")
    print("8 - Sandy Lake       18 - Fort Nelson")
    print("9 - Winnipeg         19 - Whitehorse")
    print("10 - Regina          20 - Yellowknife")


# choose a town.
def chooseTown():
    townInput = None

    while True:
        try:
            townInput = int(input("Entrez la ville :  "))
        except ValueError:
            printError()
            continue

        if townInput >= 1 and townInput <= 20:
                return townInput

        printError()


# Choose a vehicle.
def chooseVehicle():
    vehicles = ["voiture", "pick-up", "fourgon"]

    print("\nListe des types de véhicules disponibles :")
    for myVehicle in vehicles:
        print(myVehicle)

    while True:
        vehicle = input("Entrez un véhicule  :  ")

        for myVehicle in vehicles:
            if myVehicle == vehicle:
                return myVehicle

        printError()


# Read file.
def setFile():

    fileName = None
    graph = None

    while True:
        try:
            fileName = input(
                "Entrez le nom du fichier de la carte (ex: nomFichier.txt) :  ")
            graph = creerGraph(fileName)
        except:
            printError()
            continue

        return graph


# To be printed for invalid entries.
def printError():
    print("\nEntrée invalide! \nRéessayez avec une entrée valide svp ...\n")


def main():                # Define the main function

    nomFichier = None
    typeVehicule = None
    loop = True
    graph = creerGraph("villes.txt")

    while loop:      # Keep looping until loop == False
        printMenu()   # Displays menu
        choice = input("Entrez votre choix :  ")

        if choice == "1":
            print("\n", 8 * "*", "Mise à jour de la carte ", 8 * "*")
            graph = setFile()
            lireGraph(graph)

        elif choice == "2":
            print("\n", 6 * "*", "Configuarations pour le braquage ", 6 * "*")
            printTowns()
            print(
                "\nEntrez le point de la ville où aura lieu le braquage (ex: 3 pour Ottawa)")
            depart = chooseTown()
            print(
                "Entrez le point de destination après le braquage (ex: 19 pour Whitehorse)")
            arrive = chooseTown()

            typeVehicule = chooseVehicle()

            print(plusCourtChemin(graph, int(depart), int(arrive), typeVehicule))

        elif choice == "3":
            print("\nAu revoir! A bientôt pour le prochain braquage!\n")
            loop = False

        else:
            # Any input other than values 1, 2 or 3 is not allowed.
            printError()


main()      # Invoke the main function
