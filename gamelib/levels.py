class Level( object ):
    # defaults
    balls = 2
    head_pos = (320,50)

    goals_pos = [ (150,300), (490,300) ]
    goals_forces = [ (0,0), (0,0) ]
    goals = len( goals_pos )
    gravity = (0,0)

    time = 45

    title = "NO TITLE"

class Level0( Level ):
    balls = 2

    goals_pos = [ (150,300), (490,300) ]
    goals = len( goals_pos )
    gravity = (0,0)

    title = "Level 0: Tutorial"

class Level1( Level ):
    balls = 2
    head_pos = (320,50)

    goals_pos = [ (150,300), (490,300), (640/2, 250) ]
    goals_forces = [ (0,0), (0,0), (0,0) ]
    goals = len( goals_pos )

    title = "Level 1: Gong, Gong!"


class Level2( Level ):
    balls = 2
    head_pos = (320,50)

    goals_pos = [ (20,420), (620,20) ]
    goals_forces = [ (0,0), (0,0) ]
    goals = len( goals_pos )

    title = "Level 2: Corners"


class Level3( Level ):
    balls = 2
    head_pos = (320,400)

    goals_pos = [ (150,300), (180,350), (210,400) ]
    goals_forces = [ (0,0), (0,0), (0,0) ]
    goals = len( goals_pos )
    gravity = (0,-30)

    title = "Level 3: Gravity"

class Level4( Level ):
    balls = 2
    head_pos = (320,50)

    goals_pos = [ (150,300), (490,300), (640/2,250), (640/2,350) ]
    goals_forces = [ (250,0), (-250,0), (0,250), (0,-250) ]
    goals = len( goals_pos )

    title = "Level 4: Movement"


class Level5( Level ):
    balls = 8
    head_pos = (320,50)

    goals_pos = [ (640/2,480/2) ]
    goals_forces = [ (0,0) ]
    goals = len( goals_pos )

    title = "Level 5: Long Tail"

class Level6( Level ):
    balls = 8
    head_pos = (280,50)

    gravity = (0,-20)
    goals_pos = [ (320,240), (320,340) ]
    goals_forces = [ (0,0), (0,0) ]
    goals = len( goals_pos )

    title = "Level 6: Long Gravity" 

class Level7( Level ):
    time = 60
    balls = 2
    head_pos = (320,50)

    gravity = (0,-60)
    goals_pos = [ (490,60)]
    goals_forces = [ (0,1200)]
    goals = len( goals_pos )

    title = "Level 7: Jump" 


class Level8( Level ):
    time = 60
    balls = 2
    head_pos = (320,50)

    gravity = (0,-60)
    goals_pos = [ (490,60)]
    goals_forces = [ (0,1200)]
    goals = len( goals_pos )

    title = "Level 7: Jump" 


levels = [ Level0, Level1, Level2, Level3, Level4, Level5, Level6, Level7 ]
