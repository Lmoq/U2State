import re
try:
    from .constants import numbers, color_emojis
except:
    from constants import numbers, color_emojis


def get_answer_regex( text : str ) -> str:
    # Search colors
    color_pattern = r"Guess[\s\S]+\S\s+(\S+)\s*Identify"

    output = re.search( color_pattern, text )
    if output is None:
        return None

    colors = output.group(1)

    # Search digits
    # Pattern ithout positive look behind
    digits_pattern = r"\d+(?=.*emoji)"

    output = re.findall( digits_pattern, text )
    if output is None:
        return None

    index = int( ''.join( output ) ) - 1
    emoji = colors[ index ]

    result = color_emojis.get( emoji, None )
    if result is None:
        return None

    return result


def get_points( text: str ) -> str:
    # Search points
    digit_pattern = r"Bot\s*Income:\s*(\d+)\s*\W\s*Points"
    
    output = re.search( digit_pattern, text )
    if output is None:
        return None

    return output.group( 1 )

if __name__=="__main__":
    pass
