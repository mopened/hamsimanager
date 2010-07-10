# -*- coding: utf-8 -*-
import os
import Universals
import Settings
from MyObjects import translate
pluginName = str(translate("MyPlugins/KDE4_SM", "For KDE4 Applications` Service Menus"))
pluginVersion = "0.1"
pluginFiles = ["HamsiManager_KDE4_SM.desktop", 
               "HamsiManager_KDE4_SM_Dir.desktop", 
               "HamsiManager_KDE4_SM_File.desktop"]
pluginDirectory = ""
installThisPlugin = None
setupDirectory = Universals.getKDE4HomePath() + "share/kde4/services/ServiceMenus"

def isInstallable():
    return Settings.isAvailablePyKDE4()
