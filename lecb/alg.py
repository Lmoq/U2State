import re
try:
    from .constants import answer_keys
except:
    from constants import answer_keys


def get_answer( text: str ) -> str:
    answer = answer_keys.get( text, None )
    return answer


def get_points( text: str ) -> str:
    digit_pattern = r"[^\+](\d+)"

    output = re.search( digit_pattern, text )
    if output is None:
        return None

    return output.group( 1 )

