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
    head_pos = (320,50)

    goals_pos = [ (150,300), (490,300), (640/2,250) ]
    goals_forces = [ (0,0), (0,0), (0,0) ]
    goals = len( goals_pos )

    title = "Level 2: Easy"

class Level3( Level ):
    balls = 3
    head_pos = (320,50)

    goals_pos = [ (150,300), (490,300), (640/2,250), (640/2,350) ]
    goals_forces = [ (0,0), (0,0), (0,0), (0,0) ]
    goals = len( goals_pos )

    title = "Level 3: Easy"

levels = [ Level1, Level2, Level3]
