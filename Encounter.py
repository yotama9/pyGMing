#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
from PyQt4 import Qt
from PyQt4 import QtGui,QtCore
from src.text_aiders import *
from src.number_aiders import *
from src.gui_elements import *



class pyGM(QtGui.QWidget):
    
    def __init__(self,argv):
        super(pyGM,self).__init__()
        self.set_const()
        self.set_flags()
        self.initUI()
        if len(argv) > 1 and 'test' in argv:
            self.test()

    def test (self):
        args = ['name','horse','init',12,'hp',15]
        self.addInit(args)
        args = ['name','goblin','init',14,'hp',35]
        self.addInit(args)
        return
        #nothing to test for now, will have to later, probably

    def set_const(self):
        self.EXECUTE = 1
        self.READNAME = 2
        self.READINIT = 3
        self.READHP = 4
        self.READ_HP_TARGET = 5
        self.READ_HP_DELTA = 6
        self.condition = self.EXECUTE
        return

    def set_flags(self):
        self.creatureName = None
        self.creatureInit = None
        self.creatureHP = None
        self.hp_target = None
        self.hp_delta = None
        self.hp_change_sign = None
        self.creatureCount = 0
        self.commandHist = []
        return

    def initUI(self):
        #Window properties
        self.setGeometry(100,100,1150,550)
        self.setWindowTitle('pyGM')
        
        self.init_gravity_boxes()
        self.setColors()
        
        self.pop_ui_box()
        self.pop_init_box()
        self.pop_hist_box()
        self.pop_main_box()
        self.setLayout(self.vbox0)
        self.show()


    def setColors(self):
        #dark background for current init
        
        self.cur_init_color = "QFrame { background-color:rgb(215,215,215)}"
        self.main_color = "QFrame { background-color:rgb(240,240,240)}"



    def pop_init_box(self):
        #populate the initative box
        self.init_labels = []
        self.cur_init = -1
        for i in range (40,20,-1):
            label = InitLabel()
            self.init_lbox.addWidget(label)
            self.init_labels.append(label)
        for i in range (20,0,-1):
            label = InitLabel()
            self.init_rbox.addWidget(label)
            self.init_labels.append(label)
        

    def pop_hist_box(self):
        #populate the history box
        self.hist_labels = []
        for i in range (1,6):
            label = QtGui.QLabel(str(i) + '.')
            self.hist_labels.append(label)
            self.hist_vbox.addWidget(label)

    def pop_main_box(self):
        #the main box, where information is displayed
        self.main_label = QtGui.QLabel('Details')
        self.main_text = QtGui.QLabel()
        #Reading the welcome message from file
        self.main_text.setText(open('share/welcome.txt').read())

        self.main_text.setWordWrap(True) #To handle long sentenses
        self.main_vbox.addWidget(self.main_label)
        self.main_vbox.addWidget(self.main_text)
        self.main_vbox.addStretch(1)

        


    def init_gravity_boxes(self):
        #I split the frame into four frames
        #Lower one for inteface and messages
        #Left one, the main one, for info (about monsters, characters etc)
        #Right one, for sequances, the top would be used for initiatice
        #and the bottom for command history
        
        #The main gravity box, vertical
        self.vbox0 = QtGui.QVBoxLayout() 
        self.vbox0.addStretch(1)

        #creating a box that will split the 
        #area horziontally
        hbox = QtGui.QHBoxLayout()
        self.vbox0.addLayout(hbox)
        
        #The main box, vertical
        self.main_vbox = QtGui.QVBoxLayout()
        hbox.addLayout(self.main_vbox,10)

        #The side box, vertical
        side_vbox = QtGui.QVBoxLayout()
        hbox.addLayout(side_vbox,1)

        #The initiative box
        side_vbox.addWidget(QtGui.QLabel('Initiative')) 
        self.init_hbox = QtGui.QHBoxLayout()
        self.init_lbox = QtGui.QVBoxLayout()
        self.init_rbox = QtGui.QVBoxLayout()
        self.init_hbox.addLayout(self.init_lbox)
        self.init_hbox.addLayout(self.init_rbox)
        side_vbox.addLayout(self.init_hbox,7)

        #The history box
        side_vbox.addWidget(QtGui.QLabel('History')) 
        self.hist_vbox = QtGui.QVBoxLayout()
        side_vbox.addLayout(self.hist_vbox,3)

        #The uibox gravity box, vertical
        self.ui_vbox = QtGui.QVBoxLayout()
        self.vbox0.addLayout(self.ui_vbox)



    def pop_ui_box(self):
        #Create the interface section
        h_box = QtGui.QHBoxLayout()
        self.msg_label = QtGui.QLabel('Now Reading:',self)
        self.msg_line = QtGui.QLabel('commands',self) #the user message label
        self.input_line = QtGui.QLineEdit('',self) #The command line
        self.input_line.returnPressed.connect(self.executeCommand)
        h_box.addWidget(self.msg_label)
        h_box.addWidget(self.msg_line)
        h_box.addStretch(1)
        self.ui_vbox.addLayout(h_box)
        self.ui_vbox.addWidget(self.input_line)


    def stepInit(self):
        #advance the inittiative by one step
        #First, cancel clear the frame around the ended roudn
        self.init_labels[self.cur_init].setStyleSheet(self.main_color)
        self.cur_init += 1 #step
        if self.init_labels[self.cur_init].init_round < 0: #check the edge
            self.cur_init = 0

        #color new frame
        self.init_labels[self.cur_init].setStyleSheet(self.cur_init_color) 


    def addInit(self,args=[]):
        #Convert args into str
        for i in range (len(args)):
            args[i] = QtCore.QString(str(args[i]))
        #Put the creautur summerty in the main display
        for i in range(0,len(args),2):
            if args[i].compare('name',False) == 0: self.creatureName = args[i+1]
            if args[i].compare('init',False) == 0: self.creatureInit = args[i+1]
            if args[i].compare('hp',False) == 0:self.creatureHP = args[i+1]



        self.creatureInit = number_confirmer(val=self.creatureInit,minv=0)
        self.creatureHP = number_confirmer(val=self.creatureHP,minv=0)
        self.main_text.setText(make_creautre_summery(self.creatureName,
                                                     self.creatureInit,
                                                     self.creatureHP))

        if self.creatureName == None:
            # read creaure name
            self.msg_line.setText('Creature name')
            self.condition = self.READNAME
            return


        if self.creatureInit == None:
            # read creature initaitve value
            self.msg_line.setText('Creature initiative')
            self.condition = self.READINIT
            return

        if self.creatureHP == None:
            # read creature hp value
            self.msg_line.setText('Creature HP')
            self.condition = self.READHP
            return



        #Add to the init label, we need to rearange the labels
        
        for ilabel in self.init_labels:
            if ilabel.init_round == -1: 
                #Reached the end of the init list, append
                ilabel.setInitText(self.creatureName,
                                   self.creatureInit,
                                   self.creatureHP)
                #Increase creature count. This will only be reached once

                self.creatureCount += 1                 
                break
            if ilabel.init_round < self.creatureInit:
                #Found somebody that acts later, switch
                nname = ilabel.name
                ninit = ilabel.init_round
                nhp = ilabel.hp
                ilabel.setInitText(self.creatureName,
                                   self.creatureInit,
                                   self.creatureHP)
                self.creatureName = nname
                self.creatureInit = ninit
                self.creatureHP = nhp

                self.addInit()
                break

        #no reading data from user past this line
            
        #initializing the marker if there is none
        if self.cur_init < 0:
            self.cur_init = 0
            self.init_labels[0].setStyleSheet(self.cur_init_color)


        self.resetCondition()
        return

    def resetCondition(self):
        #Reset the conditions. Any condition should be set before here

        self.condition = self.EXECUTE
        self.msg_line.setText('commands')
        self.main_text.setText(open('share/welcome.txt').read())
        self.creatureName = None
        self.creatureInit = None
        self.creatureHP = None
        self.hp_delta = None
        self.hp_target = None
        self.hp_change_sign = 0
        return
        


    def dmhelp(self,args=[]):
        #help display
        if len(args) == 0: #essentially, welcome message
            self.main_text.setText(open('share/welcome.txt').read())
            return

        command = str(args[0])
        
        self.main_text.setText(open('share/{}.txt'.format(args[0])).read())


    def appendCommand(self,command):
        #manage the command history. 
        if command in self.commandHist: #remove duplicity
            i = self.commandHist.index(command)
            command = self.commandHist.pop(i)
            
        #append the command at the end
        self.commandHist.append(command)
        for i in range(len(self.hist_labels)): 
            #update the history list
            if i >= len(self.commandHist): break
            command = self.commandHist[-i-1]
            if len(command) > 10:
                command = command[:10] + '...'
            line = '{}.{}'.format(i+1,command)
            self.hist_labels[i].setText(line)

    def change_hp(self,args=[]):
        if self.creatureCount == 0:
            #No creature, can't change hp
            self.resetCondition()
            return

        #Convert args into str

        #Single creature, only one tareget. 
        #Unless something is messy in the args, it will be chosen
        if self.creatureCount == 1: self.hp_target = 0

        for i in range (len(args)):
            args[i] = QtCore.QString(str(args[i]))

        for i in range (0,len(args),2):
            #The false is for case sensetive
            if args[i].compare('target',False) == 0: self.hp_target = args[i+1]
            if args[i].compare('delta',False) == 0: self.hp_delta = args[i+1]

        self.hp_target = number_confirmer(val=self.hp_target,
                                          minv=0,
                                          maxv=self.creatureCount)
        self.hp_delta = number_confirmer(val=self.hp_delta,minv=0)



        if not self.hp_target:
            #excetued if no creature is selected, or invalid target
            #list creatures
            self.main_text.setText(list_init_round(self.init_labels))
            self.condition = self.READ_HP_TARGET
            self.msg_line.setText('Target of attack')
            return

        if not self.hp_delta:
            #ask for change in hp
            self.condition = self.READ_HP_DELTA
            self.msg_line.setText('Damage')
            return

        #No changes after this point
        self.hp_delta *= self.hp_change_sign
        self.init_labels[self.hp_target-1].change_hp(self.hp_delta)
        
        self.resetCondition()

        
        return
        #not implemented yet
        
        
    def executeCommand(self):
        fullcommand = self.input_line.text() #Get the command
        args = fullcommand.split(' ')
        if len(args) == 0:
            return
        command = args[0]
        if len(args) == 1:
            args = []
        else:
            args = args[1:]
            
        self.input_line.setText('') #Clear the command line
        if self.condition == self.READNAME:
            self.condition = self.EXECUTE
            self.addInit(['name',command])
            return
        if self.condition == self.READINIT:
            self.condition = self.EXECUTE
            self.addInit(['init',command])
            return
        if self.condition == self.READHP:
            self.condition = self.EXECUTE
            self.addInit(['hp',command])
            return
        if self.condition == self.READ_HP_TARGET:
            self.condition = self.EXECUTE
            self.change_hp(['target',command])
            return
        if self.condition == self.READ_HP_DELTA:
            self.condition = self.EXECUTE
            self.change_hp(['delta',command])
            return

        if self.condition == self.EXECUTE: #Execute a command
            self.appendCommand(fullcommand)
            if command.toLower() == 'step': #Advance the init in one
                self.stepInit()
                return
            if command.toLower() == 'add': #Add combatant
                self.msg_line.setText('Adding to inittiative order')
                self.addInit(args)
                return
            if command.toLower() == 'hit': #hit somebody, and deal damage
                self.hp_change_sign = -1
                self.msg_line.setText('Dealing damage')
                self.change_hp(args)
                return

            if command.toLower() == 'heal': #heal damage
                self.hp_change_sign = 1
                self.msg_line.setText('Dealing damage')
                self.change_hp(args)
                return

            
            if command.toLower() == 'help': #Type help
                self.dmhelp(args)
            if command.toLower() == 'exit': #exit
                self.exit()
            return


    def exit(self):
        #Exit the program, for now, no confirmation
        QtGui.QApplication.quit()


    




def main():
    app = QtGui.QApplication(sys.argv)
    dm = pyGM(sys.argv)
    sys.exit(app.exec_())

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'test':
            main()
    main()
