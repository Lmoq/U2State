import sys
from pathlib import Path; sys.path.append( str(Path(__file__).parent.parent) )

from U2.state import Task_Handler, Task_State
from U2.base import U2_Device


class FindUI_Task( Task_State ):

    def __init__( self, **kwargs ):
        self.ctx: U2_Device = None
        super().__init__( **kwargs )



class ClickUI_Task( Task_State ):

    def __init__( self, **kwargs ):
        self.ctx: U2_Device = None
        super().__init__( **kwargs )



