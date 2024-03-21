import sys
import time
import datetime
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
        self.showFullScreen()

        # Vertical layout
        self.layout = QVBoxLayout()

        # Define central widget
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        # Define background color
        color = QColor(50 ,50, 50) # Blue
        pallete = QPalette()
        pallete.setColor(QPalette.Background, color)
        self.central_widget.setAutoFillBackground(True)
        self.central_widget.setPalette(pallete)

        # Config the center point of the screen
        self.center_point = QDesktopWidget().availableGeometry().center()
        self.screen_width = QDesktopWidget().availableGeometry().width()
        self.screen_height = QDesktopWidget().availableGeometry().height()

        
                                        ###### Explanation Screen Configuration ######
        # Define the fonts size
        labelF = QFont("Arial", 28)
        next_pageF = QFont("Arial", 16)
        self.trialF = QFont("Arial", 40)
        descriptionF = QFont("Arial", 13)
        descriptionF.setWeight(QFont.Bold)
        

        # Explanation labels about the experiment
        explanation_part1 = QLabel('Esse teste vai funcionar da seuguinte maneira: \n\nA tela será dividida em 4 partes. Então, uma combinação de 1 letra e 1 número irá aparecer em uma dessas partes', self.central_widget)
        explanation_part1.setGeometry(0, 0, self.screen_width, self.screen_height)
        explanation_part1.setAlignment(Qt.AlignCenter)
        explanation_part1.setFont(labelF)
        explanation_part1.setStyleSheet("color: white;")
        explanation_part1.setWordWrap(True)

        explanation_part2 = QLabel('A cada rodada do teste você terá 4 segundos para indicar a característica da letra OU do número dependendo de onde a combinação de letra e número aparecer', self.central_widget)
        explanation_part2.setGeometry(0, 0, self.screen_width, self.screen_height)
        explanation_part2.setAlignment(Qt.AlignCenter)
        explanation_part2.setHidden(True)
        explanation_part2.setFont(labelF)
        explanation_part2.setWordWrap(True)
        explanation_part2.setStyleSheet("color: white;")

        explanation_part3 = QLabel('A resposta vai ser recebida pelas teclas "B" e "N" do teclado. "B" indica par ou vogal, "N" indica ímpar ou consoante', self.central_widget)
        explanation_part3.setGeometry(0, 0, self.screen_width, self.screen_height)
        explanation_part3.setAlignment(Qt.AlignCenter)
        explanation_part3.setHidden(True)
        explanation_part3.setFont(labelF)
        explanation_part3.setWordWrap(True)
        explanation_part3.setStyleSheet("color: white;")

        explanation_part4 = QLabel('Quando o conjunto aparecer na parte de cima da figura você precisa responder com base na característica da letra(vogal ou consoante)', self.central_widget)
        explanation_part4.setGeometry(0, 0, self.screen_width, 200)
        explanation_part4.setAlignment(Qt.AlignCenter)
        explanation_part4.setHidden(True)
        explanation_part4.setFont(labelF)
        explanation_part4.setWordWrap(True)
        explanation_part4.setStyleSheet("color: white;")

        explanation_part5 = QLabel('Quando o conjunto aparecer na parte de baixo da figura você precisa responder com base na característica do número(par ou ímpar)', self.central_widget)
        explanation_part5.setGeometry(0, 0, self.screen_width, 200)
        explanation_part5.setAlignment(Qt.AlignCenter)
        explanation_part5.setHidden(True)
        explanation_part5.setFont(labelF)
        explanation_part5.setWordWrap(True)
        explanation_part5.setStyleSheet("color: white;")

        coment1 = QLabel('Aqui no caso, "3B" está na parte de cima, logo a resposta é baseada no "B" que é uma consoante' , self.central_widget)
        coment1.setFixedSize(400, self.screen_height)
        coment1.move(self.geometry().topRight().x() - (coment1.width() + 50), 0) 
        coment1.setAlignment(Qt.AlignCenter)
        coment1.setHidden(True)
        coment1.setFont(labelF)
        coment1.setWordWrap(True)
        coment1.setStyleSheet("color: white;")

        coment2 = QLabel('Aqui no caso, "8B" está na parte de baixo, logo a resposta é baseada no "8" que é um número par' , self.central_widget)
        coment2.setFixedSize(400, self.screen_height)
        coment2.move(self.geometry().topRight().x() - (coment2.width() + 50), 0)
        coment2.setAlignment(Qt.AlignCenter)
        coment2.setHidden(True)
        coment2.setFont(labelF)
        coment2.setWordWrap(True)
        coment2.setStyleSheet("color: white;")
        
        self.build_quadrants(600, 600) # Build the quadrants just to show as an example

        example_1 = QLabel("3 B", self.central_widget)
        example_1.setAlignment(Qt.AlignCenter)
        example_1.setGeometry(self.quadrant_2.x(), self.quadrant_2.y(), self.quadrant_2.width(), self.quadrant_2.height())
        example_1.setHidden(True)
        example_1.setFont(self.trialF)

        example_2 = QLabel("8 B", self.central_widget)
        example_2.setAlignment(Qt.AlignCenter)
        example_2.setGeometry(self.quadrant_3.x(), self.quadrant_3.y(), self.quadrant_3.width(), self.quadrant_3.height())
        example_2.setHidden(True)
        example_2.setFont(self.trialF)

        next_page_explanation = QLabel('Aperte ESPAÇO para a próxima página', self.central_widget)
        next_page_explanation.setGeometry(0, 0, self.screen_width, self.screen_height)
        next_page_explanation.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        next_page_explanation.setHidden(True)
        next_page_explanation.setFont(next_pageF)
        next_page_explanation.setStyleSheet("color: white;")

        finish_explanation = QLabel('Aperte ESPAÇO para retomar a explicação \nAperte Q para iniciar o teste', self.central_widget)
        finish_explanation.setGeometry(0, 0, self.screen_width, self.screen_height)
        finish_explanation.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        finish_explanation.setHidden(True)
        finish_explanation.setFont(next_pageF)
        finish_explanation.setStyleSheet("color: red;")

        self.start_trials = QLabel('Aperte ESPAÇO para começar', self.central_widget)
        self.start_trials.setGeometry(0, 0, self.screen_width, self.screen_height)
        self.start_trials.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        self.start_trials.setHidden(True)
        self.start_trials.setFont(next_pageF)
        self.start_trials.setStyleSheet("color: white;")

        self.description = QLabel('B: Par | Vogal\n\n\n\nN: Ímpar | Consoante', self.central_widget)
        self.description.setAlignment(Qt.AlignCenter)
        self.description.setFixedSize(400, self.screen_height)
        self.description.move(self.geometry().topRight().x() - (self.description.width() + 50), 0)
        self.description.setFont(descriptionF)
        self.description.setHidden(True)
        self.description.setStyleSheet("color: white;")

        # Define the widgets that go inside each page
        fourth_page = list()
        fifth_page = list()
        for element in self.quadrants:
            fourth_page.append(element)
            fifth_page.append(element)
        fourth_page.append(example_1)
        fourth_page.append(next_page_explanation)
        fourth_page.append(explanation_part4)
        fourth_page.append(coment1)
        fifth_page.append(example_2)
        fifth_page.append(finish_explanation)
        fifth_page.append(explanation_part5)
        fifth_page.append(coment2)

        self.pages = [[explanation_part1 ,next_page_explanation], [explanation_part2, next_page_explanation], [explanation_part3, next_page_explanation], fourth_page, fifth_page]

        # Page index
        self.current_page = 0

        # Build the first page just to start the program
        for element in self.pages[self.current_page]:
            element.setHidden(False)
        
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
        self.current_time = list() # store the current time when the user presses the button

                                        ###### Number Letter Task Layout Configuration ######

        # Build the four quadrants
        self.build_quadrants(600,600)

        # Wrong answer label
        self.wrong_label = QLabel('Resposta errada')
        self.wrong_label.setAlignment(Qt.AlignHCenter)
        self.wrong_label.setStyleSheet("color: red;")
        self.wrong_label.setFont(labelF)
        self.wrong_label.setHidden(True)
        self.layout.addWidget(self.wrong_label)

        # Final screen label
        self.final_screen = QLabel('Fim', self.central_widget)
        self.final_screen.setGeometry(0, 0, self.screen_width, self.screen_height)
        self.final_screen.setAlignment(Qt.AlignCenter)
        self.final_screen.setFont(QFont("Arial", 28))
        self.final_screen.setHidden(True)
        self.final_screen.setStyleSheet("color: white;")



                                        ###### Methods ######
    def build_quadrants(self, width:int, height:int):
        """Build the four quadrants

        Args:
            
        """
        # Define the dimensions of figure area
        display_width = width
        display_height = height

        # Define the dimensions of the 4 quadrants(half the total figure area)
        quad_width = int(display_width/2)
        quad_height = int(display_height/2)

        # Center the figure
        display_x_pos = self.center_point.x() - quad_width
        display_y_pos = self.center_point.y() - quad_height

 
        # Define color variables
        color_1 = QColor(191, 191, 191)  # ligt grey

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
            information = f'{data[n]["number"]} {data[n]["letter"]}'
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
                element.setHidden(True)
            
            #Add 1 to page index and start the couting again when finished
            self.current_page = (self.current_page + 1) % len(self.pages)

            #Add widgets associated with the next page
            for element in self.pages[self.current_page]:
                element.setHidden(False)

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
        # Store the computer time and remaining time in the timer then stop the timer
        self.remaining_time.append(self.answer_timer.remainingTime())
        self.answer_timer.stop()
        self.get_time()

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
        # Store the computer time and remaining time in the timer then stop the timer
        self.remaining_time.append(self.answer_timer.remainingTime())
        self.answer_timer.stop()
        self.get_time()

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
        
        # Delete last label and trial structure
        self.nl_test_labels[self.trial_index].deleteLater()
        for element in self.quadrants:
            element.deleteLater()
        self.description.deleteLater()

        
        # Build the data file
        self.create_csv()

        # Show the last screen
        self.final_screen.setHidden(False)
    
    def on_timeout(self):
        """ This function will recieve a signal after answer_timer reach timeout
        """
        # Stop the timer
        self.answer_timer.stop()

        # Store the computer time
        self.get_time()

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

    def get_time(self): 
        hour = datetime.datetime.now().hour
        minute = datetime.datetime.now().minute
        second = datetime.datetime.now().second
        microseconds = datetime.datetime.now().microsecond
        self.current_time.append(f'{hour}:{minute}:{second}.{microseconds}')
    
    def create_csv(self):
        hour = datetime.datetime.now().hour
        minute = datetime.datetime.now().minute
        second = datetime.datetime.now().second
        with open(f"{hour}_{minute}_{second}.csv", "w", newline="") as f:
            writer = csv.writer(f)
            
            # First row
            writer.writerow(['Block', 'Text', 'Quadrant', 'Reaction Time (MS)', 'Answer Time', 'Right Answer', "User's result"])

            # Fill each row with data
            for data_dict, remaining_time, right_answer, result, current_time in zip(self.sorted_data, self.remaining_time, self.right_answer, self.user_answers, self.current_time):
                writer.writerow([
                data_dict["block"],
                f"{data_dict['number']}{data_dict['letter']}",
                data_dict["quadrant"],
                self.how_much_time - remaining_time,
                current_time,
                right_answer,
                result
                ])

        f.close()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_())
