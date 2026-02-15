from U2.task import Task_Info
from U2.debug import printLog, infoLog, debugLog


class Task_State():


    def __init__( self, task_info: Task_Info = None, desc = None, next_state: "Task_State" = None ):
        self.task_info = task_info
        self.desc = desc
        self.next_state = next_state


    def enter( self, ctx ):
        pass


    def run( self, ctx ):
        pass


    def callback( self, ctx ):
        pass


    def next( self, ctx ):
        pass


    def exit( self, ctx ):
        pass


    def __str__( self ):
        return self.desc or str( type( self ) )





    










    
