#note to self: need to make a class and object to store all of these variables
import random       #used for random number generation


class Game:
    def __init__(self):
        self.score = 0
        self.dice = [0, 0, 0, 0, 0]                         # values of individual die
        self.holds = [False, False, False, False, False]    # marks which dice are being held
        self.chances = 3                                    # number of times to roll dice
        self.table = []
        self.switch = False                                 #to indicate if the score has changed
        for i in range(13):
            self.table.append(False)

    def next(self):
        self.switch = False
        self.holds = [False, False, False, False, False]


def mainmenu():
    n = -1
    while n != 0:
        print("Welcome. This is Yahtzee!\n"
              "Press 1 for new game\n"
              "Press 2 to see high scores\n"
              "Press 0 to exit.")
        try:
            n = int(input())
        except:
            print("Invalid input\n")
            continue        #start at the beginning
        if n == 1:
            startgame()
        # if n == 2:
    return


def startgame():
    stat = Game()
    loop = True                 # will be false for bad input by player
    num = -1                    # number to add to score

    for x in range(13):
        for n in range(stat.chances):
            # roll dice
            stat.dice = roll(stat.dice, stat.holds)
            # option (hold/continue = 1/score = 0)
            if n < stat.chances - 1 and stat.switch == False:       # switch indicates if score already taken
                stat.holds = hold(stat.dice, stat.holds)
                # determine whether or not you are done rolling and would like to add to score
                while loop:
                    yn = input("Would you like to choose a score option?(y/n)")
                    if yn == 'Y' or yn == 'y':
                        stat = addscore(stat, True)     # True means able to return and reroll
                        if stat.switch == True:         # If an option was picked
                            break
                    elif yn == 'N' or yn == 'n':
                        break
                    else:
                        print("Invalid input. Please enter a 'y' or a 'n'")
            else:
                print_set(stat.dice, stat.holds)
                stat = addscore(stat, False) # False means -1 not allowed, must return score
        # reset everything and print score
        stat.next()
        print(f"Score: {stat.score}")



def get_upper(dice, value):
    score = 0
    for i in dice:
        if i == value:
            score += value
    return score


def of_a_kind(dice, count):
    score = 0
    values = [0, 0, 0, 0, 0, 0]
    for die in dice:
        score += die
        values[die-1] += 1
    for i in values:
        if i >= count:
            return score
    return 0


def full_house(dice):
    values = [0, 0, 0, 0, 0, 0]
    for i in dice:
        values[i - 1] += 1
    for i in values:
        if i == 1:
            return 0
    return 25


def straight(dice, count):
    values = [0, 0, 0, 0, 0, 0]
    start = False
    length = 1
    conversion = {      #number of points you get for given straight length
        4 : 30,
        5 : 40
    }
    for i in dice:
        values[i-1] += 1
    for i in values:
        if i > 0:
            if i == 5:
                return conversion[count]
            if start:
                length += 1
            else:
                start = True
        else:
            start = False
            if length < count:
                length = 1
    if length >= count:
        return conversion[count]
    return 0


def yahtzee(dice):
    for i in dice:
        if i != dice[0]:
            return 0
    return 50


def displayscore(dice):
    #----------------
    #render scorecard
    #----------------

    scorecard = []
    # upper section
    for i in range(6):
        scorecard.append(get_upper(dice, i + 1))        # 0-5
    # 3 and 4 of a kind
    scorecard.append(of_a_kind(dice, 3))                # 6
    scorecard.append(of_a_kind(dice, 4))                # 7
    # full house
    scorecard.append(full_house(dice))                  # 8
    # small and large straight
    scorecard.append(straight(dice, 4))                 # 9
    scorecard.append(straight(dice, 5))                 # 10
    # YAHTZEE!
    scorecard.append(yahtzee(dice))                     # 11
    # chance
    scorecard.append(of_a_kind(dice, 0))                # 12

    # --------------
    # show scorecard
    # --------------
    print("showing score")
    # note: make sure to fill with x's for used sections later
    print(f"[1] 1's:    {scorecard[0]}      [7] 3 of a kind:    {scorecard[6]}")
    print(f"[2] 2's:    {scorecard[1]}      [8] 4 of a kind:    {scorecard[7]}")
    print(f"[3] 3's:    {scorecard[2]}      [9] full house:     {scorecard[8]}")
    print(f"[4] 4's:    {scorecard[3]}      [10] small straight: {scorecard[9]}")
    print(f"[5] 5's:    {scorecard[4]}      [11] large straight: {scorecard[10]}")
    print(f"[6] 6's:    {scorecard[5]}      [12] yahtzee!:       {scorecard[11]}")
    print(f"bonus score - 0    [13] chance: {scorecard[12]}")
    return scorecard


def addscore(stat, skippable):
    loop = True
    name = {
        1 : "1's",
        2 : "2's",
        3 : "3's",
        4 : "4's",
        5 : "5's",
        6 : "6's",
        7 : "3 of a kind",
        8 : "4 of a kind",
        9 : "full house",
        10 : "small straight",
        11 : "large straight",
        12 : "yahtzee",
        13 : "chance"
    }
    while loop:
        scoretable = displayscore(stat.dice)
        try:
            if skippable:
                val = int(input("What would you like to use? Enter 0 to return: "))
            else:
                val = int(input("What would you like to use? Input a number: "))
        except:
            print("Invalid input\n")
            continue
        if 0 < val <= 13:
            print(f"Are you sure you would like to use your {name[val]} (y/n)?")
            yn = input()
            loop = not y_or_n(yn)
        elif val == 0 and skippable:
            loop = False
        else:
            print("Invalid input")
    if val != 0:
        stat.switch = True
        stat.table[val - 1] = True
        stat.score += scoretable[val - 1]
    return stat




# prints the dice currently in set with a star alongside each die that is currently being held
def print_set(dice, holds):
    output = '['
    for die, hld in zip(dice, holds):
        output = output + str(die)
        if hld:
            output = output + '*'
        output = output + ','
    output += ']'
    print(output)


def hold(dice, holds):
    n = -1
    newholds = holds
    while n != 0:
        print_set(dice, holds)
        print("Select dice to hold(1-5)\nInput '0' if done")
        try:
            n = int(input())
        except:
            print("Invalid input\n")
            continue                        #start at the beginning
        if 0 < n <= 5:
            newholds[n-1] = not newholds[n-1]       #invert hold on die
    return newholds


def roll(dice, holds):
    newdie = []
    print("Rolling dice...\n")
    for die, hld in zip(dice, holds):
        if not hld:
            newdie.append(random.randrange(6) + 1)
        else:
            newdie.append(die)
    return newdie


def y_or_n(i):
    while True:
        if i == 'Y' or i == 'y':
            return True
        elif i == 'N' or i == 'n':
            return False
        else:
            i = input("Invalid input. Please enter 'y' or 'n'.")




mainmenu()
