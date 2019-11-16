from player import Player
from ship import Ship
from board import Board

if __name__ == "__main__":
    print("....being tested")
    s1 = Ship("Carr", [(1,1),(1,2),(1,3),(1,4),(1,5)])
    s2 = Ship("Dest", [(2,1),(2,2)])
    ships_for_one = [s1, s2]      # 2 ships for p1

    
    s3 = Ship("Crui", [(3,1),(3,2),(3,3)])
    s4 = Ship("Subm",[(4,1),(4,2),(4,3)])
    ships_for_two = [s3, s4] # 2 ships for p2
    
    p1 = Player("JC", ships_for_one)
    p2 = Player("Julian", ships_for_two)
    # Note: Player class itself won't check for the square availability


    b = Board(10,[p1,p2])
    # Note: Board class itself won't check for the square
    #       out of range error.
    #       size is usually 10 x 20 (half and half)

    print(b) # show the board
    
##    [[None, None, None, None, None, None, None, None, None, None],
##     [None, Carr, Carr, Carr, Carr, Carr, None, None, None, None],
##     [None, Dest, Dest, None, None, None, None, None, None, None],
##     [None, Crui, Crui, Crui, None, None, None, None, None, None],
##     [None, Subm, Subm, Subm, None, None, None, None, None, None],
##     [None, None, None, None, None, None, None, None, None, None],
##     [None, None, None, None, None, None, None, None, None, None],
##     [None, None, None, None, None, None, None, None, None, None],
##     [None, None, None, None, None, None, None, None, None, None],
##     [None, None, None, None, None, None, None, None, None, None]]
    
    b.guess((0,0)) # guess one coordinate
    print(b) # and is a miss
    
##    [[miss, None, None, None, None, None, None, None, None, None],
##     [None, Carr, Carr, Carr, Carr, Carr, None, None, None, None],
##     [None, Dest, Dest, None, None, None, None, None, None, None],
##     [None, Crui, Crui, Crui, None, None, None, None, None, None],
##     [None, Subm, Subm, Subm, None, None, None, None, None, None],
##     [None, None, None, None, None, None, None, None, None, None],
##     [None, None, None, None, None, None, None, None, None, None],
##     [None, None, None, None, None, None, None, None, None, None],
##     [None, None, None, None, None, None, None, None, None, None],
##     [None, None, None, None, None, None, None, None, None, None]]
    
    b.guess((1,1), 1) # guess another coordinate
    print(b) # and is a hit

##   [[miss, None, None, None, None, None, None, None, None, None], 
##   [None, _hit, Carr, Carr, Carr, Carr, None, None, None, None],
##   [None, Dest, Dest, None, None, None, None, None, None, None],
##   [None, Crui, Crui, Crui, None, None, None, None, None, None],
##   [None, Subm, Subm, Subm, None, None, None, None, None, None],
##   [None, None, None, None, None, None, None, None, None, None],
##   [None, None, None, None, None, None, None, None, None, None],
##   [None, None, None, None, None, None, None, None, None, None],
##   [None, None, None, None, None, None, None, None, None, None],
##   [None, None, None, None, None, None, None, None, None, None]]
    print(b.who_is_winner()) # return -1 if is not finished

    b.guess((1,2), 1)
    b.guess((1,3), 1)
    b.guess((1,4), 1)
    b.guess((1,5), 1)
    b.guess((2,1), 1)
    b.guess((2,2), 1)
    print(b) # 6 hits

##    [[miss, None, None, None, None, None, None, None, None, None],
##     [None, _hit, _hit, _hit, _hit, _hit, None, None, None, None],
##     [None, _hit, _hit, None, None, None, None, None, None, None],
##     [None, Crui, Crui, Crui, None, None, None, None, None, None],
##     [None, Subm, Subm, Subm, None, None, None, None, None, None],
##     [None, None, None, None, None, None, None, None, None, None],
##     [None, None, None, None, None, None, None, None, None, None],
##     [None, None, None, None, None, None, None, None, None, None],
##     [None, None, None, None, None, None, None, None, None, None],
##     [None, None, None, None, None, None, None, None, None, None]]

    print(b.who_is_winner()) # 0 if p1 win, 1 if p2 win
