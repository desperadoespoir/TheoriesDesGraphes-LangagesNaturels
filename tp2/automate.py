class Automate(object):
    """Une class automate qui permet de lire des solutions
       on peut y ajouter une regle
       on peut aussi resoudre avec la fonction solve et un mot de passe

    """
    END = -1
    NOT_FOUND = 0
    START = ""

    def __init__(self, name):
        self.name = name
        self.regles = {}

    def __lshift__(self, regle):
        passed_equal = False
        first_char = True
        key = ""
        result = ""
        for char in regle:
            if char == '=':
                passed_equal, first_char = True, True
            elif first_char:
                first_char = not first_char
            elif not passed_equal:
                key += char
            else:
                result += char
        if (key not in self.regles) or (self.regles[key] == Automate.END):
            self.regles[key] = [result]
        else:
            self.regles[key] += [result]
        self.regles[result] = Automate.END

    def __contains__(self, item):
        return item in self.regles

    def __getitem__(self, key):
        return self.regles[key]

    def solve(self, string):
        i = 0
        substr = string[i]
        while substr != Automate.END and substr != Automate.NOT_FOUND:
            if substr in self.regles:
                if self.regles[substr] == Automate.END:
                    substr = Automate.END
                elif i >= len(string):
                    substr = Automate.NOT_FOUND
                else:
                    i += 1
                    substr += string[i]
            else:
                substr = Automate.NOT_FOUND

        return substr != Automate.NOT_FOUND
