import socket
import sys
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QLabel, QLineEdit, QPushButton, QScrollArea, QVBoxLayout
from worker import Worker
from PyQt5.QtCore import *



client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                                  # the socket which connects to the Server

connected = False                                                                           # the state of the connection

app = QApplication([])                                                                      # the window which contains the UI-elements

inputBox = QLineEdit()                                                                      # the textbox for the message to send

sendBtn = QPushButton('Send >')                                                             # the button which triggers the sending of a message

scrollView = QScrollArea()                                                                  # The scrollview which contains the message History

messageHistoryWidget = QWidget()                                                            # the widget which lays in the ScrollView and inherits the messageHistory

messageHistory = QVBoxLayout()                                                              # the Layout which contains the sent and received Messages

addressBox = QLineEdit()                                                                    # input boxes for address, port and nickname
portBox = QLineEdit()
nickBox = QLineEdit()

connectBtn = QPushButton('Connect')                                                         # connect and disconnect buttons
disconnectBtn = QPushButton('Disconnect')


threadpool = QThreadPool()                                                                  # manager for different threads


def receiveMessage(progress_callback):                                                      # this method listenes for incoming messages from the server
                                                                                            # has to be called in a different thread, because it blocks operation
    global connected
    global client
    while connected:                                                                        # runs as long as the server is connected
        try:                                                                                # try/except: the code in the try block always gets executed. 
                                                                                            # If an exception is raised in the try block, it immediately jumps to the except block and the code in it gets executed
            
            recMessage = client.recv(2048)                                                  # wait for a message from the server and store it in a variable
                                                                                            # throws an error if the server closes the connection
            recMessage = recMessage.decode('utf-8')                                         # decodes the received byte array to a string using the utf-8 standard
            if (recMessage != ''):                                                          # if the received message is not empty
                progress_callback.emit(recMessage)                                          # calls an update with the received message on the QThreadpool
        except:
            connected = False                                                               # update the connected variable
            updateControls()                                                                # update the ui-controls
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                      # re-initializes the socket to prepare it for a new connection

    progress_callback.emit(f"You disconnected from {addressBox.text()}:{portBox.text()}")   # update the Worker with a disconnect message

def sendMessage(message):                                                                   # sends the given string as a byte array to the server
    global client
    b = message.encode('utf-8')                                                             # encode string to byte array
    client.send(b)                                                                          # send byte array to the server



def startWindow():                                                                          #creation of the Application Window

    
    window = QWidget()                                                                      # creation of the Window
    window.setWindowTitle('Message Client')
    window.setMinimumHeight(400)
    window.setMinimumWidth(300)

    window.destroyed.connect(lambda:stopClient())                                           # adding an Eventlistener that fires when the window is closed

    
    layout = QGridLayout()                                                                  # creating the gridLayout

    layout.addWidget(addressBox, 0, 0)                                                      # adding the input boxes for address, port and nickname
    layout.addWidget(portBox, 1, 0)
    layout.addWidget(nickBox, 2, 0)

    connectBtn.clicked.connect(lambda:startClient(addressBox.text(), portBox.text()))       # adding the connect button with an event listener which fires when it is clicked
    layout.addWidget(connectBtn, 0, 1)

    disconnectBtn.clicked.connect(lambda:stopClient())                                      # adding the disconnect button with an event listener which fires when it is clicked
    layout.addWidget(disconnectBtn, 2, 1)

    
    scrollView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)                             #configuring the scrollView
    scrollView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    messageHistory.addStretch()                                                             # configuring the messageHistoryLayout

    messageHistoryWidget.setLayout(messageHistory)                                          # set the layout of the messageHistoryWidget to the QVBox messageHistory
    scrollView.setWidget(messageHistoryWidget)                                              # set the widget of the scrollview to the messageHistoryWidget


    
    scrollView.setWidgetResizable(True)                                                     # adding the scrollview
    layout.addWidget(scrollView, 3, 0, 1, 2)

    
    inputBox.returnPressed.connect(lambda:sent())                                           # adding the inputbox with an event listener which fires when the return-key is pressed
    layout.addWidget(inputBox, 4, 0)
    
    
    sendBtn.clicked.connect(lambda:sent())                                                  # adding the sendbutton with an avent listener which fires when it is clicked
    layout.addWidget(sendBtn)

    window.setLayout(layout)                                                                # set the layout of the window to the predefined gridlayout with its contents
    window.show()                                                                           # make the window visible

    
    updateControls()                                                                        # update the state of the controls

    
    app.exec_()                                                                             # run the window



def updateControls():                                                                       # updates the controls based on the connection state

    global connected

    addressBox.setDisabled(connected)
    portBox.setDisabled(connected)
    nickBox.setDisabled(connected)

    connectBtn.setDisabled(connected)
    disconnectBtn.setDisabled(not connected)

    inputBox.setDisabled(not connected)
    sendBtn.setDisabled(not connected)

                                                                                            
def sent():                                                                                 # sends the text from the inputBox to the server and adds the message to the messageHistory
                                                                                            
    if inputBox.text == '':                                                                 # return if the text in the inputBox is empty
        return
    sendMessage(inputBox.text())                                                            # sends the message to the server
    updateHistory(f"<You> {inputBox.text()}")                                               # adds the message to the messageHistory
    inputBox.setText('')                                                                    # resets the text in the inputBox

                                                                                            
def updateHistory(message):                                                                 # adds the given message to the message History

    msg = QLabel()                                                                          # creates a new label which contains the message
    msg.setText(message)
    messageHistory.insertWidget(messageHistory.count() - 1, msg)                            # adds the label to the end of the messageHistory

def stopClient():                                                                           # stops the client socket
    global client
    if not connected:                                                                       # if the client isn't connected return
        return
    client.close()                                                                          # closes the connection to the server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                              # reinitialize the socket
    

def startClient(address, port):                                                             # starts the client
    global client
    global connected

    IP_address = address
    Port = int(port)
    try:                                                                                    # try/except -> see receiveMessage
        client.connect((IP_address, Port))                                                  # connect the client to the server
        connected = True                                                                    # update connected status
        updateHistory(f"Connected to {addressBox.text()}:{portBox.text()}")                 # update the MessageHistory with a connect message 
        sendMessage(f"nick {nickBox.text()}")                                               # send a message to the server containing the nickname
    except:
        updateHistory(f"Coludn't connect to {addressBox.text()}:{portBox.text()}")          # update the MessageHistory with a disconnect message
        connected = False                                                                   # update connected status
        updateControls()                                                                    # update the ui-elements
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                          # reinitialize the socket
        return


    updateControls()                                                                        # update the ui-elements

    worker = Worker(receiveMessage)                                                         # create a new Worker which handles the message-listening-process
    
    worker.signals.message.connect(updateHistory)                                           # connect the message signal from the worker to the updatehistory function
    
    threadpool.start(worker)                                                                # start the worker


startWindow()                                                                               # start the window


