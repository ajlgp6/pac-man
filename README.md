# pac-man
This is an automated pac-man game. There are 4 ghosts (Punky: 'P', Bunky: 'B', Dunky: 'D', and Runky: 'R') that are programmed with different movement objectives. Pac-man's movement is based on a Best First Search algorithm which recursively creates a priority queue of moves that can generate a score of 24 without dying.

To run:
1. While in the repository type "./run.sh dungeon1.txt output.txt" (replace dungeon1.txt with dungeon2.txt or dungeon3.txt for different game boards)

Things to note:
1. The initial game board can be seen by opening the dungeon text file that was ran.
2. To check the output of the game, open the output.txt file.
3. The first line in the output file is pac-man's move list. It shows the moves pac-man made before either winning (getting a score of at least 24: '.'=1 point, '$'=5 points, '*'=10 points) or after losing by getting hit by a ghost (Displayed as 'X' on final game board)
4. The second line of output shows the score pac-man achieves before the game ends.
5. The third line and onward displays the final state of the game board.
