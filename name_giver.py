import sys
import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QFormLayout, QLabel, QLineEdit, QPushButton

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Window size
        self.setGeometry(100, 100, 300, 200)  # (x, y, width, height)
        self.setWindowTitle("Name Giver")

        # Layout type
        layout = QFormLayout()

        # Widgets elements
        self.code_label = QLabel("Código:")
        self.code_box = QLineEdit()
        layout.addRow(self.code_label, self.code_box)

        self.day_label = QLabel("Dia:")
        self.day_box = QLineEdit()
        layout.addRow(self.day_label, self.day_box)

        self.order_label = QLabel("Ordem:")
        self.order_box = QLineEdit()
        layout.addRow(self.order_label, self.order_box)

        self.file_button = QPushButton("Gerar nomes", self)
        self.file_button.clicked.connect(self.name_giver)
        layout.addRow(self.file_button)

        self.setLayout(layout)

    def name_giver(self):
        """Use the variables given from the user to build the file names that will be used in the experiment
        """
        self.code = self.code_box.text()
        self.exp_day = self.day_box.text()
        self.order = self.order_box.text()
        self.hour = datetime.datetime.now().hour
        self.minute = datetime.datetime.now().minute
        self.second = datetime.datetime.now().second
        self.day = datetime.datetime.now().day
        self.month = datetime.datetime.now().month 
        with open(f"{self.code}_document_names-{self.day}_{self.month}-{self.hour}_{self.minute}_{self.second}.csv.txt", 'w') as file:
            file.write(f'{self.code}_O{self.order}_pre_{self.exp_day}_htt\n\n')
            file.write(f'{self.code}_O{self.order}_pre_{self.exp_day}_nlt\n\n')
            file.write(f'{self.code}_O{self.order}_pre_{self.exp_day}_rest\n\n')
            file.write(f'{self.code}_O{self.order}_training_{self.exp_day}_calib\n\n')
            file.write(f'{self.code}_O{self.order}_training_{self.exp_day}_breath\n\n')
            file.write(f'{self.code}_O{self.order}_pos_{self.exp_day}_rest\n\n')
            file.write(f'{self.code}_O{self.order}_pos_{self.exp_day}_htt\n\n')
            file.write(f'{self.code}_O{self.order}_pos_{self.exp_day}_nlt\n\n')
        # Close the window
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
