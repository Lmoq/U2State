import cv2 as cv, os
import subprocess as sb
import shutil, re, time
from pathlib import Path

from U2.debug import Logger
from U2.process import system_type


win_dump = Logger.debug_path
dev_dump = Path( "/sdcard/termux_dump" )

def check_dirs( system_type ):
    # Verify paths
    if system_type == "Windows":
        win_dump.mkdir( exist_ok = True )

        command = f"adb shell test -d { dev_dump.as_posix() } && echo 1 || echo 0"
        result = sb.run( command, shell = True, capture_output = True ).stdout.decode().strip("\r\n")

        if not int( result ):
            sb.run( f"adb shell mkdir { dev_dump.as_posix() }", shell = True )

    elif system_type == "Linux":
        dev_dump.mkdir( exists_ok = True )


def snip_screen( uiBounds:dict = None, name = "snip", overwrite = True ) -> Path:
    # uiBounds : Element bounds to mark rectangle
    # If overwrite is False, same filename snips will have incremental name mod
    # returns image_path
    check_dirs( system_type )

    coo = uiBounds
    image_name = name + ".png"
    image_path = ( dev_dump / image_name ).as_posix()

    sb.run( f"adb shell screencap { image_path }", shell = True )

    if system_type == "Windows":
        # Pull image from device
        win_image = (win_dump / image_name).as_posix()
        sb.run( f"adb pull { image_path } { win_image }", shell = True )

        image_path = win_image

    if coo:
        if system_type == "Linux": 
            time.sleep(0.8)
        cv_image = cv.imread( image_path, cv.IMREAD_COLOR )

        lt = coo['left'], coo['top']
        rb = coo['right'], coo['bottom']

        cv.rectangle( 
            cv_image, lt, rb,
            color = ( 0,255,0 ),
            thickness = 2,
            lineType = cv.LINE_4
        )
        cv.imwrite( image_path, cv_image )

    return Path( image_path )
        




    
    



