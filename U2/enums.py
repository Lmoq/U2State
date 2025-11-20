from enum import Enum


class Wtype( Enum ):
    clickable = "android.widget.TextView"
    text = "android.view.ViewGroup"
    button = "android.widget.Button"
    editText = "android.widget.EditText"
    image = "android.widget.ImageView"


class ActionType( Enum ):
    action = 0
    click = 1
    swipe = 2
    write = 3
    wait = 4
    check = 5


class TaskType( Enum ):
    check = 1000
    wait = 2000


class Direction( Enum ):
    left = "left"
    up = "up"
    right = "right"
    down = "down"
