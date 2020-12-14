import pygame, math, sys, random, time, os
import sqlite3 as lite
from pygame.locals import *
pygame.init()

#Alot of things such as combat log, player control, arena and campagin where added as after thoughts
#Orginally the units where just going to be coloured blocks but a friend of mine drew some units for me so now they are pictures
#but im too lazy to remove all the colour refrences stored in my arrays and classes 

#Team 1 is player army with team 2 being the computers
#BattleStatus keeps track of what units are in which position on the grid during a battle


#Pygamebackground intial
x = 10
y = 30
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

Screen = pygame.display.set_mode((1200,600), 0, 32)
WHITE = (255,255,255)
NOTWHITE = (254,254,254)
RED = (255,0,0)
BLACK = (0,0,0)
GREEN = (0,255,0)
LIGHTGREEN = (0,150,0)
DARKGREEN = (34,139,34)
BLUE = (0,0,255)
LIGHTBLUE = (50,170,220)
GREY = (192,192,192)
PURPLE = (255,0,255)
YELLOW = (255,255,0)
BROWN = (210,105,30)
font = pygame.font.SysFont('Calibri', 10, True, False)
Mediumfont = pygame.font.SysFont('Calibri', 20, True, False)
Bigfont = pygame.font.SysFont('Calibri', 30, True, False)
Button = pygame.image.load("Misc/Button.png")
SmallButton = pygame.image.load("Misc/ButtonSmall.png")
BackButton = pygame.image.load("Misc/BackButton.png")
Background = pygame.image.load("Misc/NotBlured.jpg")
#LableSword = pygame.image.load("Misc/SwordSmall.png")
LableSword = pygame.image.load("Misc/NormalSword.png")
HighlightedSword = pygame.image.load("Misc/Highlighted.png")
Unitcard = pygame.image.load("Misc/Unitcard.png")
MeleeSymbol = pygame.image.load("Misc/MeleeAttack.png")
RangedSymbol = pygame.image.load("Misc/RangedAttack.png")
StatsCard = pygame.image.load("Misc/StatsCard.png")
Coin =  pygame.image.load("Misc/Coin.png")
ScorePicture =  pygame.image.load("Misc/Score.png")
PowerPicture =  pygame.image.load("Misc/Power.png")
Pointer =  pygame.image.load("Misc/Pointer.png")
Scroll = pygame.image.load("Misc/Scroll.png")



#Tile Stuff
Grass1 = pygame.image.load("Tiles/Grass1.jpg")
Grass2 = pygame.image.load("Tiles/Grass2.jpg")
Grass3 = pygame.image.load("Tiles/Grass3.jpg")
Grass4 = pygame.image.load("Tiles/Grass4.jpg")
Tiles = [Grass1,Grass2,Grass3,Grass4]

#Unit Pictures
SwordsmanPicture = pygame.image.load("Units/Swordsman.png")
ArcherPicture = pygame.image.load("Units/Archer.png")
BeserkerPicture = pygame.image.load("Units/Beserker.png")
CatapultPicture = pygame.image.load("Units/Catapult.png")
CavalryPicture = pygame.image.load("Units/Cavalry.png")
NinjaPicture = pygame.image.load("Units/Ninja.png")
PikemanPicture = pygame.image.load("Units/Pikeman.png")
SpearmanPicture = pygame.image.load("Units/Spearman.png")
HealerPicture = pygame.image.load("Units/Healer.png")
SamuraiPicture = pygame.image.load("Units/Samurai.png")
CastlePicture = pygame.image.load("Units/Castle.png")
CastlePicture= pygame.transform.scale(CastlePicture, (45, 45))
PlayerPicture = pygame.image.load("Units/Player.png")
PaladinPicture = pygame.image.load("Units/Paladin.png")

#grid intial
width = 40
height = 40
marginwidth = 5
marginheigth = 5
MainScreenX = 30
MainScreenY = 15
BattleScreenX = 20
BattleScreenY = 5
ArmySizeX = 6
ArmySizeY = 5
BattleStatus = [ [0]*(BattleScreenY) for _ in range(BattleScreenX) ]
CreateArmyGrid = [ [0]*(ArmySizeY) for _ in range(ArmySizeX) ]
TileStatus = [ [0]*(50) for _ in range(50) ]

#game intials
global Multiplier
Multipler = 1
Identification = 0

#Sounds and music
AfterBattle = pygame.mixer.Sound("Sounds/AfterBattle.wav")
AttackSound = pygame.mixer.Sound("Sounds/AttackSound.wav")
SelectSound = pygame.mixer.Sound("Sounds/Select.wav")
HealSound = pygame.mixer.Sound("Sounds/Heal.wav")

#Function for creating a grid (just a bunch of tiles) to place units on for a battle
def setupgrid(xGrid,yGrid,Start=0,Setup = True): #Create a grid
    Screen.blit(pygame.transform.scale(Background, (1200, 600)), (0, 0))
    for x in range(xGrid):#Place squares
        for y in range(yGrid):
            marginwidth = 5 + (40*x) + (5*x) + (Start*width)
            marginheigth = 5 + (40*y) + (5*y) + (Start*height)
            if Setup:
                n = random.randint(0,3)
                Grass = Tiles[n]
                TileStatus[x][y] = n
                Screen.blit(pygame.transform.scale(Grass, (40, 40)), (marginwidth, marginheigth))
            else:
                n =  TileStatus[x][y]
                Grass = Tiles[n]
                Screen.blit(pygame.transform.scale(Grass, (40, 40)), (marginwidth, marginheigth))
    pygame.display.update()

#Place a unit on a specified tile with its health bar
def PlaceUnit(xline,yline,Unit,Team,DamageTaken = 0,Start =0, Dumber = False): #Place a unit on the grid 
    if (Team == 1 or Team == 2) and Unit.Name != "Catapult":
        BattleStatus[xline][yline] = (Unit.Colour,Unit.Name,(Unit.Health-DamageTaken),Team)
    if (Team == 1 or Team == 2) and Unit.Name == "Catapult":
        if Dumber:
            BattleStatus[xline][yline] = (Unit.Colour,Unit.Name,(Unit.Health-DamageTaken),Team,BattleStatus[xline][yline][4])
        else:
            BattleStatus[xline][yline] = (Unit.Colour,Unit.Name,(Unit.Health-DamageTaken),Team,0)


    if Team == 0:
        CreateArmyGird[xline][yline] = (Unit.Colour,Unit.Name,(Unit.Health-DamageTaken),Team)

    marginwidth = 5 + (40*xline) + (5*xline) + (Start*width)
    marginheigth = 5 + (40*yline) + (5*yline) + (Start*height)
    if Unit == Swordsman:
        if Team == 1:
            Screen.blit(SwordsmanPicture, (marginwidth, marginheigth-10))
        else:
            Screen.blit(pygame.transform.flip(SwordsmanPicture, True, False), (marginwidth, marginheigth-10))
    elif Unit == Archer:
        if Team == 1:
            Screen.blit(ArcherPicture, (marginwidth, marginheigth-10))
        else:
            Screen.blit(pygame.transform.flip(ArcherPicture, True, False), (marginwidth, marginheigth-10))
    elif Unit == Beserker:
        if Team == 1:
            Screen.blit(BeserkerPicture, (marginwidth, marginheigth-10))
        else:
            Screen.blit(pygame.transform.flip(BeserkerPicture, True, False), (marginwidth, marginheigth-10))
    elif Unit == Cavalry:
        if Team == 1:
            Screen.blit(CavalryPicture, (marginwidth, marginheigth-10))
        else:
            Screen.blit(pygame.transform.flip(CavalryPicture, True, False), (marginwidth, marginheigth-10))
    elif Unit == Catapult:
        if Team == 1:
            Screen.blit(CatapultPicture, (marginwidth, marginheigth+5))
        else:
            Screen.blit(pygame.transform.flip(CatapultPicture, True, False), (marginwidth, marginheigth+5))
    elif Unit == Ninja:
        if Team == 1:
            Screen.blit(NinjaPicture, (marginwidth, marginheigth))
        else:
            Screen.blit(pygame.transform.flip(NinjaPicture, True, False), (marginwidth, marginheigth))
    elif Unit == Pikeman:
        if Team == 1:
            Screen.blit(PikemanPicture, (marginwidth, marginheigth))
        else:
            Screen.blit(pygame.transform.flip(PikemanPicture, True, False), (marginwidth, marginheigth))
    elif Unit == Spearman:
        if Team == 1:
            Screen.blit(SpearmanPicture, (marginwidth, marginheigth))
        else:
            Screen.blit(pygame.transform.flip(SpearmanPicture, True, False), (marginwidth, marginheigth))
    elif Unit == Healer:
        if Team == 1:
            Screen.blit(HealerPicture, (marginwidth, marginheigth))
        else:
            Screen.blit(pygame.transform.flip(HealerPicture, True, False), (marginwidth, marginheigth))
    elif Unit == Player:
        if Team == 1:
            Screen.blit(PlayerPicture, (marginwidth, marginheigth))
        else:
            Screen.blit(pygame.transform.flip(PlayerPicture, True, False), (marginwidth, marginheigth))
    elif Unit == Samurai:
        if Team == 1:
            Screen.blit(SamuraiPicture, (marginwidth, marginheigth))
        else:
            Screen.blit(pygame.transform.flip(SamuraiPicture, True, False), (marginwidth, marginheigth))
    elif Unit == Castle:
        if Team == 1:
            Screen.blit(CastlePicture, (marginwidth, marginheigth))
        else:
            Screen.blit(pygame.transform.flip(CastlePicture, True, False), (marginwidth, marginheigth))
    elif Unit == Paladin:
        if Team == 1:
            Screen.blit(PaladinPicture, (marginwidth, marginheigth+5))
        else:
            Screen.blit(pygame.transform.flip(PaladinPicture, True, False), (marginwidth, marginheigth+5))
    else:
        pygame.draw.polygon(Screen, Unit.Colour, [(marginwidth,marginheigth),(width + marginwidth,marginheigth),(marginwidth+width,height+marginheigth),(marginwidth,height+marginheigth)])
    
    RedAmount = int((DamageTaken/Unit.Health)*100)
    RedAmount = int((40/100)*RedAmount)
    GreenAmount = 40 - RedAmount
    pygame.draw.polygon(Screen, GREEN, [(marginwidth,marginheigth),(GreenAmount + marginwidth,marginheigth),(marginwidth+GreenAmount,4+marginheigth),(marginwidth,4+marginheigth)])
    if DamageTaken > 0:
        pygame.draw.polygon(Screen, RED, [(marginwidth + 40 - RedAmount,marginheigth),(39 + marginwidth,marginheigth),(marginwidth+39,4+marginheigth),(marginwidth + 40 - RedAmount,4+marginheigth)])
    pygame.display.update()


#replace a basic tile over selected point to make tile appear empty    
def RemoveUnit(xline,yline,Start=0): #remove unit from grid
    if Start !=-1:
        marginwidth = 5 + (40*xline) + (5*xline) + (Start*width)
        marginheigth = 5 + (40*yline) + (5*yline) + (Start*height)
    else:
        marginwidth = 5 + (40*xline) + (5*xline)
        marginheigth = 5 + (40*yline) + (5*yline)
    if Start == 0:
        BattleStatus[xline][yline] = 0
    if Start == 1:
        CreateArmyGrid[xline][yline] = 0

    n = TileStatus[xline][yline]
    Grass = Tiles[n]
    Screen.blit(pygame.transform.scale(Grass, (40, 40)), (marginwidth, marginheigth))

def EmptySquare(x,y): #check if a square is empty
    if BattleStatus[x][y] == 0:
        return True
    else:
        return False
    
#Removes unit from current square through remove unit and then place it on the new one simulating movement
def Movement(Startx,Starty,Newx,Newy,Colour,Name,Health,Team): #move between grids
    Valid = EmptySquare(Newx,Newy)
    TempUnit = ClassDictionary[Name][0]

    if Valid:
        if Team == 1 or Team ==2:
            BoardText(Startx,Starty,Newx,Newy,0)
        RemoveUnit(Startx,Starty)
        PlaceUnit(Newx,Newy,TempUnit,Team,(TempUnit.Health)-Health)
        pygame.display.update()
        return True
    else:
        return False

#Go through every tile of the map (Through an array I have set up that keeps track of units and data about them)
#Enemy team units determin if they should attack or move and do so while when coming across Player team hands them control
#Player control and playering being able to change which unit they move where both added as an after thought as with many other things 
def BoardTick(xGrid,yGrid): #Make every cell do something
    Filled = False
    MovedStatus = [ ["Ready"]*(BattleScreenY) for _ in range(BattleScreenX) ]
    Team1 = False
    Team2 = False
    for y in range(yGrid):
        for x in range(xGrid):
            if MovedStatus[x][y] == "Ready":
                Sorted = False
                Filled = EmptySquare(x,y)
                if not Filled:
                    if BattleStatus[x][y][1] == "Catapult" and BattleStatus[x][y][3] == 2:
                        if BattleStatus[x][y][4] == 0:
                            Filled = True
                            BattleStatus[x][y] = (BattleStatus[x][y][0],BattleStatus[x][y][1],BattleStatus[x][y][2],BattleStatus[x][y][3],1)
                            BoardText(x,y,0,0,-2)
                            Team2 = True
                        else:
                            BattleStatus[x][y] = (BattleStatus[x][y][0],BattleStatus[x][y][1],BattleStatus[x][y][2],BattleStatus[x][y][3],0)
                            Team2 = True                                
                if not Filled:
                    if BattleStatus[x][y][3] == 1:
                        Team1 = True
                    if BattleStatus[x][y][3] == 2:
                        Team2 = True
                    pygame.event.get()
                    time.sleep(0.1)
                    if BattleStatus[x][y][3] == 1:
                        w,z,Status = PlayerBattleChoice(x,y)
                        MovedStatus[w][z] = Status
                    else:
                        if BattleStatus[x][y][1] == "Healer":
                            Sorted = CheckHeal(x,y)
                        else:
                            Sorted = CheckAttack(x,y)
                        if not Sorted:
                            w,z = MovementChoice(x,y)
                            MovedStatus[w][z] = "Moved"
                        else:
                            MovedStatus[x][y] = "Attacked"
                pygame.display.update()
    return Team1,Team2

#Combat log that appears during a battle to diplay whats going on to the user
ScrollingText = []
def BoardText(StartX,StartY,NewX,NewY,Damage):
    pygame.draw.polygon(Screen, WHITE, [(10,330),(600,330),(600,545),(10,545)])
    if Damage == 0:
        text = BattleStatus[StartX][StartY][1] + " at " + str(StartX) + "," + str(StartY) + " Moved to " + str(NewX) + "," + str(NewY) + "."
    elif Damage == -1:
        text = BattleStatus[StartX][StartY][1] + " at " + str(StartX) + "," + str(StartY) + " ability was activated."
    elif Damage == -2:
        text = BattleStatus[StartX][StartY][1] + " at " + str(StartX) + "," + str(StartY) + " is charging up and will be avaliable to move/attack next time round."
    elif Damage == -3:
        text = BattleStatus[StartX][StartY][1] + " at " + str(StartX) + "," + str(StartY) + " Healed " + BattleStatus[NewX][NewY][1] + " at " + str(NewX) + "," + str(NewY) + " Restoring 3 Health."
    else:
        text = BattleStatus[StartX][StartY][1] + " at " + str(StartX) + "," + str(StartY) + " Attacked " + BattleStatus[NewX][NewY][1] + " at " + str(NewX) + "," + str(NewY) + " Dealing " + str(Damage) + " Damage."
    ScrollingText.append(text)
    if len(ScrollingText) > 20:
        ScrollingText.pop(0)
    Position = 0
    for x in ScrollingText:
        text = font.render(x, True, BLACK)
        Screen.blit(text,(11,335 + (10*Position)))
        Position = Position + 1 

#Attack choice for a computers unit    
def CheckAttack(x,y): #check if there is a valid enemy to attack
    Target = False
    Done = False
    TempUnit = ClassDictionary[BattleStatus[x][y][1]][0]
    Range = TempUnit.Range
    for i in range (1,Range+1):
        if not Done:
            if (x+i < 19):
                Valid = EmptySquare(x+i,y)
                if  not Valid:
                    Target = CheckTeam(x,y,x+i,y)
                    if Target:
                        Attack(x,y,x+i,y)
                        Done = True
    if not Done:
        for i in range (1,Range+1):
            if not Done:
                if (x-i >0):
                    Valid = EmptySquare(x-i,y)
                    if not Valid:
                        Target = CheckTeam(x,y,x-i,y)
                        if Target:
                            Attack(x,y,x-i,y)
                            Done = True                
    if not Done:
        for i in range (1,Range+1):
            if not Done:
                if (y+i <5):
                    Valid = EmptySquare(x,y+i)
                    if not Valid:
                        Target = CheckTeam(x,y,x,y+i)
                        if Target:
                            Attack(x,y,x,y+i)
                            Done = True  
    if not Done:
        for i in range (1,Range+1):
            if not Done:
                if (y-i >0):
                    Valid = EmptySquare(x,y-i)
                    if not Valid:
                        Target = CheckTeam(x,y,x,y-i)
                        if Target:
                            Attack(x,y,x,y-i)
                            Done = True  
    return Done

def CheckHeal(x,y): #check if there is a valid enemy to attack
    Target = False
    Done = False
    TempUnit = ClassDictionary[BattleStatus[x][y][1]][0]
    Range = TempUnit.Range
    for i in range (1,Range+1):
        if not Done:
            if (x+i < 19):
                Valid = EmptySquare(x+i,y)
                if  not Valid:
                    Target = CheckTeam(x,y,x+i,y)
                    if not Target:
                        Heal(x,y,x+i,y)
                        Done = True
    if not Done:
        for i in range (1,Range+1):
            if not Done:
                if (x-i >0):
                    Valid = EmptySquare(x-i,y)
                    if not Valid:
                        Target = CheckTeam(x,y,x-i,y)
                        if not Target:
                            Heal(x,y,x-i,y)
                            Done = True                
    if not Done:
        for i in range (1,Range+1):
            if not Done:
                if (y+i <5):
                    Valid = EmptySquare(x,y+i)
                    if not Valid:
                        Target = CheckTeam(x,y,x,y+i)
                        if not Target:
                            heal(x,y,x,y+i)
                            Done = True  
    if not Done:
        for i in range (1,Range+1):
            if not Done:
                if (y-i >0):
                    Valid = EmptySquare(x,y-i)
                    if not Valid:
                        Target = CheckTeam(x,y,x,y-i)
                        if not Target:
                            Heal(x,y,x,y-i)
                            Done = True  
    return Done

#Was writing this out too many times so made a function for it tho in some places it still has me manually checking
def CheckTeam(Startx,Starty,Attackx,Attacky): # check team #random error fixed stupidly
    Team1 = "Lol"
    Team2 = "Double lol"
    if BattleStatus[Startx][Starty] != 0:
        Team1 = BattleStatus[Startx][Starty][3]
    if BattleStatus[Attackx][Attacky] != 0:    
        Team2 = BattleStatus[Attackx][Attacky][3]
    if Team1 == Team2:
        return False
    else:
        return True

#Calculate the damage one unit does to another taking into account special abilities
def Attack(Startx,Starty,Attackx,Attacky): # Preform attack
    Temp = ClassDictionary[BattleStatus[Startx][Starty][1]][0]
    TempEnemy = ClassDictionary[BattleStatus[Attackx][Attacky][1]][0]
    
    ###Before attack increase Modifiers###
    Modified = True
    Modifier = 1
    if Temp.Ability == "RangedShot" and (Startx-Attackx > 1 or Starty-Attacky > 1 or Attackx-Startx > 1 or Attacky-Starty > 1):
        Modifier = 3
    elif Temp.Ability == "Charge" and BattleStatus[Startx][Starty][2] == Temp.Health:
        Modifier = 2
    elif Temp.Ability == "Injured" and BattleStatus[Startx][Starty][2] <= (Temp.Health/2):
        Modifier = 2
    elif Temp.Ability == "Assasinate" and ((BattleStatus[Startx][Starty][3] == 1 and Startx > Attackx) or (BattleStatus[Startx][Starty][3] == 2 and Startx < Attackx)):
        Modifier = 4
    else:
        Modified = False
    if Modified:
        BoardText(Startx,Starty,Attackx,Attacky,-1)

    ###Before attack minus Modifers
    if TempEnemy.Ability == "Numbers":
        if Attacky+1 < 5:
            if BattleStatus[Attackx][Attacky+1] != 0:
                if BattleStatus[Attackx][Attacky][3]==BattleStatus[Attackx][Attacky+1][3] and BattleStatus[Attackx][Attacky][1]==BattleStatus[Attackx][Attacky+1][1]:
                    Modifier = 0.5
                    BoardText(Attackx,Attacky,Startx,Starty,-1)
        if Attacky-1>0:
            if BattleStatus[Attackx][Attacky-1] != 0:
                if BattleStatus[Attackx][Attacky][3]==BattleStatus[Attackx][Attacky-1][3] and BattleStatus[Attackx][Attacky][1]==BattleStatus[Attackx][Attacky-1][1]:
                    Modifier = 0.5
                    BoardText(Attackx,Attacky,Startx,Starty,-1)

    Damage = (TempEnemy.Health - BattleStatus[Attackx][Attacky][2])+(Modifier*Unit.Attack(Temp,TempEnemy,Attackx,Attacky))
        
    BoardText(Startx,Starty,Attackx,Attacky,(Unit.Attack(Temp,TempEnemy,Attackx,Attacky)*Modifier))
    pygame.mixer.Sound.play(AttackSound)
    
    if TempEnemy.Health - Damage >0:
        PlaceUnit(Attackx,Attacky,TempEnemy,BattleStatus[Attackx][Attacky][3],Damage)
        if TempEnemy.Ability == "Retaliation" and Temp.Ability != "RangedShot":
            Modifier = 0.5
            BoardText(Attackx,Attacky,Startx,Starty,-1)
            BoardText(Attackx,Attacky,Startx,Starty,(Unit.Attack(Temp,TempEnemy,Attackx,Attacky)*Modifier))
            RetaliationDamage = (Temp.Health - BattleStatus[Startx][Starty][2])+(Modifier*Unit.Attack(Temp,TempEnemy,Attackx,Attacky))
            if Temp.Health - RetaliationDamage >0:
                PlaceUnit(Startx,Starty,Temp,BattleStatus[Startx][Starty][3],RetaliationDamage)
            else:
                RemoveUnit(Startx,Starty)
    else:
        if TempEnemy == Samurai:
            Finalblow(Attackx,Attacky)
        RemoveUnit(Attackx,Attacky)


    pygame.display.update()

def Finalblow(x,y):

    print("Do hella attacks")


def Heal(Startx,Starty,Attackx,Attacky):
    Temp = ClassDictionary[BattleStatus[Startx][Starty][1]][0]
    TempEnemy = ClassDictionary[BattleStatus[Attackx][Attacky][1]][0]
    Damage = (TempEnemy.Health - BattleStatus[Attackx][Attacky][2])-(Unit.Attack(Temp,TempEnemy,-5,-5))
    if Damage <0:
        Damage = 0
    PlaceUnit(Attackx,Attacky,TempEnemy,BattleStatus[Attackx][Attacky][3],Damage)
    BoardText(Attackx,Attacky,Startx,Starty,-3)
    pygame.mixer.Sound.play(HealSound)




    pygame.display.update()



def UnitInRow(x,y): # Check if unit in Row
    TempPresent = False
    Present = False
    for i in range(BattleScreenX):
        TempPresent = EmptySquare(i,y)
        if not TempPresent:
            TempPresent = CheckTeam(x,y,i,y)
            if TempPresent and BattleStatus[i][y][1] != "Catapult":
                Present = True
    return Present            

def UnitInColumn(x,y): # Check if unit in Column
    TempPresent = False
    Present = False
    for i in range(BattleScreenY):
        TempPresent = EmptySquare(x,i)
        if not TempPresent:
            TempPresent = CheckTeam(x,y,x,i)
            if TempPresent:
                Present = True
    return Present    

def MovementChoice(x,y): #Choose where to move unit for computer #awful programming I dont like how deep it runs but gotta check every cell most wont run just there incase
    
    TempUnit = ClassDictionary[BattleStatus[x][y][1]][0]
    Amount = TempUnit.Movement
    if Amount > 0:
        for i in range(1,Amount+1):
            Moved = False
            n=1
            while not Moved:
                if n == 1:
                    Moved = CheckAttack(x,y)
                if not Moved:
                    for i in range (0,n+1):
                        if not Moved:
                            if ((y+i) <5) and ((x+n) < 19):
                                TempPresent = EmptySquare(x+n,y+i)
                                if not TempPresent:
                                    TempPresent = CheckTeam(x,y,x+n,y+i)
                                    if TempPresent:
                                        Moved = Movement(x,y,x+1,y,BattleStatus[x][y][0],BattleStatus[x][y][1],BattleStatus[x][y][2],BattleStatus[x][y][3])
                                        if Moved :
                                            x=x+1
                                        else:
                                            Moved = Movement(x,y,x,y+1,BattleStatus[x][y][0],BattleStatus[x][y][1],BattleStatus[x][y][2],BattleStatus[x][y][3])
                                            if Moved:
                                                y=y+1
                        if not Moved:
                            if ((y+n) <5) and ((x+i) < 19):
                                TempPresent = EmptySquare(x+i,y+n)
                                if not TempPresent:
                                    TempPresent = CheckTeam(x,y,x+i,y+n)
                                    if TempPresent:
                                        Moved = Movement(x,y,x,y+1,BattleStatus[x][y][0],BattleStatus[x][y][1],BattleStatus[x][y][2],BattleStatus[x][y][3])
                                        if Moved :
                                            y=y+1
                                        else:
                                            Moved = Movement(x,y,x+1,y,BattleStatus[x][y][0],BattleStatus[x][y][1],BattleStatus[x][y][2],BattleStatus[x][y][3])
                                            if Moved:
                                                x=x+1
                if not Moved:
                    for i in range (0,n+1):
                        if not Moved:
                            if ((y-i) >0) and ((x+n) < 19):
                                TempPresent = EmptySquare(x+n,y-i)
                                if not TempPresent:
                                    TempPresent = CheckTeam(x,y,x+n,y-i)
                                    if TempPresent:
                                        Moved = Movement(x,y,x+1,y,BattleStatus[x][y][0],BattleStatus[x][y][1],BattleStatus[x][y][2],BattleStatus[x][y][3])
                                        if Moved :
                                            x=x+1
                                        else:
                                            Moved = Movement(x,y,x,y-1,BattleStatus[x][y][0],BattleStatus[x][y][1],BattleStatus[x][y][2],BattleStatus[x][y][3])
                                            if Moved:
                                                y=y-1
                        if not Moved:
                            if ((y-n) >0) and ((x+i) < 19):
                                TempPresent = EmptySquare(x+i,y-n)
                                if not TempPresent:
                                    TempPresent = CheckTeam(x,y,x+i,y-n)
                                    if TempPresent:
                                        Moved = Movement(x,y,x,y-1,BattleStatus[x][y][0],BattleStatus[x][y][1],BattleStatus[x][y][2],BattleStatus[x][y][3])
                                        if Moved :
                                            y=y-1
                                        else:
                                            Moved = Movement(x,y,x+1,y,BattleStatus[x][y][0],BattleStatus[x][y][1],BattleStatus[x][y][2],BattleStatus[x][y][3])
                                            if Moved:
                                                x=x+1
                if not Moved:
                    for i in range (0,n+1):
                        if not Moved:
                            if ((y+i) <5) and ((x-n) >0):
                                TempPresent = EmptySquare(x-n,y+i)
                                if not TempPresent:
                                    TempPresent = CheckTeam(x,y,x-n,y+i)
                                    if TempPresent:
                                        Moved = Movement(x,y,x-1,y,BattleStatus[x][y][0],BattleStatus[x][y][1],BattleStatus[x][y][2],BattleStatus[x][y][3])
                                        if Moved :
                                            x=x-1
                                        else:
                                            if y +1 <5:
                                                Moved = Movement(x,y,x,y+1,BattleStatus[x][y][0],BattleStatus[x][y][1],BattleStatus[x][y][2],BattleStatus[x][y][3])
                                                if Moved:
                                                    y=y+1
                        if not Moved:
                            if ((y+n) <5) and ((x-i) >0):
                                TempPresent = EmptySquare(x-i,y+n)
                                if not TempPresent:
                                    TempPresent = CheckTeam(x,y,x-i,y+n)
                                    if TempPresent:
                                        Moved = Movement(x,y,x,y+1,BattleStatus[x][y][0],BattleStatus[x][y][1],BattleStatus[x][y][2],BattleStatus[x][y][3])
                                        if Moved :
                                            y=y+1
                                        else:
                                            Moved = Movement(x,y,x-1,y,BattleStatus[x][y][0],BattleStatus[x][y][1],BattleStatus[x][y][2],BattleStatus[x][y][3])
                                            if Moved:
                                                x=x-1
                if not Moved:
                    for i in range (0,n+1):
                        if not Moved:
                            if ((y-i) >0) and ((x-n) >0):
                                TempPresent = EmptySquare(x-n,y-i)
                                if not TempPresent:
                                    TempPresent = CheckTeam(x,y,x-n,y-i)
                                    if TempPresent:
                                        Moved = Movement(x,y,x-1,y,BattleStatus[x][y][0],BattleStatus[x][y][1],BattleStatus[x][y][2],BattleStatus[x][y][3])
                                        if Moved :
                                            x=x-1
                                        else:
                                            Moved = Movement(x,y,x,y-1,BattleStatus[x][y][0],BattleStatus[x][y][1],BattleStatus[x][y][2],BattleStatus[x][y][3])
                                            if Moved:
                                                y=y-1
                        if not Moved:
                            if ((y-n) >0) and ((x-i) >0):
                                TempPresent = EmptySquare(x-i,y-n)
                                if not TempPresent:
                                    TempPresent = CheckTeam(x,y,x-i,y-n)
                                    if TempPresent:
                                        Moved = Movement(x,y,x,y-1,BattleStatus[x][y][0],BattleStatus[x][y][1],BattleStatus[x][y][2],BattleStatus[x][y][3])
                                        if Moved :
                                            y=y-1
                                        else:
                                            Moved = Movement(x,y,x-1,y,BattleStatus[x][y][0],BattleStatus[x][y][1],BattleStatus[x][y][2],BattleStatus[x][y][3])
                                            if Moved:
                                                x=x-1
                n=n+1
                if n == 21:
                    Moved = True

    return x,y

#Just for convinence when writing the next section 
def CreateArmy(Points):
    setupgrid(ArmySizeX,ArmySizeY,1)
    CreateArmyGrid = [ [0]*(ArmySizeY) for _ in range(ArmySizeX) ]
    CreateArmyScreen(ArmySizeX,ArmySizeY,Points,0)
    CreateScreenChoice(int(Points))

def CreateArmyScreen(ArmySizeX,ArmySizeY,PointsLeft,PointsUsed):
    for x in range (ArmySizeX):
        text = font.render(str(x), True, NOTWHITE)
        Screen.blit(text,(5+(width*1.5)+(width*x)+(5*x),20))
    for y in range (ArmySizeY):
        text = font.render(str(y), True, NOTWHITE)
        Screen.blit(text,(20,5+(height*1.5)+(height*y)+(5*y)))
    pygame.display.update()
    PointsSection(PointsLeft,PointsUsed)
    SelectCordinate(0,0)
    Screen.blit(SmallButton,(225,310))
    text = font.render("Save", True, BLACK)
    Screen.blit(text,(250,355))
    Screen.blit(BackButton,(1025,375))
    text = font.render("Back", True, WHITE)
    Screen.blit(text,(1070,480))
    text = font.render("Unit Choice:", True, WHITE)
    Screen.blit(text,(700,20))
    Start = 700
    n = 0
    Total = 0
    for x in UnitsList:
        if x.Name != "Player":
            Name = x.Name + " Cost:" + str(x.Points)
            pygame.draw.polygon(Screen, GREY, [(Start,30+(30*n)),(Start+100,30+(30*n)),(Start+100,50+(30*n)),(Start,50+(30*n))])
            text = font.render(Name, True, BLACK)
            Screen.blit(text,(Start+5,35+(30*n)))
            Total = Total+1
            if n < 8:
                n=n+1
            else:
                n=0
                Start = 810
    pygame.display.update()    

#Player control over the create army screen
def CreateScreenChoice(Points,Control = True):
    TotalPoints = Points
    CreateArmyGrid = [ [0]*(ArmySizeY) for _ in range(ArmySizeX) ]
    CurrentX = 0
    CurrentY = 0
    Start = 700
    while Control:
        for event in pygame.event.get():
            MousePos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()   
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (MousePos[0] in range (45,315)) and (MousePos[1] in range (45,270)) and event.button == 1:
                    x = MousePos[0] - 45
                    x = x//45
                    y = MousePos[1] - 45
                    y = y//45
                    if CreateArmyGrid[CurrentX][CurrentY] == 0:
                        RemoveUnit(CurrentX,CurrentY,1)
                    else:
                        RemoveUnit(CurrentX,CurrentY,1)
                        Temp = ClassDictionary[CreateArmyGrid[CurrentX][CurrentY]][0]
                        PlaceUnit(CurrentX,CurrentY,Temp,1,0,1)
                    SelectCordinate(x,y)
                    CurrentX = x
                    CurrentY= y
                    pygame.mixer.Sound.play(SelectSound)
                if (MousePos[0] in range (45,315)) and (MousePos[1] in range (45,270)) and event.button == 3:
                    x = MousePos[0] - 45
                    x = x//45
                    y = MousePos[1] - 45
                    y = y//45
                    pygame.mixer.Sound.play(SelectSound)
                    if CreateArmyGrid[x][y] !=0:
                        Points = Points + ClassDictionary[CreateArmyGrid[x][y]][0].Points
                        CreateArmyGrid[x][y] = 0
                        RemoveUnit(x,y,1)
                        PointsSection(Points,TotalPoints-Points)
                Start = 700
                n = 0
                for i in UnitsList:
                    if i.Name != "Player" and (Points - i.Points) > 0:
                        if (MousePos[0] in range (Start,Start+100)) and (MousePos[1] in range (30+(30*n),50+(30*n))) and event.button == 1:        
                            UnitChoice = i
                            pygame.mixer.Sound.play(SelectSound)
                            if CreateArmyGrid[CurrentX][CurrentY] !=0:
                                Temp = ClassDictionary[CreateArmyGrid[CurrentX][CurrentY]][0]
                                Points = Points + Temp.Points
                                PointsSection(Points,TotalPoints-Points)
                                RemoveUnit(CurrentX,CurrentY,1)
                            CreateArmyGrid[CurrentX][CurrentY] = UnitChoice.Name
                            PlaceUnit(CurrentX,CurrentY,UnitChoice,1,0,1)
                            SelectCordinate(CurrentX,CurrentY)
                            Points = Points - UnitChoice.Points
                            PointsSection(Points,TotalPoints-Points)
                        if n < 8:
                            n=n+1
                        else:
                            n=0
                            Start = 810
                if (MousePos[0] in range (240,325)) and (MousePos[1] in range (350,370)):
                    FileName = UserInputPopUp("Input Army Name:")
                    SaveArmy(FileName,CreateArmyGrid,True)
                    MainMenu()
                if (MousePos[0] in range (1050,1110)) and (MousePos[1] in range (450,520)):
                    MainMenu()

def PointsSection(PointsLeft,PointsUsed):
    text = font.render("Remaining Points:", True, NOTWHITE)
    Screen.blit(text,(350,55)) 
    Screen.blit(SmallButton,(425,10))
    text = font.render(str(PointsLeft), True, BLACK)
    Screen.blit(text,(450,55))
    text = font.render("Points Used:", True, NOTWHITE)
    Screen.blit(text,(350,155))
    Screen.blit(SmallButton,(425,110))
    text = font.render(str(PointsUsed), True, BLACK)
    Screen.blit(text,(450,155))        
    pygame.display.update()

#for updating current selected cordiante
def SelectCordinate(x,y):
    marginwidth = 5 + (40*(x+1)) + (5*x)
    marginheigth = 5 + (40*(y+1)) + (5*y)
    pygame.draw.polygon(Screen, GREEN, [(marginwidth+2,marginheigth+2),(width + marginwidth-2,marginheigth+2),(marginwidth+width-2,height+marginheigth-2),(marginwidth+2,height+marginheigth-2)],2)    
    text = font.render("Current Selected X:", True, NOTWHITE)
    Screen.blit(text,(50,300))      
    pygame.draw.polygon(Screen, GREY, [(50,310),(150,310),(150,330),(50,330)])
    pygame.display.update()
    text = font.render(str(x), True, BLACK)
    Screen.blit(text,(55,315))    
    text = font.render("Current Selected Y:", True, NOTWHITE)
    Screen.blit(text,(50,400))      
    pygame.draw.polygon(Screen, GREY, [(50,410),(150,410),(150,430),(50,430)])
    pygame.display.update()
    text = font.render(str(y), True, BLACK)
    Screen.blit(text,(55,415))
    pygame.display.update()
    
def SaveArmy(ArmyName,TempArmy,PlayerCreate = False):
    ArmyName=ArmyName+".txt"
    if PlayerCreate:
        ArmyName = "101"+ArmyName
    Path = os.path.dirname(__file__)
    ArmyName = "Armies/"+ArmyName 
    ArmyName = os.path.join(Path, ArmyName)
    File = open(ArmyName,"w")
    for x in range(ArmySizeX):
        for y in range(ArmySizeY):
            if TempArmy[x][y] != 0:
                File.write(str(x))
                File.write(";")
                File.write(str(y))
                File.write(";") 
                File.write(TempArmy[x][y])
                File.write(";")
                File.write("\n")
    File.close()
    
def LoadArmy(ArmyName):
    TempArmy = [ [0]*(ArmySizeY) for _ in range(ArmySizeX) ]
    ArmyName=ArmyName+".txt"
    Path = os.path.dirname(__file__)
    ArmyName = "Armies/"+ArmyName 
    File = os.path.join(Path, ArmyName)
    File = open(File)
    for line in File:
        line = line.split(";",4)
        TempArmy[int(line[0])][int(line[1])] = (line[2])
    File.close()
    return TempArmy

def LoadBattle(Team1Army,Team2Army):
    for x in range(BattleScreenX):
        for y in range(BattleScreenY):
            BattleStatus[x][y] = 0
    TempArmy = [ [0]*(ArmySizeY) for _ in range(ArmySizeX) ]
    setupgrid(BattleScreenX,BattleScreenY)
    ScrollingText = []
    text = font.render("Combat Log:", True, WHITE)
    Screen.blit(text,(10,320))
    pygame.draw.polygon(Screen, WHITE, [(10,330),(600,330),(600,545),(10,545)])
    Screen.blit(StatsCard,(650,300))
    TempArmy = LoadArmy(Team1Army)
    for x in range(ArmySizeX):
        for y in range(ArmySizeY):
            if TempArmy[x][y] != 0:
                TempUnit = ClassDictionary[TempArmy[x][y]][0]
                PlaceUnit(x,y,TempUnit,1)
    TempArmy = LoadArmy(Team2Army)
    for x in range(ArmySizeX):
        for y in range(ArmySizeY):
            if TempArmy[x][y] != 0:
                TempUnit = ClassDictionary[TempArmy[x][y]][0]
                PlaceUnit(19-x,y,TempUnit,2)
    Winner = BattleStart()
    return Winner

class Unit:
    def __init__(self,Name,BaseHealth,BaseDamage,Armour,Range,Movement,Ability,Points,Colour):
        self.Name = Name
        self.Health = BaseHealth
        self.Ability = Ability
        self.Range = Range
        self.Movement = Movement
        self.Points = Points
        self.Damage = BaseDamage
        self.Colour = Colour
        self.Armour = Armour
    def Attack(self,enemy,x,y):
        Paladin = False

        for x in range(0,100):
            ChangeX = random.randint(-1,1)
            ChangeY = random.randint(-1,1)
            if x+ChangeX > 0 and x+ChangeX<19 and y+ChangeY>0 and y+ChangeY<5:
                if (BattleStatus[x+ChangeX][y+ChangeY] !=0):
                    if (BattleStatus[x+ChangeX][y+ChangeY][1] =="Paladin"):
                        Paladin = True

                        BoardText(x+ChangeX,y+ChangeY,x,y,-1)
        if Paladin:
            Value = self.Damage-(enemy.Armour+1)
        else:
            Value = self.Damage-enemy.Armour
        if Value <=0:
            Value = 1
        return Value

#teir 1 units    
Swordsman = Unit("Swordsman",10,2,2,1,1,"None",10,RED)
Spearman = Unit("Spearman",15,1,1,1,1,"Numbers",15,RED)
Archer = Unit("Archer",5,1,0,2,1,"RangedShot",10,DARKGREEN)
Cavalry = Unit("Cavalry",10,3,2,1,2,"Charge",20,GREY)
Beserker = Unit("Beserker",20,2,0,1,1,"Injured",15,PURPLE)
Pikeman = Unit("Pikeman",15,1,2,1,1,"Retaliation",15,YELLOW)
Catapult = Unit("Catapult",2,2,0,6,1,"RangedShot",10,BROWN)
Ninja = Unit("Ninja",15,2,0,1,2,"Assasinate",15,BLACK)

#teir 2 units
Healer = Unit("Healer",25,0,1,1,1,"Heal",25,BLUE)
Samurai = Unit("Samurai",20,3,1,1,1,"LastStand",25,BLUE)
Paladin = Unit("Paladin",30,1,3,1,1,"Protect",35,BLUE)
#Vampire,mage,paladin,necromancer


#Settlement units
Castle = Unit("Castle",15,3,3,5,0,"None",35,BLUE)
#guard, peasnt, walls

#cave units
#goblin, spider

#Mythic Units
Giant = Unit("Giant",75,10,5,1,1,"None",100,BLUE) # No picture yet
Dragon = Unit("Dragon",50,15,10,1,2,"None",100,BLUE)

#Special units
Player = Unit("Player",25,5,1,1,1,"DamageBoost",35,BLUE) 
Modge = Unit("Modgeinator",200,20,10,1,1,"Skip",500000,BLACK) #Mess around

UnitsList = [Swordsman,Spearman,Archer,Cavalry,Beserker,Pikeman,Catapult,Ninja,Healer,Samurai,Paladin,Castle,Giant,Dragon,Player]
ClassDictionary = {}

for x in UnitsList:
    ClassDictionary.setdefault(x.Name,[]).append(x)


def BuildMainMenu():
    Screen = pygame.display.set_mode((1200,600), 0, 32)
    Screen.blit(pygame.transform.scale(Background, (1200, 600)), (0, 0))
    Screen.blit(SmallButton,(100,110))
    text = font.render("Standard Battle", True, BLACK)
    Screen.blit(text,(120,155))    
    Screen.blit(SmallButton,(100,210))
    text = font.render("Create Army", True, BLACK)
    Screen.blit(text,(120,255))  
    Screen.blit(SmallButton,(100,310))
    text = font.render("Arena", True, BLACK)
    Screen.blit(text,(120,355)) 
    Screen.blit(SmallButton,(100,410))
    text = font.render("Campagin", True, BLACK)
    Screen.blit(text,(120,455)) 
    pygame.display.update()

def MainMenu(Control = True):
    BuildMainMenu()
    while Control:
        for event in pygame.event.get():
            MousePos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (MousePos[0] in range (110,200)) and (MousePos[1] in range (150,170)):
                    Control = False
                    pygame.mixer.Sound.play(SelectSound)
                    Team1 = LoadArmyScreen("1")
                    Team2 = LoadArmyScreen(Team1)
                    LoadBattle(Team1,Team2)
                    MainMenu()
                if (MousePos[0] in range (110,200)) and (MousePos[1] in range (250,270)):
                    Control = False
                    pygame.mixer.Sound.play(SelectSound)
                    Points = UserInputPopUp("Input maximum points:",True)
                    CreateArmy(Points)
                if (MousePos[0] in range (110,200)) and (MousePos[1] in range (350,370)):
                    Control = False
                    pygame.mixer.Sound.play(SelectSound)
                    Round = Arena()
                    CurrentRound(Round,True)
                    MainMenu()
                if (MousePos[0] in range (110,200)) and (MousePos[1] in range (450,470)):
                    Control = False
                    pygame.mixer.Sound.play(SelectSound)
                    CharacterName = UserInputPopUp("Input your characters name:")
                    setupgrid(15,10)
                    Campagin(CharacterName)

#Choose which army to load from files with a sort of scroll bar
def LoadArmyScreen(Team):
    global LoadScreen
    Path = os.path.dirname(__file__)
    ArmyName = "Armies/"
    File = os.path.join(Path, ArmyName)
    FileList = os.listdir(File)
    Screen.blit(pygame.transform.scale(Background, (1200, 600)), (0, 0))
    text = Mediumfont.render("Saved Armies:", True, WHITE)
    Screen.blit(text,(30,30))
    UseableFiles = []
    Team2 = 0
    for x in FileList:
        if x[0:3] == "101":
            UseableFiles.append(x)
    if Team == "1":
        text = Mediumfont.render("Choose Army 1:", True, WHITE)
        Screen.blit(text,(30,0))
    else:
        ShowArmy(Team,Team2)
        text = Mediumfont.render("Choose Army 2:", True, WHITE)
        Screen.blit(text,(30,0))
        Team2 = 300
        
    Screen.blit(SmallButton,(30,500))
    text = font.render("Select File", True, BLACK)
    Screen.blit(text,(46,545))   
    Screen.blit(SmallButton,(180,500))
    text = font.render("Random Army", True, BLACK)
    Screen.blit(text,(196,545))

    text = Bigfont.render("-", True, BLACK)
    Screen.blit(text,(530,40))
    

    text = Bigfont.render("+", True, BLACK)
    Screen.blit(text,(530,440))
    
    pygame.display.update()
    FilePlacement(UseableFiles,0,0)
    Control = True
    Selected = 0
    Start = 0
    ShowArmy(UseableFiles[Selected+Start][:-4],Team2)
    while Control:
        for event in pygame.event.get():

            MousePos = pygame.mouse.get_pos()
            StartPos = 10
            p = 0
            n=0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (MousePos[0] in range (190,250)) and (MousePos[1] in range (540,570)):
                     Number = UserInputPopUp("Input army points:",True)
                     pygame.mixer.Sound.play(SelectSound)
                     RandomArmy(int(Number),Team)
                     return Team
                for x in UseableFiles:
                    if (MousePos[0] in range (StartPos,StartPos+100)) and (MousePos[1] in range (80+(80*n),105+(80*n))) and event.button == 1 and p<15:        
                        Selected = p
                        ShowArmy(x[:-4],Team2)
                        pygame.mixer.Sound.play(SelectSound)
                        FilePlacement(UseableFiles,Start,Selected)
                    if n < 4:
                        n=n+1
                    else:
                        n=0
                        StartPos = StartPos + 180
                    p = p +1
                if (MousePos[0] in range (40,100)) and (MousePos[1] in range (540,570)):
                    pygame.mixer.Sound.play(SelectSound)
                    return UseableFiles[Selected+Start][:-4]

def FilePlacement(Files,StartPoint,Selected):
    n = 0
    Start = 0
    for x in range(0,15):
        if x+StartPoint < len(Files):
            Screen.blit(LableSword,(Start,50+(80*n)))
            if x == Selected:
                Screen.blit(pygame.transform.flip(Pointer, True, False), (Start+90,75+(80*n)))
            x = x + StartPoint
            text = font.render(Files[x][3:-4], True, BLACK)
            Screen.blit(text,(Start+35,85+(80*n)))
            if n < 4:
                n=n+1
            else:
                n=0
                Start = Start + 180   
    pygame.display.update()    

def ShowArmy(Army,Increase=0):
    EnemyArmy = LoadArmy(Army)
    for x in range(ArmySizeX):#Place squaresf\
        for y in range(ArmySizeY):
            marginwidth = 600 + (40*(x+1)) + (5*x)
            marginheigth = 5 + (40*(y+1)) + (5*y) +Increase
            n = random.randint(0,3)
            Grass = Tiles[n]
            Screen.blit(pygame.transform.scale(Grass, (40, 40)), (marginwidth, marginheigth))
            if EnemyArmy[5-x][y] != 0:
                TempUnit = ClassDictionary[EnemyArmy[5-x][y]][0]
                if TempUnit == Swordsman:
                    Screen.blit(pygame.transform.flip(SwordsmanPicture, True, False), (marginwidth, marginheigth-10))
                elif TempUnit == Archer:
                    Screen.blit(pygame.transform.flip(ArcherPicture, True, False), (marginwidth, marginheigth-10))
                elif TempUnit == Beserker:
                    Screen.blit(pygame.transform.flip(BeserkerPicture, True, False), (marginwidth, marginheigth-10))
                elif TempUnit == Cavalry:
                    Screen.blit(pygame.transform.flip(CavalryPicture, True, False), (marginwidth, marginheigth-10))
                elif TempUnit == Catapult:
                    Screen.blit(pygame.transform.flip(CatapultPicture, True, False), (marginwidth, marginheigth+5))
                elif TempUnit == Ninja:
                    Screen.blit(pygame.transform.flip(NinjaPicture, True, False), (marginwidth, marginheigth))
                elif TempUnit == Pikeman:
                    Screen.blit(pygame.transform.flip(PikemanPicture, True, False), (marginwidth, marginheigth))
                elif TempUnit == Spearman:
                    Screen.blit(pygame.transform.flip(SpearmanPicture, True, False), (marginwidth, marginheigth))
                elif TempUnit == Healer:
                    Screen.blit(pygame.transform.flip(HealerPicture, True, False), (marginwidth, marginheigth))
                elif TempUnit == Samurai:
                    Screen.blit(pygame.transform.flip(SamuraiPicture, True, False), (marginwidth, marginheigth))
                elif TempUnit == Castle:
                    Screen.blit(pygame.transform.flip(CastlePicture, True, False), (marginwidth-5, marginheigth-5))
                elif TempUnit == Paladin:
                    Screen.blit(pygame.transform.flip(PaladinPicture, True, False), (marginwidth-5, marginheigth+5))


    pygame.display.update() 

#Just a pop up box for user input
def UserInputPopUp(Question,Number = False):

    Screen.blit(pygame.transform.scale(Background, (1200, 600)), (0, 0))
    text = font.render(Question, True, WHITE)
    Screen.blit(text,(500,250))      
    pygame.draw.polygon(Screen, GREY, [(500,270),(690,270),(690,290),(500,290)])
    pygame.display.update()
    UserInput = ""
    text = font.render(UserInput, True, BLACK)
    Screen.blit(text,(15,25))    
    Finished = False
    while not Finished:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                whichKey = event.key
                if whichKey == 13:
                    Finished = True
                    pygame.mixer.Sound.play(SelectSound)
                if whichKey == 8:
                    UserInput = UserInput[:-1]
                    pygame.mixer.Sound.play(SelectSound)
                if not Number:
                    if whichKey in range (32,126):
                        if event.mod & pygame.KMOD_SHIFT:
                            UserInput = UserInput + chr(whichKey).upper()
                            pygame.mixer.Sound.play(SelectSound)
                        else:
                            UserInput = UserInput + chr(whichKey)
                            pygame.mixer.Sound.play(SelectSound)
                if Number:
                    if whichKey in range (48,57):
                        UserInput = UserInput + chr(whichKey)
                        pygame.mixer.Sound.play(SelectSound)
                pygame.draw.polygon(Screen, GREY, [(500,270),(690,270),(690,290),(500,290)])
                text = font.render(UserInput, True, BLACK)
                Screen.blit(text,(505,275))                  
                pygame.display.update()    
    return UserInput

def RandomArmy(Points,Arena = 0,Teir = "1"): 
    Army = [ [0]*(ArmySizeY) for _ in range(ArmySizeX) ]
    Start = 0
    maximum = len(UnitsList)-4
    if Teir =="1":
        maximum = 7
    if Teir=="Castle":
        maximum = len(UnitsList)-3
        x = random.randint(0,ArmySizeX-1)
        y = random.randint(0,ArmySizeY-1)
        UnitSelection = Castle
        Army[x][y] = UnitSelection.Name
    if Teir=="Dragon":
        Points = 0
        x = random.randint(0,ArmySizeX-1)
        y = random.randint(0,ArmySizeY-1)
        UnitSelection = Dragon
        Army[x][y] = UnitSelection.Name        
    if Teir=="Giant":
        Points = 0
        x = random.randint(0,ArmySizeX-1)
        y = random.randint(0,ArmySizeY-1)
        UnitSelection = Giant
        Army[x][y] = UnitSelection.Name         
    while Points > 9:
        x = random.randint(0,ArmySizeX-1)
        y = random.randint(0,ArmySizeY-1)
        UnitSelection = UnitsList[random.randint(Start,maximum)]
        if UnitSelection != Player and Points - UnitSelection.Points >= 0 and Army[x][y] == 0:
            Points = Points - UnitSelection.Points
            Army[x][y] = UnitSelection.Name
    if Arena == 0:
        SaveArmy("Arena",Army)
    else:
        SaveArmy(Arena,Army)
        

def BattleStart():
    Empty = False
    n = 0
    Team1Present = True
    Team2Present = True
    while not Empty:
        n= n+1
        Team1Present,Team2Present = BoardTick(BattleScreenX,BattleScreenY)
        if not Team1Present or not Team2Present:
            Empty = True
        if n > 200:
            Empty = True
            Team2Present = False
    if Team1Present:
        pygame.mixer.Sound.play(AfterBattle)
        return 1
    if Team2Present:
        return 2

def Arena():
    PlayerUnits = []
    Points = 40
    Winner = 1
    Round = 0
    PlayerUnits.append(ArenaSelection())
    PlayerUnits.append(ArenaSelection())
    while Winner == 1:
        if Round !=0:
            PlayerUnits = LoadRoster()
        RandomArmy(Points)
        if Round%5 == 4:
            PlayerUnits.append(ArenaSelection(True))
        else:
            PlayerUnits.append(ArenaSelection())
        SaveRoster(PlayerUnits)
        PreBattleScreen(PlayerUnits)
        BattlePlacement(PlayerUnits)
        Round = Round +1
        CurrentRound(Round)
        Winner = LoadBattle("ArenaPlayer","Arena")
        if Points > 100:
            Points = Points*1.1
        else:
            Points = Points+10
    return Round

def SaveRoster(PlayerUnits,Name="ArenaRoster"):
    Path = os.path.dirname(__file__)
    ArmyName = "Armies/" + Name +".txt"
    ArmyName = os.path.join(Path, ArmyName)
    File = open(ArmyName,"w")
    for x in PlayerUnits:
        File.write(x.Name)
        File.write("\n")

def LoadRoster(Name = "ArenaRoster"):
    Path = os.path.dirname(__file__)
    ArmyName = "Armies/" + Name +".txt"
    ArmyName = os.path.join(Path, ArmyName)
    File = open(ArmyName)
    PlayerUnits = []
    for line in File:
        line = line[:-1]
        PlayerUnits.append(ClassDictionary[line][0])
    File.close()
    return PlayerUnits

def ArenaSelection(Special = False):
    Screen = pygame.display.set_mode((1200,600), 0, 32)
    Screen.blit(pygame.transform.scale(Background, (1200, 600)), (0, 0))
    if Special:
        Unit1 = UnitsList[random.randint(1,len(UnitsList)-4)]
        Unit2 = UnitsList[random.randint(1,len(UnitsList)-4)]
        Unit3 = UnitsList[random.randint(1,len(UnitsList)-4)]
    else:
        Unit1 = UnitsList[random.randint(1,8)]
        Unit2 = UnitsList[random.randint(1,8)]
        Unit3 = UnitsList[random.randint(1,8)]
    PlaceCard(Unit1,1)
    PlaceCard(Unit2,2)
    PlaceCard(Unit3,3)
    Selected = False
    while not Selected:
        for event in pygame.event.get():
            MousePos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()   
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (MousePos[0] in range (50,400)) and (MousePos[1] in range (50,550)):
                    pygame.mixer.Sound.play(SelectSound)
                    return Unit1
                    Selected = True
                if (MousePos[0] in range (425,725)) and (MousePos[1] in range (50,550)):
                    pygame.mixer.Sound.play(SelectSound)
                    return Unit2
                    Selected = True
                if (MousePos[0] in range (775,1100)) and (MousePos[1] in range (50,550)):
                    pygame.mixer.Sound.play(SelectSound)
                    return Unit3
                    Selected = True

def PlaceCard(ChosenUnit,Number):
    x = 25*Number + (325*(Number-1))
    #pygame.draw.polygon(Screen, WHITE, [(x,100),(x+200,100),(x+200,500),(x,500)])
    Screen.blit(Unitcard,(x,0))
    
    if ChosenUnit == Swordsman:
        Screen.blit(SwordsmanPicture, (x+180, 50))
    elif ChosenUnit == Archer:
        Screen.blit(ArcherPicture, (x+180, 50))
    elif ChosenUnit == Beserker:
        Screen.blit(BeserkerPicture, (x+180, 50))
    elif ChosenUnit == Cavalry:
        Screen.blit(CavalryPicture, (x+180, 50))
    elif ChosenUnit == Catapult:
        Screen.blit(CatapultPicture, (x+200, 50))
    elif ChosenUnit == Ninja:
        Screen.blit(NinjaPicture, (x+180, 50))
    elif ChosenUnit == Pikeman:
        Screen.blit(PikemanPicture, (x+180, 50))
    elif ChosenUnit == Samurai:
        Screen.blit(SamuraiPicture, (x+180, 50))
    elif ChosenUnit == Healer:
        Screen.blit(HealerPicture, (x+180, 50))
    elif ChosenUnit == Paladin:
        Screen.blit(PaladinPicture, (x+180, 55))
        
    text = font.render(ChosenUnit.Name, True, BLACK)
    Screen.blit(text,(x+140,235))
    text = font.render(str(ChosenUnit.Damage), True, BLACK)
    Screen.blit(text,(x+140,255))
    text = font.render(str(ChosenUnit.Health), True, BLACK)
    Screen.blit(text,(x+140,275))
    text = font.render(str(ChosenUnit.Armour), True, BLACK)
    Screen.blit(text,(x+140,295))
    text = font.render(str(ChosenUnit.Range), True, BLACK)
    Screen.blit(text,(x+140,315))
    text = font.render(str(ChosenUnit.Movement), True, BLACK)
    Screen.blit(text,(x+140,335))
    text = font.render(ChosenUnit.Ability, True, BLACK)
    Screen.blit(text,(x+140,355))
    pygame.display.update()
    

def PreBattleScreen(PlayerUnits,Army="Arena"):
    setupgrid(ArmySizeX,ArmySizeY,1)
    for x in range (ArmySizeX):
        text = font.render(str(x), True, NOTWHITE)
        Screen.blit(text,(5+(width*1.5)+(width*x)+(5*x),20))
    for y in range (ArmySizeY):
        text = font.render(str(y), True, NOTWHITE)
        Screen.blit(text,(20,5+(height*1.5)+(height*y)+(5*y)))    
    ShowArmy(Army)
    pygame.draw.polygon(Screen, GREEN, [(marginwidth,marginheigth),(39 + marginwidth,marginheigth),(marginwidth+39,4+marginheigth),(marginwidth,4+marginheigth)])
    Screen.blit(Button,(870,400))
    text = font.render("Continue", True, BLACK)
    Screen.blit(text,(950,495))
    UnitsInRoster(PlayerUnits)
    pygame.display.update()
    
def UnitsInRoster(Roster,Highlighted=99):
    text = font.render("Army Roster:", True, WHITE)
    Screen.blit(text,(50,280))
    Start = 0
    n = 0
    Total = 0
    for x in range (0,20):
        Screen.blit(LableSword,(Start,270+(80*n)))
        if n < 3:
            n=n+1
        else:
            n=0
            Start = Start + 150

    Start = 0
    n = 0
    for x in Roster:
        Name = x.Name
        if Highlighted == Total:
            Screen.blit(pygame.transform.flip(Pointer, True, False), (Start+90,295+(80*n)))
        else:
            Screen.blit(LableSword,(Start,270+(80*n)))
        text = font.render(Name, True, BLACK)
        Screen.blit(text,(Start+35,305+(80*n)))
        Total = Total+1
        if n < 3:
            n=n+1
        else:
            n=0
            Start = Start + 150
    pygame.display.update()
    return Total
    
    
#Allow the player to choose where to place their units in a battle     
def BattlePlacement(UnitsLeft,Arena = "ArenaPlayer", Control = True):
    CurrentX=0
    CurrentY=0
    UnitChoice = 0
    PlayerArmyGrid = [ [0]*(ArmySizeY) for _ in range(ArmySizeX) ]
    while Control:

            
        for event in pygame.event.get():
            Start = 20
            Selected = 0
            MousePos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()   
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (MousePos[0] in range (45,315)) and (MousePos[1] in range (45,270)) and event.button == 1:
                    CurrentX = MousePos[0] - 45
                    CurrentX = CurrentX//45
                    CurrentY = MousePos[1] - 45
                    CurrentY = CurrentY//45
                    if PlayerArmyGrid[CurrentX][CurrentY] == 0 and UnitChoice != 0:
                        PlayerArmyGrid[CurrentX][CurrentY] = UnitChoice.Name
                        Temp = ClassDictionary[PlayerArmyGrid[CurrentX][CurrentY]][0]
                        PlaceUnit(CurrentX,CurrentY,Temp,1,0,1)
                        UnitsLeft.remove(UnitChoice)
                        UnitsInRoster(UnitsLeft)
                        UnitChoice = 0
                        pygame.mixer.Sound.play(SelectSound)
                    elif UnitChoice != 0:
                        UnitsLeft.append(ClassDictionary[PlayerArmyGrid[CurrentX][CurrentY]][0])
                        PlayerArmyGrid[CurrentX][CurrentY] = UnitChoice.Name
                        Temp = ClassDictionary[PlayerArmyGrid[CurrentX][CurrentY]][0]
                        PlaceUnit(CurrentX,CurrentY,Temp,1,0,1)
                        UnitsLeft.remove(UnitChoice)
                        UnitsInRoster(UnitsLeft)
                        UnitChoice = 0
                        pygame.mixer.Sound.play(SelectSound)
                    else:
                        dumb = 1
                n=0
                if (MousePos[0] in range (45,315)) and (MousePos[1] in range (45,270)) and event.button == 3:
                    CurrentX = MousePos[0] - 45
                    CurrentX = CurrentX//45
                    CurrentY = MousePos[1] - 45
                    CurrentY = CurrentY//45
                    if PlayerArmyGrid[CurrentX][CurrentY] != 0:
                        UnitsLeft.append(ClassDictionary[PlayerArmyGrid[CurrentX][CurrentY]][0])
                        PlayerArmyGrid[CurrentX][CurrentY] = 0                           
                        RemoveUnit(CurrentX,CurrentY,1)
                        UnitsInRoster(UnitsLeft)
                        UnitChoice = 0
                        pygame.mixer.Sound.play(SelectSound)
                for i in UnitsLeft:
                    if (MousePos[0] in range (Start,Start+100)) and (MousePos[1] in range (300+(80*n),325+(80*n))) and event.button == 1:        
                        UnitChoice = i
                        UnitsInRoster(UnitsLeft, Selected)
                        pygame.mixer.Sound.play(SelectSound)
                        pygame.display.update()
                    if n < 3:
                        n=n+1
                    else:
                        n=0
                        Start = Start + 150
                    Selected = Selected +1
                if (MousePos[0] in range (800,1000)) and (MousePos[1] in range (480,520)):
                    Control = False
    SaveArmy(Arena,PlayerArmyGrid)

#Draw all the player options for their unit on the board
def DrawUnitOptions(x,y):
    Allowed = [ [0]*(BattleScreenY) for _ in range(BattleScreenX) ]
    w = 5
    pygame.draw.circle(Screen, BLUE, ((x*45)+25,(y*45)+25), 18, 2)
    Allowed[x][y] = "Moveable"
    SelectedUnit = ClassDictionary[BattleStatus[x][y][1]][0]
    Dumb = True
    if BattleStatus[x][y][1] == "Catapult":
        if BattleStatus[x][y][4] == 0:
            Dumb = False
        elif BattleStatus[x][y][4] == 1:
            Dumb = True

    if Dumb == True:
        for n in range (1,SelectedUnit.Movement+1):
            if (x+n) < 19 and BattleStatus[x+n][y] == 0:
                pygame.draw.polygon(Screen, GREEN, [(2+w+((x+n)*45),12+w+((y)*45)),(20+w+((x+n)*45),12+w+((y)*45)),(20+w+((x+n)*45),2+w+((y)*45)),(38+w+((x+n)*45),20+w+((y)*45)),(20+w+((x+n)*45),38+w+((y)*45)),(20+w+((x+n)*45),28+w+((y)*45)),(2+w+((x+n)*45),28+w+((y)*45))],2)
                Allowed[x+n][y] = "Moveable"
            if (x-n) > 0 and BattleStatus[x-n][y] == 0:
                pygame.draw.polygon(Screen, GREEN, [(38+w+((x-n)*45),12+w+((y)*45)),(20+w+((x-n)*45),12+w+((y)*45)),(20+w+((x-n)*45),2+w+((y)*45)),(2+w+((x-n)*45),20+w+((y)*45)),(20+w+((x-n)*45),38+w+((y)*45)),(20+w+((x-n)*45),28+w+((y)*45)),(38+w+((x-n)*45),28+w+((y)*45))],2)
                Allowed[x-n][y] = "Moveable"
            if (y+n) < 5 and BattleStatus[x][y+n] == 0:
                pygame.draw.polygon(Screen, GREEN, [(12+w+((x)*45),2+w+((y+n)*45)),(12+w+((x)*45),20+w+((y+n)*45)),(2+w+((x)*45),20+w+((y+n)*45)),(20+w+((x)*45),38+w+((y+n)*45)),(38+w+((x)*45),20+w+((y+n)*45)),(28+w+((x)*45),20+w+((y+n)*45)),(28+w+((x)*45),2+w+((y+n)*45))],2)
                Allowed[x][y+n] = "Moveable"
            if (y-n) > -1 and BattleStatus[x][y-n] == 0:
                pygame.draw.polygon(Screen, GREEN, [(12+w+((x)*45),38+w+((y-n)*45)),(12+w+((x)*45),20+w+((y-n)*45)),(2+w+((x)*45),20+w+((y-n)*45)),(20+w+((x)*45),2+w+((y-n)*45)),(38+w+((x)*45),(20+w+((y-n)*45))),(28+w+((x)*45),(20+w+((y-n)*45))),(28+w+((x)*45),(38+w+((y-n)*45)))],2)
                Allowed[x][y-n] = "Moveable"
            if n > 1:
                if (y+1) < 5 and (x+1) < 19 and BattleStatus[x+1][y+1] == 0:
                    pygame.draw.polygon(Screen, GREEN, [(12+w+((x+1)*45),2+w+((y+1)*45)),(12+w+((x+1)*45),20+w+((y+1)*45)),(2+w+((x+1)*45),20+w+((y+1)*45)),(20+w+((x+1)*45),38+w+((y+1)*45)),(38+w+((x+1)*45),20+w+((y+1)*45)),(28+w+((x+1)*45),20+w+((y+1)*45)),(28+w+((x+1)*45),2+w+((y+1)*45))],2)
                    Allowed[x+1][y+1] = "Moveable"
                if (y+1) < 5 and (x-1) >0 and BattleStatus[x-1][y+1] == 0:
                    pygame.draw.polygon(Screen, GREEN, [(12+w+((x-1)*45),2+w+((y+1)*45)),(12+w+((x-1)*45),20+w+((y+1)*45)),(2+w+((x-1)*45),20+w+((y+1)*45)),(20+w+((x-1)*45),38+w+((y+1)*45)),(38+w+((x-1)*45),20+w+((y+1)*45)),(28+w+((x-1)*45),20+w+((y+1)*45)),(28+w+((x-1)*45),2+w+((y+1)*45))],2)
                    Allowed[x-1][y+1] = "Moveable"
                if (y-1) > -1 and (x-1) >0 and BattleStatus[x-1][y-1] == 0:
                    pygame.draw.polygon(Screen, GREEN, [(12+w+((x-1)*45),38+w+((y-1)*45)),(12+w+((x-1)*45),20+w+((y-1)*45)),(2+w+((x-1)*45),20+w+((y-1)*45)),(20+w+((x-1)*45),2+w+((y-1)*45)),(38+w+((x-1)*45),(20+w+((y-1)*45))),(28+w+((x-1)*45),(20+w+((y-1)*45))),(28+w+((x-1)*45),(38+w+((y-1)*45)))],2)
                    Allowed[x-1][y-1] = "Moveable"
                if (y-1) > -1 and (x+1) <19 and BattleStatus[x+1][y-1] == 0:
                    pygame.draw.polygon(Screen, GREEN, [(12+w+((x+1)*45),38+w+((y-1)*45)),(12+w+((x+1)*45),20+w+((y-1)*45)),(2+w+((x+1)*45),20+w+((y-1)*45)),(20+w+((x+1)*45),2+w+((y-1)*45)),(38+w+((x+1)*45),(20+w+((y-1)*45))),(28+w+((x+1)*45),(20+w+((y-1)*45))),(28+w+((x+1)*45),(38+w+((y-1)*45)))],2)
                    Allowed[x+1][y-1] = "Moveable"                
        pygame.display.update()
        
        ##Attack movement squares
        if SelectedUnit != Healer:
            for n in range (1,SelectedUnit.Range+1):
                if (x+n) < 19 and BattleStatus[x+n][y] != 0:
                    AttackPossible = CheckTeam(x,y,x+n,y)
                    if AttackPossible:
                        if n == 1:
                            Screen.blit(pygame.transform.scale(MeleeSymbol, (32, 32)),(((x+n)*45)+5,(((y)*45)+10)))
                        else:
                            Screen.blit(pygame.transform.scale(RangedSymbol, (32, 32)),(((x+n)*45)+10,(((y)*45)+10)))
                        Allowed[x+n][y] = "Attackable"
                if (x-n) > 0 and BattleStatus[x-n][y] != 0:
                    AttackPossible = CheckTeam(x,y,x-n,y)
                    if AttackPossible:
                        if n == 1:
                            Screen.blit(pygame.transform.scale(MeleeSymbol, (32, 32)),(((x-n)*45)+5,(((y)*45)+10)))
                        else:
                            Screen.blit(pygame.transform.scale(RangedSymbol, (32, 32)),(((x-n)*45)+10,(((y)*45)+10)))
                        Allowed[x-n][y] = "Attackable"
                if (y+n) < 5 and BattleStatus[x][y+n] != 0:
                    AttackPossible = CheckTeam(x,y,x,y+n)
                    if AttackPossible:
                        if n == 1:
                            Screen.blit(pygame.transform.scale(MeleeSymbol, (32, 32)),(((x)*45)+5,(((y+n)*45)+10)))
                        else:
                            Screen.blit(pygame.transform.scale(RangedSymbol, (32, 32)),(((x)*45)+10,(((y+n)*45)+10)))
                        Allowed[x][y+n] = "Attackable"
                if (y-n) > -1 and BattleStatus[x][y-n] != 0:
                    AttackPossible = CheckTeam(x,y,x,y-n)
                    if AttackPossible:
                        if n == 1:
                            Screen.blit(pygame.transform.scale(MeleeSymbol, (32, 32)),(((x)*45)+5,(((y-n)*45)+10)))
                        else:
                            Screen.blit(pygame.transform.scale(RangedSymbol, (32, 32)),(((x)*45)+10,(((y-n)*45)+10)))
                        Allowed[x][y-n] = "Attackable"
        else:
            for n in range (1,SelectedUnit.Range+1):
                if (x+n) < 19 and BattleStatus[x+n][y] != 0:
                    AttackPossible = CheckTeam(x,y,x+n,y)
                    if not AttackPossible:
                        pygame.draw.polygon(Screen, GREEN, [(2+w+((x+n)*45),17+w+((y)*45)),(17+w+((x+n)*45),17+w+((y)*45)),(17+w+((x+n)*45),2+w+((y)*45)),(23+w+((x+n)*45),w+((y)*45)),(23+w+((x+n)*45),17+w+((y)*45)),(38+w+((x+n)*45),17+w+((y)*45)),(38+w+((x+n)*45),23+w+((y)*45)),(23+w+((x+n)*45),23+w+((y)*45)),(23+w+((x+n)*45),38+w+((y)*45)),(17+w+((x+n)*45),38+w+((y)*45)),(17+w+((x+n)*45),23+w+((y)*45)),(2+w+((x+n)*45),23+w+((y)*45))],2)
                        Allowed[x+n][y] = "Healable"
                if (x-n) > 0 and BattleStatus[x-n][y] != 0:
                    AttackPossible = CheckTeam(x,y,x-n,y)
                    if not AttackPossible:
                        pygame.draw.polygon(Screen, GREEN, [(2+w+((x-n)*45),17+w+((y)*45)),(17+w+((x-n)*45),17+w+((y)*45)),(17+w+((x-n)*45),2+w+((y)*45)),(23+w+((x-n)*45),w+((y)*45)),(23+w+((x-n)*45),17+w+((y)*45)),(38+w+((x-n)*45),17+w+((y)*45)),(38+w+((x-n)*45),23+w+((y)*45)),(23+w+((x-n)*45),23+w+((y)*45)),(23+w+((x-n)*45),38+w+((y)*45)),(17+w+((x-n)*45),38+w+((y)*45)),(17+w+((x-n)*45),23+w+((y)*45)),(2+w+((x-n)*45),23+w+((y)*45))],2)
                        Allowed[x-n][y] = "Healable"
                if (y+n) < 5 and BattleStatus[x][y+n] != 0:
                    AttackPossible = CheckTeam(x,y,x,y+n)
                    if not AttackPossible:
                        pygame.draw.polygon(Screen, GREEN, [(2+w+((x)*45),17+w+((y+n)*45)),(17+w+((x)*45),17+w+((y+n)*45)),(17+w+((x)*45),2+w+((y+n)*45)),(23+w+((x)*45),w+((y+n)*45)),(23+w+((x)*45),17+w+((y+n)*45)),(38+w+((x)*45),17+w+((y+n)*45)),(38+w+((x)*45),23+w+((y+n)*45)),(23+w+((x)*45),23+w+((y+n)*45)),(23+w+((x)*45),38+w+((y+n)*45)),(17+w+((x)*45),38+w+((y+n)*45)),(17+w+((x)*45),23+w+((y+n)*45)),(2+w+((x)*45),23+w+((y+n)*45))],2)
                        Allowed[x][y+n] = "Healable"
                if (y-n) > -1 and BattleStatus[x][y-n] != 0:
                    AttackPossible = CheckTeam(x,y,x,y-n)
                    if not AttackPossible:
                        pygame.draw.polygon(Screen, GREEN, [(2+w+((x)*45),17+w+((y-n)*45)),(17+w+((x)*45),17+w+((y-n)*45)),(17+w+((x)*45),2+w+((y-n)*45)),(23+w+((x)*45),w+((y-n)*45)),(23+w+((x)*45),17+w+((y-n)*45)),(38+w+((x)*45),17+w+((y-n)*45)),(38+w+((x)*45),23+w+((y-n)*45)),(23+w+((x)*45),23+w+((y-n)*45)),(23+w+((x)*45),38+w+((y-n)*45)),(17+w+((x)*45),38+w+((y-n)*45)),(17+w+((x)*45),23+w+((y-n)*45)),(2+w+((x)*45),23+w+((y-n)*45))],2)
                        Allowed[x][y-n] = "Healable"            
    pygame.display.update()
    return Allowed


def CurrentRound(Round,Finish = False):
    Screen = pygame.display.set_mode((1200,600), 0, 32)
    Screen.fill(WHITE)
    if Finish:
        text = Bigfont.render("You got to round: "+str(Round), True, BLACK)
    else:
        text = Bigfont.render("Round: "+str(Round), True, BLACK)
    Screen.blit(text,(100,50))
    pygame.display.update()
    time.sleep(1)

def DisplayUnitCard(x,y,ChosenUnit = "-1"):
    if ChosenUnit == "-1":
        ChosenUnit = ClassDictionary[BattleStatus[x][y][1]][0]
        x = 700
        y = 300
    Screen.blit(StatsCard,(x-50,y))
    x=x+35
    y=y+28
    if ChosenUnit == Swordsman:
        Screen.blit(SwordsmanPicture, (x, y))
    elif ChosenUnit == Archer:
        Screen.blit(ArcherPicture, (x, y))
    elif ChosenUnit == Beserker:
        Screen.blit(BeserkerPicture, (x, y))
    elif ChosenUnit == Cavalry:
        Screen.blit(CavalryPicture, (x, y))
    elif ChosenUnit == Catapult:
        Screen.blit(CatapultPicture, (x, y+15))
    elif ChosenUnit == Ninja:
        Screen.blit(NinjaPicture, (x, y))
    elif ChosenUnit == Pikeman:
        Screen.blit(PikemanPicture, (x, y))
    elif ChosenUnit == Spearman:
        Screen.blit(SpearmanPicture, (x, y))
    elif ChosenUnit == Healer:
        Screen.blit(HealerPicture, (x, y))
    elif ChosenUnit == Samurai:
        Screen.blit(SamuraiPicture, (x, y))
    y=y+90
    x=x-20
    text = font.render(ChosenUnit.Name, True, BLACK)
    Screen.blit(text,(x,y))
    text = font.render(str(ChosenUnit.Health), True, BLACK)
    Screen.blit(text,(x,y+10))
    text = font.render(str(ChosenUnit.Damage), True, BLACK)
    Screen.blit(text,(x,y+20))
    text = font.render(str(ChosenUnit.Armour), True, BLACK)
    Screen.blit(text,(x,y+30))
    text = font.render(str(ChosenUnit.Range), True, BLACK)
    Screen.blit(text,(x,y+40))
    text = font.render(str(ChosenUnit.Movement), True, BLACK)
    Screen.blit(text,(x,y+50))
    text = font.render(ChosenUnit.Ability, True, BLACK)
    Screen.blit(text,(x,y+60))
    pygame.display.update()    

#Player options for moveing and attacking with there unit
def PlayerBattleChoice(x,y):
    SelectedUnit = ClassDictionary[BattleStatus[x][y][1]][0]
    Allowed = [ [0]*(BattleScreenY) for _ in range(BattleScreenX) ]
    Allowed = DrawUnitOptions(x,y)
    StartX = x
    StartY = y
    Control = True
    UnitChange = False
    while Control:
        for event in pygame.event.get():
            MousePos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()   
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (MousePos[0] in range (5,900)) and (MousePos[1] in range (5,225)) and event.button == 1:
                    CurrentX = MousePos[0]
                    CurrentX = CurrentX//45
                    CurrentY = MousePos[1]
                    CurrentY = CurrentY//45
                    if BattleStatus[CurrentX][CurrentY] != 0:
                        DisplayUnitCard(CurrentX,CurrentY)                    
                    if Allowed[CurrentX][CurrentY] == "Moveable":
                        if BattleStatus[x][y][1] != "Catapult":
                            Movement(x,y,CurrentX,CurrentY,SelectedUnit.Colour,SelectedUnit.Name,BattleStatus[x][y][2],1)
                            Status = "Moved"
                            Control = False
                            StatusX = CurrentX
                            StatusY = CurrentY
                        else:
                            if BattleStatus[x][y][4] == 1:
                                BattleStatus[x][y] = (BattleStatus[x][y][0],BattleStatus[x][y][1],BattleStatus[x][y][2],BattleStatus[x][y][3],0)
                                Movement(x,y,CurrentX,CurrentY,SelectedUnit.Colour,SelectedUnit.Name,BattleStatus[x][y][2],1)
                                Status = "Moved"
                                Control = False
                                StatusX = CurrentX
                                StatusY = CurrentY
                            else:
                                BattleStatus[x][y] = (BattleStatus[x][y][0],BattleStatus[x][y][1],BattleStatus[x][y][2],BattleStatus[x][y][3],1)
                                BoardText(x,y,0,0,-2)
                                Status = "Moved"
                                Control = False
                                StatusX = CurrentX
                                StatusY = CurrentY
                                
                    elif Allowed[CurrentX][CurrentY] == "Attackable":
                        Attack(x,y,CurrentX,CurrentY)
                        Status = "Attacked"
                        StatusX = x
                        StatusY = y
                        Control= False
                        if BattleStatus[x][y][1] == "Catapult":
                            BattleStatus[x][y] = (BattleStatus[x][y][0],BattleStatus[x][y][1],BattleStatus[x][y][2],BattleStatus[x][y][3],0)

                    elif Allowed[CurrentX][CurrentY] == "Healable":
                        Heal(x,y,CurrentX,CurrentY)
                        Status = "Healed"
                        StatusX = x
                        StatusY = y
                        Control= False
                        
                    elif BattleStatus[CurrentX][CurrentY] !=0:
                        if BattleStatus[CurrentX][CurrentY][3] ==1:
                            ClearBoard(Allowed)
                            Allowed = DrawUnitOptions(CurrentX,CurrentY)
                            UnitChange = True
                            x = CurrentX
                            y = CurrentY
                            SelectedUnit = ClassDictionary[BattleStatus[x][y][1]][0]
    if UnitChange:
        Status = "Moved"
        StatusX = StartX
        StatusY = StartY        
    ClearBoard(Allowed)
    return StatusX,StatusY,Status

#Get rid of all the player options and make grid clean again without arrows and that
def ClearBoard(Allowed):
    for y in range(BattleScreenY):
        for x in range(BattleScreenX):
            if Allowed[x][y] != 0:
                if BattleStatus[x][y] !=0:
                    TempUnit = ClassDictionary[BattleStatus[x][y][1]][0]
                    RemoveUnit(x,y,-1)
                    PlaceUnit(x,y,TempUnit,BattleStatus[x][y][3],TempUnit.Health - BattleStatus[x][y][2],0,True)
                else:
                    RemoveUnit(x,y)
    pygame.display.update()    

CampaginMap = [ ["0"]*(10) for _ in range(15) ]



###Capmagin not finished can ignore from here but idea is map is randomly generate and you will be able to encounter
#armies to fight, taverns to buy units, with bosses every so many columns along with the idea being get as far along as possible 
def Campagin(Name):
    Path = os.path.dirname(__file__)
    ArmyName = Name + ".txt"
    ArmyName = os.path.join(Path, ArmyName)    
    f= open(ArmyName,"w")
    f.write("")
    f.close()
    Start=0
    ArmyRoster = [Player,]
    Inventory = []
    SaveRoster(ArmyRoster,"201"+Name)
    SelectedTeir = 1
    Gold = 10
    for x in range(0,15):
        NewColumn = CreateColumn()
        SaveColumn(Name,NewColumn)
    Loadgrid(Name,Start)
    CampaginMap[0][0] = "-1"
    
    CurrentX = 0
    CurrentY = 0
    Maximum = 0
    Power = GetPower(ArmyRoster)
    DisplayGrid(Gold,Start,Power)
    DisplayRoster(ArmyRoster,SelectedTeir)
    DisplayInventory(Inventory)
    Control = True
    while Control:
        for event in pygame.event.get():
            Power = GetPower(ArmyRoster)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()   
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_w and CurrentY-1>=0:
                    if CampaginMap[CurrentX][CurrentY-1] == "0":
                        CampaginMap[CurrentX][CurrentY] = "0"
                        CurrentY = CurrentY -1
                        CampaginMap[CurrentX][CurrentY] = "-1"
                        pygame.mixer.Sound.play(SelectSound)
                    else:
                        Gold,Control,ArmyRoster = CampaginDecider(CurrentX,CurrentY-1,Gold,Name,ArmyRoster)
                if event.key == pygame.K_s and CurrentY+1<10:
                    if CampaginMap[CurrentX][CurrentY+1] == "0":
                        CampaginMap[CurrentX][CurrentY] = "0"
                        CurrentY = CurrentY +1
                        CampaginMap[CurrentX][CurrentY] = "-1"
                        pygame.mixer.Sound.play(SelectSound)

                    else:
                        Gold,Control,ArmyRoster = CampaginDecider(CurrentX,CurrentY+1,Gold,Name,ArmyRoster)
                if event.key == pygame.K_a and CurrentX-1>=0:
                    if CampaginMap[CurrentX-1][CurrentY] == "0":
                        CampaginMap[CurrentX][CurrentY] = "0"
                        CurrentX = CurrentX -1
                        CampaginMap[CurrentX][CurrentY] = "-1"
                        if CurrentX >10:
                            Start = Start +1
                            NewColumn = CreateColumn()
                            SaveColumn(Name,NewColumn)
                            Loadgrid(Name,Start)
                            CurrentX = CurrentX-1
                            CampaginMap[CurrentX][CurrentY] = "-1"
                            
                        else:
                            DisplayGrid(Gold,CurrentX+Start,Power)
                            pygame.mixer.Sound.play(SelectSound)
                    else:
                        Gold,Control,ArmyRoster = CampaginDecider(CurrentX-1,CurrentY,Gold,Name,ArmyRoster)
                if event.key == pygame.K_d:

                    if CampaginMap[CurrentX+1][CurrentY] == "0":
                        CampaginMap[CurrentX][CurrentY] = "0"
                        CurrentX = CurrentX +1
                        CampaginMap[CurrentX][CurrentY] = "-1"
                        if CurrentX >10:
                            Start = Start +1
                            if Start > Maximum:
                                NewColumn = CreateColumn()
                                SaveColumn(Name,NewColumn)
                                Maximum = Maximum+1
                            Loadgrid(Name,Start)
                            CurrentX = CurrentX-1
                            CampaginMap[CurrentX][CurrentY] = "-1"
                            DisplayGrid(Gold,CurrentX+Start,Power)
                            pygame.mixer.Sound.play(SelectSound)
                        else:
                            pygame.mixer.Sound.play(SelectSound)
                    else:
                        Gold,Control,ArmyRoster = CampaginDecider(CurrentX+1,CurrentY,Gold,Name,ArmyRoster)
                DisplayGrid(Gold,CurrentX+Start,Power)
                DisplayRoster(ArmyRoster,SelectedTeir)
                DisplayInventory(Inventory)
    MainMenu()


def GetPower(Roster):
    Total = 0
    for x in Roster:
        Total = Total + x.Points
    return Total
    
def CreateColumn():
    List = []
    for x in range(0,10):
        Choice = random.randint(0,1000)
        
        if Choice >= 0 and Choice <40:#Normal Army
            List.append(1)
        elif Choice >= 40 and Choice <60:#City
            List.append(3)
        elif Choice >= 60 and Choice <65:#Dragon
            List.append(4)
        elif Choice >= 65 and Choice <70:#Oger
            List.append(5)
        elif Choice >= 70 and Choice <100:#Buy unit and get quests
            List.append(2)
        elif Choice >= 100 and Choice <110:#Mage guild to buy spells and get quests
            List.append(6)
        elif Choice >= 110 and Choice <120:#Armoury to buy items and get quests
            List.append(7)
        else:
            List.append(0)

    return List

def SaveColumn(FileName,Column):
    f=open(FileName+".txt", "a+")
    for x in Column:
        f.write(str(x)+",")
    f.write("\n")
    f.close

def Loadgrid(Name,Start):
    f=open(Name+".txt", "r")
    n = 0
    Column = 0
    for x in f:
        if n >=Start and n<=Start+14:
            x = x.split(",")
            for i in range(0,10):
                CampaginMap[Column][i] = x[i]
            Column = Column +1
        n=n+1

def DisplayGrid(Gold,Score,Power):
    setupgrid(15,10,0,False)
    DisplayGold(Gold)
    DisplayScore(Score)
    DisplayPower(Power)
    for x in range(15):
        for y in range(10):
            marginwidth = 5 +(x*45)
            marginheigth = 5+(y*45)
            if CampaginMap[x][y] == "1":
                Screen.blit(CavalryPicture, (marginwidth-5, marginheigth-10))
                Screen.blit(pygame.transform.flip(SwordsmanPicture, True, False), (marginwidth-15, marginheigth-10))
                Screen.blit(SwordsmanPicture, (marginwidth+15, marginheigth-10))
            elif CampaginMap[x][y] == "-1":
                Screen.blit(PlayerPicture, (marginwidth, marginheigth))
            elif CampaginMap[x][y] == "2":
                pygame.draw.polygon(Screen, GREEN, [(5 +(x*45),5+(y*45)),(45+ (x*45),5 +(y*45)),(45+ (x*45),45 +(y*45)),(5+(x*45),45 +(y*45))])
            elif CampaginMap[x][y] == "3":
                Screen.blit(CastlePicture, (marginwidth-2, marginheigth-2))
            elif CampaginMap[x][y] == "4":
                pygame.draw.polygon(Screen, YELLOW, [(5 +(x*45),5+(y*45)),(45+ (x*45),5 +(y*45)),(45+ (x*45),45 +(y*45)),(5+(x*45),45 +(y*45))])
            elif CampaginMap[x][y] == "5":
                pygame.draw.polygon(Screen, PURPLE, [(5 +(x*45),5+(y*45)),(45+ (x*45),5 +(y*45)),(45+ (x*45),45 +(y*45)),(5+(x*45),45 +(y*45))])
            elif CampaginMap[x][y] == "6":
                pygame.draw.polygon(Screen, LIGHTBLUE, [(5 +(x*45),5+(y*45)),(45+ (x*45),5 +(y*45)),(45+ (x*45),45 +(y*45)),(5+(x*45),45 +(y*45))])
            elif CampaginMap[x][y] == "7":
                pygame.draw.polygon(Screen, BLACK, [(5 +(x*45),5+(y*45)),(45+ (x*45),5 +(y*45)),(45+ (x*45),45 +(y*45)),(5+(x*45),45 +(y*45))])
    pygame.display.update()



def CampaginDecider(x,y,Gold,ArmyName,ArmyRoster):
    Winner = True
    if CampaginMap[x][y] == "1":
        Gold,Winner,Fight =ArmyEncounter(x,Gold,ArmyName,ArmyRoster)
        if Fight:
            CampaginMap[x][y] = "0"
        ArmyRoster = LoadRoster("201"+ArmyName)
    if CampaginMap[x][y] == "2":
        Gold,ArmyRoster = ShopDialog(Gold,x,ArmyRoster)
        SaveRoster(ArmyRoster,"201"+ArmyName)
        ArmyRoster = LoadRoster("201"+ArmyName)
    if CampaginMap[x][y] == "3":
        Fight = EncounterDialog(35+ (x*10),"City")
        if Fight:
            Gold = Gold + x
            RandomArmy(x*10,"CastleArmy",Teir = "Castle")
            PreBattleScreen(ArmyRoster,"CastleArmy")
            BattlePlacement(ArmyRoster,ArmyName)
            Winner = LoadBattle(ArmyName,"CastleArmy")
            ArmyRoster = LoadRoster("201"+ArmyName)
            CampaginMap[x][y] = "0"
            if Winner ==2 :
                Winner = False        
    if CampaginMap[x][y] == "4":
        Fight = EncounterDialog(100,"Special")
        if Fight:
            Gold = Gold + 10
            RandomArmy(x*10,"Dragon",Teir = "Dragon")
            PreBattleScreen(ArmyRoster,"Dragon")
            BattlePlacement(ArmyRoster,ArmyName)
            Winner = LoadBattle(ArmyName,"Dragon")
            ArmyRoster = LoadRoster("201"+ArmyName)
            CampaginMap[x][y] = "0"
            if Winner ==2 :
                Winner = False     
            else:
                ArmyRoster = ArmyRoster.append(Dragon)
                SaveRoster(ArmyRoster,"201"+Name)
                ArmyRoster = LoadRoster("201"+ArmyName)
    if CampaginMap[x][y] == "5":
        Fight = EncounterDialog(100,"Special")
        if Fight:
            Gold = Gold + 10
            RandomArmy(x*10,"Giant",Teir = "Giant")
            PreBattleScreen(ArmyRoster,"Giant")
            BattlePlacement(ArmyRoster,ArmyName)
            Winner = LoadBattle(ArmyName,"Giant")
            ArmyRoster = LoadRoster("201"+ArmyName)
            CampaginMap[x][y] = "0"
            if Winner ==2 :
                Winner = False 
            else:
                ArmyRoster = ArmyRoster.append(Giant)
                SaveRoster(ArmyRoster,"201"+Name)
                ArmyRoster = LoadRoster("201"+ArmyName)        
    return Gold,Winner,ArmyRoster

def ArmyEncounter(Position,Gold,ArmyName,ArmyRoster):
    Winner = True
    AddedGold = random.randint(1,Position+2)
    if AddedGold <1:
        AddedGold = 1
    Fight = EncounterDialog(AddedGold*10)
    if Fight:
        Gold = Gold +AddedGold
        Points = AddedGold*10
        RandomArmy(Points,"CampaginArmy")
        PreBattleScreen(ArmyRoster,"CampaginArmy")
        BattlePlacement(ArmyRoster,ArmyName)
        Winner = LoadBattle(ArmyName,"CampaginArmy")
        
        if Winner ==2 :
            Winner = False
    return Gold,Winner,Fight

def DisplayGold(Gold):
     text = Bigfont.render("Gold: "+str(Gold), True, BLACK)
     Screen.blit(Coin, (20,475))
     Screen.blit(text, (50,475))
     pygame.display.update()

def DisplayScore(Score):
     text = Bigfont.render("Score: "+str(Score), True, BLACK)
     Screen.blit(ScorePicture, (20,525))
     Screen.blit(text, (50,525))
     pygame.display.update()

def DisplayPower(Power):
     text = Bigfont.render("Power: "+str(Power), True, BLACK)
     Screen.blit(PowerPicture, (170,470))
     Screen.blit(text, (200,475))
     pygame.display.update()

def DisplayRoster(ArmyRoster,SelectedTeir):
    Screen.blit(pygame.transform.scale(Scroll, (400, 250)), (700,25))
    text = Bigfont.render("Roster Goes here", True, BLACK)
    Screen.blit(text, (750,125))
    pygame.display.update()

def DisplayInventory(Inventory):
    Screen.blit(pygame.transform.scale(Scroll, (400, 250)), (700,300))
    text = Bigfont.render("Inventory goes here", True, BLACK)
    Screen.blit(text, (750,400))
    pygame.display.update()
    
def EncounterDialog(Power, Type ="Normal"):
    Decsiscion = True
    Screen.blit(pygame.transform.scale(Scroll, (550, 250)), (80,100))
    if Type == "Normal":
        text = Bigfont.render("This army's power level is "+str(Power), True, BLACK)
    if Type =="City":
        text = Bigfont.render("This outposts power level is "+str(Power), True, BLACK)
    if Type =="Special":
        text = Bigfont.render("This Creatures power level is 100", True, BLACK)
    Screen.blit(text, (150,125))
    text = Bigfont.render("are you sure you whish to attack?", True, BLACK)
    Screen.blit(text, (150,160))
    pygame.draw.polygon(Screen, BLACK, [(400,250),(550,250),(550,300),(400,300)],5)
    pygame.draw.polygon(Screen, BLACK, [(150,250),(300,250),(300,300),(150,300)],5)
    text = Bigfont.render("Yes", True, BLACK)
    Screen.blit(text, (160,260))
    text = Bigfont.render("No", True, BLACK)
    Screen.blit(text, (410,260))
    Control = True
    pygame.display.update()
    while Control:
        for event in pygame.event.get():
            MousePos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()   
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (MousePos[0] in range (150,300)) and (MousePos[1] in range (250,300)) and event.button == 1:
                    Deciscion = True
                    Control = False
                if (MousePos[0] in range (400,550)) and (MousePos[1] in range (250,300)) and event.button == 1:
                    Deciscion = False
                    Control = False


    return Deciscion

def ShopDialog(Gold,Power,ArmyRoster):
    Power = Power*10
    Choice = 0
    AvaliableUnits = []
    while Power > 9 and len(AvaliableUnits) <4:
        x = random.randint(0,7)
        Unit = UnitsList[x]
        if Power - Unit.Points > 0:
            Power = Power - Unit.Points
            AvaliableUnits.append(Unit)
    DrawShop(AvaliableUnits,Choice)
    Control = True
    while Control:
        for event in pygame.event.get():
            MousePos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s and Choice<len(AvaliableUnits)-1:
                    Choice = Choice +1
                    pygame.mixer.Sound.play(SelectSound)
                    DrawShop(AvaliableUnits,Choice)
                if event.key == pygame.K_w and Choice>0:
                    Choice = Choice -1
                    pygame.mixer.Sound.play(SelectSound)
                    DrawShop(AvaliableUnits,Choice)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (MousePos[0] in range (130,290)) and (MousePos[1] in range (310,360)) and event.button == 1 and Gold - AvaliableUnits[Choice].Points >= 0:
                    Gold = Gold - AvaliableUnits[Choice].Points
                    ArmyRoster.append(AvaliableUnits[Choice])
                    AvaliableUnits.pop(Choice)
                    DrawShop(AvaliableUnits,Choice)
                if (MousePos[0] in range (570,600)) and (MousePos[1] in range (100,130)) and event.button == 1:
                    Control = False


    

    return Gold,ArmyRoster

def DrawShop(AvaliableUnits,Choice):

    Screen.blit(pygame.transform.scale(Scroll, (550, 280)), (80,100))
    pygame.draw.polygon(Screen, BLACK, [(570,100),(600,100),(600,130),(570,130)],6)
    pygame.draw.polygon(Screen, BLACK, [(570,100),(600,130)],5)
    pygame.draw.polygon(Screen, BLACK, [(570,130),(600,100)],5)
    Start = 125
    Current = 0
    for x in AvaliableUnits:
        text = Bigfont.render(x.Name, True, BLACK)
        Screen.blit(text, (150,Start))
        if Current == Choice:
            Screen.blit(Pointer, (125,Start-5))
            Screen.blit(pygame.transform.flip(Pointer, True, False), (300,Start-5))
            DisplayUnitCard(400,100,x)
            text = Bigfont.render(str(x.Points), True, BLACK)
            Screen.blit(text, (225,280))
        Start = Start + 35
        Current = Current+1
    pygame.draw.polygon(Screen, BLACK, [(150,310),(310,310),(310,360),(150,360)],5)
    text = Bigfont.render("Buy Now", True, BLACK)
    Screen.blit(text, (160,320))
    text = Bigfont.render("Cost: ", True, BLACK)
    Screen.blit(text, (165,280))
    Screen.blit(Coin, (140,280+2))
    
    pygame.display.update()
    
MainMenu()    

    


