import sys
import random

BOTTOMWALL = 0
RIGHTWALL = 1
VISITED = 2
CROSSING = 3

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

class Maze():
        
    def __init__(self, rows, columns):
        
        self.rows = rows
        self.columns = columns
        self.resetMaze()
        self.startrow = random.randrange(rows)
        self.startcolumn = random.randrange(columns)
        
        self.endrow = random.randrange(rows)
        if self.endrow < (rows*0.5):
            self. endrow = 0
            self.endcolumn =random.randrange(columns)
        else:
            self.endcolumn = 0
        
        self.a = 0
        # The search can be quite deep
        if rows*columns > sys.getrecursionlimit():
            sys.setrecursionlimit(rows*columns+10)
        #----------------------------------------------------------------------------
        
        # number matrix for solving maze
        self.numtable = [[[-1,-1] for j in range(columns)]for i in range(rows)]
        self.numtable2 = []
        # solution path
        self.solutionpath = []

    def resetMaze(self):
        self.maze = [[[True, True, False, False] for j in range(self.columns)] for i in range(self.rows)]
        # resetoidaan myos ratkaisumuuttujat
        self.numtable = [[[-1,-1] for j in range(self.columns)]for i in range(self.rows)]
        self.numtable2 = []
        self.solutionpath = []
    
    # tarvittavat setterit
    def setGoal(self):
        self.endrow = random.randrange(self.rows)
        self.endcolumn = random.randrange(self.columns)
        if self.endrow < 0.5*self.rows:
            self.endrow = 0
        elif self.endcolumn < 0.5*self.columns:
            self.endcolumn = 0
        elif self.endrow > 0.5*self.rows and self.columns > self.rows:
            self.endrow = self.rows -1
        elif self.endrow > 0.5*self.rows and self.columns < self.rows:
            self.endcolumn = self.columns -1
        else:
            self.endcolumn = self.columns-1
    
    def setWidth(self, width):
        self.rows = width
        
    def setHeight(self, height):
        self.columns = height
        
    def setEndRow(self, endrow):
        self.endrow = endrow

    def setEndColumn(self,endcolumn):
        self.endcolumn = endcolumn
        
    # edit one cell from maze, for testing
    def changeMaze(self,r,c, cell):
        self.maze[r][c] = cell
    
    # tarvittavat getterit    
    def getMaze(self):
        return self.maze
    
    def getRows(self):
        return self.rows
    
    def getColumns(self):
        return self.columns
    
    def getEndRow(self):
        return self.endrow
    
    def getEndColumn(self):
        return self.endcolumn
    
    # get a list with possible directions from the current position
    def _get_dirs(self,r,c):
        dirlist = []
        # check limits
        if r-1 >= 0:
            dirlist.append(UP)
        if r+1 <= self.rows-1 :
            dirlist.append(DOWN)
        if c-1 >= 0:
            dirlist.append(LEFT)
        if c+1 <= self.columns-1:
            dirlist.append(RIGHT)

        return dirlist

#------------------------------------------------------------------------------
    # generates the maze with depth-first algorithm
    def _gen_maze(self,r,c,d=None):
        
        maze = self.maze
        # knock down the wall between actual and previous position
        maze[r][c][VISITED] = True
        if   d == UP:
            maze[r][c][BOTTOMWALL] = False
        elif d == DOWN:
            maze[r-1][c][BOTTOMWALL] = False
        elif d == RIGHT:
            maze[r][c-1][RIGHTWALL]  = False
        elif d == LEFT:
            maze[r][c][RIGHTWALL]  = False

        # get the next no visited directions to move
        dirs = self._get_dirs(r,c)

        # random reorder directions
        for i in range(len(dirs)):
            j = random.randrange(len(dirs))
            dirs[i],dirs[j] = dirs[j],dirs[i]

        # make recursive call if the target cell is not visited
        for d in dirs:
            if d==UP:
                if not maze[r-1][c][VISITED]:
                    self._gen_maze( r-1,c,UP )
                #check if crossing is possible
                else:
                    if maze[r-1][c][BOTTOMWALL] and maze[r-1][c][RIGHTWALL]==False and r-2 > 0 and maze[r-2][c][VISITED] == False:
                        maze[r-1][c][CROSSING] = True
                        maze[r-1][c][BOTTOMWALL] = False
                        maze[r-1][c][RIGHTWALL] = False
                        maze[r-2][c][BOTTOMWALL] = False
                        maze[r-1][c-1][RIGHTWALL] = False
                        self._gen_maze(r-2, c, UP)
                                   
            elif d==DOWN:
                if not maze[r+1][c][VISITED]:
                    self._gen_maze( r+1,c,DOWN )
            elif d==RIGHT:
                if not maze[r][c+1][VISITED]:
                    self._gen_maze( r,c+1,RIGHT )
                #check if crossing is possible
                else:
                    if maze[r][c+1][RIGHTWALL] and maze[r][c+1][BOTTOMWALL]==False and c+2<self.columns-1 and maze[r][c+1][VISITED]==False:
                        maze[r][c+1][CROSSING] = True
                        maze[r][c+1][BOTTOMWALL] = False
                        maze[r][c+1][RIGHTWALL] = False
                        maze[r-1][c+1][BOTTOMWALL] = False
                        maze[r][c][RIGHTWALL] = False
                        self._gen_maze(r, c+2, RIGHT)
            elif d==LEFT:
                if not maze[r][c-1][VISITED]:
                    self._gen_maze( r,c-1,LEFT )
            self.setGoal()

    def set_bridge(self, r, c):
        # get the next no visited directions to move
        dirs = self._get_dirs(r,c)                       
        
    # algorithm for solving maze, a*
    def solveMaze(self, r, c, prev_r, prev_c, n):
        maze = self.maze
        numtable = self.numtable
        if maze[r][c][CROSSING] == True:
            if (prev_r==r-1 or prev_r==r+1) and numtable[r][c][0] == -1:
                numtable[r][c][0] = n
            elif (prev_c==c+1 or prev_c==c-1) and numtable[r][c][1] == -1:
                numtable[r][c][1] = n
        else:
            numtable[r][c][0] = n

        
        #check if goal reached
        if (r,c) != (self.endrow, self.endcolumn):
            directions = self._get_dirs(r, c)
            # recursive calls only if there is no wall between cells and
            # target cell is not marked (=-1)
            for d in directions:
                # jos ollaan risteyksessa ja siirtymassa pois siita
                if maze[r][c][CROSSING]==True:
                    if d ==UP and prev_r==r+1 and numtable[r-1][c][0] == -1:
                        self.solveMaze(r-1, c, r, c, n+1)
                    elif d==DOWN and prev_r==r-1 and numtable[r+1][c][0] == -1:
                        self.solveMaze(r+1,c, r, c, n+1)
                    elif d==RIGHT and prev_c==c-1 and numtable[r][c+1][0] == -1:
                        self.solveMaze(r,c+1, r, c, n+1)
                    elif d==LEFT and prev_c==c+1 and numtable[r][c-1][0] == -1:
                        self.solveMaze(r,c-1, r, c, n+1)
                # jos ollaan menossa risteykseen, alikulussa taytetaan taulukon kakkosparametri
                elif d==UP and maze[r-1][c][CROSSING] == True and numtable[r-1][c][0] == -1:
                    self.solveMaze(r-1, c, r, c, n+1)
                elif d==DOWN and maze[r+1][c][CROSSING] == True and numtable[r+1][c][0] == -1:
                    self.solveMaze(r+1,c, r, c, n+1)
                elif d==RIGHT and maze[r][c+1][CROSSING] == True and numtable[r][c+1][1] == -1:
                    self.solveMaze(r,c+1, r, c, n+1)
                elif d==LEFT and  maze[r][c-1][CROSSING] == True and numtable[r][c-1][1] == -1:
                    self.solveMaze(r,c-1, r, c, n+1)
                # jos ei olla risteyksessa eika menossa sellaiseen
                elif   d==UP and not maze[r-1][c][BOTTOMWALL] and numtable[r-1][c][0] == -1:
                    self.solveMaze(r-1,c, r, c, n+1)
                elif d==DOWN and not maze[r][c][BOTTOMWALL]   and numtable[r+1][c][0] == -1:
                    self.solveMaze(r+1,c, r, c, n+1)
                elif d==RIGHT and not maze[r][c][RIGHTWALL]    and numtable[r][c+1][0] == -1:
                    self.solveMaze(r,c+1, r, c, n+1)
                elif d==LEFT and not maze[r][c-1][RIGHTWALL]  and numtable[r][c-1][0] == -1:
                    self.solveMaze(r,c-1, r, c, n+1)
            
        else:
            # maali saavutettu kerran, ei enaa taydenneta matriisia
            self.numtable2 = numtable         
    
    # get the solution path
    def getSolutionPath(self, mouseCoordinateX, mouseCoordinateY, risteys):
        a = 0
        maze = self.maze
        actrow = self.endrow
        actcol = self.endcolumn
        startrow = mouseCoordinateX
        startcol = mouseCoordinateY
        path = []
        alla = False
        numtable = self.numtable2
        path = self.solutionpath
        while (actrow,actcol) != (startrow,startcol):
            path.append((actrow,actcol))
            directions = self._get_dirs(actrow,actcol)
            for d in directions:
                if alla == False:
                    if maze[actrow][actcol][CROSSING] == True:
                        if d== UP and (numtable[actrow][actcol][0]-1 == numtable[actrow-1][actcol][0]):
                            actrow -=1
                            alla = False
                            break
                        elif d== DOWN and (numtable[actrow][actcol][0]-1 == numtable[actrow+1][actcol][0]):
                            actrow += 1
                            alla = False
                            break
                    elif d== UP and (numtable[actrow][actcol][0]-1 == numtable[actrow-1][actcol][0]) and maze[actrow-1][actcol][BOTTOMWALL]==False:
                        actrow -=1
                        alla = False
                        break
                    elif d== DOWN and (numtable[actrow][actcol][0]-1 == numtable[actrow+1][actcol][0]) and maze[actrow][actcol][BOTTOMWALL]==False:
                        actrow += 1
                        alla = False
                        break
                    elif d== LEFT and (numtable[actrow][actcol][0]-1 == numtable[actrow][actcol-1][0]) and maze[actrow][actcol-1][RIGHTWALL]== False :
                        actcol -= 1
                        alla = False
                        break
                    elif d== LEFT and (numtable[actrow][actcol][0]-1 == numtable[actrow][actcol-1][1]):
                        actcol -= 1
                        alla = True
                        break
                    elif d== RIGHT and (numtable[actrow][actcol][0]-1 == numtable[actrow][actcol+1][0]) and maze[actrow][actcol][RIGHTWALL]== False:
                        actcol += 1
                        alla = False
                        break
                    elif d== RIGHT and (numtable[actrow][actcol][0]-1 == numtable[actrow][actcol+1][1]):
                        actcol += 1
                        alla = True
                        break
                else:

                    if d== LEFT and (numtable[actrow][actcol][1]-1 == numtable[actrow][actcol-1][0]) and path[len(path)-2][1]==actcol+1:
                        actcol -= 1
                        alla = False
                        break
                    elif d== LEFT and (numtable[actrow][actcol][1]-1 == numtable[actrow][actcol-1][1]) and path[len(path)-2][1]==actcol+1:
                        actcol -= 1
                        alla = True
                        break
                    elif d== RIGHT and (numtable[actrow][actcol][1]-1 == numtable[actrow][actcol+1][0]) and path[len(path)-2][1]==actcol-1:
                        actcol += 1
                        alla = False
                        break
                    elif d== RIGHT and (numtable[actrow][actcol][1]-1 == numtable[actrow][actcol+1][1]) and path[len(path)-2][1]==actcol-1:
                        actcol += 1
                        alla = True
                        break
        
        path.append((actrow,actcol))
        path.reverse()
        return path
        
