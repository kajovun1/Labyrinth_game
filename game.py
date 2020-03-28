import time

from maze import Maze
from mouse import Mouse
import pickle

from PyQt5.QtWidgets import (QToolTip, QPushButton, QComboBox, QLabel) 
from PyQt5.QtGui import (QFont, QIcon, QPainter, QColor, QBrush, QPalette, QPixmap, QPen, QPainterPath)
from PyQt5.QtCore import (QCoreApplication, Qt, QPointF) 
from PyQt5.Qt import QMainWindow


BOTTOMWALL = 0
RIGHTWALL = 1
VISITED = 2
CROSSING = 3

CELLSIZE = 15
WALLSIZE = 4
marginX = 150
marginY = 10

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

class Game(QMainWindow):
    def __init__(self, a):
        self.ready = False
        if (a == True):
            super().__init__()   
        self.dropDownValueWidth = 14
        self.dropDownValueHeight = 14
        
        
        self.givedUp = False
        self.solutionPath = []
        self.maze = Maze(self.dropDownValueWidth,self.dropDownValueHeight)
        if (a == True):
            self.mouse = Mouse(True)
        else:
            self.mouse = Mouse(False)
        # siirretaan hiiren paikka keskelle labya
        self.mouse.setMouseCoordinates(7, 7)
        self.mouse.setMouseEarlierCoordinates(8, 7)
        if (a == True):
            self.setCentralWidget(self.mouse)
            self.initUI()
            self.startGame()
                
    # peli-ikkunan alustus
    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        btnNewGame = QPushButton('New Game', self)
        btnNewGame.resize(110,50)
        btnNewGame.move(20, 20)
        btnNewGame.clicked.connect(self.newGameclicked)
        btnGiveUp = QPushButton('Give up', self)
        btnGiveUp.resize(110,50)
        btnGiveUp.move(20, 80)
        btnGiveUp.clicked.connect(self.giveUpclicked)
        btnSave = QPushButton('Save', self)
        btnSave.resize(110,50)
        btnSave.move(20, 140)
        btnSave.clicked.connect(self.saveClicked)
        btnLoad = QPushButton('Load', self)
        btnLoad.resize(110,50)
        btnLoad.move(20, 200)
        btnLoad.clicked.connect(self.loadClicked)
        btnQuit = QPushButton('Quit', self)
        btnQuit.resize(110,50)
        btnQuit.move(20, 260)
        btnQuit.clicked.connect(QCoreApplication.instance().quit)
        widthText = QLabel('Set height:', self)
        widthText.move(15, 320)
        heightText = QLabel('Set width:', self)
        heightText.move(15, 380)
        # alasvetovalikot
        dropDownW = QComboBox(self)
        dropDownW.addItem("14")
        dropDownW.addItem("16")
        dropDownW.addItem("18")
        dropDownW.addItem("20")
        dropDownW.addItem("22")
        dropDownW.addItem("24")
        dropDownW.addItem("26")
        dropDownW.addItem("28")
        dropDownW.addItem("30")
        dropDownW.activated[str].connect(self.onActivatedW)
        dropDownW.move(20, 350) 
 
        dropDownH = QComboBox(self)
        dropDownH.addItem("14")
        dropDownH.addItem("16")
        dropDownH.addItem("18")
        dropDownH.addItem("20")
        dropDownH.addItem("22")
        dropDownH.addItem("24")
        dropDownH.addItem("26")
        dropDownH.addItem("28")
        dropDownH.addItem("30")
        dropDownH.activated[str].connect(self.onActivatedH)
        dropDownH.move(20, 410) 
        # lucky escape teksti
        self.gameOverText = u'\u004c\u0075\u0063\u006b\u0079 \u0065\u0073\u0063\u0061\u0070\u0065\u0021'
        
        # set background image
        palette = QPalette()
        palette.setBrush(QPalette.Background,QBrush(QPixmap("sew.png")))    
        self.setPalette(palette)     
        self.setGeometry(200, 100, 1000, 600)
        self.setWindowTitle('Escape from the sewerage system')
        self.setWindowIcon(QIcon('icon.jpg'))   
        self.show()
    
    # funktiot alavetovalikkoarvojen muutamiseen
    def onActivatedW(self, text):  
        self.dropDownValueWidth = int(text)
        
    def onActivatedH(self, text):  
        self.dropDownValueHeight = int(text)
     
    #------------------------------------------------------------------------
    # funktiot jotka suoritetaan kun jtn painiketta klikattu
    
    def newGameclicked(self):
        self.givedUp = False
        # asetetaan valittu labyrintin koko
        self.maze.setWidth(self.dropDownValueWidth)
        self.maze.setHeight(self.dropDownValueHeight)
        self.maze.resetMaze()
        self.solutionPath = []
        # generoidaan uusi laby
        self.maze._gen_maze(int(self.dropDownValueWidth-1),int(self.dropDownValueHeight-1))
        self.newMaze = self.maze.getMaze()
        self.newRows = self.maze.getRows()
        self.newColumns = self.maze.getColumns()
        # asetetaan hiiri lebyn keskelle
        self.mouse.setMouseCoordinates(int(self.newRows*0.5),int(self.newColumns*0.5))
        self.mouse.setMouseCoordinates(int(self.newRows*0.5),int(self.newColumns*0.5))
        self.mouse.setMouseEarlierCoordinates(int(self.newRows*0.5)+1,int(self.newColumns*0.5))
        # mikali keskikohta osuus risteykseksi, hiiri sen sillalla
        self.mouse.setMouseCrossing(False)
        self.mouse.setMouseDirection(UP)
        self.update()
    
    def giveUpclicked(self):
        self.givedUp = True
        self.maze.solveMaze(int(self.mouse.getMouseCoordinateX()), int(self.mouse.getMouseCoordinateY()), int(self.mouse.getMouseEarlierCoordinateX()), int(self.mouse.getMouseEarlierCoordinateY()), 0)
        self.solutionPath = []
        risteys = 0
        if self.newMaze[self.mouse.getMouseCoordinateX()][self.mouse.getMouseCoordinateY()][CROSSING] == True:
            print(self.newMaze[self.mouse.getMouseCoordinateX()][self.mouse.getMouseCoordinateY()][CROSSING])
            if self.mouse.getMouseCrossing() == False:
                risteys = 1
            else:
                risteys = 2
        self.solutionPath = self.maze.getSolutionPath(int(self.mouse.getMouseCoordinateX()),int(self.mouse.getMouseCoordinateY()), risteys)
        #print(self.solutionPath)
        
        self.update()
        for i in range (len(self.solutionPath)-1):
            #UP
            if self.solutionPath[i][0] > self.solutionPath[i+1][0]:
                self.mouse.setMouseDirection(UP)
                self.mouse.update()
                self.mouse.moveMouse(UP, self.newMaze, True)
                #time.sleep(1)
            #DOWN
            elif self.solutionPath[i][0] < self.solutionPath[i+1][0]:
                self.mouse.setMouseDirection(DOWN)
                self.mouse.update()
                self.mouse.moveMouse(DOWN, self.newMaze, True)
                #time.sleep(1)

            #LEFT
            elif self.solutionPath[i][1] > self.solutionPath[i+1][1]:
                self.mouse.setMouseDirection(LEFT)
                self.mouse.update()
                self.mouse.moveMouse(LEFT, self.newMaze, True)
                #time.sleep(1)

            #RIGHT
            elif self.solutionPath[i][1] < self.solutionPath[i+1][1]:
                self.mouse.setMouseDirection(RIGHT)
                self.mouse.update()
                self.mouse.moveMouse(RIGHT, self.newMaze, True)
                #time.sleep(1)

    def saveClicked(self):
        # tarvittava tieto pelista talteen gameData stringiin
        gameData = self.saveGame()
        # tallennetaan tekstitiedostoon save.p
        pickle.dump( gameData, open( "save.p", "wb" ) )
        
    def loadClicked(self):
        # ladataan tallennettu string save.p:sta
        gameData = pickle.load( open( "save.p", "rb" ) )
        
        self.loadGame(gameData)
                  
        self.update()
        
    #-------------------------------------------------------------------
    
    # aloittaa pelin    
    def startGame(self):
        # Initial maze generation
        self.maze._gen_maze(self.dropDownValueWidth-1,self.dropDownValueHeight-1)
        self.newMaze = self.maze.getMaze()
        self.newRows = self.maze.getRows()
        self.newColumns = self.maze.getColumns()
        self.ready = True
   
    # handles saving the game
    def saveGame(self):
        header = "GAMEFILE;"
        
        # store mouse data
        currentMouseX = self.mouse.getMouseCoordinateX()
        currentMouseY = self.mouse.getMouseCoordinateY()
        currentMouseDirection = self.mouse.getMouseDirection()
        currentMouseCrossing = self.mouse.getMouseCrossing()        
        tmp = "_"+str(currentMouseX) + "_"+ str(currentMouseY) +"_"+ str(currentMouseDirection) + "_" + str(currentMouseCrossing)
        mouseData = "MOU" + tmp + ";"
        
        # store maze data
        currentMaze = self.maze.getMaze()
        numberOfRows = self.maze.getRows()
        numberOfColumns = self.maze.getColumns()
        mazeData = "MAZ" + "_" + str(numberOfRows) + "_" + str(numberOfColumns)
        for j in range(numberOfRows): 
            for i in range(numberOfColumns):
                mazeData = mazeData + "_"
                if currentMaze[j][i][BOTTOMWALL] == True:
                    mazeData = mazeData + "T"
                else: 
                    mazeData = mazeData +"F"
                if currentMaze[j][i][RIGHTWALL] == True:
                    mazeData = mazeData + "T"
                else: 
                    mazeData = mazeData +"F"
                if currentMaze[j][i][CROSSING] == True:
                    mazeData = mazeData + "T"
                else: 
                    mazeData = mazeData +"F"
        mazeData = mazeData + ";"
        endRow = self.maze.getEndRow()
        endColumn = self.maze.getEndColumn()
        # store goal
        endData = "END" + "_" + str(endRow) + "_" + str(endColumn)
        
        # all data combined
        gameData = header + mouseData + mazeData + endData
        return gameData
    
    # handles loading game
    def loadGame(self, gameData):
        gameData = gameData.split(';')
        # check header
        if not gameData[0] == "GAMEFILE":
            raise ValueError("saved file corrupted")
        # check mouseData
        mouseData= gameData[1].split("_")
        if mouseData[0] == "MOU":
            currentMouseX = int(mouseData[1])
            currentMouseY = int(mouseData[2])
            currentMouseDirection = int(mouseData[3])
            currentMouseCrossing = mouseData[4]
        else:
            raise ValueError("saved file corrupted")
        # check mazeData
        mazeData = gameData[2].split("_")
        if mazeData[0] == "MAZ":
            totalCellNumber = int(mazeData[1])*int(mazeData[2])
            a = 0
            tmpMaze = [[[True, True, False, False] for j in range(int(mazeData[2]))] for i in range(int(mazeData[1]))]
            for j in range(int(mazeData[1])):
                for i in range(int(mazeData[2])):
                    if a < totalCellNumber:
                        if mazeData[3+a][0] == "T":
                            tmpMaze[j][i][BOTTOMWALL] = True
                        else:
                            tmpMaze[j][i][BOTTOMWALL] = False
                        if mazeData[3+a][1] == "T":
                            tmpMaze[j][i][RIGHTWALL] = True
                        else:
                            tmpMaze[j][i][RIGHTWALL] = False
                        if mazeData[3+a][2] == "T":
                            tmpMaze[j][i][CROSSING] = True
                        else:
                            tmpMaze[j][i][CROSSING] = False
                        tmpMaze[j][i][VISITED] = True
                        a = a + 1      
        else:
            raise ValueError("saved file corrupted")
        # check endData
        endData = gameData[3].split("_")
        if endData[0] == "END":
            endRow = int(endData[1])
            endColumn = int(endData[2])
        else:
            raise ValueError("saved file corrupted")
        # asetetaan hiiri tiedoston mukaiseen paikkaan, oikeaan suuntaan
        self.mouse.setMouseCoordinates(currentMouseX, currentMouseY)
        self.mouse.setMouseDirection(currentMouseDirection)
        # onko hiiri alikulussa
        if currentMouseCrossing == "True":
            self.mouse.setMouseCrossing(True)
            # asetetaan keinotekoinen edellinen ruutu, mikali hiiri alukulussa
            self.mouse.setMouseEarlierCoordinates(currentMouseX, currentMouseY-1)
        else:
            self.mouse.setMouseCrossing(False)
        
        # asetetaan valittu labyrintin koko
        self.maze.setWidth(int(mazeData[1]))
        self.maze.setHeight(int(mazeData[2]))
        
        self.maze.resetMaze()
        self.solutionPath = []
        
        for j in range(int(mazeData[1])):
                for i in range(int(mazeData[2])):
                    self.maze.changeMaze(j, i, tmpMaze[j][i])
        
        self.ready = True
        # tarkistetaan onko hiiri risteyksen sillalla
        if (currentMouseCrossing == "False") and (self.maze.getMaze()[currentMouseX][currentMouseY][CROSSING] == True):
            # hiiri sillalla, asetetaan keinotekoinen edellinen ruutu
            self.mouse.setMouseEarlierCoordinates(currentMouseX-1, currentMouseY)

        self.newMaze = self.maze.getMaze()
        self.newRows = self.maze.getRows()
        self.newColumns = self.maze.getColumns()  
        # asetetaan maali
        self.maze.setEndRow(endRow)
        self.maze.setEndColumn(endColumn)
    
    # piirtofunktiot --------------------------------------     
    
    def paintEvent(self, e):
        if self.ready:
            grid = QPainter()
            grid.begin(self)
            self.drawGrid(grid)
            grid.end()

        if self.givedUp == True:
            gri = QPainter()
            gri.begin(self)
            self.drawSolutionPath(gri)
            gri.end()
    
        if self.givedUp == False and self.maze.endrow == self.mouse.getMouseCoordinateX() and self.maze.endcolumn == self.mouse.getMouseCoordinateY():
            qp = QPainter()
            qp.begin(self)
            self.drawGameOverText(e, qp)
            qp.end()
    
    # lopetustekstin piirtaminen
    def drawGameOverText(self, event, qp):
        qp.setPen(QColor(32, 51, 65))
        qp.setFont(QFont('SansSerif', 50))
        qp.drawText(event.rect(), Qt.AlignCenter, self.gameOverText)
    
    # ratkaisupolun piirtaminen
    def drawSolutionPath(self, grid):
        pen = QPen(Qt.black, 3, Qt.SolidLine)
        grid.setPen(pen)
        col = QColor(0,128,255)
        col.setNamedColor('#0080FF')
        grid.setPen(col)
        grid.setBrush(QColor(0,128,255))

        for i in range (len(self.solutionPath)-1):
            #UP
            if self.solutionPath[i][0] > self.solutionPath[i+1][0]:
                grid.setBrush(QColor(0,128,255))
                grid.drawEllipse(marginX+1+ WALLSIZE+(self.solutionPath[i][1]*CELLSIZE+self.solutionPath[i][1]*WALLSIZE), marginY+6+WALLSIZE+(self.solutionPath[i][0]*CELLSIZE+self.solutionPath[i][0]*WALLSIZE), CELLSIZE-10, CELLSIZE-10)
                grid.drawEllipse(marginX+7+ WALLSIZE+(self.solutionPath[i][1]*CELLSIZE+self.solutionPath[i][1]*WALLSIZE), marginY+6+WALLSIZE+(self.solutionPath[i][0]*CELLSIZE+self.solutionPath[i][0]*WALLSIZE), CELLSIZE-10, CELLSIZE-10)
                grid.setBrush(QColor(0,91,183))
                grid.drawEllipse(marginX+4+ WALLSIZE+(self.solutionPath[i][1]*CELLSIZE+self.solutionPath[i][1]*WALLSIZE), marginY+1+WALLSIZE+(self.solutionPath[i][0]*CELLSIZE+self.solutionPath[i][0]*WALLSIZE), CELLSIZE-11, CELLSIZE-11)
            #DOWN
            elif self.solutionPath[i][0] < self.solutionPath[i+1][0]:
                grid.setBrush(QColor(0,128,255))
                grid.drawEllipse(marginX+1+ WALLSIZE+(self.solutionPath[i][1]*CELLSIZE+self.solutionPath[i][1]*WALLSIZE), marginY+3+WALLSIZE+(self.solutionPath[i][0]*CELLSIZE+self.solutionPath[i][0]*WALLSIZE), CELLSIZE-10, CELLSIZE-10)
                grid.drawEllipse(marginX+7+ WALLSIZE+(self.solutionPath[i][1]*CELLSIZE+self.solutionPath[i][1]*WALLSIZE), marginY+3+WALLSIZE+(self.solutionPath[i][0]*CELLSIZE+self.solutionPath[i][0]*WALLSIZE), CELLSIZE-10, CELLSIZE-10)
                grid.setBrush(QColor(0,91,183))
                grid.drawEllipse(marginX+4+ WALLSIZE+(self.solutionPath[i][1]*CELLSIZE+self.solutionPath[i][1]*WALLSIZE), marginY+8+WALLSIZE+(self.solutionPath[i][0]*CELLSIZE+self.solutionPath[i][0]*WALLSIZE), CELLSIZE-11, CELLSIZE-11)
            #LEFT
            elif self.solutionPath[i][1] > self.solutionPath[i+1][1]:
                grid.setBrush(QColor(0,128,255))
                grid.drawEllipse(marginX+6+ WALLSIZE+(self.solutionPath[i][1]*CELLSIZE+self.solutionPath[i][1]*WALLSIZE), marginY+1+WALLSIZE+(self.solutionPath[i][0]*CELLSIZE+self.solutionPath[i][0]*WALLSIZE), CELLSIZE-10, CELLSIZE-10)
                grid.drawEllipse(marginX+6+ WALLSIZE+(self.solutionPath[i][1]*CELLSIZE+self.solutionPath[i][1]*WALLSIZE), marginY+7+WALLSIZE+(self.solutionPath[i][0]*CELLSIZE+self.solutionPath[i][0]*WALLSIZE), CELLSIZE-10, CELLSIZE-10)
                grid.setBrush(QColor(0,91,183))
                grid.drawEllipse(marginX+1+ WALLSIZE+(self.solutionPath[i][1]*CELLSIZE+self.solutionPath[i][1]*WALLSIZE), marginY+4+WALLSIZE+(self.solutionPath[i][0]*CELLSIZE+self.solutionPath[i][0]*WALLSIZE), CELLSIZE-11, CELLSIZE-11)

            #RIGHT
            elif self.solutionPath[i][1] < self.solutionPath[i+1][1]:
                grid.setBrush(QColor(0,128,255))
                grid.drawEllipse(marginX+3+ WALLSIZE+(self.solutionPath[i][1]*CELLSIZE+self.solutionPath[i][1]*WALLSIZE), marginY+1+WALLSIZE+(self.solutionPath[i][0]*CELLSIZE+self.solutionPath[i][0]*WALLSIZE), CELLSIZE-10, CELLSIZE-10)
                grid.drawEllipse(marginX+3+ WALLSIZE+(self.solutionPath[i][1]*CELLSIZE+self.solutionPath[i][1]*WALLSIZE), marginY+7+WALLSIZE+(self.solutionPath[i][0]*CELLSIZE+self.solutionPath[i][0]*WALLSIZE), CELLSIZE-10, CELLSIZE-10)
                grid.setBrush(QColor(0,91,183))
                grid.drawEllipse(marginX+8+ WALLSIZE+(self.solutionPath[i][1]*CELLSIZE+self.solutionPath[i][1]*WALLSIZE), marginY+4+WALLSIZE+(self.solutionPath[i][0]*CELLSIZE+self.solutionPath[i][0]*WALLSIZE), CELLSIZE-11, CELLSIZE-11)

            #pelkka pallo
            #grid.drawLine(marginX+1+ WALLSIZE+(self.solutionPath[i][1]*CELLSIZE+self.solutionPath[i][1]*WALLSIZE), marginY+1+WALLSIZE+(self.solutionPath[i][0]*CELLSIZE+self.solutionPath[i][0]*WALLSIZE), marginX+1+ WALLSIZE+(self.solutionPath[i][1]*CELLSIZE+self.solutionPath[i][1]*WALLSIZE), marginY+1+WALLSIZE+(self.solutionPath[i][0]*CELLSIZE+self.solutionPath[i][0]*WALLSIZE))
    
    # labyrintin piirto
    def drawGrid(self, grid):
        pen = QPen(Qt.black, 1, Qt.SolidLine)
        col = QColor(255, 255, 255)
        col.setNamedColor('#b0d7ec')
        grid.setPen(col)
        grid.setBrush(QColor(255,255,255))
        grid.drawRect(marginX, marginY, WALLSIZE+(self.newColumns*CELLSIZE+self.newColumns*WALLSIZE), WALLSIZE+(self.newRows*CELLSIZE+self.newRows*WALLSIZE))
        grid.setBrush(QColor(176,215,236))
        # makes grid with fully closed walls in every cell
        for i in range(self.newRows):
            for j in range(self.newColumns):
                grid.drawRect(marginX+ WALLSIZE+(j*CELLSIZE+j*WALLSIZE), marginY+WALLSIZE+(i*CELLSIZE+i*WALLSIZE), CELLSIZE, CELLSIZE)
                grid.setPen(pen)
                grid.drawLine(marginX+ WALLSIZE+(j*CELLSIZE+j*WALLSIZE), marginY+WALLSIZE+(i*CELLSIZE+i*WALLSIZE), CELLSIZE+ marginX+ WALLSIZE+(j*CELLSIZE+j*WALLSIZE), marginY+WALLSIZE+(i*CELLSIZE+i*WALLSIZE))
                grid.drawLine(marginX+ WALLSIZE+(j*CELLSIZE+j*WALLSIZE), marginY+WALLSIZE+(i*CELLSIZE+i*WALLSIZE), marginX+ WALLSIZE+(j*CELLSIZE+j*WALLSIZE), CELLSIZE+ marginY+WALLSIZE+(i*CELLSIZE+i*WALLSIZE))
                grid.drawLine(CELLSIZE+marginX+ WALLSIZE+(j*CELLSIZE+j*WALLSIZE), marginY+WALLSIZE+(i*CELLSIZE+i*WALLSIZE), CELLSIZE+marginX+ WALLSIZE+(j*CELLSIZE+j*WALLSIZE), CELLSIZE+ marginY+WALLSIZE+(i*CELLSIZE+i*WALLSIZE))
                grid.drawLine(marginX+ WALLSIZE+(j*CELLSIZE+j*WALLSIZE), CELLSIZE+marginY+WALLSIZE+(i*CELLSIZE+i*WALLSIZE), marginX+ WALLSIZE+(j*CELLSIZE+j*WALLSIZE), CELLSIZE+ marginY+WALLSIZE+(i*CELLSIZE+i*WALLSIZE))
        # kauneusvirheen korjaus
        grid.drawLine(marginX+ WALLSIZE, marginY+CELLSIZE+WALLSIZE, marginX+WALLSIZE+CELLSIZE, marginY+CELLSIZE+WALLSIZE)
        
        # makes labyrinth with removed walls
        for i in range(self.newRows):
            for j in range(self.newColumns):
                if not self.newMaze[i][j][BOTTOMWALL]:
                    grid.setPen(col)
                    grid.setBrush(QColor(176,215,236))
                    grid.drawRect(marginX+j*CELLSIZE+(j+1)*WALLSIZE, marginY+(i+1)*CELLSIZE+(i+1)*WALLSIZE, CELLSIZE, WALLSIZE)
                    grid.setPen(pen)
                    grid.drawLine(marginX+j*CELLSIZE+(j+1)*WALLSIZE, marginY+(i+1)*CELLSIZE+(i+1)*WALLSIZE, marginX+j*CELLSIZE+(j+1)*WALLSIZE, marginY+(i+1)*CELLSIZE+(i+1)*WALLSIZE+WALLSIZE)
                    grid.drawLine(marginX+j*CELLSIZE+(j+1)*WALLSIZE+CELLSIZE, marginY+(i+1)*CELLSIZE+(i+1)*WALLSIZE, marginX+j*CELLSIZE+(j+1)*WALLSIZE+CELLSIZE, marginY+(i+1)*CELLSIZE+(i+1)*WALLSIZE+WALLSIZE)
                if not self.newMaze[i][j][RIGHT]:
                    grid.setPen(col)
                    grid.setBrush(QColor(176,215,236))
                    grid.drawRect(marginX+(j+1)*CELLSIZE+(j+1)*WALLSIZE, marginY+i*CELLSIZE+(i+1)*WALLSIZE,WALLSIZE, CELLSIZE)
                    grid.setPen(pen)
                    grid.drawLine(marginX+j*CELLSIZE+(j+1)*WALLSIZE+CELLSIZE, marginY+(i+1)*CELLSIZE+(i+1)*WALLSIZE, marginX+j*CELLSIZE+(j+1)*WALLSIZE+WALLSIZE+CELLSIZE, marginY+(i+1)*CELLSIZE+(i+1)*WALLSIZE)
                    grid.drawLine(marginX+j*CELLSIZE+(j+1)*WALLSIZE+CELLSIZE, marginY+(i)*CELLSIZE+(i+1)*WALLSIZE, marginX+j*CELLSIZE+(j+1)*WALLSIZE+WALLSIZE+CELLSIZE, marginY+(i)*CELLSIZE+(i+1)*WALLSIZE)
                if self.newMaze[i][j][CROSSING]:
                    grid.setPen(col)
                    #grid.setBrush(QColor(255,128,255))
                    #grid.drawRect(marginX+ WALLSIZE+(j*CELLSIZE+j*WALLSIZE), marginY+WALLSIZE+(i*CELLSIZE+i*WALLSIZE), CELLSIZE, CELLSIZE)
                    grid.setPen(pen)
                    rand = 1
                    if rand == 1:
                        grid.drawLine(marginX+WALLSIZE+(j*CELLSIZE+j*WALLSIZE), marginY+(i*CELLSIZE+i*WALLSIZE), marginX+ WALLSIZE+(j*CELLSIZE+j*WALLSIZE), CELLSIZE+marginY+WALLSIZE+ WALLSIZE+(i*CELLSIZE+i*WALLSIZE))
                        grid.drawLine(CELLSIZE+ marginX+WALLSIZE+(j*CELLSIZE+j*WALLSIZE), marginY+(i*CELLSIZE+i*WALLSIZE),CELLSIZE+marginX+ WALLSIZE+(j*CELLSIZE+j*WALLSIZE), CELLSIZE+marginY+WALLSIZE+WALLSIZE+(i*CELLSIZE+i*WALLSIZE))
                    else:
                        grid.drawLine(marginX+(j*CELLSIZE+j*WALLSIZE), marginY+WALLSIZE+(i*CELLSIZE+i*WALLSIZE), CELLSIZE+ marginX+WALLSIZE+ WALLSIZE+(j*CELLSIZE+j*WALLSIZE), marginY+WALLSIZE+(i*CELLSIZE+i*WALLSIZE))
                        grid.drawLine(marginX+(j*CELLSIZE+j*WALLSIZE), CELLSIZE+marginY+WALLSIZE+(i*CELLSIZE+i*WALLSIZE), CELLSIZE+marginX+WALLSIZE+ WALLSIZE+(j*CELLSIZE+j*WALLSIZE), CELLSIZE+marginY+WALLSIZE+(i*CELLSIZE+i*WALLSIZE))
        # aloitus keskelle
        grid.setPen(col)
        brush = QBrush(Qt.SolidPattern)
        brush.setStyle(Qt.Dense2Pattern)
        grid.setBrush(brush)
        grid.setBrush(QColor(132,193,255))
        grid.drawRect(1+marginX+ WALLSIZE+(self.newColumns*0.5*CELLSIZE+self.newColumns*0.5*WALLSIZE) ,1+ marginY+WALLSIZE+(self.newRows*0.5*CELLSIZE+self.newRows*0.5*WALLSIZE),CELLSIZE-2,CELLSIZE-2)  
        # maali jonnekin laidalle
        grid.setPen(col)
        brush.setStyle(Qt.Dense5Pattern)
        grid.setBrush(brush)
        grid.drawRect(marginX+ WALLSIZE+(self.maze.endcolumn*CELLSIZE+self.maze.endcolumn*WALLSIZE)+1, marginY+WALLSIZE+(self.maze.endrow*CELLSIZE+self.maze.endrow*WALLSIZE)+1,CELLSIZE-2,CELLSIZE-2)
     
    #----------------------------------------------------------------------------------------------
    # triggers when A, D S or W key is pressed
    def keyPressEvent(self, event):
        key = event.key()
        
        if self.maze.endrow == self.mouse.getMouseCoordinateX() and self.maze.endcolumn == self.mouse.getMouseCoordinateY():
            self.mouse.update()
            

        elif key == Qt.Key_A:
            self.mouse.setMouseDirection(LEFT)
            self.mouse.update()
            self.mouse.moveMouse(LEFT, self.newMaze, True)
            #print(self.mouse.getMouseCoordinateX(),self.mouse.getMouseCoordinateY())
            
        elif key == Qt.Key_D:
            self.mouse.setMouseDirection(RIGHT)
            self.mouse.update()
            self.mouse.moveMouse(RIGHT, self.newMaze, True)
            #print(self.mouse.getMouseCoordinateX(),self.mouse.getMouseCoordinateY())
            
        elif key == Qt.Key_W:
            self.mouse.setMouseDirection(UP)
            self.mouse.update()
            self.mouse.moveMouse(UP, self.newMaze, True)
            #print(self.mouse.getMouseCoordinateX(),self.mouse.getMouseCoordinateY())
        
        elif key == Qt.Key_S:
            self.mouse.setMouseDirection(DOWN)
            self.mouse.update()
            self.mouse.moveMouse(DOWN, self.newMaze, True)
            #print(self.mouse.getMouseCoordinateX(),self.mouse.getMouseCoordinateY())
