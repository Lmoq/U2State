from U2.base import U2_Device
from U2.adb_tools import exec_
from U2.process import system_type


rs_main = """
    #!/bin/bash
    checkPyProc(){
    pgrep -x python > /dev/null
    }
    checkPyProc && pkill -2 python || python '$(pwd)'/main.py
    """

toggle_keyboard = """
    #!/bin/bash
    termux-toast "Switching keyboard ..."
    result=$( adb shell settings get secure default_input_method )
    case $result in
            "com.wparam.nullkeyboard/.NullKeyboard")
                    adb shell ime set com.google.android.inputmethod.latin/com.android.inputmethod.latin.LatinIME
                    ;;
            "com.google.android.inputmethod.latin/com.android.inputmethod.latin.LatinIME")
                    adb shell ime set com.wparam.nullkeyboard/.NullKeyboard
                    ;;
    esac
    """

def switchFocus( ctx: U2_Device = None, press_back = True ):
    assert isinstance( ctx, U2_Device ), "[ctx] parameter was not instance or subclass of U2_Device"

    if press_back:
        use_pipe = True if system_type == "Linux" else None

        cmd = f"input keyevent 4"
        exec_( cmd, use_pipe )

        elements = get_elements( self, 10 , Wtype.button, capture_output = True )

        if not elements:
            Handler.sig_term = True
            log = f"Failed to restart"

            infoLog( log )
            debugLog( log )
            printLog( log )

            return

        bounds = self.get_msg_tab( ctx.tab_instance_number, elements )
        adbClick( bounds )


