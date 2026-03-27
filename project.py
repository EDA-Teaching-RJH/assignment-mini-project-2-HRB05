import random
import os
import time
import re

# Card collection game

#1) Make a class for the different packs : Price | Luck %

money = 100 # Starting money
with open("Card.txt", "w") as f:
    f.write("")
os.remove("Card.txt")  # Resets the card if restarting the game

class Packs:
    def __init__(self,name,price,luck):
        self.name = name
        self.price = price # Sets all the variables for the class
        self.luck = luck
    
    def openPack(self):
        mutations = ["Common","Gold","Diamond","Unreal","God"]
        baseChance = [68.99,25,5,1,0.05] # Realised I would need this to calculate the rarity

        weights = [(baseChance[0]/self.luck),baseChance[1]/(self.luck*1.5),baseChance[2]*(self.luck/1.5),baseChance[3]*self.luck,baseChance[4]*(self.luck*1.5)] # Weights to get each mutation with a pack luck of 1
        # Weights now private so it doesnt change outside the class
    
        result = random.choices(mutations, weights=weights, k=1)[0]
        idx = mutations.index(result) # Get the index of the mutation so I can use it later 
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
        super().__init__(value, income, rarity, condition) # Inherits all the propeties and methods from the parent class
        self.mutation = mutation



def main():
    # Code for packs
    with open("Packs.txt", "w") as f:
        f.write("\n\n====== PACKS ======\n\n===================\n")
    StarterPack = Packs("Starter Pack",50,1)
    BetterPack = Packs("Better Pack",200,2)        # Creating all the packs using the Packs class
    EpicPack = Packs("Epic Pack",500,5)
    LegendaryPack = Packs("Legendary Pack",2500,10)
    GodPack = Packs("God Pack",10000,100)
    AvailablePacks = [StarterPack,BetterPack,EpicPack,LegendaryPack,GodPack]   # Creating a list of the packs so the choice can be made easily

    indexNum = 1 # Set the index number so the packs have their corresponding number next to them in the pack menu

    with open("Packs.txt", "a") as f:
        for packs in AvailablePacks:
            f.write(f"   | {packs.name}\n {indexNum} | Price : {packs.price}\n   | Luck : {packs.luck}x\n===================\n") # Writing all the packs to the txt file
            indexNum += 1

    with open("Packs.txt", "r") as f:
        lines = f.readlines()      # Read each line and put it in an array

    lines[6] = " 1 | Price : 50\n"   # Editting the first indexed the so that the price shows correctly
    with open("Packs.txt", "w") as f:   
        f.writelines(lines)    # Writes all the text back with the updated line

    return StarterPack,BetterPack,EpicPack,LegendaryPack,GodPack,AvailablePacks

StarterPack,BetterPack,EpicPack,LegendaryPack,GodPack,AvailablePacks = main()

def sellCard():
    global money
    noCard = False
    if os.path.exists("Card.txt"):    # Checking if the user actually has a card
        with open("Card.txt", "r") as f:
            lines = f.readlines()
            valueCard = re.findall(r'-?\d*\.?\d+', lines[3])   # Reads the card txt file to get the value of the card
            money += float(valueCard[0])   # Adds the value of the card to the users money
            print(f"You now have {round(money,1)} money")
        os.remove("Card.txt")
    else:
        with open("Menu.txt", "a") as f:
            f.writelines("No card to sell")
        noCard = True
    return noCard

def earning():
    global money
    with open("Card.txt", "r") as f:
        lines = f.readlines()
        incomeCard = re.findall(r'-?\d*\.?\d+', lines[4])  # Finds the income value of the card for the passive earning
    ans = int(input("How long do you want to earn for >> ")) # Asks the user how long they want to earn for
    for i in range(ans):
        money += float(incomeCard[0])
        time.sleep(1)                    # Earns 1 income per second for how long the user wants
        print(round(money,1))
        i += 1

def Menu():
    global money
    print(f"Money : {round(money,1)}")
    while True:
        with open("Menu.txt", "w") as f:
            f.write(f"\n\n===== MENU =====\n1 : Open Pack\n2 : Sell Card\n3 : Earn Money\n================\n")  # Writes the menu to the txt file

        passed = False

        notnum = False
        
        choice = input("What option do you want to select >> ")
        if passed:
            with open("Menu.txt", "r") as f:
                menuLines = f.readlines()

            menuLines[7] = ""     # Gets rid of the error messages i coded in later
            if notnum:
                menuLines[8] = ""
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
                        if money - AvailablePacks[packChoice-1].price >= 0:      # Checks if the user has enough money to buy the selected pack
                            money = money - AvailablePacks[packChoice-1].price      # Takes away the price of the picked pack from the users money
                            print(f"You now have {round(money,1)} money")
                            openedPack = True
                            break
                        else:
                            money = money
                            print(f"Not enough money. You have {round(money,1)} money") 
                    else:
                        print("1 / 2 / 3 / 4 / 5")
                except:
                    print("Enter a number")
                    continue
            with open("Menu.txt", "a") as f:
                f.writelines(f"Opened a {AvailablePacks[packChoice-1].name}") # Confirms the pack that the user selected has been opened
            print("Opening")
            time.sleep(3)
            break
        elif choice == "2":
            openedPack = False
            noCard = sellCard()
            if not noCard:
                with open("Menu.txt", "a") as f:
                    f.writelines("Card Sold")
                time.sleep(3)
                break
        elif choice == "3":
            openedPack = False
            try:
                earning()
            except:
                print("No card to earn from")
                continue
            break
        else:
            with open("Menu.txt", "a") as f:
                f.writelines("1 or 2")
    if openedPack:
        return packChoice, openedPack
    else:
        return 0, False
    
packChoice, openedPack = Menu()

result, idx, baseChance, mutations = AvailablePacks[packChoice-1].openPack()

def CreateCard():
    con = random.randint(1,100)
    rarityDenom = round((100/baseChance[idx])*(con/50),1)
    val = rarityDenom*25
    inc = rarityDenom*5
    rarityString = f"1 in {int(rarityDenom*10)}"       # Code for creating the basic card without any mutations
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
            income = rarityDenom,           # Code for creating the card with any mutation
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
    return newCard

CreateCard()
while True:
    packChoice, openedPack = Menu()
    result, idx, baseChance, mutations = AvailablePacks[packChoice-1].openPack()  # Loops the whole game so the player can collect the best card they can
    if openedPack:
        CreateCard()