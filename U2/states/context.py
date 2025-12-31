from U2.base import U2_Device
from U2.debug import printLog, infoLog, debugLog
from U2.adb_tools import adbClick, adbClickNoUi, adbKeyPress, adbKeyCombo, adbSwipeUi, adbType
from U2.enums import Direction
from U2.task import Task_Info


class Session( U2_Device ):


    def __init__( self, device: "uiautomator2.Device" = None, package_name = None ):
        self.uinfo: dict = None
        self.uiObject: "uiautomator2._selector.UiObject" = None

        self.restricted = False
        self.start_time_restriction: str = None
        self.end_time_restriction:str = None

        self.write_text: str = ""
        super().__init__( device, package_name )


    # Selectors
    def search_element( self, selector:dict = None, timeout = 0 ) -> dict:
        # Find element
        ui = self.waitElement( selector, timeout )
        
        if ui in ("FAILED", None):
            infoLog( "    <<Selector failed>>" )
            return None

        self.uiObject = ui
        uinfo = self.getInfo( ui )

        return uinfo


    def search_qualified_class_names( self, uinfo: dict = None, tfo: Task_Info = None ) -> dict:
        # Limit UiObject selection based on specified classNames
        uinfo = uinfo
        if not uinfo["className"] in tfo.class_name_delimiter:
            infoLog( f"    Element class is difference than expected" )
            # Remove unwanted selector keys
            selector = self.uiObject.selector

            for key in ( "mask", "childOrSibling", "childOrSiblingSelector" ):
                selector.pop( key )

            for class_name in tfo.class_name_delimiter:
                uinfo = self.search_element( selector | {"className" : class_name} )

                if uinfo is not None:
                    print("delimiter class found")
                    break
        return uinfo
        

    # Adb functions
    def clickUI( self ):
        info = self.uinfo
        infoLog( f"Clicking ({info['text'] or info['contentDescription']}) | {info['bounds']}" )
        adbClick( self.uinfo["bounds"] )


    def clickNoUi( self, coo:tuple[int,int] ):
        x,y = coo
        #infoLog( f"Clicking ({x}, {y})" )
        adbClickNoUi( coo )


    def pressKey( self, key ):
        info = self.uinfo
        infoLog( f"Pressing key ({key})" )
        adbKeyPress( key )


    def swipeUI( self, direction: Direction, points, duration ):
        info = self.uinfo
        infoLog( f"Swiping ({info['text'] or info['contentDescription']}) | {direction.value} | {info['bounds']}" )

        adbSwipeUi( self.uinfo["bounds"], direction, points, duration )


    def writeText( self ):
        infoLog( f"Writing ({self.write_text})" )
        # Clear edit text field
        adbKeyCombo( combo = [ "KEYCODE_CTRL_LEFT", "KEYCODE_A" ], key = "KEYCODE_DEL" )
        adbType( self.write_text )


