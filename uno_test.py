import random
import time


color = ('RED','GREEN','BLUE','YELLOW')
rank = ('0','1','2','3','4','5','6','7','8','9','Skip','Reverse','Draw2','Draw4','Wild')
ctype = {'0':'number','1':'number','2':'number','3':'number','4':'number','5':'number','6':'number',
            '7':'number','8':'number','9':'number','Skip':'action','Reverse':'action','Draw2':'action',
            'Draw4':'action_nocolor','Wild':'action_nocolor'}


class Card:

    def init(self, color, rank):
        self.rank = rank
        if ctype[rank] == 'number':
            self.color = color
            self.cardtype = 'number'
        elif ctype[rank] == 'action':
            self.color = color
            self.cardtype = 'action'
        else:
            self.color = None
            self.cardtype = 'action_nocolor'

    def str(self):
        if self.color == None:
            return self.rank
        else:
            return self.color + " " + self.rank


class Deck:

    def init(self):
        self.deck = []
        for clr in color:
            for ran in rank:
                if ctype[ran] != 'action_nocolor':
                    self.deck.append(Card(clr, ran))
                    self.deck.append(Card(clr, ran))
                else:
                    self.deck.append(Card(clr, ran))

    def str(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.str()
        return 'The deck has ' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()



class Hand:

    def init(self):
        self.cards = []
        self.cardsstr = []
        self.number_cards = 0
        self.action_cards = 0

    def add_card(self, card):
        self.cards.append(card)
        self.cardsstr.append(str(card))
        if card.cardtype == 'number':
            self.number_cards += 1
        else:
            self.action_cards += 1

    def remove_card(self, place):
        self.cardsstr.pop(place - 1)
        return self.cards.pop(place - 1)

    def cards_in_hand(self):
        for i in range(len(self.cardsstr)):
            print(f' {i + 1}.{self.cardsstr[i]}')

    def single_card(self, place):
        return self.cards[place - 1]

    def no_of_cards(self):
        return len(self.cards)
