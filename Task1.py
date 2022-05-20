import wx
import numpy as np
from wx.lib.plot import PlotCanvas, PlotGraphics, PolyMarker

def checkFunction(function,minStr,maxStr):

    if (function == ""):
         return "Error: Empty expression"
    
    for character in function:
        if ( not( (character >="0" and character <="9") or character == '*' or 
                 character == '/' or character == '+' or character == '-' or 
                 character == '^' or character == "x") ):
            return "Error: Invalid expression"

    if (len(function) > 1 and (function[0] == '+' or function[0] == '-' or function[0] == '*' or
        function[0] == '/' or function[0] == '^') ):
        return "Error: Missing operand"
    
    if (len(function) > 1 and (function[len(function)-1] == '+' or function[len(function)-1] == '-' or
        function[len(function)-1] == '*' or function[len(function)-1] == '/' or
        function[len(function)-1] == '^')):
        return "Error: Missing operand"
    
    #Check for missing operands
    for i in range(len(function)-1):
        if (function[i] == '+' or function[i] == '-' or function[i] == '*' or
            function[i] == '/' or function[i] == '^'):
            if (function[i+1] == '+' or function[i+1] == '-' or function[i+1] == '*' or
                function[i+1] == '/' or function[i+1] == '^'):
                return "Error: Missing operand"
                
    for i in range(len(function)-1):
        if (function[i] == 'x'):
            if(function[i+1] >= '0' and function[i+1] <= '9'):
                return "Error: Missing operation"
        if(function[i] >= '0' and function[i] <= '9'):
            if(function[i+1] == 'x'):
                return "Error: Missing operation"

    if (minStr == "" or maxStr == ""):
        return "Error: Empty range"

    for character in minStr:
        if ( not( (character >="0" and character <="9") ) ):
            return "Error: Invalid minimum value"
    
    for character in maxStr:
        if ( not( (character >="0" and character <="9") ) ):
            return "Error: Invalid maximum value"
    
    if (int(minStr) > int(maxStr)):
        return "Error: Invalid range"

    return ""
            
def calculateFunction(function,minStr,maxStr):
    func =""
    minNum = int(minStr)
    maxNum = int(maxStr)
    x = np.linspace(minNum, maxNum, (maxNum-minNum)*50)
    
    for character in function:
        if character != '^':
            func+=character
        else:
            func+="**"
    y = eval(func)
    
    if type(y) != list:
        y = np.full(len(x),y)
    
    return y,x

def drawCurve(y,x):    
    merged_points = tuple(zip(x, y))
    #print(merged_points)
    marker = PolyMarker(merged_points, legend='F(x)', colour='green', marker='circle',size=1)
    return PlotGraphics( [marker] ,"Result", "X", "f(X)")


function = "function"

class MyFrame(wx.Frame):    
    
    def __init__(self):
        
        wx.Frame.__init__(self, None, wx.ID_ANY,'Function Plotter')
        # Add a panel so it looks the correct on all platforms
        panel = wx.Panel(self, wx.ID_ANY)
        
        # create some sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        checkSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        
        # create the widgets
        self.canvas = PlotCanvas(panel)
        #self.canvas.Draw(drawLinePlot())
        
        toggleGrid = wx.CheckBox(panel, label="Show Grid")
        toggleGrid.Bind(wx.EVT_CHECKBOX, self.onToggleGrid)
        
        toggleLegend = wx.CheckBox(panel, label="Show Legend")
        toggleLegend.Bind(wx.EVT_CHECKBOX, self.onToggleLegend)
        
        self.functionTextBox = wx.TextCtrl(panel)
        
        self.minTextBox = wx.TextCtrl(panel)
        
        self.maxTextBox = wx.TextCtrl(panel)
                      
        my_btn = wx.Button(panel, label='Plot')
        my_btn.Bind(wx.EVT_BUTTON, self.onPress)
        
        self.errorLabel = wx.StaticText(panel, label='')
        
        # layout the widgets
        mainSizer.Add(self.canvas, 1, wx.EXPAND)
        
        checkSizer.Add(toggleGrid, 0, wx.ALL, 5)
        
        checkSizer.Add(toggleLegend, 0, wx.ALL, 5)
        
        mainSizer.Add(self.functionTextBox, 0, wx.ALL | wx.EXPAND, 5)
        
        mainSizer.Add(self.minTextBox, 0, wx.ALL | wx.EXPAND, 5)
        
        mainSizer.Add(self.maxTextBox, 0, wx.ALL | wx.EXPAND, 5)
        
        mainSizer.Add(my_btn, 0, wx.ALL | wx.CENTER, 5)
        
        mainSizer.Add(checkSizer)
        
        panel.SetSizer(mainSizer)
        
        self.Show()

    #----------------------------------------------------------------------
    def onPress(self, event):
        
        function = self.functionTextBox.GetValue().lower()
        minStr = self.minTextBox.GetValue().lower()
        maxStr = self.maxTextBox.GetValue().lower()
        
        
        ErrMsg = checkFunction(function,minStr,maxStr)
        
        if ErrMsg == "":
            y,x = calculateFunction(function,minStr,maxStr)      
            self.canvas.Draw(drawCurve(y,x))
        else:
            self.errorLabel.SetLabel(ErrMsg)
            
    #----------------------------------------------------------------------
    def onToggleGrid(self, event):
        
        self.canvas.SetEnableGrid(event.IsChecked())
        
    #----------------------------------------------------------------------
    def onToggleLegend(self, event):
        
        self.canvas.SetEnableLegend(event.IsChecked())

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
