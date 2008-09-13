import levels
__all__ = [ 'state' ]

class State( object ):
    def __init__( self ):

        # current score
        self.score = 0

        # current level
        self.level = None

        # touched goals
        self.touched_goals = 0

        # current level idx
        self.level_idx = None

    def reset( self ):
        self.score = 0
        self.level = None
        self.level_idx = None

    def set_level( self, l ):
        self.level_idx = l
        self.level = levels.levels[l]

state = State()
