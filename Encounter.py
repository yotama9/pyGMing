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

    def text (self):
        #nothing to test for now, will have to later, probably

    def set_const(self):
        self.EXECUTE = 1
        self.READNAME = 2
        self.READINIT = 3
        self.condition = self.EXECUTE
        return

    def set_flags(self):
        self.creatureName = None
        self.creatureInit = None
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
        for i in range (28,14,-1):
            label = InitLabel()
            self.init_lbox.addWidget(label)
            self.init_labels.append(label)
        for i in range (14,0,-1):
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
        self.main_label = QtGui.QLabel('Help')
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
        self.msg_label = QtGui.QLabel('Messages:',self)
        self.msg_line = QtGui.QLabel('',self) #the user message label
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
        #Put the creautur summerty in the main display
        for i in range(0,len(args),2):
            if args[i].compare('name',False) == 0: self.creatureName = args[i+1]
            if args[i].compare('init',False) == 0: self.creatureInit = args[i+1]


        self.creatureInit = number_confirmer(val=self.creatureInit,minv=0)
        self.main_text.setText(make_creautre_summery(self.creatureName,self.creatureInit))

        

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


        #Add to the init label, we need to rearange the labels
        
        for ilabel in self.init_labels:
            if ilabel.init_round == -1: 
                #Reached the end of the init list, append
                ilabel.setInitText(self.creatureName,self.creatureInit)
                break
            if ilabel.init_round < self.creatureInit:
                #Found somebody that acts later, switch
                nname = ilabel.name
                ninit = ilabel.init_round
                ilabel.setInitText(self.creatureName,self.creatureInit)
                self.creatureName = nname
                self.creatureInit = ninit

                self.addInit()
                break

        #no reading data from user past this line
            
        #initializing the marker if there is none
        if self.cur_init < 0:
            self.cur_init = 0
            self.init_labels[0].setStyleSheet(self.cur_init_color)


        #Reset the conditions. Any condition should be set before here
        self.condition = self.EXECUTE
        self.msg_line.setText('')
        self.main_text.setText(open('share/welcome.txt').read())
        self.creatureName = None
        self.creatureInit = None
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
            line = '{}.{}'.format(i+1,command)
            self.hist_labels[i].setText(line)



        
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
            self.addInit([QtCore.QString('name'),command])
            return
        if self.condition == self.READINIT:
            self.condition = self.EXECUTE
            self.addInit([QtCore.QString('init'),command])
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
            if command.toLower() == 'help': #Type help
                self.dmhelp(args)
            if command.toLower() == 'exit': #exit
                self.exit()
            return


    def exit(self):
        #Exit the program, for now, now confirmation
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
