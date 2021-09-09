class MatrixTable(object):
    def __init__(self, width_window, height_window):
        self.width_window = int(width_window / 15)
        self.height_window = int(height_window / 15)

    def make_matrix(self):
        matrix = self.height_window * [self.width_window * [0]]
        return matrix
