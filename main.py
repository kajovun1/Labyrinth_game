#!/usr/bin/python3
# -*- coding: utf-8 -*-
from game import Game
import sys
from PyQt5.QtWidgets import (QApplication) 

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    
    game = Game(True)
    
    sys.exit(app.exec_())