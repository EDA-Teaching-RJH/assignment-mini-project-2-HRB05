import random

# Card collection game

#1) Make a class for the different packs : Price | Luck %

class Packs:
    def __init__(self,price,luck):
        self.price = price
        self.luck = luck

    global mutations
    mutations = ["Common","Gold","Diamond","Unreal","God"]
    global weights
    weights = [68.99,25,5,1,0.01] # Weights to get each mutation with a pack luck of 1

    global result 
    result = random.choices(mutations, weights=weights, k=1)[0]
    global idx
    idx = mutations.index(result)

#2) Make a class for base cards : Value | Rarity | Condition

class Card:
    def __init__(self,value,income,rarity,condition):
        self.value = value
        self.income = income
        self.rarity = rarity
        self.condition = condition

# Child classes will be cards with mutations and higher rarity

class Mutation(Card):
    def __init__(self,value,income,rarity,condition,mutation):
        super().__init__(value, income, rarity, condition)
        self.mutation = mutation


cards = []
con = random.randint(1,100)
rarityDenom = round((100/weights[idx])*(con/100),1)
val = rarityDenom*10
inc = rarityDenom
if (rarityDenom) <= 1:
     rarityDenom = 1
rarityString = f"1/{rarityDenom}"
if result == "Common":
        newCard = Card(
            value = val,
            income = inc,
            rarity = rarityString,
            condition = con
        )
        mut = False
else:
    newCard = Mutation(
          value = val,
          income = rarityDenom,
          rarity = rarityString,
          condition = con,
          mutation = mutations[idx]
     )
    mut = True

print(f"Rarity | {newCard.rarity}\nCondition | {newCard.condition}\nValue | {newCard.value}\nIncome | {newCard.income}")
if mut == True:
     print(f"Mutation | {newCard.mutation}")