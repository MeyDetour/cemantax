import spacy
from flask import session
import random

llm = spacy.load("en_core_web_lg")

fr_words = [
    "ordinateur", "lampe", "chaussure", "montagne", "pyramide", "village",
    "livre", "carte", "plafond", "fleur", "bouteille", "cuisine", "jardin",
    "voiture", "brouillard", "horloge", "poisson", "table", "chaise",
    "fenetre", "soleil", "baleine", "ballon", "pluie", "bicyclette",
    "tapis", "chocolat", "camera", "calendrier", "statue", "feuille",
    "television", "toile", "brouette", "armoire", "volcan", "rivière",
    "bateau", "lune", "bureau", "oiseau"
]


class Game:
    def __init__(self):
        self.secret_word = ""

    def start_game(self):
        if not 'words' in session or not "last_element" in session or not "said" in session:

            session['words'] = []
            session['last_element'] = None
            session['said'] = []
            self.secret_word = random.choice(fr_words)
            print("SECRET WORD ::", self.secret_word)

    def get_words(self):
        return session['words']
    def get_words_said(self):
        return session['said']
    def get_last_said(self):
        return session['last_element']


    def run(self, given_word):

        for word_tuple in session['words']:
            if word_tuple[0] == self.secret_word:
                return True
        print(given_word, "is (1) ", self.secret_word, "?")

        # compare
        token_secret_word = llm(self.secret_word)
        token_given_word = llm(given_word)
        similarity = token_given_word.similarity(token_secret_word)
        similarity = round(similarity * 100, 2)
        session['said'].append(given_word)
        session['words'].append((given_word, similarity))
        session['last_element'] = given_word
        session['words'] = sorted(  session['words'], key= lambda word : word [1] , reverse=True)

        print(given_word,"is ",self.secret_word,"?")
        if given_word == self.secret_word :
            return  True


        return False
