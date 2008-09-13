class Level( object ):
    pass

class Level1( Level ):
    balls = 2
    head_pos = (320,50)

    goals_pos = [ (150,300), (490,300) ]
    goals_forces = [ (0,0), (0,0) ]
    goals = len( goals_pos )

    title = "Level 1: Easy"

class Level2( Level ):
    balls = 3
    head_pos = (200,200)
    tail_pos = (400,400)

levels = [ Level1, Level2]
