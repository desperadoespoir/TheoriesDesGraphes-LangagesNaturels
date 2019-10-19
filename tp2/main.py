from automate import *
from solution import *


def creerAutomate(file_name):
    ######################################################################
    #    Permet la creation d,un Automate et lui passe les
    #    resultats des calculs
    ######################################################################
    file = open(file_name, 'r')
    name = file.readline().replace("\n", "")
    automate = Automate(name)
    for line in file:
        automate << (line.replace("\n", ""))
    return automate


def trouverMotDePasse(variantes, no):
    ######################################################################
    #    Utilise l'automate numero no pour trouver le
    #    mot de passe parmis les variantes
    ######################################################################
    solver = automates[no]
    for var in variantes:
        if solver.solve(var):
            return var


def traiterLesEntrees(file_name):
    ######################################################################
    #    Creer une solution non resolue avec la liste de variantes
    ######################################################################
    file = open(file_name, 'r')
    no = file.readline().replace("\n", "")
    solution = Solution(no)
    for line in file:
        solution << line.replace("\n", "")
    return solution


def afficherLesMotsDePasse():
    ######################################################################
    #    Affiche les solution trouver et non trouvee
    ######################################################################
    for no in solutions:
        print(solutions[no])


def menu(erreur):
    ######################################################################
    #    Fonction d'affichage du menu
    ######################################################################
    get = None
    if erreur:
        print("Cette fonction n'existe pas! veillez entrer une fonction valide")
        print(" Exemple: entrer 'a' pour creer un automate\n")

    print("=" * 20 + " Menu " + 20 * "=")
    print("Que voulez vous faire?")
    print("  (a) Creer l'automates")
    print("  (b) Traiter des requetes")
    print("  (c) Afficher les mots de passe valides obtenus")
    print("  (d) Quitter")
    return input("")


def VariantesFichiers():
    ######################################################################
    #    Fonction d'impression des noms de fichiers de variantes
    ######################################################################
    print("\nliste de fichiers de variantes disponible \n")
    print("=> variantes1.txt")
    print("=> variantes2.txt")
    print("=> variantes3.txt")
    print("=> variantes4.txt")
    print("=> variantes5.txt")


def reglesFichiers():
    ######################################################################
    #    Fonction d'impression des noms de fichiers de regles
    ######################################################################
    print("\nliste de Fichiers de regles disponible \n")
    print("=> regles1.txt")
    print("=> regles2.txt")
    print("=> regles3.txt")
    print("=> regles4.txt")
    print("=> regles5.txt")


def ln():
    ######################################################################
    #    Permet de mettre 80 retour de ligne pour
    #    enlever tout les affichage visuel inutile
    ######################################################################
    print("\n" * 80)


def verificationVFichiers(file_name):
    ######################################################################
    #    verifie si le fichier existe
    ######################################################################
    if(file_name == "variantes1.txt" or file_name == "variantes2.txt" or file_name == "variantes3.txt" or file_name == "variantes4.txt" or file_name == "variantes5.txt"):
        return True
    return False


def verificationRFichiers(file_name):
    ######################################################################
    #    verifie si le fichier existe
    ######################################################################
    if(file_name == "regles1.txt" or file_name == "regles2.txt" or file_name == "regles3.txt" or file_name == "regles4.txt" or file_name == "regles5.txt"):
        return True
    return False

######################################################################
#    definition des variables
######################################################################


automates = {}
solutions = {}
get = ""
repR = False
repV = False
erreur = False


######################################################################
#    Code principal
######################################################################

while get != "d":
    get = menu(erreur)
    if get == 'a':
        erreur = False
        reglesFichiers()
        file_name = input("\n veillez entrer le nom du fichier choisi :: ")
        repR = verificationRFichiers(file_name)
        while repR == False:
            print(
                "\nil ne s'agit pas d'un fichier de regles, veillez entrez un bon fichier svp")
            reglesFichiers()
            file_name = input("veillez entrer le nom du fichier choisi :: ")
            repR = verificationRFichiers(file_name)
        automate = creerAutomate(file_name)
        automates[automate.name] = automate
        print("\n=> super! vous pouvez maintenant traiter des requetes en entrant 'b' ")

    elif get == 'b':
        erreur = False
        VariantesFichiers()
        file_name = input("\n veillez entrer le nom du fichier choisi :: ")
        repV = verificationVFichiers(file_name)
        while repV == False:
            print(
                "\nil ne s'agit pas d'un fichier de variante, veillez entrez un bon fichier svp")
            VariantesFichiers()
            file_name = input("veillez entrer le nom du fichier choisi : ")
            repV = verificationVFichiers(file_name)
        solution = traiterLesEntrees(file_name)
        solutions[solution.no] = solution
        print(
            "\n=> super! vous pouvez maintenant afficher les mots de passe en entrant 'c' ")
        if solution.no not in automates:
            input(
                "\nAucun automate n'existe pour cette solution ,veillez en creer un d'abord! ")
        else:
            solutions[solution.no].reponse = trouverMotDePasse(
                solutions[solution.no].variantes, solution.no)

    elif get == 'c':
        erreur = False
        if repR and repV:
            print("\nMot de passe : ")
            afficherLesMotsDePasse()
            input("\n appuyer la touche entrez")
        else:
            print(
                " => veillez creer des atomates et traiter des requette d'abord. Merci! ")

    else:
        erreur = True

print("Merci!")
