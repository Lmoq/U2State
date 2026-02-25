import regex as re
try:
    from .constants import numbers, color_emojis
except:
    from constants import numbers, color_emojis


def get_answer_regex( text : str ) -> str:
    # Search colors
    color_pattern = "Guess[\s\S]+\S\s+(\S+)\s*Identify"

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



if __name__=="__main__":
    # Patterns with usage of positive look behind feature
    color_pattern_look_behind = "(?<=\s+).+(?=\s*Identify)"
    digits_pattern_look_behind = r"(?<=[\s\S]*Identify the color of.*)(\d)(?=.*emoji)"

    color_safe = r"Guess \w+ \w+\W \w+ \S+\s+([\S]+)\s*Identify"


    # Sample usage
    sample_text = """Guess this Color: gusefring ✨

    🧡🟣🟨🟪🟥🟡💜🟧🤍💛💙🟤⚪🟩⚫🤎🟢💚🔴🟫❤🟠🖤🔵🟦
    Identify the color of 1️⃣5️⃣ emoji? = ???

    Enter your answer below: ⤵️😎"""

    print( get_answer_regex( sample_text ) )
    exit(0)

    sample_text2 = "JavaScript flavors of RegEx 5.. 6.. are supported. Validate your expression with Tests mode."

    capture = r"(?<=RegEx.*?)(\d)(?=.*?are supported)"

    output = re.findall( flex, sample_text )
    if output is not None:
        result = output

        print( result )
    else:
        print("No output")





