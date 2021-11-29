from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import * # 이미지 설정을 위한 것
from gameLogic import *
import questionData
from collections import Counter

class StartWindow( QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(500, 200, 600, 600)
        back_palette = QPalette()
        back_palette.setBrush(QPalette.Background, QBrush(QPixmap("./game_Images/background.jpg")))
        self.setPalette(back_palette)

        self.initUI()

    def initUI(self):

        startLayout = QVBoxLayout()

        # game character
        character = QLabel()
        boss_character = QPixmap("./game_Images/guessing2.png")
        boss_character = boss_character.scaledToWidth(400)
        character.setPixmap(boss_character)
        character.setAlignment((Qt.AlignHCenter))

        # game title label
        self.titleLabel = QLabel("GUESS WHO?")
        self.titleLabel.setAlignment(Qt.AlignHCenter)
        font = self.titleLabel.font()
        font.setFamily('Courier New')
        font.setBold(True)
        font.setPointSize(35)
        self.titleLabel.setFont(font)

        # start Button
        self.startButton = QToolButton()
        self.startButton.setText("START!")
        self.startButton.clicked.connect(self.openGameWindow)
        self.startButton.setMinimumSize(200, 50)

        # add Data Button
        self.addDataButton = QToolButton()
        self.addDataButton.setText("ADD Data")
        self.addDataButton.clicked.connect(self.openDataWindow)
        self.addDataButton.setMinimumSize(200, 50)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.startButton)
        buttonLayout.addWidget(self.addDataButton)

        # Set Layout
        startLayout.addWidget(self.titleLabel)
        startLayout.addWidget(character)
        startLayout.addLayout(buttonLayout)
        startLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(startLayout)
        self.setWindowTitle('Guess Who??')

    def openGameWindow(self):
        self.hide()
        openGame = GameWindow()
        openGame.exec_()
        self.show()

    def openDataWindow(self):
        self.hide()
        openData = DataWindow()
        openData.exec_()
        self.show()

class GameWindow(QDialog,QWidget):

    def __init__(self):
        super().__init__()
        self.setGeometry(500, 200, 600, 300)
        self.initUI()
        self.show()

    # game 진행 중에 보여줄 window
    def initUI(self):

        back_palette = QPalette()
        back_palette.setBrush(QPalette.Background, QBrush(QPixmap("./game_Images/background.jpg")))
        self.setPalette(back_palette)

        # question display label
        self.questionWindow = QTextEdit()
        self.questionWindow.setSizePolicy(200,100)
        self.questionWindow.setAlignment(Qt.AlignCenter)
        self.questionWindow.setReadOnly(True)

        self.questfont = self.questionWindow.font()
        self.questfont.setFamily('Courier New')
        self.questfont.setBold(True)
        self.questfont.setPointSize(12)
        self.questionWindow.setFont(self.questfont)

        #Layout
        questionLayout = QVBoxLayout()
        questionLayout.addWidget(self.questionWindow)

        #answer Button
        buttonLayout = QGridLayout()

        self.yesButton = QToolButton()
        self.yesButton.setText("Yes")
        self.yesButton.clicked.connect(self.dealUserAnswer)
        self.yesButton.setMinimumSize(100,50)
        buttonLayout.addWidget(self.yesButton, 0, 0)

        self.noButton = QToolButton()
        self.noButton.setText("No")
        self.noButton.clicked.connect(self.dealUserAnswer)
        self.noButton.setMinimumSize(100,50)
        buttonLayout.addWidget(self.noButton, 0, 1)

        #additonal function

        # game character
        character = QLabel()
        boss_character = QPixmap("./game_Images/guessing.png")
        boss_character = boss_character.scaledToWidth(400)
        character.setMaximumSize(250,400)
        character.setPixmap(boss_character)
        character.setAlignment((Qt.AlignHCenter))

        # answer label
        self.answerLabel = QLabel()
        self.answerLabel.setAlignment(Qt.AlignCenter)
        font = self.answerLabel.font()
        font.setFamily('Courier New')
        font.setBold(True)
        font.setPointSize(30)
        self.answerLabel.setFont(font)

        # back home Window Button
        self.homeButton= QToolButton()
        self.homeButton.setArrowType(Qt.LeftArrow)
        self.homeButton.clicked.connect(self.home)

        # window Layout
        mainLayout = QGridLayout()
        mainLayout.addLayout(questionLayout, 0, 0)
        mainLayout.addLayout(buttonLayout, 1, 0)
        mainLayout.addWidget(self.answerLabel, 2, 0)
        mainLayout.addWidget(self.homeButton, 3, 0)
        mainLayout.addWidget(character, 0, 1, 3, 1)

        mainLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(mainLayout)
        self.setWindowTitle('Guess Who??')

        self.startGame()

    def startGame(self):
        # button rest
        self.noButton.show()
        self.yesButton.show()
        # value reset
        self.user_answers = []
        self.data_subsets = questionData.dataset
        self.result_subsets = questionData.data_result
        self.game = decisionTreeOperation()
        self.best_gain = 1
        self.guess()

    # 사용자에게 질문을 선정해서 보여줌
    def printQuestion(self):
        self.best_gain, self.best_question = self.game.findBestSplit(self.data_subsets, self.result_subsets)
        self.questionWindow.setText( "Q. " + questionData.questions[self.best_question])

    # 사용자의 답변을 받아서 처리
    def dealUserAnswer(self):
        if self.sender() == self.yesButton:
            self.user_answer = 1
        elif self.sender() == self.noButton:
            self.user_answer = 0

        self.user_answers.append(self.user_answer)
        self.guess()

    # 사용자에게  입력을 받아 입력값을 기준으로 처리
    def guess(self):
        if len(self.user_answers) == 0:
            self.printQuestion()

        else:
            # guessing
            if self.best_gain != 0:
                self.data_subsets, self.result_subsets = self.game.split(self.data_subsets, self.result_subsets,
                                                                         self.best_question, self.user_answer)
            # guess 끝
            else:
                answer = questionData.people_name[list(Counter(self.result_subsets))[0]]
                self.questionWindow.setText(""" 당신이 생각하고 있는 \n 스우파 멤버는 바로!! """)
                self.questfont.setPointSize(17)
                self.questionWindow.setFont(self.questfont)
                self.noButton.hide()
                self.yesButton.hide()
                self.answerLabel.setText(answer)
                return

            self.printQuestion()

    def home(self):
        self.close()

# 학습 데이터를 저장하기 위한 UI
class DataWindow(QDialog, QWidget):
    def __init__(self):
        super().__init__()
        # value reset
        self.questions= questionData.questions
        self.dancerName = questionData.people_name
        self.dataset = questionData.dataset
        self.counter = 0
        self.user_answers = []

        self.initUI()
        self.show()

    def initUI(self):
        self.setGeometry(500, 200, 600, 300)
        self.setWindowTitle('ADD DATA')
        back_palette = QPalette()
        back_palette.setBrush(QPalette.Background, QBrush(QPixmap("./game_Images/background.jpg")))
        self.setPalette(back_palette)

        # first question label
        self.nameText = QTextEdit("Q. 아이키, 효진초이, 리정, 가비, 모니카, 노제, 리헤이, 허니제이 중 제일 좋아하는 멤버의 이름을 적어주세요.")
        self.nameText.setMaximumSize(600,100)
        self.nameText.setReadOnly(True)
        font = self.nameText.font()
        font.setFamily('Courier New')
        font.setPointSize(13)
        self.nameText.setFont(font)

        # favorit member name
        self.nameInput = QLineEdit()
        self.nameInput.setPlaceholderText("Write Name")

        # questions Text
        self.questionLabel = QTextEdit()
        self.questionLabel.setReadOnly(True)
        self.questionLabel.setMaximumSize(600,200)
        font = self.questionLabel.font()
        font.setFamily('Courier New')
        font.setPointSize(13)
        self.questionLabel.setFont(font)

        # Answer Button
        buttonLayout = QHBoxLayout()

        self.yesButton = QToolButton()
        self.yesButton.setText("YES")
        self.yesButton.clicked.connect(self.dealUserAnswer)
        self.yesButton.setMinimumSize(100, 20)
        buttonLayout.addWidget(self.yesButton)

        self.noButton = QToolButton()
        self.noButton.setText("NO")
        self.noButton.clicked.connect(self.dealUserAnswer)
        self.noButton.setMinimumSize(100, 20)
        buttonLayout.addWidget(self.noButton)

        # back home Window Button
        self.homeButton = QToolButton()
        self.homeButton.setArrowType(Qt.LeftArrow)
        self.homeButton.clicked.connect(self.home)

        # set layout
        questionLayout = QVBoxLayout()
        questionLayout.addWidget(self.nameText)
        questionLayout.addWidget(self.nameInput)
        questionLayout.addWidget(self.questionLabel)
        questionLayout.addLayout(buttonLayout)
        questionLayout.addWidget(self.homeButton)
        self.setLayout(questionLayout)

        self.nextQuestion()

    def nextQuestion(self):
        if self.counter == (len(self.questions) ):
            self.addData()
            self.home()
            return
        else:
            self.questionLabel.setText("Q. " + self.questions[self.counter])
            self.counter += 1

    def dealUserAnswer(self):
        if self.sender() == self.yesButton:
            self.user_answer = 1
        elif self.sender() == self.noButton:
            self.user_answer = 0

        self.user_answers.append(self.user_answer)
        self.nextQuestion()

    def addData(self):
        # open data file
        fDataset = open(".\gameData\guessData", "a")
        fResult = open(".\gameData\guessResult", "a")

        self.user_answers = list(map(str,self.user_answers))
        if len(self.questions) == len(self.user_answers) == len(self.dataset[0]):
            member = self.nameInput.text()
            member = member.strip()
            if member in self.dancerName :
                result_msg = "\n" + str(self.dancerName.index(member))
                answer_msg = "\n" + ",".join(self.user_answers)
                fResult.write(result_msg)
                fDataset.write(answer_msg)
            else:
                self.showMessage("The name is wrong. \n Please write the name that is the list")

            fDataset.close()
            fResult.close()

    def home(self):
        self.close()

    def showMessage(self, msg):
        QMessageBox.warning(self, "Warning", msg)

if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    game = StartWindow()
    game.show()
    sys.exit(app.exec_())

