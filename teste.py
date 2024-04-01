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
        
        self.exit_shortcut = QShortcut(QKeySequence("Ctrl+C"), self) #Exit the GUI
        self.exit_shortcut.activated.connect(self.close)
        self.exit_shortcut.setEnabled(True)
        
        # Variable that makes sure Q were not pressed
        self.q_is_pressed = False
        
        # Variable that is True every time the user enters the block's explanation page
        self.block_page = False

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
        descriptionF = QFont("Arial", 18)
        descriptionF.setWeight(QFont.Bold)    

        # Explanation labels about the experiment
        explanation_part1 = QLabel('Nesse teste, você responderá a números e letras apertando apenas duas teclas (B ou N).\n\nVocê verá um quadrado dividido em quatro partes (quadrantes).\n\nA cada rodada, uma combinação de uma letra e um número (ex. D3) aparecerá em algum quadrante.\n\nSe a combinação aparecer nos quadrantes de cima, atente-se apenas à LETRA.\n\nSe a combinação aparecer nos quadrantes de baixo, atente-se apenas ao NÚMERO', self.central_widget)
        explanation_part2 = QLabel('O teste terá 3 blocos. Só letras, só números, e misto', self.central_widget)
        explanation_part3 = QLabel('Agora que sabe tudo que precisa para fazer o teste.\n\nTente responder rápido, e tente cometer poucos erros.\n\nPronto? Vamos começar usando só os quadrantes de cima, ou seja, só letras', self.central_widget)
        aux_list = [explanation_part1, explanation_part2, explanation_part3]
        
        for element in aux_list:    
            element.setGeometry(0, 0, self.screen_width, self.screen_height)
            element.setAlignment(Qt.AlignCenter)
            element.setFont(labelF)
            element.setStyleSheet("color: white;")
            element.setWordWrap(True)
            element.setHidden(True)
        del aux_list

        self.build_quadrants(600, 600) # Build the quadrants just to show as an example
        
        coment1 = QLabel('Se a combinação Letra/Número aparecer nos quadrantes de CIMA, responda sobre a LETRA. Se a combinação Letra/Número aparecer nos quadrantes de BAIXO, responda sobre o NÚMERO.' , self.central_widget)
        coment2 = QLabel('Aqui no caso, "5B" está na parte de cima, logo a resposta é baseada no "B" que é uma consoante. O correto seria apertar <b>N</b>' , self.central_widget)
        coment3 = QLabel('Aqui no caso, "8B" está na parte de baixo, logo a resposta é baseada no "8" que é um número par. O correto seria apertar <b>B</b>' , self.central_widget)
        aux_list = [coment1, coment2, coment3]
        
        for element in aux_list:
            element.setFixedSize(self.screen_width, 800)    
            element.move(0, self.quadrant_4.y() + self.quad_height)
            element.setMargin(20) 
            element.setAlignment(Qt.AlignHCenter)
            element.setHidden(True)
            element.setFont(labelF)
            element.setWordWrap(True)
            element.setStyleSheet("color: white;")
        del aux_list
            
        example_1 = QLabel("5 B", self.central_widget)
        example_2 = QLabel("8 B", self.central_widget)
        aux_list = [example_1, example_2]
        
        for element in aux_list:
            element.setAlignment(Qt.AlignCenter)
            element.setHidden(True)
            element.setFont(self.trialF)
        del aux_list
        
        example_1.setGeometry(self.quadrant_1.x(), self.quadrant_1.y(), self.quadrant_1.width(), self.quadrant_1.height())
        example_2.setGeometry(self.quadrant_4.x(), self.quadrant_4.y(), self.quadrant_4.width(), self.quadrant_4.height())
        
        how_to_next_page = QLabel('Aperte ESPAÇO para a próxima página', self.central_widget)
        how_to_finish_explanation = QLabel('Aperte ESPAÇO para rever a explicação \nAperte Q para iniciar o teste', self.central_widget)
        self.how_to_start_trials = QLabel('Aperte ESPAÇO para começar', self.central_widget)
        self.how_to_return = QLabel('Aperte ESPAÇO para continuar o teste \n(Ele vai começar no momento em que você apertar espaço)', self.central_widget)
        aux_list = [how_to_next_page, how_to_finish_explanation, self.how_to_start_trials, self.how_to_return]
        
        for element in aux_list:
            element.setGeometry(0, 0, self.screen_width, self.screen_height)
            element.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
            element.setHidden(True)
            element.setFont(next_pageF)
            element.setStyleSheet("color: white;")
        del aux_list
        how_to_finish_explanation.setStyleSheet("color: red")

        self.description1 = QLabel('LETRA:\n B: vogal, N: consoante', self.central_widget)
        self.description2 = QLabel('NÚMERO:\nB: par, N: ímpar', self.central_widget)
        aux_list = [self.description1, self.description2]
        
        for element in aux_list:
            element.setAlignment(Qt.AlignCenter)
            element.setFixedSize(300, self.quad_height)
            element.setMargin(20)
            element.setFont(descriptionF)
            element.setStyleSheet("color: white;")
            element.setHidden(True)
        del aux_list
        self.description1.move(self.quadrant_2.x() + self.quad_width, self.quadrant_2.y())
        self.description2.move(self.quadrant_3.x() + self.quad_width, self.quadrant_3.y())

        # Define the widgets that go inside each page
        second_page = list()
        third_page = list()
        fourth_page = list()
        
        for element in self.quadrants:
            second_page.append(element)
            third_page.append(element)
            fourth_page.append(element)
        second_page.extend([how_to_next_page, coment1, self.description1, self.description2])
        third_page.extend([example_1, how_to_next_page, coment2, self.description1, self.description2])
        fourth_page.extend([example_2, how_to_next_page, coment3, self.description1, self.description2])

        self.pages = [[explanation_part1 ,how_to_next_page], second_page, third_page, fourth_page, [explanation_part2, how_to_next_page], [explanation_part3, how_to_finish_explanation]]

        # Page index
        self.current_page = 0

        # Build the first page just to start the program
        for element in self.pages[self.current_page]:
            element.setHidden(False)
            
        block_B = QLabel('Bloco 2:\nSomente com os quadrantes de baixo, ou seja, só números\n\n(Lembrando)\nLETRA:\nB: vogal, N: consoante\n\nNÚMERO:\nB: par, N: ímpar', self.central_widget)
        block_C = QLabel('Bloco 3:\n Todos os quadrantes estarão funcionando\n\n(Lembrando)\nLETRA:\nB: vogal, N: consoante\n\nNÚMERO:\nB: par, N: ímpar', self.central_widget)
        self.block_labels = [block_B, block_C]
        for element in self.block_labels:
            element.setGeometry(0, 0, self.screen_width, self.screen_height)
            element.setAlignment(Qt.AlignCenter)
            element.setFont(labelF)
            element.setStyleSheet("color: white;")
            element.setWordWrap(True)
            element.setHidden(True)
        
        # Block index
        self.block_index = 0
        
                                        ###### Configuration of NL Test Parameters ######
            
        # Run the number_letter_task(), which is a thread defined in number_letter_task.py
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
        """
        # Define the dimensions of the figure area
        display_width = width
        display_height = height

        # Define the dimensions of the 4 quadrants(half the total figure area)
        self.quad_width = int(display_width/2)
        self.quad_height = int(display_height/2)

        # Center the figure
        display_x_pos = self.center_point.x() - self.quad_width
        display_y_pos = self.center_point.y() - self.quad_height

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
            element.setFixedSize(self.quad_width, self.quad_height)
            element.setAutoFillBackground(True)
            element.setPalette(palette)
            element.setHidden(True)
            outline = QFrame(element)
            outline.setGeometry(element.rect())
            outline.setFrameShape(QFrame.Box) 
            outline.setLineWidth(3)

        # Define each quadrant position
        self.quadrant_1.move(display_x_pos, display_y_pos)
        self.quadrant_2.move(display_x_pos + self.quad_width, display_y_pos)
        self.quadrant_3.move(display_x_pos + self.quad_width, display_y_pos + self.quad_height)
        self.quadrant_4.move(display_x_pos, display_y_pos + self.quad_height)
    
    def nl_test_builder(self, data, right_answer, block_indicators):
        """This function receives the signal "data" from the worker thread number_letter_task defined in number_letter_task.py. three lists are inside the siginal

        Args:
            data (list): trial_builder list from number_letter_task.py. NOTE: trial_builder is a method in this file, the list comes from another file
            right_answer (list): right_answers_nl_test list from number_letter_task.py
            block_indicators (list): Each block's index indicators
        """

        # Turn the lists from the signal into a variable inside this class
        self.right_answer = right_answer
        self.sorted_data = data
        self.block_indicators = block_indicators

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
        #exit the block's information page
        if self.block_page:
            
            # Desable space bar key
            self.spc_shortcut.setEnabled(False)
            
            # Enable "B" and "N" keys
            self.b_shortcut.setEnabled(True)
            self.n_shortcut.setEnabled(True)
            
            self.block_page = False
            
            # Clear the page
            self.block_labels[self.block_index].setHidden(True)
            self.how_to_return.setHidden(True)
            
            # Add one to block's index
            self.block_index += 1
            
            #show back the quadrants
            for element in self.quadrants:
                element.setHidden(False)
            
            # Build the next trial
            self.build_the_next_trial()
        
        # Press space so the first trial will begin 
        elif self.q_is_pressed: # so it will only work after you quit explanation screen
            time.sleep(0.2)

            # Activate "B" and "N" keys
            self.b_shortcut.setEnabled(True)
            self.n_shortcut.setEnabled(True)
            
            # Deletes unwanted widget
            self.how_to_start_trials.deleteLater()

            # Show the first trial label
            self.nl_test_labels[self.trial_index].setHidden(False)

            # Remove answer especification from the display
            self.description1.deleteLater()
            self.description2.deleteLater()
            
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
                if widget in [self.description1, self.description2]:
                    pass
                else:
                    widget.deleteLater()

        # Label that informs how to start the test
        self.how_to_start_trials.setHidden(False)

        # Show the number letter task quadrants
        for element in self.quadrants:
            element.setHidden(False)

        # Display answer especifications
        self.description1.setHidden(False)
        self.description2.setHidden(False)

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

        # Set the user's answer and check if it's right or wrong
        answer = ["EVEN", "VOWEL"]
        if self.right_answer[self.trial_index] in answer:
            self.got_right = True
        else:
            self.got_wrong = True
        
        # Method that evaluetes the answer
        self.trial_builder()
    
    def second_choice(self):
        """When enable, it receives a signal everytime N is pressed
        """
        # Store the computer time and remaining time in the timer then stop the timer
        self.remaining_time.append(self.answer_timer.remainingTime())
        self.answer_timer.stop()
        self.get_time()

        # Set the user's answer and check if it's right or wrong
        answer = ["ODD", "CONSONANT"]
        if self.right_answer[self.trial_index] in answer:
            self.got_right = True
        else:
            self.got_wrong = True

        # Method that evaluetes the answer
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

        # Evaluete the user's answer
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

            # Show block's explanation page
            if self.trial_index+1 in self.block_indicators:
                self.build_block_page()
            
            # Build the next trial
            else:
                self.build_the_next_trial()
        
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
        """ This funcion will receive a signal after wrong_timer reach timeout. It will clear the wrong answer message and build the next trial when the answer is wrong
        """
        # Stop the timer
        self.wrong_timer.stop()

        # Reactivate B and N keys
        self.n_shortcut.setEnabled(True)
        self.b_shortcut.setEnabled(True)

        # Hide the wrong answer message
        self.wrong_label.setHidden(True)
        
        # Show block's explanation page
        if self.trial_index+1 in self.block_indicators:
            self.build_block_page()
        
        # Build the next trial
        else:
            self.build_the_next_trial()
    
    def build_the_next_trial(self):
        """ It erases the label of the previous trial, shows the label of the current trial and starts the answer_timer
        """
        self.nl_test_labels[self.trial_index].deleteLater()
        if self.trial_index != len(self.nl_test_labels) - 1: # Stop when reach the last trial
            self.trial_index += 1
            self.nl_test_labels[self.trial_index].setHidden(False)

            # Start the timer for the answer once again
            self.answer_timer.start()

        # After last trial
        else:
            self.last_trial()
            
    def build_block_page(self):
        """ This function builds the page between blocks
        """
        self.block_page = True
                
        # Enable space bar key
        self.spc_shortcut.setEnabled(True)
        
        # Desable "B" and "N" keys
        self.b_shortcut.setEnabled(False)
        self.n_shortcut.setEnabled(False)
        
        # Clear page
        for element in self.quadrants:
            element.setHidden(True)
        self.nl_test_labels[self.trial_index].setHidden(True)
        
        # Show block's description
        self.block_labels[self.block_index].setHidden(False)
        self.how_to_return.setHidden(False)
        
    def get_time(self):
        """ Time structure that go inside the csv file
        """
        hour = datetime.datetime.now().hour
        minute = datetime.datetime.now().minute
        second = datetime.datetime.now().second
        microseconds = datetime.datetime.now().microsecond
        self.current_time.append(f'{hour}:{minute}:{second}.{microseconds}')
    
    def create_csv(self):
        """ It builds the csv file
        """
        hour = datetime.datetime.now().hour
        minute = datetime.datetime.now().minute
        second = datetime.datetime.now().second
        with open(f"{hour}_{minute}_{second}.csv", "w", newline="") as f:
            writer = csv.writer(f)
            
            # First row
            writer.writerow(['block', 'text', 'quadrant', 'latency_ms', 'response_time', 'correct_response', "user_response"])

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
