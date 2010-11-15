# -*- coding: utf-8 -*-
## This file is part of HamsiManager.
## 
## Copyright (c) 2010 Murat Demir <mopened@gmail.com>      
##
## Hamsi Manager is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
## 
## Hamsi Manager is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with HamsiManager; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


import Variables
import Organizer
import Settings
import Universals
from MyObjects import *
import Tables
import Dialogs
import sys
import ReportBug
import Databases

class SpecialTools(MWidget):
    def __init__(self,_parent):
        MWidget.__init__(self, _parent)
        self.tbAddToBefore = MToolButton(self)
        self.btChange = MToolButton(self)
        self.tbAddToAfter = MToolButton(self)
        if Universals.windowMode==Variables.windowModeKeys[1]:
            self.isShowAdvancedSelections = False
        else:
            self.isShowAdvancedSelections = Universals.getBoolValue("isShowAdvancedSelections")
        self.tabwTabs = MTabWidget(self)
        self.specialActions = SpecialActions(self.tabwTabs)
        self.searchAndReplace = SearchAndReplace(self.tabwTabs)
        self.fill = Fill(self.tabwTabs)
        self.clear = Clear(self.tabwTabs)
        self.characterState = CharacterState(self.tabwTabs)
        self.pbtnAdvancedSelections = MPushButton("Simple")
        self.pbtnApply = MPushButton(translate("SpecialTools", "Apply"))
        self.pbtnApply.setIcon(MIcon("Images:apply.png"))
        self.pbtnApply.setObjectName("pbtnApply")
        self.tbAddToBefore.setToolTip(translate("SpecialTools", "Add In Front"))
        self.btChange.setToolTip(translate("SpecialTools", "Change"))
        self.tbAddToAfter.setToolTip(translate("SpecialTools", "Append"))
        self.tbAddToBefore.setIcon(MIcon("Images:addToBefore.png"))
        self.btChange.setIcon(MIcon("Images:change.png"))
        self.tbAddToAfter.setIcon(MIcon("Images:addToAfter.png"))
        self.tbAddToBefore.setAutoRaise(True)
        self.btChange.setAutoRaise(True)
        self.tbAddToAfter.setAutoRaise(True)
        self.tbAddToBefore.setCheckable(True)
        self.btChange.setCheckable(True)
        self.tbAddToAfter.setCheckable(True)
        self.btChange.setChecked(True)
        MObject.connect(self.tbAddToBefore, SIGNAL("clicked()"), self.changeTypeChanged)
        MObject.connect(self.btChange, SIGNAL("clicked()"), self.changeTypeChanged)
        MObject.connect(self.tbAddToAfter, SIGNAL("clicked()"), self.changeTypeChanged)
        self.tabwTabs.addTab(self.specialActions, translate("SpecialTools", "Special Actions"))
        self.tabwTabs.addTab(self.searchAndReplace, translate("SpecialTools", "Search - Replace"))
        self.tabwTabs.addTab(self.fill, translate("SpecialTools", "Fill"))
        self.tabwTabs.addTab(self.clear, translate("SpecialTools", "Clear"))
        self.tabwTabs.addTab(self.characterState, translate("SpecialTools", "Character State"))
        self.tabwTabs.setCurrentIndex(int(Universals.MySettings["activeTabNoOfSpecialTools"]))
        HBox0 = MHBoxLayout()
        HBox0.addWidget(self.tbAddToBefore)
        HBox0.addWidget(self.btChange)
        HBox0.addWidget(self.tbAddToAfter)
        lblX = MLabel(translate("SpecialTools", "X : "))
        lblY = MLabel(translate("SpecialTools", "Y : "))
        self.cbInformationSection = MComboBox()
        self.cbInformationSection.addItems([translate("SpecialTools", "All"), 
                                        translate("SpecialTools", "Before X"), 
                                        translate("SpecialTools", "After X"), 
                                        translate("SpecialTools", "From Last, Before X"), 
                                        translate("SpecialTools", "From Last After X"), 
                                        translate("SpecialTools", "Between X And Y"), 
                                        translate("SpecialTools", "Not Between X And Y")])
        self.cbInformationSectionX = MSpinBox()
        self.cbInformationSectionX.setRange(1, 100)
        self.cbInformationSectionX.setValue(3) 
        self.cbInformationSectionY = MSpinBox()
        self.cbInformationSectionY.setRange(1, 100)
        self.cbInformationSectionY.setValue(5) 
        self.pnlAdvancedSelections = MWidget()
        VBox = MVBoxLayout()
        self.pnlAdvancedSelections.setLayout(VBox)
        VBox1 = MVBoxLayout()
        VBox1.addStretch(3)
        VBox1.addWidget(self.pbtnAdvancedSelections)
        VBox.addWidget(self.cbInformationSection)
        HBoxs1 = MHBoxLayout()
        HBoxs1.addWidget(lblX)
        HBoxs1.addWidget(self.cbInformationSectionX)
        HBoxs1.addWidget(lblY)
        HBoxs1.addWidget(self.cbInformationSectionY)
        VBox.addLayout(HBoxs1)
        VBox.addLayout(HBox0)
        VBox1.addWidget(self.pnlAdvancedSelections)
        VBox1.addWidget(self.pbtnApply)
        HBox = MHBoxLayout()
        HBox.addWidget(self.tabwTabs)
        HBox.addLayout(VBox1)
        self.setLayout(HBox)
        _parent.dckSpecialTools = MDockWidget(translate("SpecialTools", "Special Tools"))
        _parent.dckSpecialTools.setObjectName(translate("SpecialTools", "Special Tools"))
        _parent.dckSpecialTools.setWidget(self)
        _parent.dckSpecialTools.setAllowedAreas(Mt.AllDockWidgetAreas)
        _parent.dckSpecialTools.setFeatures(MDockWidget.AllDockWidgetFeatures)
        _parent.addDockWidget(Mt.BottomDockWidgetArea,_parent.dckSpecialTools)
        MObject.connect(self.pbtnApply, SIGNAL("clicked()"), self.apply)
        MObject.connect(self.pbtnAdvancedSelections, SIGNAL("clicked()"), self.showOrHideAdvancedSelections)
        MObject.connect(self.tabwTabs, SIGNAL("currentChanged(int)"), self.tabChanged)
        self.cbInformationSectionX.setEnabled(False)
        self.cbInformationSectionY.setEnabled(False)
        self.cbInformationSection.setFixedWidth(175)
        MObject.connect(self.cbInformationSection, SIGNAL("currentIndexChanged(int)"), self.InformationSectionChanged)
        self.refreshForColumns()
        self.reFillCompleters()
        
    def InformationSectionChanged(self):
        if self.cbInformationSection.currentIndex()==0:
            self.cbInformationSectionX.setEnabled(False)
        else:
            self.cbInformationSectionX.setEnabled(True)
        if self.cbInformationSection.currentIndex()>4:
            self.cbInformationSectionY.setEnabled(True)
        else:
            self.cbInformationSectionY.setEnabled(False)
        
    def refreshForColumns(self):
        self.searchAndReplace.columns.clear()
        self.fill.columns.clear()
        self.clear.columns.clear()
        self.characterState.columns.clear()
        try:
            for btn in self.specialActions.pbtnAddObjects:
                btn.setVisible(False)
                btn.deleteLater()
        except:pass
        self.specialActions.pbtnAddObjects=[]
        self.searchAndReplace.columns.addItem(translate("SpecialTools", "All"))
        self.clear.columns.addItem(translate("SpecialTools", "All"))
        self.characterState.columns.addItem(translate("SpecialTools", "All"))
        for columnName in Universals.MainWindow.Table.tableColumns:
            self.searchAndReplace.columns.addItem(columnName)
            self.fill.columns.addItem(columnName)
            self.clear.columns.addItem(columnName)
            self.characterState.columns.addItem(columnName)
            tb = MToolButton()
            tb.setText(columnName)
            tb.setObjectName(columnName)
            tb.setAutoRaise(True)
            self.specialActions.pbtnAddObjects.append(tb)
            MObject.connect(self.specialActions.pbtnAddObjects[-1], SIGNAL("clicked()"), self.specialActions.AddObjects)
        try:
            if Universals.tableType==2:
                for x in range(0, 5):
                    self.specialActions.HBoxs[0].addWidget(self.specialActions.pbtnAddObjects[x])
                for x in range(len(self.specialActions.pbtnAddObjects)-1, 4, -1):
                    self.specialActions.HBoxs[1].insertWidget(0, self.specialActions.pbtnAddObjects[x])
            else:
                for btn in self.specialActions.pbtnAddObjects:
                    self.specialActions.HBoxs[0].addWidget(btn)
        except:pass
        self.specialActions.refreshBookmarks()
        if self.isShowAdvancedSelections==False:
            self.hideAdvancedSelections()
        else:
            self.showAdvancedSelections()
        
    def changeTypeChanged(self):
        self.tbAddToBefore.setChecked(False)
        self.btChange.setChecked(False)
        self.tbAddToAfter.setChecked(False)
        if self.sender().toolTip()==translate("SpecialTools", "Add In Front"):
            self.tbAddToBefore.setChecked(True)
        elif self.sender().toolTip()==translate("SpecialTools", "Change"):
            self.btChange.setChecked(True)
        elif self.sender().toolTip()==translate("SpecialTools", "Append"):
            self.tbAddToAfter.setChecked(True)
    
    def tabChanged(self, _index):
        Universals.setMySetting("activeTabNoOfSpecialTools", str(_index))
        self.tbAddToBefore.setEnabled(True)
        self.tbAddToAfter.setEnabled(True)
        if _index==0:
            self.cbInformationSection.setCurrentIndex(0)
            self.cbInformationSection.setEnabled(False)
        elif _index==1:
            self.cbInformationSection.setEnabled(True)
            self.changeTypeChanged()
            self.btChange.setChecked(True)
        elif _index==2:
            self.cbInformationSection.setCurrentIndex(0)
            self.cbInformationSection.setEnabled(False)
        elif _index==3:
            self.cbInformationSection.setEnabled(True)
            self.changeTypeChanged()
            self.btChange.setChecked(True)
            self.tbAddToBefore.setEnabled(False)
            self.tbAddToAfter.setEnabled(False)
        elif _index==4:
            self.cbInformationSection.setEnabled(True)
            self.changeTypeChanged()
            self.btChange.setChecked(True)
            self.tbAddToBefore.setEnabled(False)
            self.tbAddToAfter.setEnabled(False)
        
    def showOrHideAdvancedSelections(self):
        try:
            if self.isShowAdvancedSelections == False:
                self.showAdvancedSelections()
            else:
                self.hideAdvancedSelections()
        except:
            error = ReportBug.ReportBug()
            error.show()
    
    def showAdvancedSelections(self):
        self.pbtnAdvancedSelections.setText(translate("SpecialTools", "Simple"))
        self.pnlAdvancedSelections.setVisible(True)
        self.isShowAdvancedSelections = True
        self.tabwTabs.setMaximumHeight(155)
        self.setMaximumHeight(155)
        self.specialActions.showAdvancedSelections()
        self.fill.showAdvancedSelections()
        self.searchAndReplace.showAdvancedSelections()
        self.clear.showAdvancedSelections()
        self.characterState.showAdvancedSelections()
    
    def hideAdvancedSelections(self):
        self.pbtnAdvancedSelections.setText(translate("SpecialTools", "Advance"))
        self.cbInformationSection.setCurrentIndex(0)
        self.pnlAdvancedSelections.setVisible(False)
        self.isShowAdvancedSelections = False
        self.tabwTabs.setMaximumHeight(100)
        self.setMaximumHeight(100)
        self.specialActions.hideAdvancedSelections()
        self.fill.hideAdvancedSelections()
        self.searchAndReplace.hideAdvancedSelections()
        self.clear.hideAdvancedSelections()
        self.characterState.hideAdvancedSelections()
        
    def apply(self):
        try:
            self.checkCompleters()
            self.reFillCompleters()
            Universals.MainWindow.Table.createHistoryPoint()
            if self.tabwTabs.currentIndex()==0:
                if Organizer.whatDoesSpecialCommandDo(unicode(self.specialActions.leSplitPointer.text()).encode("utf-8"),
                                            self.specialActions.whereIsSplitPointer,
                                            self.specialActions.actionCommand, 
                                            True)==True:
                    Organizer.applySpecialCommand(unicode(self.specialActions.leSplitPointer.text()).encode("utf-8"),
                                self.specialActions.whereIsSplitPointer,
                                self.specialActions.actionCommand, self)
            elif self.tabwTabs.currentIndex()==1:
                Organizer.searchAndReplaceTable(unicode(self.searchAndReplace.leSearch.text()).encode("utf-8"),unicode(self.searchAndReplace.leReplace.text()).encode("utf-8"), self)
            elif self.tabwTabs.currentIndex()==2:
                Organizer.fillTable(self.fill.columns.currentText(), self, unicode(self.fill.leFill.text()).encode("utf-8"))
            elif self.tabwTabs.currentIndex()==3:
                Organizer.clearTable(self)
            elif self.tabwTabs.currentIndex()==4:
                Organizer.correctCaseSensitiveTable(self)
        except:
            error = ReportBug.ReportBug()
            error.show()
    
    def checkCompleters(self):
        if Universals.getBoolValue("isActiveCompleter"):
            self.specialActions.checkCompleters()
            self.searchAndReplace.checkCompleters()
            self.fill.checkCompleters()
            self.clear.checkCompleters()
            self.characterState.checkCompleters()
    
    def reFillCompleters(self):
        if Universals.getBoolValue("isActiveCompleter"):
            self.specialActions.reFillCompleters()
            self.searchAndReplace.reFillCompleters()
            self.fill.reFillCompleters()
            self.clear.reFillCompleters()
            self.characterState.reFillCompleters()
    
class SpecialActions(MWidget):
    def __init__(self, _parent):
        MWidget.__init__(self, _parent)
        self.history, self.future, self.isPressedAddObjects=[], [], False
        self.pbtnAddObjects = []
        self.details = MLabel(translate("SpecialTools", "Please Select An Action!.."))
        self.details.setWordWrap(True)
        self.whereIsSplitPointer, self.numberOfActionCommand, self.commaAndSplitControl="right",0,0
        self.actionCommand = ""
        self.leActionString = MLineEdit("")
        self.leSplitPointer = MLineEdit("-")
        fntFont = MFont()
        fntFont.setPointSize(16)
        fntFont.setBold(True)
        self.leSplitPointer.setFont(fntFont)
        self.cbBookmarks = MComboBox()
        self.refreshBookmarks()
        self.tbAddComma = MToolButton()
        self.tbAddComma.setText(translate("SpecialTools", ","))
        self.tbAddComma.setAutoRaise(True)
        self.tbAddSplit = MToolButton()
        self.tbAddSplit.setText(translate("SpecialTools", "Hyphen(-)"))
        self.tbAddSplit.setAutoRaise(True)
        self.tbClear = MToolButton(self)
        self.tbAddBookmark = MToolButton(self)
        self.tbDeleteBookmark = MToolButton(self)
        self.tbGoBack = MToolButton(self)
        self.tbGoForward = MToolButton(self)
        self.tbWhatDoesThisCommandDo = MToolButton(self)
        self.tbClear.setToolTip(translate("SpecialTools", "Clear"))
        self.tbAddBookmark.setToolTip(translate("SpecialTools", "Add To Bookmarks"))
        self.tbDeleteBookmark.setToolTip(translate("SpecialTools", "Remove From Bookmarks"))
        self.tbGoBack.setToolTip(translate("SpecialTools", "Back"))
        self.tbGoForward.setToolTip(translate("SpecialTools", "Forward"))
        self.tbWhatDoesThisCommandDo.setToolTip(translate("SpecialTools", "What Does This Command Do?"))
        self.tbClear.setIcon(MIcon("Images:actionClear.png"))
        self.tbAddBookmark.setIcon(MIcon("Images:addBookmark.png"))
        self.tbDeleteBookmark.setIcon(MIcon("Images:actionDelete.png"))
        self.tbGoBack.setIcon(MIcon("Images:actionBack.png"))
        self.tbGoForward.setIcon(MIcon("Images:actionForward.png"))
        self.tbWhatDoesThisCommandDo.setIcon(MIcon("Images:whatDoesThisCommandDo.png"))
        self.tbClear.setAutoRaise(True)
        self.tbAddBookmark.setAutoRaise(True)
        self.tbDeleteBookmark.setAutoRaise(True)
        self.tbGoBack.setAutoRaise(True)
        self.tbGoForward.setAutoRaise(True)
        self.tbWhatDoesThisCommandDo.setAutoRaise(True)
        self.leActionString.setEnabled(False)
        self.tbDeleteBookmark.setEnabled(False)
        MObject.connect(self.cbBookmarks, SIGNAL("currentIndexChanged(int)"), self.cbBookmarksChanged)
        MObject.connect(self.tbAddComma, SIGNAL("clicked()"), self.addComma)
        MObject.connect(self.tbAddSplit, SIGNAL("clicked()"), self.addSplit)
        MObject.connect(self.tbClear, SIGNAL("clicked()"), self.makeClear)
        MObject.connect(self.tbGoBack, SIGNAL("clicked()"), self.goBack)
        MObject.connect(self.tbGoForward, SIGNAL("clicked()"), self.goForward)
        MObject.connect(self.tbWhatDoesThisCommandDo, SIGNAL("clicked()"), self.whatDoesThisCommandDo)
        MObject.connect(self.tbAddBookmark, SIGNAL("clicked()"), self.addBookmark)
        MObject.connect(self.tbDeleteBookmark, SIGNAL("clicked()"), self.deleteBookmark)
        self.HBoxs = []
        self.HBoxs.append(MHBoxLayout())
        self.HBoxs.append(MHBoxLayout())
        self.HBoxs[1].addWidget(self.tbAddComma)
        self.HBoxs[1].addWidget(self.tbAddSplit)
        self.HBoxs[1].addWidget(self.leSplitPointer)
        self.HBoxs.append(MHBoxLayout())
        self.HBoxs[2].addWidget(self.cbBookmarks)
        self.HBoxs[2].addWidget(self.tbDeleteBookmark)
        self.HBoxs.append(MHBoxLayout())
        self.HBoxs[3].addWidget(self.tbGoBack)
        self.HBoxs[3].addWidget(self.tbGoForward)
        self.HBoxs[3].addWidget(self.tbClear)
        self.HBoxs[3].addWidget(self.leActionString)
        self.HBoxs[3].addWidget(self.tbAddBookmark)
        self.HBoxs[3].addWidget(self.tbWhatDoesThisCommandDo)
        self.HBoxs[3].addWidget(self.details)
        vblSpecialActions = MVBoxLayout()
        vblSpecialActions.addLayout(self.HBoxs[0])
        vblSpecialActions.addLayout(self.HBoxs[1])
        vblSpecialActions.addLayout(self.HBoxs[2])
        vblSpecialActions.addLayout(self.HBoxs[3])
        self.setLayout(vblSpecialActions)
        self.cbBookmarks.setSizeAdjustPolicy(MComboBox.AdjustToMinimumContentsLength)
        self.leSplitPointer.setMaximumWidth(40)
        self.tbAddComma.setMaximumWidth(40)
        self.tbAddComma.setMaximumWidth(40)
        self.leSplitPointer.setMaximumHeight(30)   
        if self.parent().parent().isShowAdvancedSelections==True:
            self.details.hide()
            
    def showAdvancedSelections(self):
        self.leActionString.show()
        self.leSplitPointer.show()
        for btn in self.pbtnAddObjects:
            btn.show()
        self.tbAddComma.show()
        self.tbAddSplit.show()
        self.tbClear.show()
        self.tbGoBack.show()
        self.tbGoForward.show()
        self.tbWhatDoesThisCommandDo.show()
        self.tbAddBookmark.show()
        self.tbDeleteBookmark.show()
        self.details.hide()
    
    def hideAdvancedSelections(self):
        self.leActionString.hide()
        self.leSplitPointer.hide()
        for btn in self.pbtnAddObjects:
            btn.hide()
        self.tbAddComma.hide()
        self.tbAddSplit.hide()
        self.tbClear.hide()
        self.tbGoBack.hide()
        self.tbGoForward.hide()
        self.tbWhatDoesThisCommandDo.hide()
        self.tbAddBookmark.hide()
        self.tbDeleteBookmark.hide()
        self.details.show()
        
    def AddObjects(self):
        try:
            if self.isPressedAddObjects==False:
                self.history.append(self.leActionString.text())
                self.future=[]
                self.tbGoForward.setEnabled(False)
                self.numberOfActionCommand+=1
                self.isPressedAddObjects=True
                self.leActionString.setText((str(self.leActionString.text()) + 
                            str(self.sender().objectName())+" ").decode("utf-8"))
                self.actionCommand += Universals.MainWindow.Table.getColumnKeyFromName(self.sender().text())
        except:
            error = ReportBug.ReportBug()
            error.show()
            
    def addComma(self):
        try:
            if self.numberOfActionCommand>0 and (self.commaAndSplitControl==0 or self.commaAndSplitControl<self.numberOfActionCommand) and self.numberOfActionCommand<100:
                self.history.append(self.leActionString.text())
                self.future=[]
                self.tbGoForward.setEnabled(False)
                self.leActionString.setText(self.leActionString.text() + ", ".decode("utf-8"))
                self.actionCommand += ", "
                self.tbAddComma.setEnabled(False)
                self.numberOfActionCommand+=100
                self.commaAndSplitControl = self.numberOfActionCommand
                self.isPressedAddObjects=False
        except:
            error = ReportBug.ReportBug()
            error.show()
            
    def addSplit(self):
        try:
            if self.numberOfActionCommand>0 and (self.commaAndSplitControl==0 or self.commaAndSplitControl<self.numberOfActionCommand) and (self.whereIsSplitPointer=="right" or self.numberOfActionCommand<100) :
                if self.numberOfActionCommand<100:
                    self.whereIsSplitPointer="left"
                if unicode(self.leSplitPointer.text()).encode("utf-8").upper()!=unicode(self.leSplitPointer.text()).encode("utf-8").decode("utf-8").lower() or unicode(self.leSplitPointer.text()).encode("utf-8").strip()=="":
                    self.leSplitPointer.setText("-")
                self.history.append(self.leActionString.text())
                self.future=[]
                self.tbGoForward.setEnabled(False)
                self.leActionString.setText(self.leActionString.text() + (str(self.leSplitPointer.text()).strip() + " ").decode("utf-8"))
                self.actionCommand += str(self.leSplitPointer.text()).strip() + " "
                self.numberOfActionCommand+=10
                self.commaAndSplitControl = self.numberOfActionCommand
                self.isPressedAddObjects=False
        except:
            error = ReportBug.ReportBug()
            error.show()
            
    def makeClear(self):
        try:
            self.history.append(self.leActionString.text())
            self.future=[]
            self.tbGoForward.setEnabled(False)
            self.leActionString.setText("")
            self.actionCommand = ""
            self.tbAddComma.setEnabled(True)
            self.numberOfActionCommand=0
            self.commaAndSplitControl=0
            self.whereIsSplitPointer="right"
            self.isPressedAddObjects=False
        except:
            error = ReportBug.ReportBug()
            error.show()
    
    def whatDoesThisCommandDo(self):
        try:
            Organizer.whatDoesSpecialCommandDo(unicode(self.leSplitPointer.text()).encode("utf-8"),self.whereIsSplitPointer,self.actionCommand)
        except:
            error = ReportBug.ReportBug()
            error.show()
    
    def goBack(self):
        try:
            if len(self.history)>0:
                if str(self.leActionString.text())[-2:].strip()==str(self.leSplitPointer.text()).strip():
                    self.numberOfActionCommand-=10
                    self.commaAndSplitControl = self.numberOfActionCommand-1
                    self.isPressedAddObjects=True
                elif str(self.leActionString.text())[-2:].strip()==",":
                    self.tbAddComma.setEnabled(True)
                    self.numberOfActionCommand-=100
                    self.commaAndSplitControl = self.numberOfActionCommand-1
                    self.isPressedAddObjects=True
                else:
                    self.numberOfActionCommand-=1
                    self.isPressedAddObjects=False
                self.future.append(self.leActionString.text())
                h = self.history.pop()
                self.leActionString.setText(h)
                self.actionCommand = unicode(h, "utf-8")
                self.tbGoForward.setEnabled(True)
            else:
                self.tbGoBack.setEnabled(False)
        except:
            error = ReportBug.ReportBug()
            error.show()
            
    def goForward(self):
        try:
            if len(self.future)>0:
                future_temp=self.future.pop()
                if str(future_temp)[-2:].strip()==str(self.leSplitPointer.text()).strip():
                    self.numberOfActionCommand+=10
                    self.commaAndSplitControl = self.numberOfActionCommand
                    self.isPressedAddObjects=False
                elif str(future_temp)[-2:].strip()==",":
                    self.tbAddComma.setEnabled(False)
                    self.numberOfActionCommand+=100
                    self.commaAndSplitControl = self.numberOfActionCommand
                    self.isPressedAddObjects=False
                else: 
                    self.numberOfActionCommand+=1
                    self.isPressedAddObjects=True
                self.history.append(self.leActionString.text())
                self.leActionString.setText(future_temp)
                self.actionCommand = unicode(future_temp, "utf-8")
                self.tbGoBack.setEnabled(True)
            else:
                self.tbGoForward.setEnabled(False)
        except:
            error = ReportBug.ReportBug()
            error.show()
           
    def cbBookmarksChanged(self,_index):
        try:
            if _index>0:
                tempT = Databases.BookmarksOfSpecialTools.fetchAllByType()[_index-1][2]
                tempString = tempT.split(";")
                tempT = ""
                tempA = ""
                for t in tempString[:-2]:
                    tempT += t
                    tempA += t
                    for colNo, colName in enumerate(Universals.MainWindow.Table.tableColumnsKey):
                        tempT = tempT.replace(colName, str(Universals.MainWindow.Table.tableColumns[colNo]))
                self.history.append(self.leActionString.text())
                self.future=[]
                self.leActionString.setText(tempT.decode("utf-8"))
                self.actionCommand = tempA
                self.whereIsSplitPointer = tempString[-2]
                self.numberOfActionCommand = int(tempString[-1])
                self.commaAndSplitControl = self.numberOfActionCommand-1
                self.tbDeleteBookmark.setEnabled(True)
                self.isPressedAddObjects=True
                self.tbGoBack.setEnabled(True)
                self.tbGoForward.setEnabled(False)
                self.tbAddComma.setEnabled(False)
                self.details.setText(str(Organizer.whatDoesSpecialCommandDo(unicode(self.leSplitPointer.text()).encode("utf-8"),
                                    self.whereIsSplitPointer,
                                    self.actionCommand, 
                                    _isReturnDetails=True)).decode("utf-8"))
            else:
                self.whereIsSplitPointer, self.numberOfActionCommand, self.commaAndSplitControl, self.isPressedAddObjects="right",0,0, False
                self.leActionString.setText("")
                self.actionCommand = ""
                self.tbDeleteBookmark.setEnabled(False)
                self.tbAddComma.setEnabled(True)
                self.details.setText(translate("SpecialTools", "Please Select An Action!"))
        except:
            error = ReportBug.ReportBug()
            error.show()
        
    def addBookmark(self):
        try:
            tempString = self.actionCommand
            if Organizer.whatDoesSpecialCommandDo(unicode(self.leSplitPointer.text()).encode("utf-8"),self.whereIsSplitPointer,unicode(self.leActionString.text()).encode("utf-8"),True)==True:
                addition = " ;"+self.whereIsSplitPointer +";"+ str(self.numberOfActionCommand)
                Databases.BookmarksOfSpecialTools.insert("", tempString+addition)
                self.refreshBookmarks()
                self.cbBookmarks.setCurrentIndex(self.cbBookmarks.count()-1)
        except:
            error = ReportBug.ReportBug()
            error.show()
           
    def deleteBookmark(self):
        try:
            if self.cbBookmarks.currentIndex()!=-1 and self.cbBookmarks.currentIndex()!=0:
                Databases.BookmarksOfSpecialTools.delete(Databases.BookmarksOfSpecialTools.fetchAllByType()[self.cbBookmarks.currentIndex()-1][0])
                self.refreshBookmarks()
        except:
            error = ReportBug.ReportBug()
            error.show()
            
    def refreshBookmarks(self):
        try:
            self.cbBookmarks.clear()
            self.cbBookmarks.addItem(translate("SpecialTools", "Please Select An Action!"))
            for fav in Databases.BookmarksOfSpecialTools.fetchAllByType():
                self.cbBookmarks.addItem(fav[1].decode("utf-8"))
        except:
            error = ReportBug.ReportBug()
            error.show()
    
    def checkCompleters(self):
        pass
        
    def reFillCompleters(self):
        pass
    
                
class SearchAndReplace(MWidget):
    def __init__(self, _parent):
        MWidget.__init__(self, _parent)
        self.lblSearch=MLabel(translate("SpecialTools", "Search: "))
        self.lblReplace=MLabel(translate("SpecialTools", "Replace: "))
        self.leSearch = MLineEdit("")
        self.leReplace = MLineEdit("")
        lblColumns = MLabel(translate("SpecialTools", "Column: "))
        srExamples = translate("SpecialTools", "<table><tr><td><nobr>Before</nobr></td><td>>></td><td><nobr>Search</nobr></td><td>-</td><td><nobr>Replace</nobr></td><td>>></td><td><nobr>After</nobr></td></tr>" +
                                 "<tr><td><nobr>HamsiManager</nobr></td><td>>></td><td><nobr>ager</nobr></td><td>-</td><td><nobr></nobr></td><td>>></td><td><nobr>HamsiMan</nobr></td></tr>" +
                                 "</table><table>")
        sExample=translate("SpecialTools", "<tr><td><nobr>Example: \"search 1<b>;</b>search 2<b>;</b>search 3<b>;</b>...<b>;</b>search n<b>;</b>\"</nobr></td></tr>")
        rExample=translate("SpecialTools", "<tr><td><nobr>Example: \"Change/replace 1<b>;</b>Change/replace 2<b>;</b>Change/replace 3<b>;</b>...<b>;</b>Change/replace n<b>;</b>\"</nobr></td></tr>")
        self.cckbCaseSensitive = MCheckBox(translate("SpecialTools", "Case Insensitive"))
        self.cckbCaseSensitive.setChecked(True)
        self.cckbRegExp = MCheckBox(translate("SpecialTools", "Regular Expression (RegExp)"))
        self.leSearch.setToolTip(srExamples+sExample+"</table>".decode("utf-8"))
        self.leReplace.setToolTip(srExamples+rExample+"</table>".decode("utf-8"))
        self.columns = MComboBox()
        self.columns.addItem(translate("SpecialTools", "All"))
        self.pbtnEditValueForSearch = MPushButton(translate("Options", "*"))
        self.pbtnEditValueForSearch.setObjectName(translate("Options", "Edit Values With Advanced Value Editor") + "For Search".decode("utf-8"))
        self.pbtnEditValueForSearch.setToolTip(translate("Options", "Edit values with Advanced Value Editor"))
        self.pbtnEditValueForSearch.setFixedWidth(25)
        MObject.connect(self.pbtnEditValueForSearch, SIGNAL("clicked()"), self.pbtnEditValueClicked)
        self.pbtnEditValueForReplace = MPushButton(translate("Options", "*"))
        self.pbtnEditValueForReplace.setObjectName(translate("Options", "Edit Values With Advanced Value Editor") + "For Replace".decode("utf-8"))
        self.pbtnEditValueForReplace.setToolTip(translate("Options", "Edit values with Advanced Value Editor"))
        self.pbtnEditValueForReplace.setFixedWidth(25)
        MObject.connect(self.pbtnEditValueForReplace, SIGNAL("clicked()"), self.pbtnEditValueClicked)
        self.lblSearch.setFixedWidth(60)
        self.lblReplace.setFixedWidth(100)
        lblColumns.setFixedWidth(60)
        HBoxs = []
        HBoxs.append(MHBoxLayout())
        HBoxs[0].addWidget(self.lblSearch)
        HBoxs[0].addWidget(self.leSearch)
        HBoxs[0].addWidget(self.pbtnEditValueForSearch)
        HBoxs[0].addWidget(self.lblReplace)
        HBoxs[0].addWidget(self.leReplace)
        HBoxs[0].addWidget(self.pbtnEditValueForReplace)
        HBoxs.append(MHBoxLayout())
        HBoxs[1].addWidget(lblColumns)
        HBoxs[1].addWidget(self.columns)
        HBoxs[1].addStretch(2)
        HBoxs[1].addWidget(self.cckbCaseSensitive)
        HBoxs.append(MHBoxLayout())
        HBoxs[2].addStretch(3)
        HBoxs[2].addWidget(self.cckbRegExp)
        vblSearchAndReplace = MVBoxLayout()
        vblSearchAndReplace.addLayout(HBoxs[0])
        vblSearchAndReplace.addLayout(HBoxs[1])
        vblSearchAndReplace.addLayout(HBoxs[2])
        self.setLayout(vblSearchAndReplace)
            
    def showAdvancedSelections(self):
        self.cckbRegExp.show()
        self.pbtnEditValueForSearch.show()
        self.pbtnEditValueForReplace.show()
    
    def hideAdvancedSelections(self):
        self.cckbRegExp.hide()
        self.pbtnEditValueForSearch.hide()
        self.pbtnEditValueForReplace.hide()
        self.cckbRegExp.setChecked(False)
        
    def pbtnEditValueClicked(self):
        sarled = SearchAndReplaceListEditDialog(self)
    
    def checkCompleters(self):
        Databases.CompleterTable.insert(self.lblSearch.text(), self.leSearch.text())
        Databases.CompleterTable.insert(self.lblReplace.text(), self.leReplace.text())
    
    def reFillCompleters(self):
        setCompleter(self.leReplace, self.lblReplace.text())
        setCompleter(self.leSearch, self.lblSearch.text())
        

class Fill(MWidget):
    def __init__(self, _parent):
        MWidget.__init__(self, _parent)
        lblFillType = MLabel(translate("SpecialTools", "Content Type: "))
        self.cbFillType = MComboBox()
        self.cbFillType.addItems([translate("SpecialTools", "Text"),
                                translate("SpecialTools", "Number")])
        lblspCharNumberOfDigit = MLabel(translate("SpecialTools", "Number Of Characters: "))
        self.spCharNumberOfDigit = MSpinBox()
        self.spCharNumberOfDigit.setRange(1, 20)
        self.spCharNumberOfDigit.setValue(2) 
        self.columns = MComboBox()
        lblColumns = MLabel(translate("SpecialTools", "Column: "))
        lblColumns.setFixedWidth(60)
        self.lblFill = MLabel(translate("SpecialTools", "Text: "))
        self.lblFill.setFixedWidth(60)
        self.leFill = MLineEdit("")
        self.lblSort = MLabel(translate("SpecialTools", "Sort: "))
        self.lblSort.setFixedWidth(80)
        self.cbSort = MComboBox()
        self.cbSort.addItems([translate("SpecialTools", "Ascending"),
                            translate("SpecialTools", "Descending")])
        self.lblStartDigit = MLabel(translate("SpecialTools", "Begins With: "))
        self.lblStartDigit.setFixedWidth(120)
        self.spStartDigit = MSpinBox()
        self.spStartDigit.setRange(-999999, 999999)
        self.spStartDigit.setValue(0)
        self.spCharNumberOfDigit.setEnabled(False)
        self.cbSort.setEnabled(False)
        self.spStartDigit.setEnabled(False)
        HBoxs = []
        HBoxs.append(MHBoxLayout())
        HBoxs[0].addWidget(lblColumns)
        HBoxs[0].addWidget(self.columns)
        HBoxs[0].addWidget(lblFillType)
        HBoxs[0].addWidget(self.cbFillType)
        HBoxs.append(MHBoxLayout())
        HBoxs[1].addWidget(self.lblFill)
        HBoxs[1].addWidget(self.leFill)
        HBoxs[1].addWidget(lblspCharNumberOfDigit)
        HBoxs[1].addWidget(self.spCharNumberOfDigit)
        HBoxs.append(MHBoxLayout())
        HBoxs[2].addWidget(self.lblSort)
        HBoxs[2].addWidget(self.cbSort)
        HBoxs[2].addWidget(self.lblStartDigit)
        HBoxs[2].addWidget(self.spStartDigit)
        vblFill = MVBoxLayout()
        vblFill.addLayout(HBoxs[0])
        vblFill.addLayout(HBoxs[1])
        vblFill.addLayout(HBoxs[2])
        self.setLayout(vblFill)
        MObject.connect(self.columns, SIGNAL("currentIndexChanged(int)"), self.columnsChanged)
        MObject.connect(self.cbFillType, SIGNAL("currentIndexChanged(int)"), self.fillTypeChanged)
        
    def showAdvancedSelections(self):
        self.lblSort.show()
        self.cbSort.show()
        self.lblStartDigit.show()
        self.spStartDigit.show()
    
    def hideAdvancedSelections(self):
        self.cbSort.setCurrentIndex(0)
        self.spStartDigit.setValue(0)
        self.lblSort.hide()
        self.cbSort.hide()
        self.lblStartDigit.hide()
        self.spStartDigit.hide()
        
    def columnsChanged(self,_index):
        try:
            if unicode(self.columns.currentText()).encode("utf-8")=="Track No":
                self.cbFillType.setCurrentIndex(1)
                self.cbFillType.setEnabled(False)
                self.leFill.setEnabled(False)
                self.spCharNumberOfDigit.setEnabled(True)
            else:
                self.cbFillType.setCurrentIndex(0)
                self.cbFillType.setEnabled(True)
                self.leFill.setEnabled(True)
                self.spCharNumberOfDigit.setEnabled(False)
        except:
            error = ReportBug.ReportBug()
            error.show()
            
    def fillTypeChanged(self):
        if self.cbFillType.currentIndex()==1:
            self.leFill.setEnabled(False)
            self.spCharNumberOfDigit.setEnabled(True)
            self.cbSort.setEnabled(True)
            self.spStartDigit.setEnabled(True)
        else:
            self.leFill.setEnabled(True)
            self.spCharNumberOfDigit.setEnabled(False)
            self.cbSort.setEnabled(False)
            self.spStartDigit.setEnabled(False)
    
    def checkCompleters(self):
        Databases.CompleterTable.insert(self.lblFill.text(), self.leFill.text())
    
    def reFillCompleters(self):
        setCompleter(self.leFill, self.lblFill.text())
       
class Clear(MWidget):
    def __init__(self, _parent):
        MWidget.__init__(self, _parent)
        self.leClear = MLineEdit("")
        self.lblClear = MLabel(translate("SpecialTools", "Text: "))
        lblColumns = MLabel(translate("SpecialTools", "Column: "))
        lblClearType = MLabel(translate("SpecialTools", "Content Type: "))
        self.cbClearType = MComboBox()
        self.cbClearType.addItems([translate("SpecialTools", "All"),
                                translate("SpecialTools", "Letters"),
                                translate("SpecialTools", "Numbers"),
                                translate("SpecialTools", "Other Characters"),
                                translate("SpecialTools", "Selected Text")])
        self.columns = MComboBox()
        self.columns.addItem(translate("SpecialTools", "All"))
        self.cckbCaseSensitive = MCheckBox(translate("SpecialTools", "Case Insensitive"))
        self.cckbRegExp = MCheckBox(translate("SpecialTools", "Regular Expression (RegExp)"))
        self.cckbCaseSensitive.setChecked(True)
        HBoxs = []
        HBoxs.append(MHBoxLayout())
        HBoxs[0].addWidget(lblColumns)
        HBoxs[0].addWidget(self.columns)
        HBoxs[0].addWidget(lblClearType)
        HBoxs[0].addWidget(self.cbClearType)
        HBoxs.append(MHBoxLayout())
        HBoxs[1].addWidget(self.lblClear)
        HBoxs[1].addWidget(self.leClear)
        HBoxs[1].addWidget(self.cckbCaseSensitive)
        HBoxs.append(MHBoxLayout())
        HBoxs[2].addStretch(3)
        HBoxs[2].addWidget(self.cckbRegExp)
        vblClear = MVBoxLayout()
        vblClear.addLayout(HBoxs[0])
        vblClear.addLayout(HBoxs[1])
        vblClear.addLayout(HBoxs[2])
        self.setLayout(vblClear)
        self.cckbCaseSensitive.setEnabled(False)
        self.cckbRegExp.setEnabled(False)
        self.lblClear.setEnabled(False)
        self.leClear.setEnabled(False)
        lblColumns.setFixedWidth(60)
        self.lblClear.setFixedWidth(60)
        MObject.connect(self.cbClearType, SIGNAL("currentIndexChanged(int)"), self.clearTypeChanged)
        
    def clearTypeChanged(self):
        if self.cbClearType.currentIndex()!=4:
            self.cckbCaseSensitive.setEnabled(False)
            self.lblClear.setEnabled(False)
            self.leClear.setEnabled(False)
            self.cckbRegExp.setEnabled(False)
        else:
            self.cckbCaseSensitive.setEnabled(True)
            self.lblClear.setEnabled(True)
            self.leClear.setEnabled(True)
            self.cckbRegExp.setEnabled(True)
        
    def showAdvancedSelections(self):
        self.cckbRegExp.show()
    
    def hideAdvancedSelections(self):
        self.cckbRegExp.hide()
        self.cckbRegExp.setChecked(False)
    
    def checkCompleters(self):
        Databases.CompleterTable.insert(self.lblClear.text(), self.leClear.text())
    
    def reFillCompleters(self):
        setCompleter(self.leClear, self.lblClear.text())
            
class CharacterState(MWidget):
    def __init__(self, _parent):
        MWidget.__init__(self, _parent)
        self.leSearch = MLineEdit("")
        self.cckbCorrectText = MCheckBox(translate("SpecialTools", "Correct Text"))
        lblColumns = MLabel(translate("SpecialTools", "Column: "))
        lblCharacterType = MLabel(translate("SpecialTools", "Character Format: "))
        self.columns = MComboBox()
        self.cbCharacterType = MComboBox()
        self.cbCharacterType.addItems([translate("Options", "Title"), 
                            translate("Options", "All Small"), 
                            translate("Options", "All Caps"), 
                            translate("Options", "Sentence"), 
                            translate("Options", "Don`t Change")])
        self.cckbCaseSensitive = MCheckBox(translate("SpecialTools", "Case Insensitive"))
        self.cckbRegExp = MCheckBox(translate("SpecialTools", "Regular Expression (RegExp)"))
        HBoxs = []
        HBoxs.append(MHBoxLayout())
        HBoxs[0].addWidget(lblColumns)
        HBoxs[0].addWidget(self.columns)
        HBoxs[0].addWidget(lblCharacterType)
        HBoxs[0].addWidget(self.cbCharacterType)
        HBoxs.append(MHBoxLayout())
        HBoxs[1].addWidget(self.cckbCorrectText)
        HBoxs[1].addWidget(self.leSearch)
        HBoxs[1].addWidget(self.cckbCaseSensitive)
        HBoxs.append(MHBoxLayout())
        HBoxs[2].addStretch(3)
        HBoxs[2].addWidget(self.cckbRegExp)
        self.cckbCaseSensitive.setEnabled(False)
        self.cckbRegExp.setEnabled(False)
        self.leSearch.setEnabled(False)
        vblCharacterState = MVBoxLayout()
        vblCharacterState.addLayout(HBoxs[0])
        vblCharacterState.addLayout(HBoxs[1])
        vblCharacterState.addLayout(HBoxs[2])
        self.setLayout(vblCharacterState)
        lblColumns.setFixedWidth(60)
        MObject.connect(self.cckbCorrectText, SIGNAL("stateChanged(int)"), self.cckbCorrectTextChanged)
        
    def showAdvancedSelections(self):
        self.cckbRegExp.show()
    
    def hideAdvancedSelections(self):
        self.cckbRegExp.hide()
        self.cckbRegExp.setChecked(False)
        
    def cckbCorrectTextChanged(self, _value):
        if _value==2:
            self.cckbCaseSensitive.setEnabled(True)
            self.cckbRegExp.setEnabled(True)
            self.leSearch.setEnabled(True)
        else:
            self.cckbCaseSensitive.setEnabled(False)
            self.cckbRegExp.setEnabled(False)
            self.leSearch.setEnabled(False)
    
    def checkCompleters(self):
        Databases.CompleterTable.insert(self.cckbCorrectText.text(), self.leSearch.text())
    
    def reFillCompleters(self):
        setCompleter(self.leSearch, self.cckbCorrectText.text())
            
            
class SearchAndReplaceListEditDialog(MDialog):
    def __init__(self, _parent):
        MDialog.__init__(self, _parent)
        if Universals.isActivePyKDE4==True:
            self.setButtons(MDialog.None)
        self.setWindowTitle(translate("SearchAndReplaceListEditDialog", "Advanced Value Editor"))
        currentValueForSearch = str(self.parent().leSearch.text())
        currentValueForReplace = str(self.parent().leReplace.text())
        if Universals.isActivePyKDE4==True:
            self.EditorWidgetForSearch = MEditListBox(self)
            self.EditorWidgetForSearch.setItems([x.decode("utf-8") for x in currentValueForSearch.split(";")])
            self.EditorWidgetForReplace = MEditListBox(self)
            self.EditorWidgetForReplace.setItems([x.decode("utf-8") for x in currentValueForReplace.split(";")])
        else:
            self.EditorWidgetForSearch = MTextEdit(self)
            self.EditorWidgetForSearch.setText(currentValueForSearch.replace(";", "\n").decode("utf-8"))
            self.EditorWidgetForReplace = MTextEdit(self)
            self.EditorWidgetForReplace.setText(currentValueForReplace.replace(";", "\n").decode("utf-8"))
        pnlMain = MWidget(self)
        vblMain = MVBoxLayout(pnlMain)
        pbtnCancel = MPushButton(translate("SearchAndReplaceListEditDialog", "Cancel"))
        pbtnApply = MPushButton(translate("SearchAndReplaceListEditDialog", "Apply"))
        MObject.connect(pbtnCancel, SIGNAL("clicked()"), self.close)
        MObject.connect(pbtnApply, SIGNAL("clicked()"), self.apply)
        vblMain.addWidget(MLabel(translate("SearchAndReplaceListEditDialog", "Search List : ")))
        vblMain.addWidget(self.EditorWidgetForSearch)
        vblMain.addWidget(MLabel(translate("SearchAndReplaceListEditDialog", "Replace List : ")))
        vblMain.addWidget(self.EditorWidgetForReplace)
        hblBox = MHBoxLayout()
        hblBox.addWidget(pbtnApply)
        hblBox.addWidget(pbtnCancel)
        vblMain.addLayout(hblBox)
        if Universals.isActivePyKDE4==True:
            self.setMainWidget(pnlMain)
        else:
            self.setLayout(vblMain)
        self.setMinimumSize(550, 400)
        self.show()
        
    def apply(self):
        valueForSearch = ""
        valueForReplace = ""
        if Universals.isActivePyKDE4==True:
            for y, info in enumerate(self.EditorWidgetForSearch.items()):
                if y!=0:
                    valueForSearch += ";"
                valueForSearch += unicode(info, "utf-8")
            for y, info in enumerate(self.EditorWidgetForReplace.items()):
                if y!=0:
                    valueForReplace += ";"
                valueForReplace += unicode(info, "utf-8")
        else:
            valueForSearch = unicode(self.EditorWidgetForSearch.toPlainText(), "utf-8").replace("\n", ";")
            valueForReplace = unicode(self.EditorWidgetForReplace.toPlainText(), "utf-8").replace("\n", ";")
        self.parent().leSearch.setText(valueForSearch.decode("utf-8"))
        self.parent().leReplace.setText(valueForReplace.decode("utf-8"))
        self.close()
        
        
        
        