import socket  
import sys 
import threading
  

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                                      # creates a new server socket
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)                                    # sets some socket options
  
  
if len(sys.argv) != 3:                                                                          # checks whether sufficient arguments have been provided
    print ("Correct usage: script, IP address, port number") 
    exit()  
 
IP_address = str(sys.argv[1])                                                                   # takes the first argument from command prompt as IP address 

Port = int(sys.argv[2])                                                                         # takes second argument from command prompt as port number  
server.bind((IP_address, Port))                                                                 # binds the server to the given Ip-Address and port

server.listen(100)                                                                              # allows the server to connect to up to 100 incoming connections
  
list_of_clients = []                                                                            # create a list in which all connected clients are stored
  
def clientthread(conn, addr):                                                                   # listens for incoming messages from the given client and sends them to the other clients which are connected

    nick = ''                                                                                   # the nickname of a user
    
    while True:                                                                                 # runs forever
            try:  
                message = conn.recv(2048)                                                       # listens for incoming messages
                if message:                                                                     # if the message is a vaild string longer than 1
                    message = message.decode('utf-8')                                           # decodes the message using the utf-8 standard
                    if (message.split()[0] == 'nick'):                                          # if the first word in the message is 'nick'
                        nick = message[5:]                                                      # set the nick to the rest of the message
                        b = f"Welcome to this chatroom, {nick}!".encode('utf-8')                # create a welcome Message for the client
                        conn.send(b)                                                            # send the message to the client
                        broadcast(f"{nick} joined the chatroom!", conn, addr)                   # broadcast a join Message to all attentees of the chatroom
                        continue                                                                # goes back to the beginning of the loop

                    print (f"<{addr[0]}:{addr[1]} | {nick}> {message}")                         # send the message to the console
    
                    message_to_send = f"<{nick}> {message}"                                     # formats the incoming message to send to the other attendees
                    broadcast(message_to_send, conn, addr)                                      # broadcasts the message to the attendees
  
                else:
                    remove(conn, addr)                                                          # removes the connection
                    break                                                            
  
            except:  
                broadcast(f"{nick} left the chatroom!", conn, addr)                             # broadcasts a leave message to the chatroom
                remove(conn, addr)                                                              # removes the connection
                break
  

def broadcast(message, connection, addr):                                                       # sends a message to all clients that are not the client who sent the message
    message = message.encode("utf-8")                                                           # encodes the message to a byte array
    for clients in list_of_clients:                                                             # goes through every client in the liet of clients
        if clients != connection:                                                               # if the current client from the list is not the given client which sent the message
            try:  
                clients.send(message)                                                           # tries to send the message
            except:                                                                             # if sending did not succeed
                remove(clients, addr)                                                           # removes the connection
  
def remove(connection, addr):                                                                   # removes the connection from the list and closes the connection
    if connection in list_of_clients:  
        list_of_clients.remove(connection)  
        connection.close()
        print(f"{addr[0]}:{addr[1]} disconnected")                                              # sends a leave message to the console
  
while True:                                                                                     # runs forever
    conn, addr = server.accept()                                                                # listens for incoming client connetions, stries the client and its address in seperate variables

    list_of_clients.append(conn)                                                                # adds the client to the list of clients
  
    print (f"{addr[0]}:{addr[1]} connected")                                                    # prints the address of the user that just connected  
  
    threading._start_new_thread(clientthread,(conn,addr))                                       # creates and individual thread for every user 


server.close()                                                                                  # closes the server