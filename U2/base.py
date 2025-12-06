import traceback, time, sys, subprocess as sb

from U2.process import get_system_info, system_type
from U2.notif import NotifLog


class U2_Device:

    _device = None # : uiautomator2.Device
    _target_package = ""
    _launch_activity = ""


    @classmethod
    def init_device_session( cls, device = None, package_name = None ):
        # Initialization of shared ( class level attribute ) device and target_package
        assert device is not None, "Device parameter must not be None"

        cls._device = device
        package = package_name if package_name else device.info["currentPackageName"] 
        
        cls._target_package = package
        cls._launch_activity = cls.get_launch_activity( package )


    @staticmethod
    def get_launch_activity( package_name ):
        result = sb.run( f"adb shell cmd package resolve-activity --brief {package_name}", shell = True, capture_output = True )
        return result.stdout.decode().strip().splitlines()[-1]


    def __init__( self, device = None, package_name: str = None ):
        # Allows to have an option to initialize instance level attributes, 
        # takes precedence over class level even after being set
        if device is not None:

            if type(self)._device is not None:
                print(f"Notice: {type(self)} already has class attribute of device.. proceeding to set instance level attr")
            self._instance_device = device

            if package_name is not None:
                self._instance_target_package = package_name
            else:
                self._instance_target_package = device.info["currentPackageName"]
            self._instance_launch_activity = self.get_launch_activity( self._instance_target_package )


    @property
    def device( self ):
        # Attribute look up, instance attribute takes precedence over class attribute
        if getattr( self, "_instance_device", None ) is not None:

            print( "Returning instance level attr device" )
            return self._instance_device

        print( "Returning class level attr device" )
        return type( self )._device


    @device.setter
    def device( self, device ):
        # Set instance-level device attr
        self._instance_device = device
        

    @property
    def target_package( self ):
        # Attribute look up, instance attribute takes precedence over class attribute
        if getattr( self, "_instance_target_package", None ) is not None:

            print( f"Returning instance level attr target_package" )
            return self._instance_target_package

        print( "Returning class level attr target_package" )
        return type( self )._target_package


    @target_package.setter
    def target_package( self, package_name ):
        # Set instance-level target_package attr
        self._instance_target_package = package_name


    @property
    def launch_activity( self ):
        # Attribute look up, instance attribute takes precedence over class attribute
        if getattr( self, "_instance_launch_activity", None ) is not None:
            
            print( "Returning instance level attr launch_activity" )
            return self._instance_launch_activity

        print( "Returning class level attr launch_activity" )
        return type( self )._launch_activity


    @launch_activity.setter
    def launch_activity( self, launch_activity ):
        # Set instance-level launch_activity attr
        self._instance_launch_activity = launch_activity


    def waitElement( self, selector: dict = None, timeout=0 ):
        # Wait until ui element exists then returns UiObject
        try: 
            ui = self.device( **selector )

            if not ui.wait( timeout = timeout ):
                return None
            return ui
        
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__, file=sys.stdout)
            time.sleep(1)
            return 'FAILED'


    def waitSiblingElement( self, base: dict = None, sibling: dict = None, timeout=0 ):
        try:
            ui = self.device( **base ).sibling( **sibling )

            if not ui.wait( timeout = timeout ):
                return None
            return ui

        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__, file=sys.stdout)
            return 'FAILED'


    def getInfo( self, ui ):
        success = False
        
        retries = 0
        info = None
        
        while not info:
            try:
                info = ui.info       
            except Exception:
                retries += 1
                time.sleep( 0.5 )

            #if retries > NotifLog.gInfo:
            #    NotifLog.gInfo = retries
            #    pass

        return info


if __name__=='__main__':
    pass
