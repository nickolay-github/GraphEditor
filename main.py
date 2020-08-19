import sys
import math
import operator

from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QAction, qApp, QSizePolicy, QSlider
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QIcon, QImage
from source import processing





class MainWindow(QMainWindow):
    MODE_NODE = 'N'
    MODE_NODE_DEL = 'D'
    MODE_EDGE = 'E'
    MODE_DIRECTED_EDGE = 'A'
    MODE_PATH = 'P'
    
    MSG_MODE_NODE = 'Add and move Node mode'
    MSG_MODE_NODE_DEL = 'Delete Node mode'
    MSG_MODE_EDGE = 'Add Edge mode'
    MSG_MODE_DIRECTED_EDGE = 'Add directed Edge mode'
    MSG_MODE_PATH = 'Minimal Path mode'
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
    
    def initUI(self):
        
        self.mode = self.MODE_NODE
        
        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('Draw a graph')
        
        self.canvas = processing.Canvas()
        self.setCentralWidget(self.canvas)
        
        exitAction = QAction(QIcon('images/exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(qApp.quit)
        
        insertNodeAction = QAction(QIcon('images/node.png'), 'Node', self)
        insertNodeAction.setShortcut('Ctrl+N')
        insertNodeAction.triggered.connect(self.nodeMode)
        
        addEdgeAction = QAction(QIcon('images/line.png'), 'Edge', self)
        addEdgeAction.setShortcut('Ctrl+E')
        addEdgeAction.triggered.connect(self.edgeMode)
        
        addDirectedEdgeAction = QAction(QIcon('images/arrow.png'), 'DirectedEdge', self)
        addDirectedEdgeAction.setShortcut('Ctrl+A')
        addDirectedEdgeAction.triggered.connect(self.directedEdgeMode)
        
        deleteNodeAction = QAction(QIcon('images/delete.png'), 'Delete', self)
        deleteNodeAction.setShortcut('Ctrl+D')
        deleteNodeAction.triggered.connect(self.deleteMode)
        
        findPathAction = QAction(QIcon('images/find.png'), 'Path', self)
        findPathAction.setShortcut('Ctrl+F')
        findPathAction.triggered.connect(self.findMode)
        
        self.statusBar()
        self.statusBar().showMessage(self.MSG_MODE_NODE)
        
        self.toolbar = self.addToolBar('Simple graph')
        
        self.toolbar.addAction(insertNodeAction)
        self.toolbar.addAction(addEdgeAction)
        self.toolbar.addAction(addDirectedEdgeAction)
        self.toolbar.addAction(deleteNodeAction)
        self.toolbar.addAction(findPathAction)
        
        sld = QSlider(Qt.Horizontal)
        sld.valueChanged.connect(self.nodeAndArrowResize)
        sld.setMinimum(3)
        sld.setMaximum(15)
        
        self.toolbar.addWidget(sld)
        
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.toolbar.addWidget(spacer)
        
        self.toolbar.addAction(exitAction)
        
        self.show()
    
    def nodeAndArrowResize(self, value):
        self.canvas.pt_radius = value
        if value > 5:
            self.canvas.arrow_size_coef = 0.3 * value
        else:
            self.canvas.arrow_size_coef = 1.25
        self.canvas.update()
    
    def nodeMode(self):
        self.canvas.mode = self.MODE_NODE
        self.selected_node_idx = None
        self.draggin_idx = []
        self.statusBar().showMessage(self.MSG_MODE_NODE)
    
    def deleteMode(self):
        self.canvas.mode = self.MODE_NODE_DEL
        self.selected_node_idx = None
        self.draggin_idx = []
        self.statusBar().showMessage(self.MSG_MODE_NODE_DEL)
    
    def edgeMode(self):
        self.canvas.mode = self.MODE_EDGE
        self.selected_node_idx = None
        self.draggin_idx = []
        self.statusBar().showMessage(self.MSG_MODE_EDGE)
    
    def directedEdgeMode(self):
        self.canvas.mode = self.MODE_DIRECTED_EDGE
        self.selected_node_idx = None
        self.draggin_idx = []
        self.statusBar().showMessage(self.MSG_MODE_DIRECTED_EDGE)
    
    def findMode(self):
        self.canvas.mode = self.MODE_PATH
        self.selected_node_idx = None
        self.draggin_idx = []
        self.statusBar().showMessage(self.MSG_MODE_PATH)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
