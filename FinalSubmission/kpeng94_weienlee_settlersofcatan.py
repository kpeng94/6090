import pygame,random, math, sys;

## GLOBAL VARIABLES
RADIUS = 75
BCENX = 380
BCENY = 350
ERROR = 10 #clicking boundary error

# RGB Color definitions
black = (0, 0, 0)
grey = (100, 100, 100)
white = (255, 255, 255)
green = (0, 255, 0)
freen = (34, 139, 34)
red   = (255, 0, 0)
blue  = (0, 0, 255)
yellow = (255, 255, 0)
brown = (139, 69, 19)
beige = (245, 245, 220)

def newGame(size = 1000):
    pygame.init()

    window_size = [size+100, size-300]
    screen = pygame.display.set_mode(window_size)
    # screen.fill(blue)
    pygame.display.set_caption("Settlers of Catan")

    board = Board()
    dice = Dice()
    
    turnCount = 0
    # settSelection = False

    #INITIALIZE PLAYERS
    p1 = Player(board, 1)#RED
    p2 = Player(board, 2)#BLUE
    p3 = Player(board, 3)#WHITE
    p4 = Player(board, 4)#ORANGE
    # p1.resInv = {"wheat": 5, "stone": 5,"wood": 5,"brick": 5, "sheep": 5}
    p1.resInv = {"wheat": 1, "stone": 0,"wood": 1,"brick": 0, "sheep": 1}
    # p2.resInv = {"wheat": 4, "stone": 1,"wood": 4, "brick": 1, "sheep": 4}
    p2.resInv = {"wheat": 0, "stone": 1,"wood": 0,"brick": 1, "sheep": 1}
    p3.resInv = {"wheat": 0, "stone": 1,"wood": 1,"brick": 0, "sheep": 1}
    p4.resInv = {"wheat": 1, "stone": 0,"wood": 1,"brick": 0, "sheep": 1}
    
    drawbg(board,screen,p1,p2,p3,p4)
    drawButtons1(board,screen)
    mainLoop(screen, dice, board, turnCount, False, p1, p2, p3, p4)


def endT(board, screen, p1,p2,p3,p4):
    plarray=[p1,p2,p3,p4]
    curPlayer=0
    for i in xrange(0,4):
        if plarray[i].turn==True:
            plarray[i].turn=False
            plarray[i].diceRolled=False
            curPlayer=i
    if(1 == (plarray[curPlayer].number % 4) + 1):
        p1.turn = True
        board.resInvPlayer=0
    elif(2 == (plarray[curPlayer].number % 4) + 1):
        p2.turn = True
        board.resInvPlayer=1        
    elif(3 == (plarray[curPlayer].number % 4) + 1):
        p3.turn = True
        board.resInvPlayer=2
    elif(4 == (plarray[curPlayer].number % 4) + 1):
        p4.turn = True
        board.resInvPlayer=3

def drawbg(board, screen, p1,p2,p3,p4):
    """
    draws background, useful for drawing over buttons
    """
    #draws ocean background
    ocean=pygame.image.load("ocean.png")
    oceanRect=ocean.get_rect()
    screen.blit(ocean,oceanRect)
    
    #draws resource box
    resourcebg=pygame.image.load("resourcebg.png").convert_alpha()
    resourcebgRect=resourcebg.get_rect(center=(890,560))
    screen.blit(resourcebg,resourcebgRect)
    
    #draws hexagons
    board.hex.draw(screen)
    
    #draws hexagon numbers
    for hex in board.boardHex:
        hex.drawNumber(screen,board)

    #draws resource inventory
    board.resDisplay.draw(screen)
    if (board.resInvPlayer==0):
        p1.displayResources(board,screen)
    elif (board.resInvPlayer==1):
        p2.displayResources(board,screen)
    elif(board.resInvPlayer==2):
        p3.displayResources(board,screen)
    elif(board.resInvPlayer==3):
        p4.displayResources(board,screen)
def drawPieces(board,screen,p1,p2,p3,p4):
    """
    draws all pieces to the screen
    """
    board.robber.draw(screen)
    p1.roads.draw(screen)
    p2.roads.draw(screen)
    p3.roads.draw(screen)
    p4.roads.draw(screen)
    p1.buildings.draw(screen)
    p2.buildings.draw(screen)
    p3.buildings.draw(screen)
    p4.buildings.draw(screen)

def drawButtons1(board,screen):
    board.buttons.draw(screen)
    for button in board.buttonList:
        button.buttonText(screen)

def drawButtons2(board,screen):
    board.buttons2.draw(screen)
    for button in board.buttonList2:
        button.buttonText(screen)

def drawButtons3(board,screen):
    board.buttons3.draw(screen)
    for button in board.buttonList3:
        button.buttonText(screen)

def menu1(board,screen,player,p1,p2,p3,p4):
    #Build Button
    if (pygame.mouse.get_pressed()==(True,False,False)):
        if (725<pygame.mouse.get_pos()[0]<875) and (130<pygame.mouse.get_pos()[1]<170):
            board.buttonList[0].buttonClick(screen)
            drawButtons1(board,screen)
            pygame.display.flip()
            board.menustate=2
            drawbg(board,screen,p1,p2,p3,p4)
            drawPieces(board,screen,p1,p2,p3,p4)
            drawButtons2(board,screen)
    elif (725<pygame.mouse.get_pos()[0]<875) and (130<pygame.mouse.get_pos()[1]<170):
        board.buttonList[0].buttonHover(screen)
    else:
        board.buttonList[0].image.fill(white)
        board.buttonList[0].buttonText(screen)
    #Trade Button
    if (pygame.mouse.get_pressed()==(True,False,False)):
        if (915<pygame.mouse.get_pos()[0]<1065) and (130<pygame.mouse.get_pos()[1]<170):
            board.buttonList[1].buttonClick(screen)
            drawButtons1(board,screen)
            pygame.display.flip()
            board.menustate=3
            drawbg(board,screen,p1,p2,p3,p4)
            drawPieces(board,screen,p1,p2,p3,p4)
            drawButtons3(board,screen)
    elif (915<pygame.mouse.get_pos()[0]<1065) and (130<pygame.mouse.get_pos()[1]<170):
        board.buttonList[1].buttonHover(screen)
    else:
        board.buttonList[1].image.fill(white)
        board.buttonList[1].buttonText(screen)
    #endTurn Button

    if (pygame.mouse.get_pressed()==(True,False,False)):
        if (915<pygame.mouse.get_pos()[0]<1065) and (380<pygame.mouse.get_pos()[1]<420):
            board.buttonList[2].buttonClick(screen)
            endT(board, screen, p1, p2, p3, p4)
            drawbg(board,screen,p1,p2,p3,p4)
            drawPieces(board, screen, p1,p2,p3,p4)            
    elif (915<pygame.mouse.get_pos()[0]<1065) and (380<pygame.mouse.get_pos()[1]<420):
        board.buttonList[2].buttonHover(screen)
    else:
        board.buttonList[2].image.fill(white)
        board.buttonList[2].buttonText(screen)

    #left Button
    if (pygame.mouse.get_pressed()==(True,False,False)):
        if (1005<pygame.mouse.get_pos()[0]<1035) and (648<pygame.mouse.get_pos()[1]<678):
            board.leftButton.buttonClick(screen)
            board.resInvPlayer=((board.resInvPlayer-1)%4)
            drawbg(board, screen, p1,p2,p3,p4)
    elif (1005<pygame.mouse.get_pos()[0]<1035) and (648<pygame.mouse.get_pos()[1]<678):
        board.leftButton.buttonHover(screen)
    else:
        board.leftButton.image.fill(white)
        board.leftButton.buttonText(screen)

    #right Button
    if (pygame.mouse.get_pressed()==(True,False,False)):
        if (1038<pygame.mouse.get_pos()[0]<1068) and (648<pygame.mouse.get_pos()[1]<678):
            board.rightButton.buttonClick(screen)
            board.resInvPlayer=((board.resInvPlayer+1)%4)
            drawbg(board, screen, p1,p2,p3,p4)
    elif (1038<pygame.mouse.get_pos()[0]<1068) and (648<pygame.mouse.get_pos()[1]<678):
        board.rightButton.buttonHover(screen)
    else:
        board.rightButton.image.fill(white)
        board.rightButton.buttonText(screen)

def menu2(board,screen,player,p1,p2,p3,p4):
    #    drawbg(board,screen,player)
    #    drawPieces(board,screen,p1,p2,p3,p4)
    #    drawButtons2(board,screen)
    # print player.settSelection

    #back button
    if (pygame.mouse.get_pressed()==(True,False,False)):
        if (725<pygame.mouse.get_pos()[0]<875) and (380<pygame.mouse.get_pos()[1]<420):
            board.buttonList2[0].buttonClick(screen)
            drawButtons2(board,screen)
            pygame.display.flip()
            board.menustate=1
            drawbg(board,screen,p1,p2,p3,p4)
            drawPieces(board,screen,p1,p2,p3,p4)
            board.buttonList[0].image.fill(white)
            for button in board.buttonList2:
                button.image.fill(white)
            drawButtons1(board,screen)
            player.roadSelection=False
            player.settSelection=False
            player.citySelection=False
    elif (725<pygame.mouse.get_pos()[0]<875) and (380<pygame.mouse.get_pos()[1]<420):
        board.buttonList2[0].buttonHover(screen)
    else:
        board.buttonList2[0].image.fill(white)
        board.buttonList2[0].buttonText(screen)
        
    #road
    if(player.roadSelection == False):
        if (pygame.mouse.get_pressed()==(True,False,False)):
            if (915<pygame.mouse.get_pos()[0]<1065) and (130<pygame.mouse.get_pos()[1]<170):
                board.buttonList2[1].buttonClick(screen)
                player.roadSelection = True
                player.settSelection = False
                player.citySelection = False
        elif (915<pygame.mouse.get_pos()[0]<1065) and (130<pygame.mouse.get_pos()[1]<170):
            board.buttonList2[1].buttonHover(screen)
        else:
            board.buttonList2[1].image.fill(white)
            board.buttonList2[1].buttonText(screen)
    
    if(player.roadSelection == True):
        if (pygame.mouse.get_pressed()==(True,False,False)):
            if(45<pygame.mouse.get_pos()[0]<715) and (30<pygame.mouse.get_pos()[1]<670):
                # print "OMG NO WAY"
                # print (pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
                player.build(board, "road", (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]), False)
                player.roadSelection = False              

    #settlement
    if(player.settSelection == False):
        if (pygame.mouse.get_pressed()==(True,False,False)):
            if (915<pygame.mouse.get_pos()[0]<1065) and (180<pygame.mouse.get_pos()[1]<220):
                board.buttonList2[2].buttonClick(screen)
                player.settSelection = True
                player.roadSelection = False
                player.citySelection = False
                # print "YEAH"
                # print player.settSelection
        elif (915<pygame.mouse.get_pos()[0]<1065) and (180<pygame.mouse.get_pos()[1]<220):
            board.buttonList2[2].buttonHover(screen)
        else:
            board.buttonList2[2].image.fill(white)
            board.buttonList2[2].buttonText(screen)

    if(player.settSelection == True):
        if (pygame.mouse.get_pressed()==(True,False,False)):
            if(45<pygame.mouse.get_pos()[0]<715) and (30<pygame.mouse.get_pos()[1]<670):
                # print (pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
                player.build(board, "settlement", (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]), False)
                player.settSelection = False              

    #city
    if(player.citySelection == False):
        if (pygame.mouse.get_pressed()==(True,False,False)):
            if (915<pygame.mouse.get_pos()[0]<1065) and (230<pygame.mouse.get_pos()[1]<270):
                board.buttonList2[3].buttonClick(screen)
                player.citySelection = True
                player.roadSelection = False
                player.settSelection = False
        elif (915<pygame.mouse.get_pos()[0]<1065) and (230<pygame.mouse.get_pos()[1]<270):
            board.buttonList2[3].buttonHover(screen)
        else:
            board.buttonList2[3].image.fill(white)
            board.buttonList2[3].buttonText(screen)

    if(player.citySelection == True):
        if (pygame.mouse.get_pressed()==(True,False,False)):
            if(45<pygame.mouse.get_pos()[0]<715) and (30<pygame.mouse.get_pos()[1]<670):
                # print (pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
                player.build(board, "city", (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]), False)
                player.citySelection = False              

    #endTurn Button
    if (pygame.mouse.get_pressed()==(True,False,False)):
        if (915<pygame.mouse.get_pos()[0]<1065) and (380<pygame.mouse.get_pos()[1]<420):
            board.buttonList2[4].buttonClick(screen)
            endT(board, screen, p1, p2, p3, p4)
            drawbg(board,screen,p1,p2,p3,p4)
            drawPieces(board, screen, p1,p2,p3,p4)            
    elif (915<pygame.mouse.get_pos()[0]<1065) and (380<pygame.mouse.get_pos()[1]<420):
        board.buttonList2[4].buttonHover(screen)
    else:
        board.buttonList2[4].image.fill(white)
        board.buttonList2[4].buttonText(screen)

    #left Button
    if (pygame.mouse.get_pressed()==(True,False,False)):
        if (1005<pygame.mouse.get_pos()[0]<1035) and (648<pygame.mouse.get_pos()[1]<678):
            board.leftButton.buttonClick(screen)
            board.resInvPlayer=((board.resInvPlayer-1)%4)
            drawbg(board, screen, p1,p2,p3,p4)
    elif (1005<pygame.mouse.get_pos()[0]<1035) and (648<pygame.mouse.get_pos()[1]<678):
        board.leftButton.buttonHover(screen)
    else:
        board.leftButton.image.fill(white)
        board.leftButton.buttonText(screen)
        
    #right Button
    if (pygame.mouse.get_pressed()==(True,False,False)):
        if (1038<pygame.mouse.get_pos()[0]<1068) and (648<pygame.mouse.get_pos()[1]<678):
            board.rightButton.buttonClick(screen)
            board.resInvPlayer=((board.resInvPlayer+1)%4)
            drawbg(board, screen, p1,p2,p3,p4)
    elif (1038<pygame.mouse.get_pos()[0]<1068) and (648<pygame.mouse.get_pos()[1]<678):
        board.rightButton.buttonHover(screen)
    else:
        board.rightButton.image.fill(white)
        board.rightButton.buttonText(screen)

def menu3(board,screen,player,p1,p2,p3,p4):
    #Trade Button
    if (pygame.mouse.get_pressed()==(True,False,False)):
        if (915<pygame.mouse.get_pos()[0]<1065) and (130<pygame.mouse.get_pos()[1]<170):
            board.buttonList3[0].buttonClick(screen)
            displayTradePrompt(board, screen)
            pygame.display.flip()
            numOfSheep = int(raw_input("How many sheep do you want to trade away?"))
            numOfWood = int(raw_input("Wood?"))
            numOfStone = int(raw_input("Stone?"))
            numOfWheat = int(raw_input("Wheat?"))
            numOfBrick = int(raw_input("Brick?"))
            playerToTradeWith = raw_input("Which player number do you want to trade with?")
            sheepP = int(raw_input("How many sheep would you like?"))
            woodP = int(raw_input("Wood?"))
            stoneP = int(raw_input("Stone?"))
            wheatP = int(raw_input("Wheat?"))
            brickP = int(raw_input("Brick?"))
            myTrades = {"sheep": numOfSheep, "wood": numOfWood, "stone": numOfStone, "wheat": numOfWheat, "brick": numOfBrick}
            otherTrades = {"sheep": sheepP, "wood": woodP, "stone": stoneP, "wheat": wheatP, "brick": brickP}
            result = raw_input("For the other player, would you like to accept the trade? Enter yes or no")
            tradeP = None
            if(playerToTradeWith == "1"):
                tradeP = p1
            if(playerToTradeWith == "2"):
                tradeP = p2
            if(playerToTradeWith == "3"):
                tradeP = p3
            if(playerToTradeWith == "4"):
                tradeP = p4
            player.requestTrade(myTrades, tradeP, otherTrades)
            board.menustate=1
            drawbg(board,screen,p1,p2,p3,p4)
            drawPieces(board,screen,p1,p2,p3,p4)
            board.buttonList[0].image.fill(white)
            drawButtons1(board,screen)
    elif (915<pygame.mouse.get_pos()[0]<1065) and (130<pygame.mouse.get_pos()[1]<170):
        board.buttonList3[0].buttonHover(screen)
    else:
        board.buttonList3[0].image.fill(white)
        board.buttonList3[0].buttonText(screen)


    #back button
    if (pygame.mouse.get_pressed()==(True,False,False)):
        if (725<pygame.mouse.get_pos()[0]<875) and (380<pygame.mouse.get_pos()[1]<420):
            board.buttonList3[1].buttonClick(screen)
            drawButtons3(board,screen)
            pygame.display.flip()
            board.menustate=1
            drawbg(board,screen,p1,p2,p3,p4)
            drawPieces(board,screen,p1,p2,p3,p4)
            board.buttonList[0].image.fill(white)
            drawButtons1(board,screen)
    elif (725<pygame.mouse.get_pos()[0]<875) and (380<pygame.mouse.get_pos()[1]<420):
        board.buttonList3[1].buttonHover(screen)
    else:
        board.buttonList3[1].image.fill(white)
        board.buttonList3[1].buttonText(screen)

    #endTurn Button
    if (pygame.mouse.get_pressed()==(True,False,False)):
        if (915<pygame.mouse.get_pos()[0]<1065) and (380<pygame.mouse.get_pos()[1]<420):
            board.buttonList3[2].buttonClick(screen)
            endT(board, screen, p1, p2, p3, p4)
            drawbg(board,screen,p1,p2,p3,p4)
            drawPieces(board, screen, p1,p2,p3,p4)            
    elif (915<pygame.mouse.get_pos()[0]<1065) and (380<pygame.mouse.get_pos()[1]<420):
        board.buttonList3[2].buttonHover(screen)
    else:
        board.buttonList3[2].image.fill(white)
        board.buttonList3[2].buttonText(screen) 

    #left Button
    if (pygame.mouse.get_pressed()==(True,False,False)):
        if (1005<pygame.mouse.get_pos()[0]<1035) and (648<pygame.mouse.get_pos()[1]<678):
            board.leftButton.buttonClick(screen)
            board.resInvPlayer=((board.resInvPlayer-1)%4)
            drawbg(board, screen, p1,p2,p3,p4)
    elif (1005<pygame.mouse.get_pos()[0]<1035) and (648<pygame.mouse.get_pos()[1]<678):
        board.leftButton.buttonHover(screen)
    else:
        board.leftButton.image.fill(white)
        board.leftButton.buttonText(screen)

    #right Button
    if (pygame.mouse.get_pressed()==(True,False,False)):
        if (1038<pygame.mouse.get_pos()[0]<1068) and (648<pygame.mouse.get_pos()[1]<678):
            board.rightButton.buttonClick(screen)
            board.resInvPlayer=((board.resInvPlayer+1)%4)
            drawbg(board, screen, p1,p2,p3,p4)
    elif (1038<pygame.mouse.get_pos()[0]<1068) and (648<pygame.mouse.get_pos()[1]<678):
        board.rightButton.buttonHover(screen)
    else:
        board.rightButton.image.fill(white)
        board.rightButton.buttonText(screen)
    
def giveResources(p1, p2, p3, p4, board, numRolled):
    if (numRolled == 7):
        pass
    for i in xrange(19):
        if (board.boardHex[i].diceNumber == numRolled):
            for j in xrange(1,7):
                if(board.boardHex[i].pointSettlement[str(j)] != False):
                    if(p1.number == board.boardHex[i].pointSettlement[str(j)]):
                        p1.resInv[board.boardHex[i].resource]+=1
                    if(p2.number == board.boardHex[i].pointSettlement[str(j)]):
                        p2.resInv[board.boardHex[i].resource]+=1
                    if(p3.number == board.boardHex[i].pointSettlement[str(j)]):
                        p3.resInv[board.boardHex[i].resource]+=1
                    if(p4.number == board.boardHex[i].pointSettlement[str(j)]):
                        p4.resInv[board.boardHex[i].resource]+=1
                if(board.boardHex[i].pointCity[str(j)] != False):
                    if(p1.number == board.boardHex[i].pointCity[str(j)]):
                        p1.resInv[board.boardHex[i].resource]+=1
                    if(p2.number == board.boardHex[i].pointCity[str(j)]):
                        p2.resInv[board.boardHex[i].resource]+=1
                    if(p3.number == board.boardHex[i].pointCity[str(j)]):
                        p3.resInv[board.boardHex[i].resource]+=1
                    if(p4.number == board.boardHex[i].pointCity[str(j)]):
                        p4.resInv[board.boardHex[i].resource]+=1
    # print numRolled
    # print p1.resInv
    # print p2.resInv
    # print p3.resInv
    # print p4.resInv

def mainLoop(screen, dice, board, turnCount, gameOver, p1, p2, p3, p4):
    #pygame.draw.line(screen,blue,(0,BCENY),(500,BCENY),1) #was using this to fix board positioning
    pygame.display.flip()

    p1.build(board, "settlement", board.getHexagon(0).getCorner(2), True)
    p1.build(board, "settlement", board.getHexagon(0).getCorner(6), True)
    p2.build(board, "settlement", board.getHexagon(10).getCorner(6), True)
    p2.build(board, "settlement", board.getHexagon(18).getCorner(4), True)
    p3.build(board, "settlement", board.getHexagon(9).getCorner(1), True)
    p3.build(board, "settlement", board.getHexagon(6).getCorner(6), True)
    p4.build(board, "settlement", board.getHexagon(1).getCorner(1), True)
    p4.build(board, "settlement", board.getHexagon(7).getCorner(2), True)
    p1.build(board, "road", ((board.getHexagon(0).getCorner(6)[0]+board.getHexagon(0).getCorner(1)[0])/2,(board.getHexagon(0).getCorner(6)[1]+board.getHexagon(0).getCorner(1)[1])/2), True)
    p1.build(board, "road", ((board.getHexagon(3).getCorner(6)[0]+board.getHexagon(3).getCorner(1)[0])/2,(board.getHexagon(3).getCorner(6)[1]+board.getHexagon(3).getCorner(1)[1])/2), True)
    p2.build(board, "road", ((board.getHexagon(5).getCorner(3)[0]+board.getHexagon(5).getCorner(4)[0])/2,(board.getHexagon(5).getCorner(4)[1]+board.getHexagon(5).getCorner(3)[1])/2), True)
    p2.build(board, "road", ((board.getHexagon(11).getCorner(6)[0]+board.getHexagon(11).getCorner(5)[0])/2,(board.getHexagon(11).getCorner(6)[1]+board.getHexagon(11).getCorner(5)[1])/2), True)
    p3.build(board, "road", ((board.getHexagon(3).getCorner(2)[0]+board.getHexagon(3).getCorner(3)[0])/2,(board.getHexagon(3).getCorner(2)[1]+board.getHexagon(3).getCorner(3)[1])/2), True)
    p3.build(board, "road", ((board.getHexagon(6).getCorner(6)[0]+board.getHexagon(6).getCorner(5)[0])/2,(board.getHexagon(6).getCorner(6)[1]+board.getHexagon(6).getCorner(5)[1])/2), True)
    p4.build(board, "road", ((board.getHexagon(1).getCorner(6)[0]+board.getHexagon(1).getCorner(1)[0])/2,(board.getHexagon(1).getCorner(6)[1]+board.getHexagon(1).getCorner(1)[1])/2), True)
    p4.build(board, "road", ((board.getHexagon(7).getCorner(3)[0]+board.getHexagon(7).getCorner(2)[0])/2,(board.getHexagon(7).getCorner(3)[1]+board.getHexagon(7).getCorner(2)[1])/2), True)

    pygame.display.flip()

    while gameOver == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver=True
        #DO NEXT MOVES
        #PREGAME SETUP
        # print (4-p1.inventory["city"])*2 + (5-p1.inventory["settlement"]) 
        # if (p1.turn):
        if(p1.turn):
            if(p1.diceRolled == False):
                numRolled = dice.roll()
                giveResources(p1,p2,p3,p4,board,numRolled)
                p1.diceRolled = True
            #STEP 1: Player rolls, everyone gets resources
            drawPieces(board,screen,p1,p2,p3,p4)
            if (board.menustate==1):
                drawButtons1(board,screen)
                menu1(board,screen,p1,p1,p2,p3,p4)
            if (board.menustate==2):
                drawButtons2(board,screen)
                menu2(board,screen,p1,p1,p2,p3,p4)
            if (board.menustate==3):
                drawButtons3(board,screen)
                menu3(board,screen,p1,p1,p2,p3,p4)                    
            pygame.display.flip()
        elif (p2.turn):
            if(p2.diceRolled == False):
                numRolled = dice.roll()
                giveResources(p1,p2,p3,p4,board,numRolled)
                p2.diceRolled = True
            #STEP 1: Player rolls, everyone gets resources
            drawPieces(board,screen,p1,p2,p3,p4)
            if (board.menustate==1):
                drawButtons1(board,screen)
                menu1(board,screen,p2,p1,p2,p3,p4)
            if (board.menustate==2):
                drawButtons2(board,screen)
                menu2(board,screen,p2,p1,p2,p3,p4)
            if (board.menustate==3):
                drawButtons3(board,screen)
                menu3(board,screen,p2,p1,p2,p3,p4)                    
            pygame.display.flip()
        elif (p3.turn):
            if(p3.diceRolled == False):
                numRolled = dice.roll()
                giveResources(p1,p2,p3,p4,board,numRolled)
                p3.diceRolled = True
            #STEP 1: Player rolls, everyone gets resources
            drawPieces(board,screen,p1,p2,p3,p4)
            if (board.menustate==1):
                drawButtons1(board,screen)
                menu1(board,screen,p3,p1,p2,p3,p4)
            if (board.menustate==2):
                drawButtons2(board,screen)
                menu2(board,screen,p3,p1,p2,p3,p4)
            if (board.menustate==3):
                drawButtons3(board,screen)
                menu3(board,screen,p3,p1,p2,p3,p4)                    
            pygame.display.flip()
        elif (p4.turn):
            if(p4.diceRolled == False):
                numRolled = dice.roll()
                giveResources(p1,p2,p3,p4,board,numRolled)
                p4.diceRolled = True
            #STEP 1: Player rolls, everyone gets resources
            drawPieces(board,screen,p1,p2,p3,p4)
            if (board.menustate==1):
                drawButtons1(board,screen)
                menu1(board,screen,p4,p1,p2,p3,p4)
            if (board.menustate==2):
                drawButtons2(board,screen)
                menu2(board,screen,p4,p1,p2,p3,p4)
            if (board.menustate==3):
                drawButtons3(board,screen)
                menu3(board,screen,p4,p1,p2,p3,p4)                    
            pygame.display.flip()

            #Resources

        pass
    pygame.quit()

def displayTradePrompt(board, screen):
    font=pygame.font.Font(None,30)
    text=font.render("Please use the shell to request trade.",True, black, white)
    textRect=text.get_rect()
    textRect.centerx=(900)
    textRect.centery=(250)
    screen.blit(text,textRect)
    
    
class Board:
    def __init__ (self):        
        self.hex = pygame.sprite.RenderPlain()
        self.boardHex = []
        self.menustate=1
        self.resInvPlayer=0
        # self.currentstring=""
        #Construct one hexagon in the center
        h = Hexagon(yellow,11,RADIUS,BCENX,BCENY)
        self.hex.add(h)
        self.boardHex.append(h)
        self.robberLoc = 16
        #Construct other hexagons
        
        for i in xrange(6):#INNER 6 HEXAGONS, START WITH 0 DEGREE ANGLE + ROTATE
            if(i == 0 or i == 3):
                col = freen
                dice = 3
                if(i == 0):
                    dice = 4
            if(i == 4 or i == 5):
                col = green
                dice = 10
                if(i == 5):
                    dice = 9
            if(i == 1):
                col = brown
                dice = 5
            if(i == 2):
                col = grey
                dice = 6
            h = Hexagon(col, dice, RADIUS, BCENX +  2*math.cos(i*math.pi/3) * RADIUS * math.sin(math.pi/3), BCENY - 2*math.sin(i*math.pi/3) * RADIUS * math.sin(math.pi/3))
            self.hex.add(h)
            self.boardHex.append(h)
        for i in xrange(6):#GROUP 2 HEXAGONS: DISTANCE IS SLIGHTLY FARTHER, START WITH 30 DEGREE ANGLE + ROTATE
            if(i == 0 or i == 1):
                col = green
                dice = 10
                if(i == 1):
                    dice = 12                
            if(i == 2 or i == 3):
                col = brown
                dice = 4
                if(i == 3):
                    dice = 8
            if(i == 4):
                col = yellow
                dice = 2
            if(i == 5):
                col = grey
                dice = 3
            h = Hexagon(col, dice, RADIUS, BCENX + 2*math.cos(i*math.pi/3 + math.pi/6)*3 * RADIUS / 2, BCENY - 2*math.sin(i*math.pi/3 + math.pi/6)*3 * RADIUS / 2)
            self.hex.add(h)
            self.boardHex.append(h)
        for i in xrange(6):#GROUP 3 HEX: DISTANCE FARTHEST, START WITH 0 DEGREE ANGLE + ROTATE
            if(i == 0 or i == 1):
                col = yellow
                dice = 8
                if(i == 1):
                    dice = 9
            if(i == 2 or i == 5):
                col = freen
                dice = 11
                if(i == 5):
                    dice = 6
            if(i == 3):
                col = beige
                dice = 0
            if(i == 4):
                col = grey
                dice = 5
            h = Hexagon(col, dice, RADIUS, BCENX +  2*math.cos(i*math.pi/3) * 2 * RADIUS * math.sin(math.pi/3), BCENY - 2*math.sin(i*math.pi/3) * 2 * RADIUS * math.sin(math.pi/3))
            self.hex.add(h)
            self.boardHex.append(h)

        #initializes robber to desert hexagon
        self.robber=pygame.sprite.RenderPlain()
        r=Piece(self,"robber",16,0,0)
        self.robber.add(r)

        #adds buttons
        self.buttons=pygame.sprite.RenderPlain()
        self.buttonList=[]
        self.buttons2=pygame.sprite.RenderPlain()
        self.buttonList2=[]
        self.buttons3=pygame.sprite.RenderPlain()
        self.buttonList3=[]

        buildButton=Button(800,150,"Build")
        self.buttons.add(buildButton)
        self.buttonList.append(buildButton)

        tradeButton=Button(990,150,"Trade")
        self.buttons.add(tradeButton)
        self.buttonList.append(tradeButton)

        backButton=Button(800,400,"Back")
        self.buttons2.add(backButton)
        self.buttonList2.append(backButton)
        self.buttons3.add(backButton)
        self.buttonList3.append(backButton)

        roadButton=Button(990,150, "Road")
        self.buttons2.add(roadButton)
        self.buttonList2.append(roadButton)

        settleButton=Button(990,200, "Settlement")
        self.buttons2.add(settleButton)
        self.buttonList2.append(settleButton)

        cityButton=Button(990,250,"City")
        self.buttons2.add(cityButton)
        self.buttonList2.append(cityButton)

        endButton=Button(990,400,"End Turn")
        self.buttons.add(endButton)
        self.buttons2.add(endButton)
        self.buttons3.add(endButton)
        self.buttonList.append(endButton)
        self.buttonList2.append(endButton)
        self.buttonList3.append(endButton)

        self.leftButton=Button(1020,663,"<")
        self.leftButton.makeArrow()
        self.rightButton=Button(1053,663,">")
        self.rightButton.makeArrow()
        self.buttons.add(self.leftButton)
        self.buttons2.add(self.leftButton)
        self.buttons3.add(self.leftButton)
        self.buttonList.append(self.leftButton)
        self.buttonList2.append(self.leftButton)
        self.buttonList3.append(self.leftButton)
        self.buttons.add(self.rightButton)
        self.buttons2.add(self.rightButton)
        self.buttons3.add(self.rightButton)
        self.buttonList.append(self.rightButton)
        self.buttonList2.append(self.rightButton)
        self.buttonList3.append(self.rightButton)

        #adds resource inventory squares
        self.resDisplay=pygame.sprite.RenderPlain()
        r1=invResource(750,500,green)
        r2=invResource(750,540,grey)
        r3=invResource(750,580,yellow)
        r4=invResource(750,620,freen)
        r5=invResource(750,660,brown)
        r6=buildResource(900,500,"road")
        r7=buildResource(900,540,"settlement")
        r8=buildResource(900,585,"city")
        self.resDisplay.add(r1)
        self.resDisplay.add(r2)
        self.resDisplay.add(r3)
        self.resDisplay.add(r4)
        self.resDisplay.add(r5)
        self.resDisplay.add(r6)
        self.resDisplay.add(r7)
        self.resDisplay.add(r8)

    def getHexagon(self, x):
        #Given a hexagon #, return the hexagon at that location
        return self.boardHex[x]
    
    def moveRobber(self):
        """
        move robber to a different hexagon
        """
        for sprite in self.robber:
            self.robber.remove(sprite)
        x = random.random() * 19
        self.robberLoc = x
        r=Piece(self,"robber", x,0,0)
        self.robber.add(r)

class Hexagon(pygame.sprite.Sprite):
    def __init__(self,color,diceNumber,r,x,y):
        theta = math.pi/6
        pygame.sprite.Sprite.__init__(self)
        self.r=r
        self.color=color
        
        #COLORS -> RESOURCES
        if(color == green):
            self.resource = "sheep"
        if(color == grey):
            self.resource = "stone"
        if(color == freen):
            self.resource = "wood"
        if(color == brown):
            self.resource = "brick"
        if(color == yellow):
            self.resource = "wheat"
        if(color == beige):
            self.resource = "desert"

        self.diceNumber=diceNumber
        self.x=x
        self.y=y
        self.points={'1':(x+r*math.cos(0+theta),y-r*math.sin(0+theta)),'2':(x+r*math.cos(2*math.pi/6+theta),y-r*math.sin(2*math.pi/6+theta)),'3':(x+r*math.cos(2*math.pi/3+theta),y-r*math.sin(2*math.pi/3+theta)),'4':(x+r*math.cos(2*math.pi/2+theta),y-r*math.sin(2*math.pi/2+theta)),'5':(x+r*math.cos(4*math.pi/3+theta),y-r*math.sin(4*math.pi/3+theta)),'6':(x+r*math.cos(5*math.pi/3+theta),y-r*math.sin(5*math.pi/3+theta))}
        self.pointSettlement = {'1': False, '2': False, '3': False, '4': False, '5': False, '6': False}
        self.pointCity = {'1': False, '2': False, '3': False, '4': False, '5': False, '6': False}
        self.pointRoad = {'1': False, '2': False, '3': False, '4': False, '5': False, '6': False}
        self.image=pygame.Surface([1000,1000], pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect=self.image.get_rect()
        pygame.draw.polygon(self.image, color, [self.points['1'],self.points['2'],self.points['3'],self.points['4'],self.points['5'],self.points['6']],0)
        pygame.draw.polygon(self.image, black, [self.points['1'],self.points['2'],self.points['3'],self.points['4'],self.points['5'],self.points['6']],5)
        pygame.draw.circle(self.image,white,(int(round(x)),int(round(y))),20,0)
        pygame.draw.circle(self.image,black,(int(round(x)),int(round(y))),20,1)

    def getCorner(self, number):
        #returns the corner of the hexagon
        return self.points[str(number)]

    def getEdgeMidpoint(self, number):
        self.getCorner(number)
    
    def getSettlementAtCorner(self, number):
        return self.pointSettlement[str(number)]

    def getRoadAtEdge(self, number):
        return self.pointRoad[str(number)]

    def getCityAtCorner(self, number):
        return self.pointCity[str(number)]

    def drawNumber(self,screen,board):
        font=pygame.font.Font(None,30)
        text=font.render(str(self.diceNumber), True, black, white)
        textRect=text.get_rect()
        textRect.centerx=round(self.x)
        textRect.centery=round(self.y)
        screen.blit(text,textRect)

class Player:
    def __init__(self, board, number):
        self.settSelection = False
        self.roadSelection = False
        self.citySelection = False
        self.resInv = {}
        self.built = {"settlement": [], "city": [], "road": []}
        self.inventory = {"settlement": 3, "city": 4 , "road": 13}
        self.number = number
        #arrays of resources and pieces played
        self.buildings = pygame.sprite.RenderPlain()
        self.roads=pygame.sprite.RenderPlain()
        self.diceRolled = False
        if(self.number == 1):
            self.turn = True
        else:
            self.turn = False

        #i changed these values to test the piece drawing
        # for i in xrange(5):
        #     p = Piece(board, "city", self.number, (i%6)+1, self.number)
        #     # self.buildings.add(p)
        # for i in xrange(15):
        #     p = Piece(board, "road", self.number, (i%6)+1, self.number)
        #     print self.number
            # self.roads.add(p)
#        for i in xrange(4)
#            p = Piece("city", -1, 0
    
    def build(self, board, piece, location, start):
        if(start == True): #if its the start of the game, build w/e
            (i,j) = self.getPositionFromLocation(board, piece, location)
            self.built[piece].append(location)
            # print "Adding Settlement"
            if(piece == "road"):
                p = Piece(board, "road", i, j, self.number)
                self.roads.add(p)
                board.getHexagon(i).pointRoad[str(j)]= self.number                
            if(piece == "settlement"):
                p = Piece(board, piece, i, j, self.number)
                self.buildings.add(p)
                board.getHexagon(i).pointSettlement[str(j)]= self.number                
            if(piece == "city"):
                p = Piece(board, piece, i, j, self.number)
                self.buildings.add(p)
                board.getHexagon(i).pointCity[str(j)]= self.number                
        elif(self.canBuildAtLocation(board, piece, location)):    
                (i,j) = self.getPositionFromLocation(board, piece, location)
                if(i!=-1 and j!=-1):
                    if(piece == "road"):
                        self.resInv["wood"]-=1
                        self.resInv["brick"]-=1
                        self.inventory["road"]-=1
                        self.built[piece].append(location)
                        p = Piece(board, piece, i,j, self.number)
                        self.roads.add(p)
                        board.getHexagon(i).pointRoad[str(j)]= self.number
                        # for i in xrange(19):
                        #     for j in xrange(1,7):
                        #         print (i,j)
                        #         print board.getHexagon(i).pointRoad[str(j)]

                    if(piece == "settlement"):
                        self.resInv["wood"]-=1
                        self.resInv["brick"]-=1
                        self.resInv["wheat"]-= 1
                        self.resInv["sheep"]-= 1
                        self.inventory["settlement"]-=1
                        self.built[piece].append(location)
                        p = Piece(board, piece, i,j, self.number)
                        self.buildings.add(p)
                        board.getHexagon(i).pointSettlement[str(j)]= self.number
                        # for i in xrange(19):
                        #     for j in xrange(1,7):
                        #         print (i,j)
                        #         print board.getHexagon(i).pointSettlement[str(j)]

                        # print "Adding Settlement"
                    if(piece == "city"):
                        self.resInv["wheat"]-= 2
                        self.resInv["stone"]-= 3
                        self.inventory["settlement"]+=1
                        self.inventory["city"]-=1
                        self.built[piece].append(location)
                        p = Piece(board, piece, i,j, self.number)
                        self.buildings.add(p)
                        board.getHexagon(i).pointCity[str(j)]=self.number
                        #remove settlement

    def getPositionFromLocation(self, board, piece, location):
        k = -1
        m = -1             
        for i in xrange(19):
            for j in xrange(1,7):
                dist_x = math.fabs(board.getHexagon(i).getCorner(j)[0] - location[0])
                dist_y = math.fabs(board.getHexagon(i).getCorner(j)[1] - location[1])
                dist_x2 = math.fabs(board.getHexagon(i).getCorner(j%6+1)[0] - location[0])
                dist_y2 = math.fabs(board.getHexagon(i).getCorner(j%6+1)[1] - location[1])
                #CHANGE IT SO THAT THE ROADS WILL ALSO CHECK FOR COLOR
                if(piece == "settlement" and (dist_x**2 + dist_y**2) < ERROR**2):
                    k = j 
                    m = i
                    board.getHexagon(i).pointSettlement[str(j)]=self.number
                #GO HERE FOR PIECE DRAWING
                if(piece == "city" and (dist_x**2 + dist_y**2) < ERROR**2):
                    k = j
                    m = i
                    board.getHexagon(i).pointCity[str(j)]= self.number                    
                    #CONSIDER THE CASE OF REMOVING THE SETTLEMENT AND ADDING THE CITY, BUT THEN CHANGING canBuildAtLocation to check for cities one spot away too
                # if(piece == "road" and math.fabs(board.getHexagon(i).getCorner(j)[0] - location[0]) > ERROR and math.fabs(board.getHexagon(i).getCorner(j)[1] - location[1]) > ERROR and math.fabs(board.getHexagon(i).getCorner(j)[0] - location[0]) < (RADIUS / 2 + ERROR) and math.fabs(board.getHexagon(i).getCorner(j)[1] - location[1]) < (RADIUS / 2 + ERROR)):
                if(piece == "road" and (dist_x**2 + dist_y**2) > (ERROR/2)**2 and ((dist_x**2 + dist_y**2) < (((RADIUS**2) / 4) + ERROR)) and (dist_x2**2 + dist_y2**2) < ((RADIUS+ERROR)**2+ERROR)):
                    k = j
                    m = i
                    board.getHexagon(i).pointRoad[str(j)]= self.number
                    # print "xyz"
                    # print (location[0], location[1])
                    # print "yzx"
                    # print (board.getHexagon(1).getCorner(2)[0], board.getHexagon(1).getCorner(2)[1])
                    # print "zxy"
                    # print (board.getHexagon(2).getCorner(5)[0], board.getHexagon(2).getCorner(5)[1])

        return (m,k)

    def displayResources(self, board, screen):
        font=pygame.font.Font(None,30)
        font2=pygame.font.Font(None,20)
        text=font.render("..........."+str(self.resInv["sheep"]),True, white)
        textRect=text.get_rect()
        textRect.centerx=(800)
        textRect.centery=(500)
        screen.blit(text,textRect)

        text2=font.render("..........."+str(self.resInv["stone"]),True, white)
        textRect2=text2.get_rect()
        textRect2.centerx=(800)
        textRect2.centery=(540)
        screen.blit(text2,textRect2)

        text3=font.render("..........."+str(self.resInv["wheat"]),True, white)
        textRect3=text3.get_rect()
        textRect3.centerx=(800)
        textRect3.centery=(580)
        screen.blit(text3,textRect3)

        text4=font.render("..........."+str(self.resInv["wood"]),True, white)
        textRect4=text4.get_rect()
        textRect4.centerx=(800)
        textRect4.centery=(620)
        screen.blit(text4,textRect4)

        text5=font.render("..........."+str(self.resInv["brick"]),True, white)
        textRect5=text5.get_rect()
        textRect5.centerx=(800)
        textRect5.centery=(660)
        screen.blit(text5,textRect5)

        text6=font.render("Player "+str(self.number),True,white)
        textRect6=text6.get_rect()
        textRect6.centerx=(750)
        textRect6.centery=(450)
        screen.blit(text6,textRect6)

        text7=font.render("..........."+str(self.inventory["road"]),True, white)
        textRect7=text7.get_rect()
        textRect7.centerx=(960)
        textRect7.centery=(500)
        screen.blit(text7,textRect7)

        text8=font.render("..........."+str(self.inventory["settlement"]),True, white)
        textRect8=text8.get_rect()
        textRect8.centerx=(960)
        textRect8.centery=(540)
        screen.blit(text8,textRect8)

        text9=font.render("..........."+str(self.inventory["city"]),True, white)
        textRect9=text9.get_rect()
        textRect9.centerx=(960)
        textRect9.centery=(585)
        screen.blit(text9,textRect9)

    # def getHexagonFromLocation(self, board, piece, location):              
    #     m = -1
    #     for i in xrange(19):
    #         for j in xrange(1,7):
    #             dist_x = math.fabs(board.getHexagon(i).getCorner(j)[0] - location[0])
    #             dist_y = math.fabs(board.getHexagon(i).getCorner(j)[1] - location[1])
    #             dist_x2 = math.fabs(board.getHexagon(i).getCorner(j%6+1)[0] - location[0])
    #             dist_y2 = math.fabs(board.getHexagon(i).getCorner(j%6+1)[1] - location[1])
    #             #CHANGE IT SO THAT THE ROADS WILL ALSO CHECK FOR COLOR
    #             if(piece == "settlement" and (dist_x**2 + dist_y**2) < ERROR**2):
    #                 # board.getHexagon(i).pointSettlement[str(j)]= self.number
    #                 m = i 

    #                 #GO HERE FOR PIECE DRAWING
    #             if(piece == "city" and (dist_x**2 + dist_y**2) < ERROR**2):
    #                 # board.getHexagon(i).pointCity[str(j)]= self.number
    #                 m = i
    #                 #CONSIDER THE CASE OF REMOVING THE SETTLEMENT AND ADDING THE CITY, BUT THEN CHANGING canBuildAtLocation to check for cities one spot away too
    #             if(piece == "road" and (dist_x**2 + dist_y**2) > ERROR**2 and ((dist_x**2 + dist_y**2) < (((RADIUS**2) / 4) + ERROR)) and (dist_x2**2 + dist_y2**2) < ((RADIUS)**2)):
    #                 # board.getHexagon(i).pointRoad[str(j)]= self.number
    #                 m = i
    #     return m

    def canBuildAtLocation(self, board, piece, location):
        #CHANGE TO DISPLAY / CHANGE LATER TO NOT EVEN ABLE TO CLICK BUTTONS IF THIS IS FALSE ?!
        
        #if can build at location, do the following:
        #location will be retrieved from a mouse click

        canBuild = True #assume True...unless road (see below)
        if(piece == "road"):
            canBuild = False

        #HEXAGON POSITION CHECKING CODE
        #CHANGE ORDER IF SPEED IS TOO SLOW
        for i in xrange(19):
            for j in xrange(1,7):
                #SETTLEMENT CASES
                dist_x = math.fabs(board.getHexagon(i).getCorner(j)[0] - location[0])
                dist_y = math.fabs(board.getHexagon(i).getCorner(j)[1] - location[1])
                dist_x2 = math.fabs(board.getHexagon(i).getCorner(j%6+1)[0] - location[0])
                dist_y2 = math.fabs(board.getHexagon(i).getCorner(j%6+1)[1] - location[1])
                # if((piece == "settlement" or piece == "city") and (dist_x**2 + dist_y**2) >= ERROR**2):
                #     canBuild = False
                # if(piece == "settlement" and (dist_x**2 + dist_y**2) < ERROR**2):
                #     if(board.getHexagon(i).getSettlementAtCorner((j + 7) % 6) == False and board.getHexagon(i).getSettlementAtCorner((j + 5) % 6) == False):
                #         return True
                k = (j+5) % 6
                if(k == 0):
                    k = 6
                if(piece == "settlement" and (dist_x**2 + dist_y**2) < ERROR**2):
                    if(board.getHexagon(i).getSettlementAtCorner((j % 6)+1) != False or board.getHexagon(i).getSettlementAtCorner(k) != False or board.getHexagon(i).getSettlementAtCorner(j) != False):
                        canBuild = False #if another piece is on an adjacent square already, no settlement
                        print "!"
                if(piece == "city" and (dist_x**2 + dist_y**2) < ERROR**2):
                    if(board.getHexagon(i).getSettlementAtCorner(j) == False):
                        canBuild = False #if there's no settlement there, no city upgrade    
                    if(board.getHexagon(i).getCityAtCorner(j) != False):
                        canBuild = False                    
                if(piece == "road" and (dist_x**2 + dist_y**2) > ERROR**2 and ((dist_x**2 + dist_y**2) < (((RADIUS**2) / 4) + ERROR)) and (dist_x2**2 + dist_y2**2) < ((RADIUS)**2)):
                    # canBuild = False #ASSUME FALSE
                    # canBuild = True
                    if(board.getHexagon(i).getRoadAtEdge(j) != False):
                        canBuild = False #False if there is an existing road at the location, prioritizes over last condition
                        # print "What what"
                    elif(board.getHexagon(i).getRoadAtEdge(j%6+1) == self.number or board.getHexagon(i).getRoadAtEdge(k) == self.number):
                        canBuild = True #IF THERE IS A ROAD NEXT TO YOUR ROAD ON THIS HEX, CHANGE TO TRUE
                        # print "??"


        if(canBuild == False):
            return False #If you already know you can't build it, then just end the method

        #canBuild is assumed to be True if you are still up to here
        if(piece == "road"):
            if(self.inventory["road"] == 0): #no more roads in your inventory
                print "NOT ENOUGH ROADS"
                canBuild = False
            elif(self.resInv["wood"] < 1 or self.resInv["brick"] < 1):
                print "NOT ENOUGH RESOURCES"
                canBuild = False
        if(piece == "settlement"):
            if(self.inventory["settlement"] == 0): #no more setts in your inventory
                print "NOT ENOUGH SETTLEMENTS"
                canBuild = False
            elif(self.resInv["wood"] < 1 or self.resInv["brick"] < 1 or self.resInv["wheat"] < 1 or self.resInv["sheep"] < 1):
                print "NOT ENOUGH RESOURCES"
                canBuild = False
        if(piece == "city"):
            if(self.inventory["city"] == 0): #no more cities in your inventory
                print "NOT ENOUGH CITIES"
                canBuild = False
            elif(self.inventory["settlement"] == 5): #no more setts on map
                print "NO SETTLEMENTS PLAYED"
                canBuild = False
            elif(self.resInv["wheat"] < 2 or self.resInv["stone"] < 3):
                print "NOT ENOUGH RESOURCES"
                canBuild = False
        return canBuild
#
                    #if hexagon tuple x and y are both within a certain error distance, set to the player color and piece
                        #pointSettlement's dictionary will now have a player-piece tuple for that element instead
            
    def requestTrade(self, myTrade, other, otherTrade):
        if(self.resInv["wheat"] < myTrade["wheat"] or self.resInv["brick"] < myTrade["brick"] or self.resInv["wood"] < myTrade["wood"] or self.resInv["sheep"] < myTrade["sheep"] or self.resInv["stone"] < myTrade["stone"]):
            return False
        if(other.resInv["wheat"] < otherTrade["wheat"] or other.resInv["brick"] < otherTrade["brick"] or other.resInv["wood"] < otherTrade["wood"] or other.resInv["sheep"] < otherTrade["sheep"] or other.resInv["stone"] < otherTrade["stone"]):
            return False
        self.resInv["wheat"] += (otherTrade["wheat"] - myTrade["wheat"])
        self.resInv["brick"] += (otherTrade["brick"] - myTrade["brick"])
        self.resInv["stone"] += (otherTrade["stone"] - myTrade["stone"])
        self.resInv["wood"] += (otherTrade["wood"] - myTrade["wood"])
        self.resInv["sheep"] += (otherTrade["sheep"] - myTrade["sheep"])
        other.resInv["wheat"] += (myTrade["wheat"] - otherTrade["wheat"])
        other.resInv["brick"] += (myTrade["brick"] - otherTrade["brick"])
        other.resInv["stone"] += (myTrade["stone"] - otherTrade["stone"])
        other.resInv["wood"] += (myTrade["wood"] - otherTrade["wood"])
        other.resInv["sheep"] += (myTrade["sheep"] - otherTrade["sheep"])
        return True  
    
class Dice:
    def roll(self):
        """
        textSize = 20
        font = pygame.font.Font(None, 20)
        textY = 0 + textSize
        """
        number = (int(random.random()*6) + int(random.random()*6) + 2)
        """
        text = font.render("Dice Roll: " + str(number), True, white, black)
        textRect = text.get_rect()
        textRect.centerx = 11 * 100
        textRect.centerY = textY
        screen.blit(text, textRect)
        """
        return number;

class Piece(pygame.sprite.Sprite):
    def __init__(self,board,typePiece,hexagon,position,player):
        pygame.sprite.Sprite.__init__(self)
        self.player=player
        self.typePiece=typePiece
        self.hexagon=hexagon
        self.position=position
        if typePiece=="robber": #draws image for robber
            self.image=pygame.Surface([1000,1000], pygame.SRCALPHA, 32)
            self.image = self.image.convert_alpha()
            self.rect=self.image.get_rect()
            pygame.draw.circle(self.image,black,(int(round(board.boardHex[hexagon].x)),int(round(board.boardHex[hexagon].y))),35,15)
        elif self.player==1: #sets proper image for red pieces
            if typePiece=="settlement":
                self.image = pygame.image.load("houseR.png").convert_alpha()
                if(position!=0):
                    self.rect=self.image.get_rect(center=(board.boardHex[hexagon].points[str(position)]))
            elif self.typePiece=="city":
                self.image = pygame.image.load("cityR.png").convert_alpha()
                if(position!=0):
                    self.rect=self.image.get_rect(center=(board.boardHex[hexagon].points[str(position)][0],board.boardHex[hexagon].points[str(position)][1]-5))
            elif self.typePiece=="road":
                if position==2 or position==5:
                    self.image=pygame.image.load("road1r.png").convert_alpha()
                    self.rect=self.image.get_rect(center=((board.boardHex[hexagon].points[str(position)][0]+board.boardHex[hexagon].points[str(position+1)][0])/2,(board.boardHex[hexagon].points[str(position)][1]+board.boardHex[hexagon].points[str(position+1)][1])/2))
                elif position==1 or position ==4:
                    self.image=pygame.image.load("road2r.png").convert_alpha()
                    self.rect=self.image.get_rect(center=((board.boardHex[hexagon].points[str(position)][0]+board.boardHex[hexagon].points[str(position+1)][0])/2,(board.boardHex[hexagon].points[str(position)][1]+board.boardHex[hexagon].points[str(position+1)][1])/2))
                elif position==3 or position ==6:
                    self.image=pygame.image.load("road3r.png").convert_alpha()
                    self.rect=self.image.get_rect(center=((board.boardHex[hexagon].points[str(position)][0]+board.boardHex[hexagon].points[str((position+1)%6)][0])/2,(board.boardHex[hexagon].points[str(position)][1]+board.boardHex[hexagon].points[str((position+1)%6)][1])/2))
            if position == 0:
                self.image=pygame.image.load("road1r.png").convert_alpha()
                self.rect=self.image.get_rect(center = (player*100,player*100))

        elif self.player==2: #sets proper image for blue pieces
            if typePiece=="settlement":
                self.image = pygame.image.load("houseB.png").convert_alpha()
                if(position!=0):
                    self.rect=self.image.get_rect(center=(board.boardHex[hexagon].points[str(position)]))
            elif self.typePiece=="city":
                self.image = pygame.image.load("cityB.png").convert_alpha()
                if(position!=0):
                    self.rect=self.image.get_rect(center=(board.boardHex[hexagon].points[str(position)][0],board.boardHex[hexagon].points[str(position)][1]-5))
            elif self.typePiece=="road":
                if position==2 or position==5:
                    self.image=pygame.image.load("road1b.png").convert_alpha()
                    self.rect=self.image.get_rect(center=((board.boardHex[hexagon].points[str(position)][0]+board.boardHex[hexagon].points[str(position+1)][0])/2,(board.boardHex[hexagon].points[str(position)][1]+board.boardHex[hexagon].points[str(position+1)][1])/2))
                elif position==1 or position ==4:
                    self.image=pygame.image.load("road2b.png").convert_alpha()
                    self.rect=self.image.get_rect(center=((board.boardHex[hexagon].points[str(position)][0]+board.boardHex[hexagon].points[str(position+1)][0])/2,(board.boardHex[hexagon].points[str(position)][1]+board.boardHex[hexagon].points[str(position+1)][1])/2))
                elif position==3 or position ==6:
                    self.image=pygame.image.load("road3b.png").convert_alpha()
                    self.rect=self.image.get_rect(center=((board.boardHex[hexagon].points[str(position)][0]+board.boardHex[hexagon].points[str((position+1)%6)][0])/2,(board.boardHex[hexagon].points[str(position)][1]+board.boardHex[hexagon].points[str((position+1)%6)][1])/2))
            if position == 0:
                self.image=pygame.image.load("road1b.png").convert_alpha()
                self.rect=self.image.get_rect(center = (player*100,player*100))
                    
        elif self.player==3: #sets proper image for white pieces
            if typePiece=="settlement":
                self.image = pygame.image.load("houseW.png").convert_alpha()
                if(position!=0):
                    self.rect=self.image.get_rect(center=(board.boardHex[hexagon].points[str(position)]))
            elif self.typePiece=="city":
                self.image = pygame.image.load("cityW.png").convert_alpha()
                if(position!=0):
                    self.rect=self.image.get_rect(center=(board.boardHex[hexagon].points[str(position)][0],board.boardHex[hexagon].points[str(position)][1]-5))
            elif self.typePiece=="road":
                if position==2 or position==5:
                    self.image=pygame.image.load("road1w.png").convert_alpha()
                    self.rect=self.image.get_rect(center=((board.boardHex[hexagon].points[str(position)][0]+board.boardHex[hexagon].points[str(position+1)][0])/2,(board.boardHex[hexagon].points[str(position)][1]+board.boardHex[hexagon].points[str(position+1)][1])/2))
                elif position==1 or position ==4:
                    self.image=pygame.image.load("road2w.png").convert_alpha()
                    self.rect=self.image.get_rect(center=((board.boardHex[hexagon].points[str(position)][0]+board.boardHex[hexagon].points[str(position+1)][0])/2,(board.boardHex[hexagon].points[str(position)][1]+board.boardHex[hexagon].points[str(position+1)][1])/2))
                elif position==3 or position ==6:
                    self.image=pygame.image.load("road3w.png").convert_alpha()
                    self.rect=self.image.get_rect(center=((board.boardHex[hexagon].points[str(position)][0]+board.boardHex[hexagon].points[str((position+1)%6)][0])/2,(board.boardHex[hexagon].points[str(position)][1]+board.boardHex[hexagon].points[str((position+1)%6)][1])/2))
            if position == 0:
                self.image=pygame.image.load("road1w.png").convert_alpha()
                self.rect=self.image.get_rect(center = (player*100,player*100))

        elif self.player==4: #sets proper image for orange pieces
            if typePiece=="settlement":
                self.image = pygame.image.load("houseO.png").convert_alpha()
                if(position!=0):
                    self.rect=self.image.get_rect(center=(board.boardHex[hexagon].points[str(position)]))
            elif self.typePiece=="city":
                self.image = pygame.image.load("cityO.png").convert_alpha()
                if(position!=0):
                    self.rect=self.image.get_rect(center=(board.boardHex[hexagon].points[str(position)][0],board.boardHex[hexagon].points[str(position)][1]-5))
            elif self.typePiece=="road":
                if position==2 or position==5:
                    self.image=pygame.image.load("road1o.png").convert_alpha()
                    self.rect=self.image.get_rect(center=((board.boardHex[hexagon].points[str(position)][0]+board.boardHex[hexagon].points[str(position+1)][0])/2,(board.boardHex[hexagon].points[str(position)][1]+board.boardHex[hexagon].points[str(position+1)][1])/2))
                elif position==1 or position ==4:
                    self.image=pygame.image.load("road2o.png").convert_alpha()
                    self.rect=self.image.get_rect(center=((board.boardHex[hexagon].points[str(position)][0]+board.boardHex[hexagon].points[str(position+1)][0])/2,(board.boardHex[hexagon].points[str(position)][1]+board.boardHex[hexagon].points[str(position+1)][1])/2))
                elif position==3 or position ==6:
                    self.image=pygame.image.load("road3o.png").convert_alpha()
                    self.rect=self.image.get_rect(center=((board.boardHex[hexagon].points[str(position)][0]+board.boardHex[hexagon].points[str((position+1)%6)][0])/2,(board.boardHex[hexagon].points[str(position)][1]+board.boardHex[hexagon].points[str((position+1)%6)][1])/2))
            if position == 0:
                self.image=pygame.image.load("road1o.png").convert_alpha()
                self.rect=self.image.get_rect(center = (player*100,player*100))

    def isPieceOfPlayer(self,player):
        """
        Returns true if piece belongs to player, false otherwise
        """
        if self.player==player:
            return True
        else:
            return False

    def isRobber(self):
        """
        Returns true if piece is robber, false otherwise
        """
        if self.typePiece=="robber":
            return True
        else:
            return False

class Button(pygame.sprite.Sprite):
    def __init__(self,x,y,text):
        pygame.sprite.Sprite.__init__(self)
        self.x=x
        self.y=y
        self.text=text
        self.image=pygame.Surface([150,40])
        self.image.fill(white)
        self.rect=self.image.get_rect(center=(x,y))

    def makeArrow(self):
        self.image=pygame.Surface([30,30])
        self.image.fill(white)
        self.rect=self.image.get_rect(center=(self.x,self.y))

    def buttonText(self, screen):
        font=pygame.font.Font(None,30)
        text=font.render(self.text,True, black)
        textRect=text.get_rect()
        textRect.centerx=(self.x)
        textRect.centery=(self.y)
        screen.blit(text,textRect)

    def buttonHover(self,screen):
        self.image.fill((255, 182, 193))
        self.buttonText(screen)

    def buttonClick(self,screen):
        self.image.fill((255,20,147))
        self.buttonText(screen)
        pygame.draw.rect(self.image,black,self.image.get_rect(),5)

class invResource(pygame.sprite.Sprite):
    def __init__(self,x,y,color):
        pygame.sprite.Sprite.__init__(self)
        self.x=x
        self.y=y
        self.image=pygame.Surface([20,20])
        self.image.fill(color)
        self.rect=self.image.get_rect(center=(x,y))

class buildResource(pygame.sprite.Sprite):
    def __init__(self,x,y,piece):
        pygame.sprite.Sprite.__init__(self)
        self.x=x
        self.y=y
        if (piece=="road"):
            self.image = pygame.image.load("road1r.png").convert_alpha()
        if (piece=="settlement"):
            self.image = pygame.image.load("houseB.png").convert_alpha()
        if (piece=="city"):
            self.image = pygame.image.load("cityO.png").convert_alpha()
        self.rect=self.image.get_rect(center=(x,y))

newGame()
