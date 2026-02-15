from U2.states import Handler


class Bot_Handler:

    def __init__( self, bot_handler: Handler = None ):
        self.bot = bot_handler
        self.name = ""
        self.key_name = ""

    def __repr__( self ):
        return self.name



if __name__=="__main__":
    pass
