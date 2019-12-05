Description:
  Simulation of genetic knowledge (instinct) arising in a population.  Allows for full monitoring as well as full user control and creation capabilities for the environment.

How to Run:
  run main.py

Dependencies:
  numpy
  matplotlib
  tkinter

Shortcuts:
  Edit mode = "e"
  pause = "p"

Some of the features may be a bit unintuitive so it may be helpful read this before running
USER MANUAL:
Tiles = basic environment unit on map, contains different properties for food, etc

Creatures = the circles shown on screen.  They can either eat or move. All traits (speed, color, size, etc) are determined by the creature's genome

Decisions = creatures make decisions using a modified FFNN that learns via genetics only

SpawnNode, Node = spawns in creatures (only visible in edit mode)

Food = speckles visible on screen, spawend by tiles, consumed by creatures for energy, 3 tiers of food available
Edit mode:
  edit mode can be toggled with "e"

  while active, select tiles from the box on the far left to paint on the map with that tile using the map

  the triangle in the bottom right is a spawn node. Clicking it allows spawn nodes to be placed using the map (not painted)

Creature Loading/access:
the large box to the left of the map import/export box allows for creature access
They can be loaded from a file or selected by clicking "pick creature" then clicking a creature displayed on screen

This creature will be highlighted with a yellow or pink dot accordingly for easy observation

This creature can then be saved to a file or used for other functions

Node Config:
  the box directly to the bottom right of the tile box allows nodes to be configured before adding

  creatures can be loaded by clicking "add" then clicking one of the large boxes in the creature Loading/access area or one of the boxes containing the top creatures

  Loading just the top box makes a node of all clones
  Loading both makes the node all children of the two
  Loading neither makes a default (random) node

  Clear selections by clicking the box with the creature (to the left of add)


Analysis:
  plots can be displayed corresponding to the buttons shown

  top creature buttons function like large creature buttons in creature loading/access block

NOTE - when the file dialog opens tkinter will not call mouseReleased.  Whenever saving/loading click a blank spot before doing anything else or risk
mouseDragged never being called again (among other horrors)
