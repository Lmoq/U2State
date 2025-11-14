import sys
from pathlib import Path; sys.path.append( str(Path(__file__).parent.parent.parent) )

from U2.adb_tools import adbClick, adbClickNoUi, adbSwipeUi, adbType, adbKeyCombo


def default_match( self, session=None, selector=None, timeout=0 ) -> dict:
    u2 = session
    tfo = self.task_info

    ui = u2.waitElement( selector, timeout )

    if ui == "FAILED" or ui == None:
        log = f"[{self}] selector match failed @task.number[{current_task.number}]"
        print( log )
        return None

    uinfo = u2.getInfo( ui ) 
    return uinfo


def click( self, ctx ):
    adbClick( ctx.uinfo['bounds'] )

