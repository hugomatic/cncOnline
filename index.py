#!/usr/bin/python

#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# You will find the latest version of this code at the following address:
# http://hugomatic.ca/source/cncOnline
#
# You can contact me at the following email address:
# hugo@hugomatic.ca
#


import os
import sys
import inspect
from xml.dom.minidom import parse

from hugomatic.toolkit import isWebApplication

def getGenerators():
    # these files aren't in the list
    doNotPublish = ['index.py']      # generates the list of generators
    f = inspect.getfile(getGenerators)
    d = os.path.dirname(f)
    if len(d)==0:
        d = "." # on Siteground hosting, d is empty
    allFiles =  os.listdir(d)
    files = []
    for f in allFiles:
        if f.endswith(".py"):
            if doNotPublish.__contains__(f) == False:
                files.append(f)
    files.sort()
    return files


dom = None
def getCatalogFileName():
    f = inspect.getfile(getCatalogFileName)
    tail,head = os.path.split(f)
    short_name = head.replace(".py",".xml")
    filename = tail + "/" + short_name
    return filename

def removeElement(dom, name):
    elements = dom.documentElement.getElementsByTagName(name)
    element = elements[0]
    selectionText = element.firstChild.nodeValue
    dom.documentElement.removeChild(element)

    
def loadCatalog():
    fileName = getCatalogFileName()
    dom = parse(fileName)
    
    selectionElements = dom.documentElement.getElementsByTagName('Selected')
    selectionElement = selectionElements[0]
    selectionText = selectionElement.firstChild.nodeValue
    removeElement(dom, 'Selected')
    gens = getGenerators()
    
    nodeList = dom.documentElement.getElementsByTagName('Catalog')
    catalogElement = nodeList[0]
    # add a node for every generator in the catalog section
    for generator in gens:
        e = dom.createElementNS(None,u'py')
        e.setAttributeNS('','name', generator )
        catalogElement.appendChild(e)
    return dom, selectionText

if isWebApplication():
    import hugomatic.web.index
    dom, selectionText = loadCatalog()
    header = """<h1>CNC Online</h1>
    <h2>Useful G-Code routines</h2>
    <p>Based on Hugomatic G-Code generators</p>
    """
    hugomatic.web.index.print_index(dom, header)
    sys.exit(2)
    
################################################
#
#
#
from Tkinter import *
from idlelib.TreeWidget import TreeItem, TreeNode



def saveCatalog(path):
    
    removeElement(dom,u'Catalog')
    catElement = dom.createElementNS(None,u'Catalog')
    
    selectedElement = dom.createElementNS(None,u'Selected')
    pathStr = u''
    for e in path:
        pathStr += e + u'/'
    pathStr = pathStr[0:-1]
        
    textNode = dom.createTextNode(pathStr)
    selectedElement.appendChild(textNode)
    dom.documentElement.appendChild(catElement)
    dom.documentElement.appendChild(selectedElement)
    f = open(getCatalogFileName(),'w')
    dom.writexml(f)    
    f.close()
    
def launchModule(module, path):
    saveCatalog(path)
    root.destroy()
    exec("import " + module)
    sys.exit()

def createCanvas(root):
     ## Grid sizing behavior in window
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    ## Canvas
    canvas = Canvas(root)
    canvas.grid(row=0, column=0, sticky='nswe')
    ## Scrollbars for canvas
    hScroll = Scrollbar(root, orient=HORIZONTAL, command=canvas.xview)
    hScroll.grid(row=1, column=0, sticky='we')
    vScroll = Scrollbar(root, orient=VERTICAL, command=canvas.yview)
    vScroll.grid(row=0, column=1, sticky='ns')
    canvas.configure(xscrollcommand=hScroll.set, yscrollcommand=vScroll.set)
    canvas.config(bg='white')
    ## Frame in canvas
    frm = Frame(canvas)
    ## This puts the frame in the canvas's scrollable zone
    canvas.create_window(0, 0, window=frm, anchor='nw')
    ## Frame contents
    return canvas

def get_name_from_xml_node(node):
    if node.nodeType == node.ELEMENT_NODE:
            s = node.nodeName
            a = node.getAttribute('name')
            if len(a) > 0:
                s = a
            return s
    elif node.nodeType == node.TEXT_NODE:
        return node.nodeValue

class DomTreeItem(TreeItem):
    def __init__(self, node):
        self.node = node
           
    def GetText(self):
        s = get_name_from_xml_node(self.node)
        return s
        
    def IsExpandable(self):
        node = self.node
        return node.hasChildNodes()
    
    def GetSubList(self):
        parent = self.node
        children = parent.childNodes
        prelist = [DomTreeItem(node) for node in children]
        itemlist = [item for item in prelist if item.GetText().strip()]
        
        return itemlist
    
    def _getPath(self):
        path = []
        path.append(self.GetText())
        node = self.node.parentNode
        while node != None:
            name = get_name_from_xml_node(node)
            path.insert(0,name)
            node = node.parentNode
        if len(path) >= 2:
            path = path[2:]
        return path
    
    def OnDoubleClick(self):
        text = self.GetText()
        icn =  self.GetIconName() 
        if icn == "python":
            module = text.replace(".py","")
            path = self._getPath()
            launchModule(module,path)
            
        #s = self.GetSelectedIconName()   
    def GetIconName(self):
        if not self.IsExpandable():
            return "python"
        return None

def selectNodeFromPath(parent, path):
    def getChild(node, name):
        children = node.children
        for child in children:
            txt = child.item.GetText()
            if name == txt:
                return child
        return None    
    node = parent
    for element in path:
        child = getChild(node, element)
        if child != None:
            node = child
            node.select()
            node.expand()
    return node    


## Main window
root = Tk()
canvas = createCanvas(root)



dom, selectionText = loadCatalog()
item = DomTreeItem(dom.documentElement)
node = TreeNode(canvas, None, item)
node.update()
node.expand()

#selectionText = selectionText.replace('"','')   
selection = selectionText.split("/")  # ("Projects","LED gizmo", "gizmoLed.py")
for i in range(len(selection)):
    s = selection[i].strip()
    selection[i] = s
    
selectNodeFromPath(node, selection)


root.mainloop() 

    
