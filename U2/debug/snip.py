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
        dev_dump.mkdir( exist_ok = True )


def snip_screen( uiBounds:dict = None, name = "snip", unique = False ) -> Path:
    # uiBounds : Element bounds to mark rectangle
    # If unique is True, filename with be extended by timestamp
    # returns Path() of image
    check_dirs( system_type )
    coo = uiBounds

    prefix = time.strftime( "_%m_%d_%Y_%I-%M-%S-%p" ) if unique else ""
    image_name = prefix + name + ".png"

    # Revise string for file name
    replaced_spaces = image_name.replace( ' ','_' )
    image_name = re.sub( r'[^a-zA-Z0-9_\-\[\].]', '' , replaced_spaces )

    image_path = ( dev_dump / image_name ).as_posix()
    sb.run( f"adb shell screencap { image_path }", shell = True )

    if system_type == "Windows":
        # Pull image from device
        win_image = ( win_dump / image_name ).as_posix()
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
        




    
    



