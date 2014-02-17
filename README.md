# Protomg
protomg - game prototype to test yet another match-like game mechanism.

The code is dirty and primary developed to play with different game multipliers and time constraints rather than introduce good game design itself.

Written on python with help of amazing pygame library. Developed and tested on Ubuntu 13.10.

## Install

On Ubuntu 13.10 install pygame before running the game:

    apt-get install python-pygame

## Run

Get the sources, make sure that game.py is executable and there is level.dat in the same directory:

    cd protomg
    ./game.py
    
## Gameplay

Player should drag cells to match 4 and more cells with the same color. For more than 5 cells player will be rewarded with additonal score and additional time.

To match cells please press left mouse button on a cell you want to move then drag it to any diagonal direction and release mouse button.



