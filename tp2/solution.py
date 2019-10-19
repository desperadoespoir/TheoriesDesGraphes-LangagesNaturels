class Solution:
    """
    Une classe permettant de garder une liste de mots de passe a resoudre
    """

    def __init__(self, no):
        self.no = no
        self.variantes = []
        self.reponse = None

    def __lshift__(self, item):
        self.variantes.append(item)

    def __str__(self):
        return self.no + ". " + ("No password found" if not self.reponse else self.reponse)
