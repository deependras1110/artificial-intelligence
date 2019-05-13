To Start with execute the following command:
  make graphplan

Tower of Hanoi:
  There are two objects defined. That is a Peg and a Disk
  Disk = { disk1, disk2, disk3, disk4, disk5 }
  Peg  = { A, B, C }

  Understanding the literals:
  1. on <Disk-1> <Disk-2> : This says that 'Disk-2' is placed on 'Disk=1'
          Example: (on disk1 disk2)
  2. on <Disk> <Peg> : This says that 'Disk' is placed on 'Peg'
          Example: (on disk1 A)
  3. clear <Disk> : This says that there is nothing on 'Disk'
          Example: (clear disk5)
  4. clear <Peg> : This says that there is nothing on a 'Peg'
          Example: (clear C)

  There are four functions defined to move a Disk. They are:
  1. moveFromPegToPeg   - To move a disk from a peg to another peg
  2. moveFromPegToDisk  - To move a disk from a peg to a disk kept on another peg
  3. moveFromDiskToPeg  - To move a disk from a disk of one peg to another peg which is empty
  3. moveFromDiskToDisk - To move a disk from one disk to another, both on different pegs

  To run the program with facts file 1
    ./graphplan -o tower_of_hanoi/ops.txt -f tower_of_hanoi/facts1.txt

  To run the program with facts file 2
    ./graphplan -o tower_of_hanoi/ops.txt -f tower_of_hanoi/facts2.txt

  To run the program with your facts
    ./graphplan -o tower_of_hanoi/ops.txt -f [your-fact-file]

7 Puzzle:
  There are three objects defined. That is a Piece, an Empty and a Location
  Piece = { 1, 2, 3, 4, 5, 6, 7}
  Empty = { X }
  Peg  = { one, two, three, four, five, six, seven, eight, nine }

  Understanding the literals:
  1. on <Piece> <Location> : This says that a Piece 'x' is on Location 'y'
          Example: (on 1 one)
  2. adj <Location> <Location> : This says that the two locations are adjacent
          Example: (adj one two)

  There is one functions defined to play a move. They are:
  1. move - To move a piece from one location to another location where 'Empty' object is present

  To run the program with facts file 1
    ./graphplan -o 7_puzzle/ops.txt -f 7_puzzle/facts1.txt

  To run the program with facts file 2
    ./graphplan -o 7_puzzle/ops.txt -f 7_puzzle/facts2.txt

  To run the program with your facts
    Note: Use the same format of the above fact files with adj literals in your fact file
    ./graphplan -o 7_puzzle/ops.txt -f [your-fact-file]