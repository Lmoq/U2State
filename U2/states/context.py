from U2.base import U2_Device
from U2.debug import printLog, infoLog, debugLog
from U2.adb_tools import adbClick


class Session( U2_Device ):


    def __init__( self, device: "uiautomator2.Device" = None, package_name = None ):
        self.uinfo: dict = None
        self.restricted = False

        self.start_time_restriction: str = None
        self.end_time_restriction:str = None

        super().__init__( device, package_name )


    def search_element( self, selector=None, timeout=0 ) -> dict:
        # Find element
        ui = self.waitElement( selector, timeout )
        
        if ui in ("FAILED", None):
            printLog( "<<Selector failed>>" )
            return None

        uinfo = self.getInfo( ui )
        return uinfo


    def clickUI( self ):
        infoLog( f"Clicking {self.uinfo['bounds']}" )
        adbClick( self.uinfo["bounds"] )

