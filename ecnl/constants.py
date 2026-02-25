question = "Guess this Color"

numbers = {
    "0️⃣" : "0",
    "1️⃣" : "1",
    "2️⃣" : "2",
    "3️⃣" : "3",
    "4️⃣" : "4",
    "5️⃣" : "5",
    "6️⃣" : "6",
    "7️⃣" : "7",
    "8️⃣" : "8",
    "9️⃣" : "9"
}

emclr = {
    "💙🔵🟦" : "blue",
    "💜🟣🟪" : "purple",
    "🧡🟠🟧" : "orange",
    "❤️🔴🟥" : "red",
    "🖤⚫⬛" : "black",
    "💛🟡🟨" : "yellow",
    "🤍⚪⬜" : "white",
    "🤎🟤🟫" : "brown",
    "💚🟩🟢" : "green"
}

color_emojis = {}
for key, value in emclr.items():
    for k in key:
        color_emojis[k] = value

