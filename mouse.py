from PyQt5.QtCore import (QRectF, QPointF)
from PyQt5.QtGui import (QPainter, QColor, QPainterPath)
from PyQt5.QtWidgets import QFrame

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

class Mouse(QFrame):

    def __init__(self, a):
        if (a == True):
            super().__init__()
        self.x = 0
        self.y = 0
        self.direction = UP
        self.crossing = False
        self.earlier = [0,0]
        self.initMouse()
          
    def initMouse(self): 
        self.x = 0
        self.y = 0
        self.direction = UP
        self.earlier = [0,0]

    def paintEvent(self, event):   
        qp = QPainter()
        qp.begin(self)
        self.drawMouse(qp)
        qp.end()
    
    #hiiren piirto
    def drawMouse(self, qp):
        if self.direction == LEFT:
            #body
            qp.setBrush(QColor(185, 122, 87)) 
            if self.crossing == True:
                qp.setBrush(QColor(113, 183, 221)) #blue if in tunneli
            qp.drawEllipse(((CELLSIZE+WALLSIZE)*self.y)+marginX+WALLSIZE+3, ((CELLSIZE+WALLSIZE)*self.x)+marginY+WALLSIZE+3, 9, 7)
            #ears
            qp.setBrush(QColor(132,92,62))
            if self.crossing == True:
                qp.setBrush(QColor(113, 183, 221)) #blue if in tunneli           
            qp.drawEllipse(((CELLSIZE+WALLSIZE)*self.y)+marginX+WALLSIZE+2, ((CELLSIZE+WALLSIZE)*self.x)+marginY+WALLSIZE+2, 3, 3)
            qp.drawEllipse(((CELLSIZE+WALLSIZE)*self.y)+marginX+WALLSIZE+2, ((CELLSIZE+WALLSIZE)*self.x)+marginY+WALLSIZE+8, 3, 3)
            # tail
            path = QPainterPath(QPointF(((CELLSIZE+WALLSIZE)*self.y)+marginX+WALLSIZE+7+5, ((CELLSIZE+WALLSIZE)*self.x)+marginY+WALLSIZE+7))
            path.cubicTo(((CELLSIZE+WALLSIZE)*self.y)+marginX+WALLSIZE+7+7, ((CELLSIZE+WALLSIZE)*self.x)+marginY+WALLSIZE+9, ((CELLSIZE+WALLSIZE)*self.y)+marginX+WALLSIZE+7+5, ((CELLSIZE+WALLSIZE)*self.x)+marginY+WALLSIZE+10, ((CELLSIZE+WALLSIZE)*self.y)+marginX+WALLSIZE+7+13, ((CELLSIZE+WALLSIZE)*self.x)+marginY+WALLSIZE+10)
            qp.setBrush(0)
            qp.drawPath(path)
        elif self.direction == RIGHT:
            #body
            qp.setBrush(QColor(185, 122, 87))
            if self.crossing == True:
                qp.setBrush(QColor(113, 183, 221)) #blue if in tunneli
            qp.drawEllipse(((CELLSIZE+WALLSIZE)*self.y)+marginX+WALLSIZE+3, ((CELLSIZE+WALLSIZE)*self.x)+marginY+WALLSIZE+3, 9, 7)
            #ears
            qp.setBrush(QColor(132,92,62))
            if self.crossing == True:
                qp.setBrush(QColor(113, 183, 221)) #blue if in tunneli
            qp.drawEllipse(((CELLSIZE+WALLSIZE)*self.y)+marginX+WALLSIZE+10, ((CELLSIZE+WALLSIZE)*self.x)+marginY+WALLSIZE+2, 3, 3)
            qp.drawEllipse(((CELLSIZE+WALLSIZE)*self.y)+marginX+WALLSIZE+10, ((CELLSIZE+WALLSIZE)*self.x)+marginY+WALLSIZE+8, 3, 3)
            # tail
            path = QPainterPath(QPointF(((CELLSIZE+WALLSIZE)*self.y)+marginX+WALLSIZE+7-5, ((CELLSIZE+WALLSIZE)*self.x)+marginY+WALLSIZE+7))
            path.cubicTo(((CELLSIZE+WALLSIZE)*self.y)+marginX+WALLSIZE+7-6, ((CELLSIZE+WALLSIZE)*self.x)+marginY+WALLSIZE+9, ((CELLSIZE+WALLSIZE)*self.y)+marginX+WALLSIZE+7-5, ((CELLSIZE+WALLSIZE)*self.x)+marginY+WALLSIZE+10, ((CELLSIZE+WALLSIZE)*self.y)+marginX+WALLSIZE+7-13, ((CELLSIZE+WALLSIZE)*self.x)+marginY+WALLSIZE+10)
            qp.setBrush(0)
            qp.drawPath(path)
            
        elif self.direction == UP:
            #body
            qp.setBrush(QColor(185, 122, 87))
            if self.crossing == True:
                qp.setBrush(QColor(113, 183, 221))  #blue if in tunneli
            qp.drawEllipse(((CELLSIZE+WALLSIZE)*self.y)+marginX+WALLSIZE+3, ((CELLSIZE+WALLSIZE)*self.x)+marginY+WALLSIZE+3, 7, 9)
            #ears
            qp.setBrush(QColor(132,92,62))
            if self.crossing == True:
                qp.setBrush(QColor(113, 183, 221)) #blue if in tunneli
            qp.drawEllipse(((CELLSIZE+WALLSIZE)*self.y)+marginX+WALLSIZE+2, ((CELLSIZE+WALLSIZE)*self.x)+marginY+WALLSIZE+2, 3, 3)
            qp.drawEllipse(((CELLSIZE+WALLSIZE)*self.y)+marginX+WALLSIZE+8, ((CELLSIZE+WALLSIZE)*self.x)+marginY+WALLSIZE+2, 3, 3)
            # tail
            path = QPainterPath(QPointF(((CELLSIZE+WALLSIZE)*self.y)+marginX+WALLSIZE+7, ((CELLSIZE+WALLSIZE)*self.x)+marginY+WALLSIZE+12))
            path.cubicTo(((CELLSIZE+WALLSIZE)*self.y)+marginX+WALLSIZE+7-4, ((CELLSIZE+WALLSIZE)*self.x)+marginY+WALLSIZE+12+3, ((CELLSIZE+WALLSIZE)*self.y)+marginX+WALLSIZE+7-4, ((CELLSIZE+WALLSIZE)*self.x)+marginY+WALLSIZE+12+8, ((CELLSIZE+WALLSIZE)*self.y)+marginX+WALLSIZE+7+0, ((CELLSIZE+WALLSIZE)*self.x)+marginY+WALLSIZE+12+12)
            qp.setBrush(0)
            qp.drawPath(path)
            
        elif self.direction == DOWN:
            #body
            qp.setBrush(QColor(185, 122, 87))
            if self.crossing == True:
                qp.setBrush(QColor(113, 183, 221)) #blue if in tunneli
            qp.drawEllipse(((CELLSIZE+WALLSIZE)*self.y)+marginX+WALLSIZE+3, ((CELLSIZE+WALLSIZE)*self.x)+marginY+WALLSIZE+3, 7, 9)
            #ears
            qp.setBrush(QColor(132,92,62))
            if self.crossing == True:
                qp.setBrush(QColor(113, 183, 221)) #blue if in tunneli
            qp.drawEllipse(((CELLSIZE+WALLSIZE)*self.y)+marginX+WALLSIZE+2, ((CELLSIZE+WALLSIZE)*self.x)+marginY+WALLSIZE+10, 3, 3)
            qp.drawEllipse(((CELLSIZE+WALLSIZE)*self.y)+marginX+WALLSIZE+8, ((CELLSIZE+WALLSIZE)*self.x)+marginY+WALLSIZE+10, 3, 3)                 
            # tail
            path = QPainterPath(QPointF(((CELLSIZE+WALLSIZE)*self.y)+marginX+WALLSIZE+7, ((CELLSIZE+WALLSIZE)*self.x)+marginY+WALLSIZE+2))
            path.cubicTo(((CELLSIZE+WALLSIZE)*self.y)+marginX+WALLSIZE+7-4, ((CELLSIZE+WALLSIZE)*self.x)+marginY+WALLSIZE+12-15, ((CELLSIZE+WALLSIZE)*self.y)+marginX+WALLSIZE+7-3, ((CELLSIZE+WALLSIZE)*self.x)+marginY+WALLSIZE+12-14, ((CELLSIZE+WALLSIZE)*self.y)+marginX+WALLSIZE+7-1, ((CELLSIZE+WALLSIZE)*self.x)+marginY+WALLSIZE+12-17)
            qp.setBrush(0)
            qp.drawPath(path)
            
    # tarvittavat getterit
    def getMouse(self):
        return self.mouse
    
    def getMouseCoordinateX(self):
        return self.x
    
    def getMouseCoordinateY(self):
        return self.y
    
    def getMouseEarlierCoordinateX(self):
        return self.earlier[0]
    
    def getMouseEarlierCoordinateY(self):
        return self.earlier[1]
    
    def getMouseDirection(self):
        return self.direction
    
    def getMouseCrossing(self):
        return self.crossing
    
    # tarvittavat setterit
    def setMouseCoordinates(self, X, Y):
        self.x = X
        self.y= Y
    
    def setMouseEarlierCoordinates(self, X, Y):
        self.earlier[0] = X
        self.earlier[1] = Y 
    
    def setMouseDirection(self, direction):
        self.direction = direction
    
    def setMouseCrossing(self, crossing):
        self.crossing = crossing
        
    def boundingRect( self ):
        return QRectF( 0, 0, self.width, self.height )
    
    # funktio hiiren liikuttamiseen
    def moveMouse(self,direction,maze,a):
        #in case mouse is  in crossing
        if maze[self.x][self.y][CROSSING] == True:
            if direction == UP:
                if self.earlier == [self.x-1,self.y] or self.earlier == [self.x+1,self.y]:
                    self.earlier = [self.x,self.y]
                    self.x = self.x - 1
            if direction == DOWN:
                if self.earlier == [self.x-1,self.y] or self.earlier == [self.x+1,self.y]:
                    self.earlier = [self.x,self.y] 
                    self.x = self.x + 1
            if direction == RIGHT:
                if self.earlier == [self.x,self.y-1] or self.earlier == [self.x,self.y+1]:
                    self.earlier = [self.x,self.y]
                    self.y = self.y + 1                                        
            if direction == LEFT:
                if self.earlier == [self.x,self.y-1] or self.earlier == [self.x,self.y+1]:
                    self.earlier = [self.x,self.y]
                    self.y = self.y - 1
        #jos ei risteyksessa
        elif direction == UP:
                if maze[self.x-1][self.y][BOTTOMWALL] == False:
                    self.earlier = [self.x,self.y]
                    if self.x-1 >= 0:
                        self.x = self.x - 1
        elif direction == DOWN:
                if maze[self.x][self.y][BOTTOMWALL] == False:
                    self.earlier = [self.x,self.y]
                    self.x = self.x + 1
        elif direction == RIGHT:
                if maze[self.x][self.y][RIGHTWALL] ==False:
                    self.earlier = [self.x,self.y]
                    self.y = self.y +1
        elif direction == LEFT:
                if maze[self.x][self.y-1][RIGHTWALL] == False:
                    self.earlier = [self.x,self.y]
                    if self.y-1 >= 0:
                        self.y = self.y - 1
        # needed because mouse color changes to blue under crossing
        if maze[self.x][self.y][CROSSING] == True and (self.earlier == [self.x,self.y-1] or self.earlier == [self.x,self.y+1]) :
            self.crossing = True
        else:
            self.crossing = False
        if (a == True):
            self.update()