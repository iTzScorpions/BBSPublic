# Chat Room

## About

A simple Chatroom with a Server written in python and two clients that can connect to it using a GUI one written in python and one as a WPF-Application using C#

## Requirements

You need to be able to run python scripts and be able to build and run C# programs:

- [python](https://www.python.org)
- [dotnet](https://dotnet.microsoft.com)

You also need some python packages:

- [PyQt5](https://pypi.org/project/PyQt5/)
- [Events](https://pypi.org/project/Events/)

## How to use

#### Start the Programs

- Start the server:
  - direct to the [python folder](python)
  - use the command `py server.py <address> <port>`
  - now the server will accept incoming connections and display their messages in the terminal
- Start the python client:
  - direct to the [python folder](python)
  - use the command `py client.py`
  - now the GUI pops up
- Stat the WPF client:
  - direct to the [c# folder](c#)
  - use the command `dotnet run`
  - now the GUI pops up

#### Edit the code

- You can open the code in any editor which supports either python or WPF-C# applications
- I myself used Visual Studio Code for the python scripts and Visual Studio for the WPF-Application

#### Use the client

- There are 3 Input Boxes at the Top:

  1.  for the **server address**

  2.  for the **server port**

  3.  for the **username** of the client which is free to choose

- After entering the connection-data you can connect to the Server by clicking the **Connect** button

- When you're connected:

  - You can disconnect by clicking the **Disconnect** button
  - You can read the message feed in the big box in the center
  - You can enter messages into the box at the bottom
  - You can send those messages by hitting return while the input box is focused or by pressing the **Send >** button

