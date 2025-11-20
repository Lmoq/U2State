import os, subprocess as sb, sys, time
from pathlib import Path; sys.path.append( str(Path(__file__).parent.parent.parent) )

from U2.enums import Direction
from U2.process import system_type



def adbClick( uiBounds : dict, offsetx : int = 0, offsety : int = 0, log = False):
    # Click center of UiObject
    coo = uiBounds
    
    left = coo['left']
    right = coo['right']

    top = coo['top']
    bottom = coo['bottom']

    x = left + int(( right - left) / 2) + offsetx
    y = top + int(( bottom - top ) / 2) + offsety
    if log: print( f"Tapped {x} {y}" )
    
    cm = f"input tap {x} {y}"
    exec_( cm )


def adbClickNoUi( coo : tuple, log = False ):
    # Click directly using adb shell
    x,y = coo
    if log: print( f"Tapped {x} {y}" )

    cm = f"input tap {x} {y}"
    exec_( cm )


def adbSwipeUi( uiBounds : dict, direction : Direction, points : int = 100, duration : int = 50 ):
    coo = uiBounds

    left = coo['left']
    right = coo['right']

    top = coo['top']
    bottom = coo['bottom']

    x = left + int(( right - left) / 2)
    y = top + int(( bottom - top ) / 2)

    cm = ""

    match direction:
        case Direction.left:
            cm = f"input swipe {x} {y} {x-points} {y} {duration}"
        case Direction.up:
            cm = f"input swipe {x} {y} {x} {y-points} {duration}"
        case Direction.right:
            cm = f"input swipe {x} {y} {x+points} {y} {duration}"
        case Direction.down:
            cm = f"input swipe {x} {y} {x} {y+points} {duration}"
    exec_( cm )


def adbType( text : str ):
    cm = f'''input text "{repr(text)}"'''
    exec_( cm )


def adbKeyCombo( combo = [], key = None ):
    # combo - list of keys to press in combination
    # key - proceeding key to press
    # See https://gist.github.com/arjunv/2bbcca9a1a1c127749f8dcb6d36fb0bc for keylist
    keyS = " ".join( [f"{k}" for k in combo] )
    keyS += f"; input keyevent {key}" if key else ""
    
    cm = f"input keycombination {keyS}"
    exec_( cm )


def vib( duration, times ):
    duration = int( duration * 1000 )
    cm = []
    for i in range( times ): 
        cm.append( f"termux-vibrate -f -d {duration}" )
        time.sleep(0.2)
        sb.run( cm, shell=True, stdout=sb.DEVNULL )

vibrate = vib

def switch_keyboard( toggle : str = "on/off" ):
    # Set default ime
    if toggle.lower() == "on":
        subprocess.run( "adb shell ime set com.google.android.inputmethod.latin/com.android.inputmethod.latin.LatinIME", stdout=subprocess.DEVNULL, shell=True )
    # Disable keyboard
    elif toggle.lower() == "off":
        subprocess.run( "adb shell ime set com.wparam.nullkeyboard/.NullKeyboard", stdout=subprocess.DEVNULL, shell=True )


def _set_process_caller( system_type ):
    global vibrate

    def bash_preset( args ):
        sb.run( f"echo {args} > ~/pipes/adbpipe &", shell=True )

    def cmd_preset( args ):
        sb.run( f"adb shell {args}", shell=True, stdout=sb.DEVNULL )

    def vb( duration, times ):
        # Disable termux-vibrate shell call for windows
        return None

    match system_type:
        case "Windows":
            vibrate = vb
            print("Using Windows preset for adb calls")
            return cmd_preset
        case "Linux":
            print("Linux preset preset for adb calls")
            return bash_preset

exec_ = _set_process_caller( system_type )


if __name__=='__main__':
    pass


