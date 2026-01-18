from U2.base import U2_Device
from U2.enums import Wtype, get_wtype_enum
from U2.debug import Logger, printLog
from U2.process import system_type
from .snip import dev_dump, win_dump, check_dirs, snip_screen

from pathlib import Path
import subprocess as sb, re
import cv2 as cv



def dump( device: U2_Device = None, file_name: str = "" ):
    assert not not file_name, "Output path should be specified"
    check_dirs( system_type )

    output_path = ( dev_dump / file_name ).as_posix()

    with open( output_path, "w", encoding="utf-8" ) as f:
        dmp = device.device.dump_hierarchy( compressed=False )
        f.write( dmp )

    return output_path


def get_element( device: U2_Device = None, selector: dict = None, show_bounds = False, 
                 show_info = False, snip = False, get_center = False 
    ):
    ui = device.waitElement( selector )

    if ui in ( "FAILED", None ):
        print( "get_element.. Element not found" )
        return

    fo = device.getInfo( ui )

    try:
        text = fo['text'] or fo['contentDescription'] or None
        classn = fo['className']
        log = f"Tag : {text} | class : {classn} [Wtype.{ get_wtype_enum(classn) }]"

        if show_bounds: log += f" | Bounds : [{ fo['bounds'] }]"
        printLog( log )

        if show_info:
            printLog( f"Uinfo : [{fo}]" )

        coo = fo['bounds']
        if coo is not None:

            if get_center:
                width = coo['right'] - coo['left']
                height = coo['bottom'] - coo['top']

                x = coo['right'] - ( width // 2 )
                y = coo['bottom'] - ( height // 2 )

                printLog( f"Center {x}:{y}" )

            if snip:
                check_dirs( system_type )
                
                replaced_spaces = text.replace( ' ','_' )
                refined_text = re.sub( r'[^a-zA-Z0-9_\-\[\]]', '' , replaced_spaces )

                image_path = ( dev_dump / ( refined_text + ".png" ) ).as_posix()
                printLog( f"Saving to { image_path }" )

                sb.run( f"adb shell screencap { image_path }" )
                
                if system_type == "Windows":
                    sb.run( f"adb pull { image_path } { win_dump / ( refined_text + '.png' ) }" )
                    image_path = win_dump / ( refined_text + '.png' ).as_posix()

                elif system_type == "Linux":
                    time.sleep( 0.8 )

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
        else:
            print( f"Ui bounds not retrieved.. will not proceed get_center or snip" )

    except Exception as e:
        print( f"Selector : [{selector}]", e )

        
def get_elements( device: U2_Device = None, instance_range: tuple = (0,1), class_name: Wtype = None, show_bounds = False, 
                  show_info = False, snip = False, get_center = False
    ):
    range_ = instance_range
    found_elements = {}

    for i in range( range_ if type(range_) is int else ( range_[0], range_[1] ) ):
        ui = device.waitElement( selector = { "className" : class_name.value, "instance" : i } )

        if ui in ( "FAILED", None ):
            print( "get_elements .. Element not found" )
            return

        fo = device.getInfo( ui )
        
        try:
            text = fo['text'] or fo['contentDescription']
            log = f"Instance_{i}_{text} "

            if show_bounds: log += f"Bounds : [{ fo['bounds'] }]"
            printLog( log )

            if show_info:
                printLog( f"Uinfo : [{fo}]" )

            coo = fo['bounds']
            if coo is not None:

                if get_center:
                    width = coo['right'] - coo['left']
                    height = coo['bottom'] - coo['top']

                    x = coo['right'] - ( width // 2 )
                    y = coo['bottom'] - ( height // 2 )

                    printLog( f"Center {x}:{y}" )

                if snip:
                    replaced_spaces = text.replace( ' ','_' )

                    refined_text = re.sub( r'[^a-zA-Z0-9_\-\[\]]', '' , replaced_spaces )
                    file_name = f"Instance{ i }_{ class_name.name }_{ refined_text }.png"

                    found_elements[ file_name ] = coo
            else:
                print( f"Ui bounds not retrieved.. will not proceed get_center or snip" )

        except Exception as e:
            print( f"Selector : [Instance{i}]", e )

    if found_elements:
        check_dirs( system_type )
        image_name = "snip"

        image_path = Path( snip_screen( name = image_name ) )
         
        image = cv.imread( image_path, cv.IMREAD_COLOR )
        if image is not None:
            print( "Image ok" ) 

        for file_name, bounds in found_elements.items():
            #printLog(f"base : {file_name} bounds : {bounds}")
            cv_image = image.copy()
            coo = bounds

            lt = coo['left'], coo['top']
            rb = coo['right'], coo['bottom']

            cv.rectangle( 
                cv_image, lt, rb,
                color = ( 0,255,0 ),
                thickness = 2,
                lineType = cv.LINE_4
            )
            cv.imwrite( image_path.with_name( file_name ), cv_image )

















