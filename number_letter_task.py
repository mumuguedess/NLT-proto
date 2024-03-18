import sys
import random
import asyncio
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QThread, pyqtSignal, QObject, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QLabel, QCheckBox, QDesktopWidget, QDialog, QMessageBox, QStatusBar, QLineEdit, QSpacerItem, QSizePolicy

class number_letter_task(QThread):
    # It sends information to build the nl test
    data = pyqtSignal(list, list)

    # Number of trials
    block_A_size = 10
    block_B_size = 10
    block_C_size = 10
    random_quadrants = True

    def __init__(self):
            '''
            Initialize the class variables
            '''
            super().__init__()

    
    def run(self):
        '''
        Function that are started when this WorkerThread are started

        This function calculate all the right answeres from the number_letter_task
        '''
        # Run the events
        loop = asyncio.new_event_loop()

        loop.run_until_complete(self.trials())

    async def trials(self):
        """Store all the right answers from the trials
        """
        #variable that will store all the sorted numbers, letters and quadrant
        trial_builder = list()

        #loop for sorting information in block A
        for n in range(self.block_A_size):
            number = random.randint(0, 9)
            letter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            quadrant = 0 if n % 2 == 0 else 1
            trial_builder.append({'number' : number, 'letter': letter, 'quadrant': quadrant, 'block': 'A'})

        #loop for sorting information in block B
        for n in range(self.block_B_size):
            number = random.randint(0, 9)
            letter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            quadrant = 2 if n % 2 == 0 else 3
            trial_builder.append({'number' : number, 'letter': letter, 'quadrant': quadrant, 'block': 'B'})
        
        #loop for sorting information in block C
        quadrants = [0, 1, 2, 3]
        for n in range(self.block_C_size):
            number = random.randint(0, 9)
            letter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            if self.random_quadrants:
                quadrant = random.randint(0, 3)
            else:
                quadrant = quadrants[n % len(quadrants)]

            trial_builder.append({'number' : number, 'letter': letter, 'quadrant': quadrant, 'block': 'C'})
        


        #variable that stores the right answers
        right_answers_nl_test = list()

        for trial in trial_builder:
            #upper quadrants where the answer is based on the letter
            if trial['quadrant'] == 0 or trial['quadrant'] == 1:
                #VOWELS
                if trial['letter'] in "AEIOU":
                    right_answers_nl_test.append("VOWEL")
                #CONSONANTS 
                else:
                    right_answers_nl_test.append("CONSONANT")
            
            #lower quadrants where the answer is based on the number
            else:
                #EVEN
                if trial['number'] % 2 == 0:
                    right_answers_nl_test.append("EVEN")
                #ODD
                if trial['number'] % 2 == 1:
                    right_answers_nl_test.append("ODD")

        
        self.data.emit(trial_builder, right_answers_nl_test)

                      
                  

