import random
import os
import time

# Card collection game

#1) Make a class for the different packs : Price | Luck %

global money
money = 100

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
        f.write("\n\n====== PACKS ======\n\n===================\n")
    StarterPack = Packs("Starter Pack",50,1)
    BetterPack = Packs("Better Pack",200,2)
    EpicPack = Packs("Epic Pack",500,5)
    LegendaryPack = Packs("Legendary Pack",500,10)
    GodPack = Packs("God Pack",10000,100)
    AvailablePacks = [StarterPack,BetterPack,EpicPack,LegendaryPack,GodPack]

    indexNum = 1

    with open("Packs.txt", "a") as f:
        for packs in AvailablePacks:
            f.write(f"   | {packs.name}\n {indexNum} | Price : {packs.price}\n   | Luck : {packs.luck}x\n===================\n")
            indexNum += 1

    with open("Packs.txt", "r") as f:
        lines = f.readlines()

    lines[6] = " 1 | Price : 50\n"
    with open("Packs.txt", "w") as f:
        f.writelines(lines)

    return StarterPack,BetterPack,EpicPack,LegendaryPack,GodPack,AvailablePacks

StarterPack,BetterPack,EpicPack,LegendaryPack,GodPack,AvailablePacks = main()

result, idx, baseChance, mutations = StarterPack.openPack()

def CreateCard():
    cards = []
    con = random.randint(1,100)
    rarityDenom = round((100/baseChance[idx])*(con/50),1)
    val = rarityDenom*25
    inc = rarityDenom*5
    rarityString = f"1 in {int(rarityDenom*10)}"
    if result == "Common":
            newCard = Card(
                value = round(val,0),
                income = inc,
                rarity = rarityString,
                condition = con
            )
            mut = False
    else:
        newCard = Mutation(
            value = round(val,0),
            income = rarityDenom,
            rarity = rarityString,
            condition = con,
            mutation = mutations[idx]
        )
        mut = True

    with open("Card.txt", "w") as f:
        f.writelines("==== MY CARD ====\n")
        f.write(f"Rarity | {newCard.rarity}\nCondition | {newCard.condition}\nValue | {newCard.value}\nIncome | {newCard.income}\n")
        if mut == True:
            f.write(f"Mutation | {newCard.mutation}")

    cards.append(newCard)

def sellCard():
    if os.path.exists("Card.txt"):
        os.remove("Card.txt")
    else:
        with open("Menu.text", "a") as f:
            f.writelines("No card to sell")

def Menu():
    while True:
        with open("Menu.txt", "w") as f:
            f.write(f"\n\n===== MENU =====\n1 : Open Pack\n2 : Sell Card\n================\nMoney : {money}\n================\n")

        passed = False

        notnum = False

        while True:
            choice = input("What option do you want to select >> ")
            if passed:
                with open("Menu.txt", "r") as f:
                    menuLines = f.readlines()

                menuLines[8] = ""
                if notnum:
                    menuLines[9] = ""
                    notnum = False

                with open("Menu.txt", "w") as f:
                    f.writelines(menuLines)
            passed = True
            try:
                int(choice)
            except:
                with open("Menu.txt", "a") as f:
                    f.writelines("Enter a number\n")
                    notnum = True
            if choice == "1":
                main()
                while True:
                    try:
                        packChoice = int(input("What pack do you want to open >> "))
                        if packChoice >= 1 and packChoice <= 5:
                            break
                        else:
                            print("1 / 2 / 3 / 4 / 5")
                    except:
                        print("Enter a number")
                        continue
                CreateCard()
                with open("Menu.txt", "a") as f:
                    f.writelines(f"Opened a {AvailablePacks[packChoice-1].name}")
                time.sleep(2)
                break
            elif choice == "2":
                sellCard()
                with open("Menu.txt", "a") as f:
                    f.writelines("Card Sold")
                time.sleep(2)
                break
            else:
                with open("Menu.txt", "a") as f:
                    f.writelines("1 or 2")


Menu()

