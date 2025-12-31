from U2.enums import ActionType, TaskType


class Task_Info( dict ):

    __preset__ = {
        "number" : 100,

        # Parent Match Selector
        "match_selector" : {},
        "match_alt_selector" : {},
        "match_selector_timeout" : 10,

        "class_name_delimiter" : [],

        # Actions
        "action_type" : ActionType.action,

            # Click
        "offsetx" : 0,
        "offsety" : 0,
        "delay" : 0,
        "noUiClick" : None,

            # Swipe
        "swipe_direction" : "up/left/right/down",
        "swipe_points" : 0,
        "swipe_duration" : 100,

            # Write
        "write_text" : "",
            
            # Keys
        "key" : "",
        "keyCombo" : [],

        # Check
        "check_selector" : {},
        "check_selector_timeout" : 5,

        "next_wait_time" : 0,
    }


    def __init__( self, *args, **kwargs ):        
        super().__init__( *args, **kwargs )
        self |= Task_Info.__preset__
        
        for k,v in kwargs.items():
            setattr( self, k, v )


    def __getattr__( self, attr ):
        if not attr in self:
            raise AttributeError( f"Task has no attribute named '{attr}'")
        return self[ attr ]


    def __setattr__( self, attr, value ):
        if not attr in self:
            raise AttributeError( f"Task has no attribute named '{attr}'")
        self[ attr ] = value


if __name__=='__main__':
    pass
