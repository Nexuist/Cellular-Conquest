### Introduction

Cellular Conquest was a game I built for a friend's Connecticut Science Center exhibit. It was my first experience using `pygame`. The goal of the game was to serve as a simple tablet/desktop-based simulation of a cell's defense system, particularly antibodies and proteasomes.

> **NOTE:** This is a very barebones tech demo and by no means a final version. There are plenty of gameplay bugs, but the game is still playable. The code is open sourced for both historical purposes but also to show how a beginner can approach `pygame` and develop something more sophisticated than demo code.

### How To Play

##### Dependencies

* pygame
	* http://www.pygame.org/download.shtml
	* For OS X Homebrew users:
		* `brew install pygame`

* Python 2.7+
	* Comes preinstalled on most Linux / OS X versions
	* https://www.python.org/downloads/

##### Running

The default game resolution is `1280x800`. Depending on your screen resolution, you may need to change this. You can do so in line 8.
TODO

In a console:
> python main.py

##### Gameplay

Here's a screenshot:

![Screenshot](demo.png)

The main goal of the game is to protect your
	<img src="res/cell.png" alt = "cell" width="24" />
cell from
	<img src = "res/virus.png" alt = "virus" width = "24" />
viruses. If any virus manages to touch your
	<img src = "res/nucleus.png" alt = "virus" width = "24" />
nucleus, you will lose the game.

You can do this by placing down
	<img src = "res/antibody.png" alt = "antibody" width = "24" />
antibodies outside of the cell. Antibodies can't move, but they can slow down any virus that hits them. When a virus hits an antibody, it will get tagged:
	<img src = "res/virus_tagged.png" alt = "antibody" width = "24" />

### License
