## This file is part of HamsiManager.
##
## Copyright (c) 2010 - 2014 Murat Demir <mopened@gmail.com>
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

from Core import Organizer
import FileUtils as fu
import SearchEngines
from Core.MyObjects import *
from Details import MusicDetails
from Core import Universals as uni
from Core import Dialogs
import Taggers
from Core import Records
from Core import ReportBug
from Tables import CoreTable


class AmarokCopyTable(CoreTable):
    def __init__(self, *args, **kwargs):
        CoreTable.__init__(self, *args, **kwargs)
        from Amarok import Filter

        self.keyName = "amarokCopy"
        self.amarokFilterKeyName = "AmarokFilterAmarokCopyTable"
        self.hiddenTableColumnsSettingKey = "hiddenAmarokCopyTableColumns"
        self.refreshColumns()
        lblDestinationDir = MLabel(translate("AmarokCopyTable", "Destination Path : "))
        self.leDestinationDirPath = MLineEdit(fu.userDirectoryPath)
        self.pbtnSelectDestinationDir = MPushButton(translate("AmarokCopyTable", "Browse"))
        self.connect(self.pbtnSelectDestinationDir, SIGNAL("clicked()"), self.selectDestinationDir)
        self.wFilter = Filter.FilterWidget(self, self.amarokFilterKeyName)
        self.hblBox = MHBoxLayout()
        self.hblBox.addWidget(self.wFilter, 5)
        self.hblBox.addWidget(lblDestinationDir)
        self.hblBox.addWidget(self.leDestinationDirPath, 1)
        self.hblBox.addWidget(self.pbtnSelectDestinationDir)
        getMainWindow().MainLayout.addLayout(self.hblBox)
        pbtnVerifyTableValues = MPushButton(translate("AmarokCopyTable", "Verify Table"))
        pbtnVerifyTableValues.setMenu(SearchEngines.SearchEngines(self))
        self.mContextMenu.addMenu(SearchEngines.SearchEngines(self, True))
        self.isPlayNow = MToolButton()
        self.isPlayNow.setToolTip(translate("AmarokCopyTable", "Play Now"))
        self.isPlayNow.setIcon(MIcon("Images:playNow.png"))
        self.isPlayNow.setCheckable(True)
        self.isPlayNow.setAutoRaise(True)
        self.isPlayNow.setChecked(uni.getBoolValue("isPlayNow"))
        self.hblBox.insertWidget(self.hblBox.count() - 3, self.isPlayNow)
        self.hblBox.insertWidget(self.hblBox.count() - 1, pbtnVerifyTableValues)

    def writeContents(self):
        self.changedValueNumber = 0
        uni.startThreadAction()
        import Amarok

        allItemNumber = len(self.values)
        Dialogs.showState(translate("FileUtils/Musics", "Writing Music Tags"), 0, allItemNumber, True)
        for rowNo in range(self.rowCount()):
            isContinueThreadAction = uni.isContinueThreadAction()
            if isContinueThreadAction:
                try:
                    if self.isRowHidden(rowNo) == False:
                        baseNameOfDirectory = str(self.values[rowNo]["baseNameOfDirectory"])
                        baseName = str(self.values[rowNo]["baseName"])
                        if self.isChangeableItem(rowNo, 0, baseNameOfDirectory):
                            baseNameOfDirectory = str(self.item(rowNo, 0).text())
                            self.changedValueNumber += 1
                        if self.isChangeableItem(rowNo, 1, baseName, False):
                            baseName = str(self.item(rowNo, 1).text())
                            self.changedValueNumber += 1
                        newFilePath = fu.getRealPath(
                            fu.joinPath(str(self.leDestinationDirPath.text()), baseNameOfDirectory,
                                        baseName))
                        if fu.isFile(self.values[rowNo]["path"]) and fu.isReadableFileOrDir(
                            self.values[rowNo]["path"], False, True):
                            if fu.isWritableFileOrDir(newFilePath, False, True):
                                newFilePathCopied = fu.copyOrChange(self.values[rowNo]["path"],
                                                                    newFilePath)
                                if self.values[rowNo]["path"] != newFilePathCopied:
                                    newFilePath = newFilePathCopied
                                    try:
                                        if Amarok.getSelectedTagTargetType("AmarokCopyTable").find("ID3") > -1:
                                            typeTemp = Amarok.getSelectedTagTargetType("AmarokCopyTable").split(" + ")
                                            if len(typeTemp) > 1:
                                                taggerType = typeTemp[1]
                                            else:
                                                taggerType = typeTemp[0]
                                            Taggers.setSelectedTaggerTypeForWriteName(taggerType)
                                        tagger = Taggers.getTagger()
                                        tagger.loadFileForWrite(newFilePath)
                                        if self.isChangeableItem(rowNo, 2):
                                            value = str(self.item(rowNo, 2).text())
                                            tagger.setArtist(value)
                                            Records.add(str(translate("AmarokCopyTable", "Artist")),
                                                        str(self.values[rowNo]["artist"]),
                                                        value)
                                            self.changedValueNumber += 1
                                        if self.isChangeableItem(rowNo, 3):
                                            value = str(self.item(rowNo, 3).text())
                                            tagger.setTitle(value)
                                            Records.add(str(translate("AmarokCopyTable", "Title")),
                                                        str(self.values[rowNo]["title"]),
                                                        value)
                                            self.changedValueNumber += 1
                                        if self.isChangeableItem(rowNo, 4):
                                            value = str(self.item(rowNo, 4).text())
                                            tagger.setAlbum(value)
                                            Records.add(str(translate("AmarokCopyTable", "Album")),
                                                        str(self.values[rowNo]["album"]),
                                                        value)
                                            self.changedValueNumber += 1
                                        if self.isChangeableItem(rowNo, 5):
                                            value = str(self.item(rowNo, 5).text())
                                            tagger.setTrackNum(value)
                                            Records.add(str(translate("AmarokCopyTable", "Track No")),
                                                        str(self.values[rowNo]["trackNum"]),
                                                        value)
                                            self.changedValueNumber += 1
                                        if self.isChangeableItem(rowNo, 6):
                                            value = str(self.item(rowNo, 6).text())
                                            tagger.setDate(value)
                                            Records.add(str(translate("AmarokCopyTable", "Year")),
                                                        str(self.values[rowNo]["year"]), value)
                                            self.changedValueNumber += 1
                                        if self.isChangeableItem(rowNo, 7):
                                            value = str(self.item(rowNo, 7).text())
                                            tagger.setGenre(value)
                                            Records.add(str(translate("AmarokCopyTable", "Genre")),
                                                        str(self.values[rowNo]["genre"]),
                                                        value)
                                            self.changedValueNumber += 1
                                        if self.isChangeableItem(rowNo, 8):
                                            value = str(self.item(rowNo, 8).text())
                                            tagger.setFirstComment(value)
                                            Records.add(str(translate("AmarokCopyTable", "Comment")), str(
                                                self.values[rowNo]["firstComment"]), value)
                                            self.changedValueNumber += 1
                                        if self.tableColumnsKey.count("Lyrics") > 0 and self.isChangeableItem(rowNo, 9):
                                            value = str(self.item(rowNo, 9).text())
                                            tagger.setFirstLyrics(value)
                                            Records.add(str(translate("AmarokCopyTable", "Lyrics")),
                                                        str(self.values[rowNo]["firstLyrics"]),
                                                        value)
                                            self.changedValueNumber += 1
                                        tagger.update()
                                    except:
                                        Dialogs.showError(translate("AmarokCopyTable", "Tags Cannot Changed"),
                                                          str(translate("AmarokCopyTable",
                                                                        "\"%s\" : cannot be changed tags.")
                                                          ) % Organizer.getLink(newFilePath))
                except:
                    ReportBug.ReportBug()
            else:
                allItemNumber = rowNo + 1
            Dialogs.showState(translate("FileUtils/Musics", "Writing Music Tags"), rowNo + 1, allItemNumber, True)
            if isContinueThreadAction == False:
                break
        uni.finishThreadAction()
        return True

    def showTableDetails(self, _fileNo, _infoNo):
        MusicDetails.MusicDetails(self.values[_fileNo]["path"],
                                  uni.getBoolValue("isOpenDetailsInNewWindow"), self.isPlayNow.isChecked())

    def cellClickedTable(self, _row, _column):
        currentItem = self.currentItem()
        if currentItem is not None:
            cellLenght = len(currentItem.text()) * 8
            if cellLenght > self.columnWidth(_column):
                self.setColumnWidth(_column, cellLenght)
            if _column == 8 or _column == 9:
                if self.rowHeight(_row) < 150:
                    self.setRowHeight(_row, 150)
                if self.columnWidth(_column) < 250:
                    self.setColumnWidth(_column, 250)

    def cellDoubleClickedTable(self, _row, _column):
        try:
            if _column == 8 or _column == 9:
                self.showTableDetails(_row, _column)
            else:
                if uni.getBoolValue("isRunOnDoubleClick"):
                    self.showTableDetails(_row, _column)
        except:
            Dialogs.showError(translate("AmarokCopyTable", "Cannot Open Music File"),
                              str(translate("AmarokCopyTable",
                                            "\"%s\" : cannot be opened. Please make sure that you selected a music file.")
                              ) % Organizer.getLink(self.values[_row]["path"]))

    def refreshColumns(self):
        self.tableColumns = Taggers.getAvailableLabelsForTable()
        self.tableColumnsKey = Taggers.getAvailableKeysForTable()
        self.valueKeys = ["baseNameOfDirectory", "baseName", "artist", "title", "album",
                          "trackNum", "year", "genre", "firstComment", "firstLyrics"]

    def saveTable(self):
        MusicDetails.MusicDetails.closeAllMusicDialogs()
        self.checkFileExtensions(1, "baseName")
        return self.writeContents()

    def refreshTable(self, _path):
        self.values = []
        self.setColumnWidth(5, 70)
        self.setColumnWidth(6, 40)
        uni.startThreadAction()
        import Amarok

        Dialogs.showState(translate("AmarokCoverTable", "Checking For Amarok..."), 0, 2)
        if Amarok.checkAmarok():
            Dialogs.showState(translate("AmarokCoverTable", "Getting Values From Amarok"), 1, 2)
            isContinueThreadAction = uni.isContinueThreadAction()
            if isContinueThreadAction:
                from Amarok import Operations

                musicFileValuesWithNames = Operations.getAllMusicFileValuesWithNames(
                    uni.MySettings[self.amarokFilterKeyName])
                Dialogs.showState(translate("AmarokCoverTable", "Values Are Being Processed"), 2, 2)
                isContinueThreadAction = uni.isContinueThreadAction()
                if isContinueThreadAction:
                    if musicFileValuesWithNames != None:
                        allItemNumber = len(musicFileValuesWithNames)
                        self.setRowCount(allItemNumber)
                        rowNo = 0
                        for musicFileRow in musicFileValuesWithNames:
                            isContinueThreadAction = uni.isContinueThreadAction()
                            if isContinueThreadAction:
                                try:
                                    if fu.isFile(musicFileRow["filePath"]) and fu.isReadableFileOrDir(
                                        musicFileRow["filePath"], False, True):
                                        if Amarok.getSelectedTagSourseType("AmarokCopyTable") == "Amarok":
                                            content = {}
                                            content["path"] = musicFileRow["filePath"]
                                            content["baseNameOfDirectory"] = ""
                                            content["baseName"] = fu.getBaseName(musicFileRow["filePath"])
                                            content["artist"] = musicFileRow["artist"]
                                            content["title"] = musicFileRow["title"]
                                            content["album"] = musicFileRow["album"]
                                            content["trackNum"] = musicFileRow["tracknumber"]
                                            content["year"] = musicFileRow["year"]
                                            content["genre"] = musicFileRow["genre"]
                                            content["firstComment"] = musicFileRow["comment"]
                                            content["firstLyrics"] = musicFileRow["lyrics"]
                                            self.values.append(content)
                                        else:
                                            tagger = Taggers.getTagger()
                                            try:
                                                tagger.loadFile(musicFileRow["filePath"])
                                            except:
                                                Dialogs.showError(translate("FileUtils/Musics", "Incorrect Tag"),
                                                                  str(translate("FileUtils/Musics",
                                                                                "\"%s\" : this file has the incorrect tag so can't read tags.")
                                                                  ) % Organizer.getLink(musicFileRow["filePath"]))
                                            content = {}
                                            content["path"] = musicFileRow["filePath"]
                                            content["baseNameOfDirectory"] = ""
                                            content["baseName"] = fu.getBaseName(musicFileRow["filePath"])
                                            content["artist"] = tagger.getArtist()
                                            content["title"] = tagger.getTitle()
                                            content["album"] = tagger.getAlbum()
                                            content["trackNum"] = tagger.getTrackNum()
                                            content["year"] = tagger.getYear()
                                            content["genre"] = tagger.getGenre()
                                            content["firstComment"] = tagger.getFirstComment()
                                            content["firstLyrics"] = tagger.getFirstLyrics()
                                            self.values.append(content)

                                        newBaseNameOfDirectory = Organizer.emend(
                                            self.values[rowNo]["baseNameOfDirectory"], "directory")
                                        itemBaseNameOfDirectory = self.createTableWidgetItem(newBaseNameOfDirectory,
                                                                                             self.values[rowNo][
                                                                                                 "baseNameOfDirectory"])
                                        self.setItem(rowNo, 0, itemBaseNameOfDirectory)

                                        newBaseName = Organizer.emend(self.values[rowNo]["baseName"], "file")
                                        itemBaseName = self.createTableWidgetItem(newBaseName,
                                                                                  self.values[rowNo]["baseName"])
                                        self.setItem(rowNo, 1, itemBaseName)

                                        newArtist = Organizer.emend(self.values[rowNo]["artist"])
                                        itemArtist = self.createTableWidgetItem(newArtist, self.values[rowNo]["artist"])
                                        self.setItem(rowNo, 2, itemArtist)

                                        newTitle = Organizer.emend(self.values[rowNo]["title"])
                                        itemTitle = self.createTableWidgetItem(newTitle, self.values[rowNo]["title"])
                                        self.setItem(rowNo, 3, itemTitle)

                                        newAlbum = Organizer.emend(self.values[rowNo]["album"])
                                        itemAlbum = self.createTableWidgetItem(newAlbum, self.values[rowNo]["album"])
                                        self.setItem(rowNo, 4, itemAlbum)

                                        newTrackNum = str(self.values[rowNo]["trackNum"])
                                        itemTrackNum = self.createTableWidgetItem(newTrackNum,
                                                                                  self.values[rowNo]["trackNum"])
                                        self.setItem(rowNo, 5, itemTrackNum)

                                        newYear = Organizer.emend(self.values[rowNo]["year"])
                                        itemYear = self.createTableWidgetItem(newYear, self.values[rowNo]["year"])
                                        self.setItem(rowNo, 6, itemYear)

                                        newGenre = Organizer.emend(self.values[rowNo]["genre"])
                                        itemGenre = self.createTableWidgetItem(newGenre, self.values[rowNo]["genre"])
                                        self.setItem(rowNo, 7, itemGenre)

                                        newFirstComment = Organizer.emend(self.values[rowNo]["firstComment"])
                                        itemFirstComment = self.createTableWidgetItem(newFirstComment,
                                                                                      self.values[rowNo][
                                                                                          "firstComment"])
                                        self.setItem(rowNo, 8, itemFirstComment)

                                        newFirstLyrics = Organizer.emend(self.values[rowNo]["firstLyrics"])
                                        itemFirstLyrics = self.createTableWidgetItem(newFirstLyrics,
                                                                                     self.values[rowNo]["firstLyrics"])
                                        self.setItem(rowNo, 9, itemFirstLyrics)
                                except:
                                    ReportBug.ReportBug()
                                rowNo += 1
                            else:
                                allItemNumber = rowNo
                            Dialogs.showState(translate("Tables", "Generating Table..."), rowNo, allItemNumber, True)
                            if isContinueThreadAction == False:
                                break
        uni.finishThreadAction()
        self.setRowCount(len(self.values))  # In case of Non Readable Files and Canceled process

    def correctTable(self):
        for rowNo in range(self.rowCount()):
            for itemNo in range(self.columnCount()):
                if self.isChangeableItem(rowNo, itemNo):
                    if itemNo == 0:
                        newString = Organizer.emend(str(self.item(rowNo, itemNo).text()), "directory")
                    elif itemNo == 1:
                        newString = Organizer.emend(str(self.item(rowNo, itemNo).text()), "file")
                    else:
                        newString = Organizer.emend(str(self.item(rowNo, itemNo).text()))
                    self.item(rowNo, itemNo).setText(str(newString))

    def selectDestinationDir(self):
        try:
            destinationDirPath = Dialogs.getExistingDirectory(
                translate("AmarokCopyTable", "Please Select Destination Directory"), self.leDestinationDirPath.text(),
                0)
            if destinationDirPath is not None:
                self.leDestinationDirPath.setText(str(destinationDirPath))
        except:
            ReportBug.ReportBug()
