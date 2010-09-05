# -*- coding: utf-8 -*-
import json
import urllib
import subprocess

""" aur.py can be used to access the AUR API, combined with some pacman functions to check if there
are AUR updates 
"""

_aurApiBase = "http://aur.archlinux.org/rpc.php"

def _accessApi( urlArgs ):
    url = _aurApiBase + urlArgs
    
    try:
        f = urllib.urlopen(url)
    except IOError as e:
        print("Error: Cannot access the api at aur.archlinux.org:")
        print(e.args[0])
        f.close()
        raise
    info = json.loads(f.read().decode())
    if info["type"] == "error":
        return None
    return info["results"]
    
    
def _getForeignPackages():
    try:
        obj = subprocess.Popen(['pacman', '-Qm'], stdout=subprocess.PIPE)
        data = obj.communicate()[0].decode()
    except subprocess.CalledProcessError as e:
        print("Error: Could not execute pacman")
        raise
    dataList = data.strip().splitlines();
    for i in range(len(dataList)):
        dataList[i] = dataList[i].split()
    return dataList
    
    
def _isGreater( versionStr1, versionStr2 ):
    if versionStr1 != versionStr2:
        return True
    return False
# Need to to that a better way, see below for a first idea   
#    verList = []
#    for v in (versionStr1, versionStr2):
#        v = v.split('-')
#        s = []
#        for i in range(len(v)):
#            for l in v[i].split('.'):
#                s.append(l)
#        verList.append(s)
#    print(verList[0])
#    
#    ver2len = len(verList[1])-1
#    for i in range(len(verList[0])-1):
#        if i > ver2len:
#            return True
#        if verList[0][i] > verList[1][i]:
#            return True
#        if verList[0][i] < verList[1][i]:
#            return False
#    return False


def search( searchStr ):
    """searches the AUR
    
    Takes a search string as argument, returns a list of dictionaries,
    or None, if there are no results.
    If it fails to access the AUR, an IOError is risen.
    """
    return _accessApi("?type=search&arg={0}".format(searchStr))


def packageInfo( pkgName):
    """gets information about the AUR package
    
    pkgName is the exact name of the package. If there is no
    such package, the result is None, else a dictionary with information
    about this package.
    If it fails to access the AUR, an IOError is risen.
    """
    return _accessApi("?type=info&arg={0}".format(pkgName))
    
    
def aurUpdates():
    """searches for updates, packages out of date and unmaintained packages
    
    returns a list of updates, a list of packages out of date, a list of 
    packages not maintained any longer and a list of packages not found
    in aur. Every package is a tuple of the name, the installed version and,
    if it's available, the version in the aur.
    CalledProcessError for pacman-errors, IOError for AUR/internet errors
    """
    
    updateList = []
    notFoundList = []
    outOfDateList = []
    unmaintainedList = []
    packageList = _getForeignPackages()
    for p in packageList:
        aurdict = packageInfo(p[0])
        if aurdict == None:
            notFoundList.append(p[::])
            continue
        if _isGreater(aurdict["Version"], p[1]):
            updateList.append( (p[0], p[1], aurdict["Version"]) )
        if aurdict["OutOfDate"] == 1:
            outOfDateList.append(p[::])
    return updateList, outOfDateList, unmaintainedList, notFoundList



    
        