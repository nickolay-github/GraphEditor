import sys
import math
import operator
import main
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QAction, qApp, QSizePolicy, QSlider
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QIcon, QImage,QFont, QPen


from .NodeEdge import Node, Edge


class Canvas(QWidget):

    pt_radius = 3
    arrow_size_coef = 1.25
    delta_coef = 3 #for define active area around point

    def __init__(self, parent=None):
        super().__init__()
        
        self.setGeometry(0,0,400,400)
        self.nodes = []
        self.edges = {}
        self.drag_idx = []
        self.path_edges = []
        self.selected_node_idx = None
        self.mode = main.MainWindow.MODE_NODE
        self.cotrolPressed = False


    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawGraph(qp)
        qp.end()

    def __calculateTip(self, edge):
        vector = float(edge.v1.x - edge.v2.x), float(edge.v1.y - edge.v2.y)
        vector_length = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        vector_sized = vector[0] * 10 / vector_length, vector[1] * 10 / vector_length
    
        alpha = 30 * 2 * math.pi / 360
    
        sin_alpha = math.sin(alpha)
        cos_alpha = math.cos(alpha)
    
        tip1 = (vector_sized[0] * cos_alpha - vector_sized[1] * sin_alpha,
                vector_sized[0] * sin_alpha + vector_sized[1] * cos_alpha)
    
        sin_alpha = math.sin(-alpha)
        cos_alpha = math.cos(-alpha)
    
        tip2 = (vector_sized[0] * cos_alpha - vector_sized[1] * sin_alpha,
                vector_sized[0] * sin_alpha + vector_sized[1] * cos_alpha)
    
        return tip1, tip2

        
    def drawGraph(self, qp):
        qp.setPen(Qt.black)
        qp.setBrush(Qt.black)

        for i, node in enumerate(self.nodes):

            qpoint = QPoint(node.x, node.y)

            if i == self.selected_node_idx:
                qp.setBrush(Qt.red)
            elif i in self.drag_idx:
                qp.setBrush(Qt.blue)

            qp.drawEllipse(qpoint, self.pt_radius*2, self.pt_radius*2)

            qp.setBrush(Qt.black)
                
        for _, edges in self.edges.items():
            for edge in edges:
                dx = edge.v2.x - edge.v1.x
                dy = edge.v2.y - edge.v1.y
                weight = str(int(abs(edge)))
                qp.drawLine(edge.v1.x, edge.v1.y, edge.v2.x, edge.v2.y)
                font = QFont("Helvetica")
                font.setPixelSize(13.5)
                qp.setFont(font)
                qp.drawText(dx/2 + edge.v1.x, dy/2 + edge.v1.y, weight)
                if edge.direction:
                    qp.setPen(Qt.green)
                    tip = self.__calculateTip(edge)
                    coef = self.arrow_size_coef
                    qp.drawPolygon(QPoint(edge.v2.x, edge.v2.y),
                                       QPoint(edge.v2.x + coef*tip[0][0], edge.v2.y + coef*tip[0][1]),
                                       QPoint(edge.v2.x + coef*tip[1][0], edge.v2.y + coef*tip[1][1]))
                    qp.setPen(Qt.black)

        if self.path_edges:
            path_nodes = []
            for _ in self.path_edges:
                for node in self.nodes:
                    if _ == id(node):
                        path_nodes.append(node)
                
            for i in range(len(path_nodes)):
                if i == len(path_nodes)-1:
                    break
                qPen = QPen()
                qPen.setColor(Qt.yellow)
                qPen.setWidth(2)
                qp.setPen(qPen)
                qp.drawLine(path_nodes[i].x, path_nodes[i].y, path_nodes[i+1].x, path_nodes[i+1].y)
                qp.setPen(Qt.black)
                
            


    def _get_point(self, evt):
        return evt.pos().x(), evt.pos().y()


    def _focus_node(self, x, y):
        node = Node([x, y])
        distances = []
        for v in self.nodes:
            distances.append(math.sqrt(sum((i1 - i2)**2 for i1, i2 in zip(v, node))))
        if distances and (min(distances) < self.pt_radius + self.delta_coef):
            focused_node_idx = distances.index(min(distances))
            return focused_node_idx
        return None


    def addNode(self, x, y):
        new_node = Node([x, y])
        self.nodes.append(new_node)
        self.edges[id(new_node)] = []
        print(self.nodes)
        print(self.edges)
        return


    def deleteNode(self, node_idx):
        node = self.nodes[node_idx]
        print(node)
        for node_id, edges in self.edges.items():
            for i, edge in enumerate(edges):
                print("Incoming edges:")
                print(edge)
                if edge.v2 == node:
                    print("Deleting {}".format(edge))
                    del edges[i]
        print("Deleting outgoing edges")
        del self.edges[id(node)]
        print("Deleting node")
        del self.nodes[node_idx]


    def addEdge(self, v1_idx, v2_idx, directed=False):
        v1 = self.nodes[v1_idx]
        v2 = self.nodes[v2_idx]
        new_edge = Edge(v1, v2, directed)
        new_edge_back = Edge(v2, v1, directed)
        if not new_edge in self.edges[id(v1)] and not new_edge_back in self.edges[id(v2)]:
            self.edges[id(v1)].append(new_edge)
        return


    def grabNode(self, node_idx):
        self.path_edges = []
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ShiftModifier:

            print('Shift+MouseClick')
            if node_idx not in self.drag_idx:
                self.drag_idx.append(node_idx)
            else:
                self.drag_idx.remove(node_idx)

            self.cotrolPressed = True
            self.update()

        else:
            if self.cotrolPressed == True:
                if node_idx not in self.drag_idx:
                    self.drag_idx.append(node_idx)
                else:
                    self.drag_idx.remove(node_idx)
                    self.drag_idx.append(node_idx) # making sure the pointed node is the last in the indices list
                self.cotrolPressed = False
            else:
                self.drag_idx = [node_idx, ]

        print("$"*50)
        print(self.drag_idx)
        return

    def mousePressEvent(self, evt):

        if self.mode == main.MainWindow.MODE_NODE:
            
            self.path_edges = []
            if evt.button() == Qt.LeftButton:
                x, y = self._get_point(evt)
                focused_node_idx = self._focus_node(x, y)
                print(focused_node_idx)
                if not focused_node_idx is None:
                    self.grabNode(focused_node_idx)
                else:                    
                    self.addNode(x, y)
                    self.update()

        elif self.mode == main.MainWindow.MODE_EDGE:
    
            self.path_edges = []
            if evt.button() == Qt.LeftButton and self.drag_idx == []:
                x, y = self._get_point(evt)
                focused_node_idx = self._focus_node(x, y)
                if not focused_node_idx is None:
                    if self.selected_node_idx is None:
                        self.selected_node_idx = focused_node_idx
                        self.update()
                    else:
                        if self.selected_node_idx == focused_node_idx: # same node, deselect
                            self.selected_node_idx = None
                            self.update()
                        else:
                            self.addEdge(self.selected_node_idx, focused_node_idx)
                            self.selected_node_idx = None
                            self.update()

        elif self.mode == main.MainWindow.MODE_DIRECTED_EDGE:
            self.path_edges = []
            if evt.button() == Qt.LeftButton and self.drag_idx == []:
                x, y = self._get_point(evt)
                focused_node_idx = self._focus_node(x, y)
                if not focused_node_idx is None:
                    if self.selected_node_idx is None:
                        self.selected_node_idx = focused_node_idx
                        self.update()
                    else:
                        if self.selected_node_idx == focused_node_idx:
                            self.selected_node_idx = None
                            self.update()
                        else:
                            self.addEdge(self.selected_node_idx, focused_node_idx, directed=True)
                            self.selected_node_idx = None
                            self.update()

        elif self.mode == main.MainWindow.MODE_NODE_DEL:
            if evt.button() == Qt.LeftButton and self.drag_idx == []:
                x, y = self._get_point(evt)
                focused_node_idx = self._focus_node(x, y)

                if not focused_node_idx is None:
                    self.deleteNode(focused_node_idx)

                self.update()

        elif self.mode == main.MainWindow.MODE_PATH:
            if evt.button() == Qt.LeftButton and self.drag_idx == []:
                x, y = self._get_point(evt)
                focused_node_idx = self._focus_node(x, y)
                if not focused_node_idx is None:
                    if self.selected_node_idx is None:
                        self.selected_node_idx = focused_node_idx
                        self.update()
                    else:
                        if self.selected_node_idx == focused_node_idx: # same node
                            self.selected_node_idx = None
                            self.update()
                        else:
                            print("Selected")
                            print(self.selected_node_idx)
                            print(focused_node_idx)
                            distances, chain = self.dijkstra(self.selected_node_idx, focused_node_idx)
                            print("#"*30, " Dijkstra result ", "#"*30)
                            print(distances, chain)
                            self.selected_node_idx = None
                            self.update()


    def mouseMoveEvent(self, evt):
        if self.drag_idx != [] and not self.cotrolPressed:

            print(self.nodes)
            print(self.edges)
            print(self.drag_idx)

            moving_nodes = [self.nodes[i] for i in self.drag_idx]
            last_node = moving_nodes[-1]

            x, y = self._get_point(evt)

            x_delta = x - last_node.x
            y_delta = y - last_node.y

            for node in moving_nodes:
                node.x += x_delta
                node.y += y_delta

            self.update()


    def mouseReleaseEvent(self, evt):
        if evt.button() == Qt.LeftButton and not self.cotrolPressed and self.drag_idx != []:

            print('*'*40)
            print(self.nodes)
            print(self.edges)
            print(self.drag_idx)
            
            moving_nodes = [self.nodes[i] for i in self.drag_idx]
            last_node = moving_nodes[-1]

            x, y = self._get_point(evt)

            x_delta = x - last_node.x
            y_delta = y - last_node.y

            for node in moving_nodes:
                node.x += x_delta
                node.y += y_delta

            self.drag_idx = []
            self.update()


    def dijkstra(self, v1_idx, v2_idx, directed=True):
        
        
        v1 = self.nodes[v1_idx]
        v2 = self.nodes[v2_idx]
        
        
        dist = {}
        prev = {}
        q = {}
        visited = set()

        for v in self.nodes:
            dist[id(v)] = 999999999
            prev[id(v)] = -1
            q[id(v)] = v

        print(self.edges)
        print(v1)
        print(q)

        dist[id(v1)] = 0

        while len(visited) != len(q):

            #print('visited')
            #print(visited)

            temp_dict = {}
            for k,v in dist.items():
                if k not in visited:
                    temp_dict[k] = v
            i = min(temp_dict, key=temp_dict.get)

            print(i)
            visited.add(i)

            v = q[i]
            #print('Visiting {0!r}'.format(v))
            
            
            for e in self.edges[i]:
                if id(e.v2) in q and id(e.v2) not in visited:
                    alt = dist[i] + abs(e)
                    if alt < dist[id(e.v2)]:
                        dist[id(e.v2)] = alt
                        prev[id(e.v2)] = i

            print("*"*50)
            l = []
            l.append(id(v2))
            prev_id = prev[id(v2)]
            l.append(prev_id)
            while prev_id != -1:
                prev_id = prev[prev_id]
                if prev_id != -1 :
                    l.append(prev_id)
                    
            self.path_edges = l
            print(l)
        
        return dist, prev


