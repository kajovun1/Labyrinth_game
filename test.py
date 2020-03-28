

import unittest
from maze import Maze
from mouse import Mouse
from game import Game



BOTTOMWALL = 0
RIGHTWALL = 1
VISITED = 2
CROSSING = 3

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

CELLSIZE = 15
WALLSIZE = 4
marginX = 150
marginY = 10

class Test(unittest.TestCase):
    
    def testMouseMovements(self):
        #create simple maze
        maze = Maze(6,6)
        maze._gen_maze(5, 5)
        maze.changeMaze(0, 0, [False, False, True, False])
        maze.changeMaze(0, 1, [False, True, True, False])
        maze.changeMaze(0, 2, [False, False, True, False])
        maze.changeMaze(0, 3, [True, False, True, False])
        maze.changeMaze(0, 4, [True, False, True, False])
        maze.changeMaze(0, 5, [False, True, True, False])
        maze.changeMaze(1, 0, [False, True, True, False])
        maze.changeMaze(1, 1, [False, True, True, False])
        maze.changeMaze(1, 2, [False, False, True, False])
        maze.changeMaze(1, 3, [True, True, True, False])
        maze.changeMaze(1, 4, [False, False, True, False])
        maze.changeMaze(1, 5, [False, True, True, False])
        maze.changeMaze(2, 0, [False, True, True, False])
        maze.changeMaze(2, 1, [True, False, True, False])
        maze.changeMaze(2, 2, [True, True, True, False])
        maze.changeMaze(2, 3, [False, False, True, False])
        maze.changeMaze(2, 4, [True, True, True, False])
        maze.changeMaze(2, 5, [True, True, True, False])
        maze.changeMaze(3, 0, [False, True, True, False])
        maze.changeMaze(3, 1, [False, False, True, False])
        maze.changeMaze(3, 2, [True, True, True, False])
        maze.changeMaze(3, 3, [True, False, True, False])
        maze.changeMaze(3, 4, [True, False, True, False])
        maze.changeMaze(3, 5, [False, True, True, False])
        maze.changeMaze(4, 0, [True, False, True, False])
        maze.changeMaze(4, 1, [False, False, True, True])
        maze.changeMaze(4, 2, [True, False, True, False])
        maze.changeMaze(4, 3, [False, True, True, False])
        maze.changeMaze(4, 4, [False, True, True, False])
        maze.changeMaze(4, 5, [False, True, True, False])
        maze.changeMaze(5, 0, [True, False, True, False])
        maze.changeMaze(5, 1, [True, False, True, False])
        maze.changeMaze(5, 2, [True, False, True, False])
        maze.changeMaze(5, 3, [True, False, True, False])
        maze.changeMaze(5, 4, [True, True, True, False])
        maze.changeMaze(5, 5, [True, True, True, False])
        mouse = Mouse(False)
        
        ######## HIIRI RISTEYKSESSA YLATASANTEELLA TESTIT#################
        
        #aseta hiiri risteykseen, suuntaan UP, edellinen alempi ruutu
        mouse.setMouseCoordinates(4, 1)
        mouse.setMouseEarlierCoordinates(5, 1)
        mouse.setMouseDirection(UP)
        
        #kokeillaan liikuttaa vasemmalle
        mouse.moveMouse(LEFT, maze.getMaze(), False)
        self.assertEqual([4,1], [mouse.getMouseCoordinateX(), mouse.getMouseCoordinateY()], "mouse(UP) on crossing overpass, can't move LEFT")
        #kokeillaan liikuttaa oikealle
        mouse.moveMouse(RIGHT, maze.getMaze(), False)        
        self.assertEqual([4,1], [mouse.getMouseCoordinateX(), mouse.getMouseCoordinateY()], "mouse(UP) on crossing overpass, can't move RIGHT")
        
        #liikutetaan suuntaan UP, kun hiiri itse suuntaan UP
        mouse.moveMouse(UP, maze.getMaze(), False)
        self.assertEqual([3,1], [mouse.getMouseCoordinateX(), mouse.getMouseCoordinateY()], "mouse(UP) on crossing overpass, can move UP")
        
        mouse.setMouseCoordinates(4, 1)
        mouse.setMouseEarlierCoordinates(5, 1)
        mouse.setMouseDirection(DOWN)
        #liikutetaan suuntaan UP, kun hiiri itse suuntaan DOWN
        mouse.moveMouse(DOWN, maze.getMaze(), False)
        self.assertEqual([5,1], [mouse.getMouseCoordinateX(), mouse.getMouseCoordinateY()], "mouse(DOWN) on crossing overpass, can move UP")
        
        #aseta hiiri risteykseen, suuntaan UP, edellinen alempi ruutu
        mouse.setMouseCoordinates(4, 1)
        mouse.setMouseEarlierCoordinates(3, 1)
        mouse.setMouseDirection(UP)
        #liikutetaan suuntaan DOWN
        mouse.moveMouse(DOWN, maze.getMaze(), False)
        self.assertEqual([5,1], [mouse.getMouseCoordinateX(), mouse.getMouseCoordinateY()], "mouse(UP) on crossing overpass, can move DOWN")
        
        #aseta hiiri risteykseen, suuntaan UP, edellinen alempi ruutu
        mouse.setMouseCoordinates(4, 1)
        mouse.setMouseEarlierCoordinates(3, 1)
        mouse.setMouseDirection(DOWN)
        #liikutetaan suuntaan DOWN
        mouse.moveMouse(DOWN, maze.getMaze(), False)
        self.assertEqual([5,1], [mouse.getMouseCoordinateX(), mouse.getMouseCoordinateY()], "mouse(UP) on crossing overpass, can move DOWN")
        
        
        ########### HIIRI RISTEKYKSEN TUNNELISSA TESTIT ################
        
        #aseta hiiri risteykseen, suuntaan LEFT, edellinen oikealla oleva ruuut
        mouse.setMouseCoordinates(4, 1)
        mouse.setMouseEarlierCoordinates(4, 2)
        mouse.setMouseDirection(LEFT)
        
        #kokeillaan liikuttaa UP
        mouse.moveMouse(UP, maze.getMaze(), False)
        self.assertEqual([4,1], [mouse.getMouseCoordinateX(), mouse.getMouseCoordinateY()], "mouse(LEFT) in crossing underpass, can't move UP")
        #kokeillaan liikuttaa DOWN
        mouse.moveMouse(DOWN, maze.getMaze(), False)        
        self.assertEqual([4,1], [mouse.getMouseCoordinateX(), mouse.getMouseCoordinateY()], "mouse(LEFT) in crossing underpass, can't move DOWN")

        #kokeillaan liikuttaa vasemmalle
        mouse.moveMouse(LEFT, maze.getMaze(), False)
        self.assertEqual([4,0], [mouse.getMouseCoordinateX(), mouse.getMouseCoordinateY()], "mouse(LEFT) in crossing underpass, can move LEFT")
        
        #aseta hiiri risteykseen, suuntaan LEFT, edellinen oikealla oleva ruutu
        mouse.setMouseCoordinates(4, 1)
        mouse.setMouseEarlierCoordinates(4, 2)
        mouse.setMouseDirection(LEFT)
        
        #kokeillaan liikuttaa oikealle
        mouse.moveMouse(RIGHT, maze.getMaze(), False)        
        self.assertEqual([4,2], [mouse.getMouseCoordinateX(), mouse.getMouseCoordinateY()], "mouse(LEFT) in crossing underpass, can move RIGHT")

        ####### HIIRI AIVAN VASEMMASSA YLAKULMASSA #######

        #aseta hiiri ylakulmaan, suuntaan UP, edellinen alapuolella
        mouse.setMouseCoordinates(0, 0)
        mouse.setMouseEarlierCoordinates(0,1 )
        mouse.setMouseDirection(UP)
        
        #kokeillaan liikuttaa LEFT suuntaan
        mouse.moveMouse(LEFT, maze.getMaze(), False)        
        self.assertEqual([0,0], [mouse.getMouseCoordinateX(), mouse.getMouseCoordinateY()], "mouse [0,0], moves LEFT, stays")
        
        #kokeillaan liikuttaa UP suuntaan
        mouse.moveMouse(UP, maze.getMaze(), False)        
        self.assertEqual([0,0], [mouse.getMouseCoordinateX(), mouse.getMouseCoordinateY()], "mouse [0,0], moves UP, stays")
        
        #kokeillaan liikuttaa DOWN suuntaan
        mouse.moveMouse(DOWN, maze.getMaze(), False)        
        self.assertEqual([1,0], [mouse.getMouseCoordinateX(), mouse.getMouseCoordinateY()], "mouse [0,0], move DOWN :moves to [1,0]")
        
        #aseta hiiri ylakulmaan
        mouse.setMouseCoordinates(0, 0)
        mouse.setMouseEarlierCoordinates(0,1 )
        mouse.setMouseDirection(UP)
        
        #kokeillaan liikuttaa RIGHT suuntaan
        mouse.moveMouse(RIGHT, maze.getMaze(), False)        
        self.assertEqual([0,1], [mouse.getMouseCoordinateX(), mouse.getMouseCoordinateY()], "mouse [0,0], move RIGHT :moves to [0,1]")
        
        
        ####### HIIRI AIVAN VASEMMASSA ALAKULMASSA #######

        #aseta hiiri alakulmaan, suuntaan LEFT, edellinen vasemmalla
        mouse.setMouseCoordinates(5, 0)
        mouse.setMouseEarlierCoordinates(5,1 )
        mouse.setMouseDirection(LEFT)
        
        #kokeillaan liikuttaa UP suuntaan
        mouse.moveMouse(UP, maze.getMaze(), False)        
        self.assertEqual([5,0], [mouse.getMouseCoordinateX(), mouse.getMouseCoordinateY()], "mouse [5,0], moves UP, stays, koska wall")
        
        #kokeillaan liikuttaa DOWN suuntaan
        mouse.moveMouse(DOWN, maze.getMaze(), False)        
        self.assertEqual([5,0], [mouse.getMouseCoordinateX(), mouse.getMouseCoordinateY()], "mouse [5,0], moves DOWN, stays, koska alanurkka")
        
        #kokeillaan liikuttaa RIGTH suuntaan
        mouse.moveMouse(RIGHT, maze.getMaze(), False)        
        self.assertEqual([5,1], [mouse.getMouseCoordinateX(), mouse.getMouseCoordinateY()], "mouse [5,0], move RIGHT, moves koska ei seinaa")
        
        ##### HIIRI OIKEASSA YLANURKASSA
        
        #aseta hiiri ylakulmaan, suuntaan UP, edellinen alapuolella
        mouse.setMouseCoordinates(0, 5)
        mouse.setMouseEarlierCoordinates(1,5)
        mouse.setMouseDirection(UP)
        #kokeillaan liikuttaa RIGTH suuntaan
        mouse.moveMouse(RIGHT, maze.getMaze(), False)        
        self.assertEqual([0,5], [mouse.getMouseCoordinateX(), mouse.getMouseCoordinateY()], "mouse [0,5], move RIGHT, wall koska nurkka") 
        #kokeillaan liikuttaa UP suuntaan
        mouse.moveMouse(UP, maze.getMaze(), False)        
        self.assertEqual([0,5], [mouse.getMouseCoordinateX(), mouse.getMouseCoordinateY()], "mouse [0,5], move UP, wall koska nurkka") 
        
        
        ##### HIIRI OIKEASSA ALANURKASSA
        
        #aseta hiiri alakulmaan, suuntaan DOWN, edellinen ylapuolella
        mouse.setMouseCoordinates(5, 5)
        mouse.setMouseEarlierCoordinates(4,5)
        mouse.setMouseDirection(DOWN)
        #kokeillaan liikuttaa RIGTH suuntaan
        mouse.moveMouse(RIGHT, maze.getMaze(), False)        
        self.assertEqual([5,5], [mouse.getMouseCoordinateX(), mouse.getMouseCoordinateY()], "mouse [5,5], move RIGHT, wall koska nurkka") 
        #kokeillaan liikuttaa DOWN suuntaan
        mouse.moveMouse(DOWN, maze.getMaze(), False)        
        self.assertEqual([5,5], [mouse.getMouseCoordinateX(), mouse.getMouseCoordinateY()], "mouse [5,5], move DOWN, wall koska nurkka") 
        #kokeillaan liikuttaa LEFT suuntaan
        mouse.moveMouse(LEFT, maze.getMaze(), False)        
        self.assertEqual([5,5], [mouse.getMouseCoordinateX(), mouse.getMouseCoordinateY()], "mouse [5,5], move LEFT, wall koska seina")
        #kokeillaan liikuttaa UP suuntaan
        mouse.moveMouse(UP, maze.getMaze(), False)        
        self.assertEqual([4,5], [mouse.getMouseCoordinateX(), mouse.getMouseCoordinateY()], "mouse [5,5], move LEFT, moves [4,5]")
        
    def testResetMaze(self):
        #create simple 2x2 maze
        maze = Maze(2,2)
        maze._gen_maze(1, 1)
        #tyhja 2x2 labyrintti
        empty = [[[True, True, False, False], [True, True, False, False]],[[True, True, False, False],[True, True, False, False]]]
        #luotiin maze, nyt resetoidaan se
        maze.resetMaze()
        #testataan etta maze tyhja
        self.assertEqual(empty, maze.getMaze(), "maze reset toimii")
    
    # testaa kahdella eri labyrintilla etta generoinnin jlkeen joka solu kayty lapi    
    def testMazeGenerate(self):
        maze = Maze(3,6)
        maze._gen_maze(1, 1)
        for i in range(maze.getRows()):
            for j in range(maze.getRows()):
                self.assertEqual(True, maze.getMaze()[j][i][2], "gen_maze goes through every cell")
        maze2 = Maze(6,9)
        maze2._gen_maze(1, 1)
        for i in range(maze2.getRows()):
            for j in range(maze2.getRows()):
                self.assertEqual(True, maze2.getMaze()[j][i][2], "gen_maze goes through every cell")
    
    def testMazesetterit(self):
        #create simple 2x2 maze
        maze = Maze(2,2)
        maze.setHeight(6)
        maze.setWidth(4)
        maze.setEndRow(1)
        maze.setEndColumn(2)
        self.assertEqual(maze.rows, 4, "mazen setHeight toimii")
        self.assertEqual(maze.columns, 6, "mazen setWidth toimii")
        self.assertEqual(maze.endrow, 1, "mazen setEndRow toimii")
        self.assertEqual(maze.endcolumn, 2, "mazen setEndColumn toimii")
        #setGoal testit
        maze.setGoal()
        self.assertGreaterEqual(maze.getRows(), maze.getEndRow(), "rivien lkm aina suurempi tai yhtasuuri kuin maaliX")
        self.assertGreaterEqual(maze.getColumns(), maze.getEndColumn(), "sarakkeiden lkm aina suurempi tai yhtasuuri kuin maaliY")
        self.assertGreaterEqual(maze.getEndRow(), 0, "maaliX suurempaa tai yhtasuurta kuin 0")
        self.assertGreaterEqual(maze.getEndColumn(), 0, "maaliY suurempaa tai yhtasuureta kuin 0")
        
    def testMazeGetterit(self):
        maze = Maze(2,4)
        self.assertEqual(2, maze.getRows(), "getRows toimii")
        self.assertEqual(4, maze.getColumns(), "getColumns toimii")
        maze.setEndRow(0)
        maze.setEndColumn(1)
        self.assertEqual(0, maze.getEndRow(), "getEndRow toimii")
        self.assertEqual(1, maze.getEndColumn(), "getEndColumn toimii")
        empty = [[[True, True, False, False], [True, True, False, False]],[[True, True, False, False],[True, True, False, False]]]
        maze2 = Maze(2,2)
        maze2.resetMaze()
        self.assertEqual(empty, maze2.getMaze(), "getMaze toimii")
        
    def testMouseGetterit(self):
        mouse = Mouse(False)
        self.assertEqual(0, mouse.getMouseCoordinateX(), "getMouseCoordinateX toimii")
        self.assertEqual(0, mouse.getMouseCoordinateY(), "getMouseCoordinateY toimii")
        self.assertEqual(False, mouse.getMouseCrossing(), "getMouseCrossing toimii")
        self.assertEqual(UP, mouse.getMouseDirection(), "getMouseDirection toimii")
        self.assertEqual(0, mouse.getMouseEarlierCoordinateX(), "getMouseEarlierCoordinateX toimii")
        self.assertEqual(0, mouse.getMouseEarlierCoordinateY(), "getMouseEarlierCoordinateY toimii")
            
    def testMouseSetterit(self):
        mouse = Mouse(False)
        mouse.setMouseCoordinates(4, 5)
        self.assertEqual(4, mouse.getMouseCoordinateX(), "setMouseCoordantes X:lle toimii")
        self.assertEqual(5, mouse.getMouseCoordinateY(), "setMouseCoordantes Y:lle toimii")
        mouse.setMouseCrossing(True)
        self.assertEqual(True, mouse.getMouseCrossing(), "setMouseCrossing toimii")
        mouse.setMouseDirection(UP)
        self.assertEqual(UP, mouse.getMouseDirection(), "setMouseDirection toimii")
        mouse.setMouseEarlierCoordinates(5, 6)
        self.assertEqual(5, mouse.getMouseEarlierCoordinateX(), "setMouseEarlierCoordinates toimii X:lle")
        self.assertEqual(6, mouse.getMouseEarlierCoordinateY(), "setMouseEarlierCoordinates toimii Y:lle")
        
    def testSaveGame(self):
        game = Game(False)
        # peli olio arpoo maalin kun se luodaan, muutetaan se tassa 0,0:ksi
        game.maze.setEndRow(0)
        game.maze.setEndColumn(0)
        gameData = game.saveGame()
        # mika saveGame pitaisi tallentaa
        comparisonData = "GAMEFILE;MOU_7_7_0_False;MAZ_14_14_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF;END_0_0"
        # verrataan ovatko samat
        self.assertEqual(comparisonData, gameData, "testi1: saveGame toimii")
        # muutetaan maalia
        game.maze.setEndRow(9)
        game.maze.setEndColumn(8)
        # muutetaan muutamaa solua mazessa
        game.maze.changeMaze(0, 0, [False, False, True, True]) #crossing
        game.maze.changeMaze(0, 1, [False, False, True, False]) # kaikki seinat pois
        game.maze.changeMaze(0, 2, [True, False, True, False]) # vain pohjaseina
        game.maze.changeMaze(0, 3, [False, True, True, False]) # vain oikeaseina
        #asetetaan hiiri risteykseen, suunta alas
        game.mouse.setMouseCoordinates( 0, 0)
        game.mouse.setMouseCrossing(True)
        game.mouse.setMouseDirection(DOWN)
        gameData = game.saveGame()
        # testataan vastaako file asetettua sisaltoa
        comparisonData = "GAMEFILE;MOU_0_0_2_True;MAZ_14_14_FFT_FFF_TFF_FTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF;END_9_8"
        # verrataan ovatko samat
        self.assertEqual(comparisonData, gameData, "testi 2:saveGame toimii")
        # muutetaan maalia
        
    def testLoadGame(self):
        game = Game(False)
        gameData = "GAMEFILE;MOU_7_7_0_False;MAZ_14_14_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF;END_0_0"
        game.loadGame(gameData)
        self.assertEqual(7, game.mouse.getMouseCoordinateX(), "loadGame:hiiren x-koordiaatti oikein")
        self.assertEqual(7, game.mouse.getMouseCoordinateY(), "loadGame:hiiren y-koordiaatti oikein")
        self.assertEqual(0, game.mouse.getMouseDirection(), "loadGame:hiiren suunta oikein")
        self.assertEqual(False, game.mouse.getMouseCrossing(), "loadGame: hiiren alikulkutilanne oikein")
        self.assertEqual(14, game.maze.getRows(), "loadGame: mazen korkeus oikein")
        self.assertEqual(14, game.maze.getColumns(),"loadGame: mazen leveys oikein")
        self.assertEqual([True,True, True, False], game.maze.getMaze()[0][0], "loadGame: maze[0][0] oikein")
        self.assertEqual([True,True, True, False], game.maze.getMaze()[0][1], "loadGame: maze[0][1] oikein")
        self.assertEqual(0, game.maze.getEndRow(), "loadGame: mazen maalin y-koord oikein")
        self.assertEqual(0, game.maze.getEndColumn(), "loadGame: mazen maalin x-koord oikein")
        gameData = "GAMEFILE;MOU_12_8_3_True;MAZ_14_14_FFF_FFT_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF_TTF;END_10_11"
        game.loadGame(gameData)
        self.assertEqual(12, game.mouse.getMouseCoordinateX(), "loadGame:hiiren x-koordiaatti oikein")
        self.assertEqual(8, game.mouse.getMouseCoordinateY(), "loadGame:hiiren y-koordiaatti oikein")
        self.assertEqual(3, game.mouse.getMouseDirection(), "loadGame:hiiren suunta oikein")
        self.assertEqual(True, game.mouse.getMouseCrossing(), "loadGame: hiiren alikulkutilanne oikein")
        self.assertEqual(14, game.maze.getRows(), "loadGame: mazen korkeus oikein")
        self.assertEqual(14, game.maze.getColumns(),"loadGame: mazen leveys oikein")
        self.assertEqual([False,False, True, False], game.maze.getMaze()[0][0], "loadGame: maze[0][0] oikein")
        self.assertEqual([False,False, True, True], game.maze.getMaze()[0][1], "loadGame: maze[0][1] oikein")
        self.assertEqual(10, game.maze.getEndRow(), "loadGame: mazen maalin y-koord oikein")
        self.assertEqual(11, game.maze.getEndColumn(), "loadGame: mazen maalin x-koord oikein")
     
    #luodaan tunnettu labyrintti ja testataan vastaako ratkaisu oletettua    
    def testMazeSolveMazeandGetSolutionPath(self):
        maze = Maze(3,3)
        maze._gen_maze(2, 2)
        maze.changeMaze(0, 0, [False, False, True, False])
        maze.changeMaze(0, 1, [False, True, True, False])
        maze.changeMaze(0, 2, [False, True, True, False])
        maze.changeMaze(1, 0, [False, False, True, False])
        maze.changeMaze(1, 1, [False, False, True, True])
        maze.changeMaze(1, 2, [False, True, True, False])
        maze.changeMaze(2, 0, [True, False, True, False])
        maze.changeMaze(2, 1, [True, False, True, False])
        maze.changeMaze(2, 2, [True, True, True, False])
        maze.setEndColumn(0)
        maze.setEndRow(0)
        mouse = Mouse(False)
        mouse.setMouseCoordinates(1, 2)
        maze.solveMaze(1, 2, 1, 0, 0)
        self.assertEqual([[[5, -1], [4, -1], [1, -1]], [[4, -1], [3, 5], [0, -1]], [[3, -1], [2, -1], [1, -1]]], maze.numtable2, "solvemaze toimii")
        polku = maze.getSolutionPath(1, 2, 0)
        self.assertEqual([(1, 2), (2, 2), (2, 1), (2, 0), (1, 0), (0, 0)], polku, "getsolution path toimii")
     
    # dropdown arvojen tarkistus    
    def testGameonActivatedW(self):
        game = Game(False)
        game.onActivatedH(3)
        self.assertEqual(3, game.dropDownValueHeight, "gamen onActivatedW toimii")

        
    def testGameonActivatedH(self):
        game = Game(False)
        game.onActivatedW(3)
        self.assertEqual(3, game.dropDownValueWidth, "gamen onActivatedH toimii")
  
        
        
if __name__ == '__main__':
    unittest.main()


