import cv2 as cv, os
import subprocess as sb
import shutil, re, time
import numpy as np
from pathlib import Path

from U2.time import Stime
from U2.debug import Logger, infoLog, debugLog, printLog
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


def snip_screen( uiBounds:dict = None, name = "snip", unique = False, write = True, image_data = False ) -> Path | tuple:
    # uiBounds : Element bounds to mark rectangle
    # unique : If True, filename with be extended by timestamp
    # write : If True, snipped image will automatically be saved in default output path
    # image_data : If True, return type will be tuple consisting of Path object and cv_image data
    # Returns Path( output_path ) object
    infoLog( f"Taking snip : {name}" ) 

    check_dirs( system_type )
    coo = uiBounds

    prefix = time.strftime( "%m_%d_%Y_%I-%M-%S-%p" ) if unique else ""
    image_name = prefix + "_" + name + ".png"

    # Revise string for file name
    replaced_spaces = image_name.replace( ' ','_' )
    image_name = re.sub( r'[^a-zA-Z0-9_\-\[\].]', '' , replaced_spaces )

    image_path = ( dev_dump / image_name ).as_posix()

    # Take screenshot output to subprocess stdout
    pipe = sb.run("adb shell screencap -p",
        stdin = sb.PIPE,
        stdout = sb.PIPE, shell = True )

    image_bytes = pipe.stdout
    cv_image = cv.imdecode( np.frombuffer( image_bytes, np.uint8 ), cv.IMREAD_COLOR )

    if system_type == "Windows":
        # Pull image from device
        win_image = ( win_dump / image_name ).as_posix()
        sb.run( f"adb pull { image_path } { win_image }", shell = True )

        image_path = win_image

    if coo:
        lt = coo['left'], coo['top']
        rb = coo['right'], coo['bottom']

        cv.rectangle( 
            cv_image, lt, rb,
            color = ( 0,255,0 ),
            thickness = 2,
            lineType = cv.LINE_4
        )
    image_path_ = Path( image_path )

    if write: 
        cv.imwrite( image_path, cv_image )

    return ( image_path_, cv_image ) if image_data else image_path
        




    
    



