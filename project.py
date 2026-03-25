import random

# Card collection game

#1) Make a class for the different packs : Price | Luck %

class Packs:
    def __init__(self,name,price,luck):
        self.name = name
        self.price = price
        self.luck = luck
    
    def openPack(self):
        mutations = ["Common","Gold","Diamond","Unreal","God"]
        baseChance = [68.99,25,5,1,0.05] # Realised i would need this to calculate the rarity

        weights = [(baseChance[0]/self.luck),baseChance[1]/(self.luck*1.5),baseChance[2]*(self.luck/1.5),baseChance[3]*self.luck,baseChance[4]*(self.luck*1.5)] # Weights to get each mutation with a pack luck of 1
        # Weights now private so it doesnt change outside the class
    
        result = random.choices(mutations, weights=weights, k=1)[0]
        idx = mutations.index(result)
        return result, idx, baseChance, mutations

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



def main():
    # Code for packs
    with open("Packs.txt", "w") as f:
        f.write("\n\n=== PACK MENU ===\n\n=================\n")
    StarterPack = Packs("Starter Pack",50,1)
    BetterPack = Packs("Better Pack",200,2)
    EpicPack = Packs("Epic Pack",500,5)
    LegendaryPack = Packs("Legendary Pack",500,10)
    GodPack = Packs("God Pack",10000,100)
    AvailablePacks = [StarterPack,BetterPack,EpicPack,LegendaryPack,GodPack]
    with open("Packs.txt", "a") as f:
        for packs in AvailablePacks:
            f.write(f"{packs.name}\nPrice : {packs.price}\nLuck : {packs.luck}x\n=================\n")
    with open("Packs.txt", "r") as f:
        lines = f.readlines()

    lines[6] = "Price : 50\n"
    with open("Packs.txt", "w") as f:
        f.writelines(lines)

    return StarterPack,BetterPack,EpicPack,LegendaryPack,GodPack

StarterPack,BetterPack,EpicPack,LegendaryPack,GodPack = main()
result, idx, baseChance, mutations = GodPack.openPack()

def CreateCard():
    cards = []
    con = random.randint(1,100)
    rarityDenom = round((100/baseChance[idx])*(con/50),1)
    val = rarityDenom*25
    inc = rarityDenom*5
    rarityString = f"1 in {int(rarityDenom*10)}"
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

    cards.append(newCard)

CreateCard()
