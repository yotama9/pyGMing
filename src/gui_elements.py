from number_aiders import *
from text_aiders import *
from PyQt4 import QtGui,QtCore


class InitLabel(QtGui.QLabel):
    #This class is used to display and store information about initative round
    def __init__(self):
        super(InitLabel,self).__init__()
        self.setInitText()

    def setInitText(self,name=None,iround=None,hp=None):
        #Set init and name values, and display the label

        if not name:
            name = ''
        if not iround:
            iround = -1
        if not hp:
            hp = 0
         

        text = make_init_text(name,iround,hp)
        self.name = name
        self.init_round = iround
        self.hp = hp
        self.setMaxHP(self.hp)
        self.setText(text)
        return

    def setMaxHP(self,hp):
        self.maxHP = hp
        return

    def change_hp(self,delta):
        try:
            delta = int(delta)
        except ValueError:
            return

        self.hp += delta
        #Update the text
        self.setText(make_init_text(self.name,self.init_round,self.hp))

    
