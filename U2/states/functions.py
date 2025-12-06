from U2.adb_tools import adbClick, adbClickNoUi, adbSwipeUi, adbType, adbKeyCombo


def default_match( self, session=None, selector=None, timeout=0 ) -> dict:
    u2 = session
    tfo = self.task_info

    ui = u2.waitElement( selector, timeout )

    if ui == "FAILED" or ui == None:
        log = f"[{self}] selector match failed]"
        print( log )
        return None

    uinfo = u2.getInfo( ui ) 
    return uinfo


def click( self, ctx ):
    adbClick( ctx.uinfo['bounds'] )


def swipe( self, ctx ):
    uinfo = ctx.uinfo
    tfo = self.task_info
    adbSwipeUi( uinfo['bounds'], tfo.swipe_direction, tfo.swipe_points )


def write( self, ctx ):
    tfo = self.task_info
    adbKeyCombo( ["KEYCODE_CTRL_LEFT", "KEYCODE_A"], "KEYCODE_DEL" )
    adbType( tfo.write_text )

