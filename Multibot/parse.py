import re

text = ""

with open( "logs/info.log", 'r', encoding = "utf-8" ) as f:
    text = f.read()

pattern = r"Guess.*\s+\W+\s+.*emoji\? = \?\?\?\s+Enter your answer below: ⤵️😎"
match = re.findall( pattern, text )

find = 0
records = {}

for t in match:
    if t not in records.keys():
        records[ t ] = 0
    else:
        records[ t ] += 1
        dup_num = records[ t ]
        print( f"At find :{find} a duplicate is found, dup amount : { dup_num }" )
        print( "================== Text ==============================" )
        print( t )
        print( "================== End of text =======================\n\n" )
    find += 1

