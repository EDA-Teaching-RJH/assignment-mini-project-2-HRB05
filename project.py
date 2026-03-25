import random

# Card collection game

#1) Make a class for the different packs : Price | Luck %

class Packs:
    def __init__(self,price,luck):
        self.price = price
        self.luck = luck

    mutations = ["Common","Gold","Diamond","Unreal","God"]
    global weights
    weights = [68.99,25,5,1,0.01] # Weights to get each mutation with a pack luck of 1

    global result 
    result = random.choices(mutations, weights=weights, k=1)[0]
    global idx
    idx = mutations.index(result)
    print(result,idx)

#2) Make a class for base cards : Value | Rarity | Condition

class Card:
    def __init__(self,value,income,rarity,condition):
        self.value = value
        self.income = income
        self.rarityVal = rarity
        self.condition = condition

# Child classes will be cards with mutations and higher rarity

class Mutation(Card):
    def __init__(self,value,income,rarity,condition,mutation,rarityx):
        super().__init__(value, income, rarity, condition)
        self.mutation = mutation
        self.rarityx = rarityx
        self.rarity = float(self.rarityVal*self.rarityx)

cards = []
con = random.randint(1,100)
print(con)
rarityDenom = round((100/weights[idx])*(con/100),1)
if (rarityDenom) <= 1:
     rarityDenom = 1
rarityString = f"1/{rarityDenom}"
print(rarityString)
if result == "Common":
        newCard = Card(
            value = (10*(con/50)), # Means that the value is only increased if condition >= 50
            income = 1,
            rarity = rarityString
        )