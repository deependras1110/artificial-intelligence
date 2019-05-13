_______________________________________________________________________________________________________

The current game MAXCONNECT4 has been built on python. 
It is compatible with Python 1.6.0 and our omega machines.

The program has been developed with an evaluation algorithm and currenly has two modes
Mode 1) one-move
Mode 2) interactive

Both these mode uses depth limited searching and the depth needs to be greater than 0 for it to execute

To execute the program we use the following syntax:

    $ python maxconnect4.py one-move input.txt output.txt depth

    $ python maxconnect4.py interactive input.txt [human-next/computer-next] depth

Note:
-> It is important to give the initial state for the program, that is input.txt
-> The program plans to win the game at the last stage and not intermidiate levels

_______________________________________________________________________________________________________

Time Analysis in one-move mode for increasing depth levels.

Note:
-> The Initial State used here is an empty game board with first move as 1
-> The time are based on Omega Machines

    depth   |   Time (in seconds)
    ________|____________________
    1       |   0.050
    2       |   0.054
    3       |   0.088
    4       |   0.091
    5       |   0.323
    6       |   0.406
    7       |   1.326
    8       |   1.493
    9       |   6.605
    10      |   7.980
    11      |   23.673
    12      |   35.790
    13      |   156.329

_______________________________________________________________________________________________________