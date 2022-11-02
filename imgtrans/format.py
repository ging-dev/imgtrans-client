from imgtrans.textbox import TextBox

def format_tboxes(tboxes: list[TextBox]):
    return map(lambda tbox: ((tbox.x1, tbox.y1, tbox.x2, tbox.y2), tbox.text), tboxes)
