import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent, QPainter, QPen, QPixmap, QPalette, QBrush, QColor, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QMessageBox


def generate_permutations(n:int, edges:list) -> list:
    def is_connected(graph, vertex1, vertex2):
        return (vertex1, vertex2) in graph or (vertex2, vertex1) in graph

    def backtrack(curr_permutation):
        if len(curr_permutation) == n+1:
            permutations.append(curr_permutation[:])
            return
        
        for num in range(1, n + 1):
            if num not in curr_permutation:
                if any(is_connected(edges, v, num) for v in curr_permutation):
                    curr_permutation.append(num)  
                    backtrack(curr_permutation) 
                    curr_permutation.pop() 

    permutations = []
    backtrack([0])
    return permutations

class GreetingWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(400, 300)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(255, 219, 88, 100))
        rect = self.rect()
        rect.setHeight(300)
        painter.drawRect(rect)
        painter.setPen(Qt.black)
        font = QFont("cleopatra", 20) 
        painter.setFont(font)
        painter.drawText(rect.translated(0, 40), Qt.AlignHCenter | Qt.AlignTop, "Привет, архитектор!")
        painter.drawText(rect.translated(0, 90), Qt.AlignHCenter | Qt.AlignTop, "Построй комнаты")


class GraphEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.vertices = []
        self.edges = []
        self.selected_vertex = None
        self.start_vertex = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.black, 2))
        
        for edge in self.edges:
            start_point = self.vertices[edge[0]]
            end_point = self.vertices[edge[1]]
            painter.drawLine(start_point, end_point)
            
        for index, vertex in enumerate(self.vertices):
            painter.setBrush(Qt.white)
            painter.setPen(QPen(Qt.black, 2))
            painter.drawEllipse(vertex, 15, 15)
            painter.drawText(vertex.x()-5, vertex.y()+1, str(index))


    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            for vertex in self.vertices:
                distance = (event.pos() - vertex).manhattanLength()
                if distance <= 10:
                    self.start_vertex = vertex
                    break
            else:
                self.vertices.append(event.pos())
                self.update()

        elif event.button() == Qt.RightButton:
            for vertex in self.vertices:
                distance = (event.pos() - vertex).manhattanLength()
                if distance <= 10:
                    self.vertices.remove(vertex)
                    self.edges = [edge for edge in self.edges if vertex not in edge]
                    self.update()
                    break

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() & Qt.LeftButton and self.start_vertex:
            self.selected_vertex = event.pos()
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton and self.start_vertex:
            for vertex in self.vertices:
                distance = (event.pos() - vertex).manhattanLength()
                if distance <= 10 and vertex != self.start_vertex:
                    self.edges.append((self.vertices.index(self.start_vertex), self.vertices.index(vertex)))
                    break
            self.selected_vertex = None
            self.start_vertex = None
            self.update()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Скрытые порядки строительства Казак Дура")
        self.setGeometry(100, 100, 800, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        greeting_widget = GreetingWidget()

        frame = QFrame()
        frame.setFrameShape(QFrame.Box) 
        frame.setFixedSize(350, 500)
        frame.setStyleSheet("QFrame { background-color: rgba(255, 219, 88, 100); border: 2px solid rgba(0, 0, 0, 100); }")  
    

        self.graph_editor = GraphEditor()
       
        main_layout.addWidget(greeting_widget)
        main_layout.addWidget(frame, alignment=Qt.AlignRight)
        frame_layout = QVBoxLayout(frame)
        frame_layout.addWidget(self.graph_editor)
        background_image = QPixmap("C:/Users/sibfl/OneDrive/Рабочий стол/спбгу/4 семестр/алгоритмы/4 лаба/phon1.png")
        if background_image.isNull():
            print("Ошибка загрузки изображения")
        else:
            palette = main_widget.palette()
            palette.setBrush(QPalette.Background, QBrush(background_image))
            main_widget.setPalette(palette)

        calculate_button = QPushButton("Найти все скрытые порядки", self)
        calculate_button.setFixedSize(350, 50)
        calculate_button.setFont(QFont("cleopatra", 14))
        calculate_button.move(35, 350)
        calculate_button.clicked.connect(self.calculate)
        main_widget.setAutoFillBackground(True)

            
    def calculate(self):
        edges = self.graph_editor.edges
        vertices_set = set()

        for tuple_item in edges:
            vertices_set.add(tuple_item[0])
            vertices_set.add(tuple_item[1])
        answer = generate_permutations(len(vertices_set)-1, edges)
        
        with open("hidden_orders.txt", "w") as file:
            for order in answer:
                file.write(" -> ".join(map(str, order)) + "\n")

        QMessageBox.information(self, "Готово", "Скрытые порядки были записаны в файл hidden_orders.txt")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
