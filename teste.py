import sys
import time
import csv
from number_letter_task import number_letter_task
from PyQt5.QtGui import QFont, QColor, QPalette, QKeySequence
from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QLabel, QDesktopWidget, QFrame, QShortcut

class TestWindow(QMainWindow): 
    def __init__(self):
        super().__init__()
                                        ###### Variables ######

        #shortcuts key bindings
        self.spc_shortcut = QShortcut(QKeySequence("Space"), self)
        self.spc_shortcut.activated.connect(self.next_page)

        self.q_shortcut = QShortcut(QKeySequence("q"), self)
        self.q_shortcut.activated.connect(self.exit_explanation)

        self.b_shortcut = QShortcut(QKeySequence("b"), self)
        self.b_shortcut.activated.connect(self.first_choice)
        self.b_shortcut.setEnabled(False)

        self.n_shortcut = QShortcut(QKeySequence("n"), self)
        self.n_shortcut.activated.connect(self.second_choice)
        self.n_shortcut.setEnabled(False)
        
        # Variable that makes sure Q were not pressed
        self.q_is_pressed = False

        # Signal that start building the csv file with data
        self.finish_task = pyqtSignal()


                                        ###### Window Configuration ######
        # Name the new window
        self.setWindowTitle('Numer Letter Task')

        # Config the window size
        self.setGeometry(0, 0, 1200, 800)

        # Vertical layout
        self.layout = QVBoxLayout()

        # Define central widget
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        # Config the center point of the screen and move the main window to it
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        
                                        ###### Explanation Screen Configuration ######
        # Define the fonts size
        labelF = QFont("Arial", 28)
        next_pageF = QFont("Arial", 16)
        self.trialF = QFont("Arial", 40)
        descriptionF = QFont("Arial", 13)
        descriptionF.weight()
        descriptionF.setWeight(QFont.Bold)
        

        # Explanation labels about the experiment
        explanation_part1 = QLabel('Esse teste vai funcionar da seuginte maneira: \n\nA tela será dividida em 4 partes. Então, uma combinação de 1 letra e 1 número irá aparecer em uma dessas partes')
        explanation_part1.setAlignment(Qt.AlignHCenter)
        explanation_part1.setFont(labelF)
        explanation_part1.setWordWrap(True)

        explanation_part2 = QLabel('A intenção é que você preste atenção se a letra é uma vogal ou uma consoante e se o número é par ou ímpar')
        explanation_part2.setAlignment(Qt.AlignHCenter)
        explanation_part2.setFont(labelF)
        explanation_part2.setWordWrap(True)

        explanation_part3 = QLabel('A cada rodada do teste você terá 4 segundos para indicar a característica da letra OU do número dependendo de onde a combinação de letra e número aparecer')
        explanation_part3.setAlignment(Qt.AlignHCenter)
        explanation_part3.setFont(labelF)
        explanation_part3.setWordWrap(True)

        next_page_explanation = QLabel('Aperte ESPAÇO para a próxima página')
        next_page_explanation.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        next_page_explanation.setFont(next_pageF)

        finish_explanation = QLabel('Aperte ESPAÇO para retomar a explicação \nAperte Q para iniciar o teste')
        finish_explanation.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        finish_explanation.setFont(next_pageF)

        self.start_trials = QLabel('Aperte ESPAÇO para começar')
        self.start_trials.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        self.start_trials.setFont(next_pageF)

        self.description = QLabel('B: Par | Vogal\n\n\n\nN: Ímpar | Consoante', self.central_widget)
        self.description.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.description.setFixedSize(200, 200)
        self.description.setFont(descriptionF)
        self.description.setHidden(True)
        self.description.move(800, 300)

        # Define the widgets that go inside each page
        self.pages = [[explanation_part1 ,next_page_explanation], [explanation_part2, next_page_explanation], [explanation_part3, finish_explanation]]

        # Page index
        self.current_page = 0

        # Build the first page just to start the program
        for element in self.pages[self.current_page]:
            self.layout.addWidget(element)
        
                                        ###### Configuration of NL Test Parameters ######
            
        # Execute the number_letter_task(), which is a thread defined in number_letter_task.py
        self.nlt_thread = number_letter_task()
        self.nlt_thread.data.connect(self.nl_test_builder)
        self.nlt_thread.start()

        # Timer used to wait user's answer to each trial
        self.answer_timer = QTimer()
        self.how_much_time = 4000 # 4 seconds
        self.answer_timer.setInterval(self.how_much_time)  
        self.answer_timer.timeout.connect(self.on_timeout)

        # Timer used to stop the program when the user got the wrong answer
        self.wrong_timer = QTimer()
        self.wrong_timer.setInterval(3000)  # 3 seconds
        self.wrong_timer.timeout.connect(self.clear_wrong_label)

        # Variables that are involved in the number letter task implementation
        self.got_right = False # tell if the answer is right
        self.got_wrong = False # tell if the answer is wrong
        self.trial_index = 0 # tell the trial number, used to iterate through self.nl_test_labels 
        self.user_answers = list() # store all the user's answers
        self.nl_test_labels = list() # store all labels with (numer-letter) text. used to quickly turn on/off setHidden method 
        self.remaining_time = list() # store the remaining time of all user's answer, it will be 0 if the user don't answer anything

                                        ###### Number Letter Task Layout Configuration ######

        # Define the dimensions of figure area
        display_x_pos = 40
        display_y_pos = 100
        display_width = 600
        display_height = 600

        # Define the dimensions of the 4 quadrants(half the total figure area)
        quad_width = int(display_width/2)
        quad_height = int(display_height/2)

 
        # Define color variables
        color_1 = QColor(200, 200, 200)  # ligt grey

        # Palette object
        palette = QPalette()
        palette.setColor(QPalette.Background, color_1)


        # create four quadrants
        self.quadrant_1 = QLabel("", self.central_widget)
        self.quadrant_2 = QLabel("", self.central_widget)
        self.quadrant_3 = QLabel("", self.central_widget)
        self.quadrant_4 = QLabel("", self.central_widget)

        # Put all the quadrants in a list so it's easier to work with them        
        self.quadrants = [self.quadrant_1, self.quadrant_2, self.quadrant_3, self.quadrant_4]

        # Manipulate the quadrants
        for element in self.quadrants:
            element.setFixedSize(quad_width, quad_height)
            element.setAutoFillBackground(True)
            element.setPalette(palette)
            element.setHidden(True)
            outline = QFrame(element)
            outline.setGeometry(element.rect())
            outline.setFrameShape(QFrame.Box) 
            outline.setLineWidth(3)

        # Define each quadrant position
        self.quadrant_1.move(display_x_pos, display_y_pos)
        self.quadrant_2.move(display_x_pos + quad_width, display_y_pos)
        self.quadrant_3.move(display_x_pos + quad_width, display_y_pos + quad_height)
        self.quadrant_4.move(display_x_pos, display_y_pos + quad_height)

        # Wrong answer label
        self.wrong_label = QLabel('Resposta errada')
        self.wrong_label.setAlignment(Qt.AlignHCenter)
        self.wrong_label.setFont(labelF)
        self.wrong_label.setHidden(True)
        self.layout.addWidget(self.wrong_label)



                                        ###### Methods ######
    def nl_test_builder(self, data, right_answer):
        """This function receives the signal "data" from the worker thread number_letter_task defined in number_letter_task.py. Two lists are inside the siginal

        Args:
            data (list): trial_builder list from number_letter_task.py. NOTE: trial_builder is a method in this file, the list comes from another file
            right_answer (list): right_answers_nl_test list from number_letter_task.py.
        """

        # Turn the lists from the signal in a variable inside this class
        self.right_answer = right_answer
        self.sorted_data = data

        # It gets the text (numer-letter) sorted in the worker thread and put them all in labels
        for n in range(len(data)):
            information = f'{data[n]["number"]}{data[n]["letter"]}'
            label = QLabel(information, parent=self.central_widget)
            label.setFixedSize(self.quadrant_1.width(), self.quadrant_1.height()) # all the quadrants have the same size, so I picked any
            label.setAlignment(Qt.AlignCenter)
            label.setHidden(True)
            label.setFont(self.trialF)

            # Set the position of each label based on the quadrant
            if data[n]['quadrant'] == 0:
                label.move(self.quadrant_1.x(), self.quadrant_1.y())
            if data[n]['quadrant'] == 1:
                label.move(self.quadrant_2.x(), self.quadrant_2.y())
            if data[n]['quadrant'] == 2:
                label.move(self.quadrant_3.x(), self.quadrant_3.y())
            if data[n]['quadrant'] == 3:
                label.move(self.quadrant_4.x(), self.quadrant_4.y())

            # List where all the labels are stored
            self.nl_test_labels.append(label)

    def next_page(self):
        """
        When enable, it receives a signal everytime space bar is pressed
        """
        # Last time you will press space so the first trial will begin 
        if self.q_is_pressed: # so it will only work after you quit explanation screen
            time.sleep(0.2)

            # Activate "B" and "N" keys
            self.b_shortcut.setEnabled(True)
            self.n_shortcut.setEnabled(True)
            
            # Deletes unwanted widget
            self.start_trials.deleteLater()

            # Show the first trial label
            self.nl_test_labels[self.trial_index].setHidden(False)

            # Desable space bar key
            self.spc_shortcut.setEnabled(False)

            # Start the timer for the user to give an answer
            self.answer_timer.start()

        # Use space bar to get through explanation pages
        else:
            time.sleep(0.2)
            #Remove widgets associated with the previous page
            for element in self.pages[self.current_page]:
                self.layout.removeWidget(element)
                element.setHidden(True)
            
            #Add 1 to page index and start the couting again when finished
            self.current_page = (self.current_page + 1) % len(self.pages)

            #Add widgets associated with the next page
            for element in self.pages[self.current_page]:
                element.setHidden(False)
                self.layout.addWidget(element)

    def exit_explanation(self):
        """When enable, it receives a signal everytime Q is pressed
        """
        time.sleep(0.2)
        # Delete all widgets from explanation pages
        for page in self.pages:
            for widget in page:
                widget.deleteLater()

        
        # Label that informs how to start the test
        self.layout.addWidget(self.start_trials)

        # Show the number letter task quadrants
        for element in self.quadrants:
            element.setHidden(False)

        # Display answer especifications
        self.description.setHidden(False)

        # Desable Q key
        self.q_shortcut.setEnabled(False)
        
        # Varialble that tells if Q were pressed 
        self.q_is_pressed = True

    def first_choice(self):
        """When enable, it receives a signal everytime B is pressed
        """
        # Store the remaining time in the timer and stop it
        self.remaining_time.append(self.answer_timer.remainingTime())
        self.answer_timer.stop()

        # Set the user answer and check if it's right or wrong
        answer = ["EVEN", "VOWEL"]
        if self.right_answer[self.trial_index] in answer:
            self.got_right = True
        else:
            self.got_wrong = True
        
        # Method that compute the answer
        self.trial_builder()
    
    def second_choice(self):
        """When enable, it receives a signal everytime N is pressed
        """
        # Store the remaining time in the timer and stop it
        self.remaining_time.append(self.answer_timer.remainingTime())
        self.answer_timer.stop()

        # Set the user answer and check if it's right or wrong
        answer = ["ODD", "CONSONANT"]
        if self.right_answer[self.trial_index] in answer:
            self.got_right = True
        else:
            self.got_wrong = True

        # Method that compute the answer
        self.trial_builder()

    def last_trial(self):
        """ It will be called when the last trial was taken
        """
        # Disable B and N keys after the last trial
        self.b_shortcut.setEnabled(False)
        self.n_shortcut.setEnabled(False)
        
        # Delete last label
        self.nl_test_labels[self.trial_index].deleteLater()
        
        # Build the data file
        self.create_csv()
        app.quit()
    
    def on_timeout(self):
        """ This function will recieve a signal after answer_timer reach timeout
        """
        # Stop the timer
        self.answer_timer.stop()

        # Set the user's answer as wrong
        self.got_wrong = True

        # Compute the user's answer
        self.trial_builder()

        # Store the remaining time as 0
        self.remaining_time.append(0)

    def trial_builder(self):
        """ Store the user's answer and build the next trial
        """
        
        # If the answer is right
        if self.got_right:
            self.got_right = False
            self.user_answers.append("Correct")

            # Build the next trial
            self.nl_test_labels[self.trial_index].deleteLater()
            if self.trial_index != len(self.nl_test_labels) - 1: # Stop when reach the last trial
                self.trial_index += 1
                self.nl_test_labels[self.trial_index].setHidden(False)
                
                # Start the timer for the answer once again
                self.answer_timer.start()
            
            # After the last trial
            else:
                self.last_trial()

        
        # If the answer is wrong
        elif self.got_wrong:
            self.wrong_label.setHidden(False)
            self.got_wrong = False
            self.user_answers.append("Wrong")
            
            # Start a diferent timer that will send a signal to claear_wrong_label
            self.wrong_timer.start()

            # Disable B and N keys
            self.n_shortcut.setEnabled(False)
            self.b_shortcut.setEnabled(False)

    def clear_wrong_label(self):
        """ This funcion will receive a signal after wrong_timer reach timeout. Clear the wrong answer message and build the next trial when the answer is wrong
        """
        # Stop the timer
        self.wrong_timer.stop()

        # Reactivate B and N keys
        self.n_shortcut.setEnabled(True)
        self.b_shortcut.setEnabled(True)

        # Hide the wrong answer message and build the next tial
        self.wrong_label.setHidden(True)
        self.nl_test_labels[self.trial_index].deleteLater()
        if self.trial_index != len(self.nl_test_labels) - 1: # Stop when reach the last trial
            self.trial_index += 1
            self.nl_test_labels[self.trial_index].setHidden(False)

            # Start the timer for the answer once again
            self.answer_timer.start()

        # After last trial
        else:
            self.last_trial()

    def create_csv(self):
        with open("output.csv", "w", newline="") as f:
            writer = csv.writer(f)
            
            # First row
            writer.writerow(['Block', 'Text', 'Quadrant', 'Reaction Time (MS)', 'Right Answer', "User's result"])

            # Fill each row with data
            for data_dict, remaining_time, right_answer, result in zip(self.sorted_data, self.remaining_time, self.right_answer, self.user_answers):
                writer.writerow([
                data_dict["block"],
                f"{data_dict['number']}{data_dict['letter']}",
                data_dict["quadrant"],
                self.how_much_time - remaining_time,
                right_answer,
                result
                ])

        f.close()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_())

