from U2.task import Task_Info
from U2.debug import printLog, infoLog, debugLog


class Task_State():


    def __init__( self, task_info: Task_Info = None, desc = None, next_state: "Task_State" = None ):
        self.task_info = task_info
        self.desc = desc
        self.next_state = next_state


    def enter( self, ctx ):
        printLog( f"Entering <<{self}>>" )


    def run( self, ctx ):
        printLog( f"Executing <<{self}>>" )
        pass


    def callback( self, ctx ):
        pass


    def next( self, ctx ):
        pass


    def exit( self, ctx ):
        printLog( f"Exiting <<{self.desc}>> task" )


    def __repr__( self ):
        return self.desc or str( type( self ) )



    










    
