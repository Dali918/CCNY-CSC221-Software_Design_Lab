import csv
import sys
import numpy as np
from PyQt6.QtCore import Qt, QPoint, QRect, QSize
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtWidgets import \
(
    QApplication, 
    QWidget,
    QMainWindow, 
    QListWidget, 
    QLabel, 
    QLayout, 
    QVBoxLayout, 
    QHBoxLayout,  
    QStackedLayout,
    QGridLayout,
    QSizePolicy,
    QPushButton
)

def read_csv(file_name):
    matrix = []
    with open(file_name, newline='') as csvfile:
        matrix_reader = csv.reader(csvfile, delimiter=',')
        for row in matrix_reader:
            matrix.append([num for num in row])
    return matrix


def recurse(curr_int, i, j, vector, cache, matrix):
    x, y = vector[0] + i, vector[1] + j
    if i < len(matrix) and j < len(matrix[0]) and j > -1 and matrix[i][j] == curr_int:
        if cache[i][j] > 0:
            return cache[i][j]
        cache[i][j] = 1 + recurse(curr_int, x, y, vector, cache, matrix)
        return cache[i][j]
    else:
        return 0

def max_directions(matrix, vector, row, col):

    cache = [[0 for j in range(col)] for i in range(row)]   #start with empty cache for storing directional length from position
    max = -1        #start with max being -1
    x, y = 0, 0
    for i in range(row):
        for j in range(col):
            curr_int = matrix[i][j]
            curr_max = recurse(curr_int, i, j, vector, cache, matrix)   #determine directional length from current index
            if curr_max > max:      #update current directional maximum and starting index
                x, y = i, j
                max = curr_max
   
    return x, y, max    #return starting index and step size

def solve_matrix(matrix):
    row, col = len(matrix), len(matrix[0])
    x,y,step = -1, -1, 0
    directions = [(0, 1), (1, 1), (1, 0), (1, -1)]
    longest = (0, 0)
    for i in range(len(directions)):
        """
        Get Starting position (x,y), and step size for each direction vector then determine which one has has the longest 
        """
        curr_x,curr_y,curr_step= max_directions(matrix, directions[i], row, col)
        if curr_step > step:
            x,y,step, longest = curr_x, curr_y, curr_step, directions[i]
    
    return x, y, step, longest      


def print_matrix(matrix):
    print(np.array(matrix))

def print_longest(matrix,x,y,step,longest):
    print_matrix(matrix)
    for i in range(step):
        matrix[x][y] = matrix[x][y] + '*'
        x += longest[0]
        y += longest[1]

    print_matrix(matrix)
    print( x,y,step, longest)   #helper function printing to terminal

class Color(QWidget):
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

class MainWindow(QMainWindow):
    def __init__(self,name,matrix):
        self.matrix = matrix
        super(MainWindow,self).__init__()
        self.grid_layout = self.create_matrix(self.matrix)
        self.grid_layout.setContentsMargins(0,0,0,0)
        
        self.grid_widget = QWidget()
        self.grid_widget.setLayout(self.grid_layout)
        self.button = QPushButton("Solve!")
        self.button.clicked.connect(self.solve)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.grid_widget)
        self.main_layout.addWidget(self.button)
        

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setWindowTitle(name)
        self.setMinimumWidth(300)
        self.setMinimumHeight(300)
        self.setCentralWidget(self.main_widget)

    def create_matrix(self,matrix):
        grid_layout = QGridLayout()
        grid_layout.setSpacing(2)
        grid_layout.setSpacing(0)

        for i in range(len(matrix)):
            for j in range(len(matrix[0])):

                widget = QLabel(matrix[i][j])
                widget.setStyleSheet("background-color: rgb(255,255,255); color: #22295F; margin:0.5; font-weight: bold")
                
                font = widget.font()
                font.setPointSize(12)
                widget.setFont(font)
                widget.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
                grid_layout.addWidget(widget, i, j)


        return grid_layout

    def solve(self):
        x, y, step, direction = solve_matrix(self.matrix)
        for i in range(step):
            widget =  self.grid_layout.itemAtPosition(x,y)
            widget = widget.widget()
            widget.setStyleSheet("background-color: yellow")

            x += direction[0]
            y += direction[1]

def main():
    # Command line args are in sys.argv[1], sys.argv[2] ...
    # sys.argv[0] is the script name itself and can be ignored
    csv_file = sys.argv[1]
    matrix = read_csv(csv_file)
    app = QApplication(sys.argv)
    app_name= "CSC221-HW4"
    window =MainWindow(app_name,matrix)
    window.show()
    app.exec()  


if __name__ == '__main__':
    main()
