from math import dist
from imgtrans.textbox import TextBox

#                         _ooOoo_
#                        o8888888o
#                        88" . "88
#                        (| -_- |)
#                        O\  =  /O
#                     ____/`---'\____
#                   .'  \\|     |//  `.
#                  /  \\|||  :  |||//  \
#                 /  _||||| -:- |||||_  \
#                 |   | \\\  -  /'| |   |
#                 | \_|  `\`---'//  |_/ |
#                 \  .-\__ `-. -'__/-.  /
#               ___`. .'  /--.--\  `. .'___
#            ."" '<  `.___\_<|>_/___.' _> \"".
#           | | :  `- \`. ;`. _/; .'/ /  .' ; |
#           \  \ `-.   \_\_`. _.'_/_/  -' _.' /
# ===========`-.`___`-.__\ \___  /__.-'_.'_.-'================
#                         `=--=-'
#                         Moo Fuk
def ocr(filename: str, lang: str = 'en', paragraph: bool = False) -> list[TextBox]:
    from paddleocr import PaddleOCR
    ocr = PaddleOCR(use_angle_cls=True, lang=lang, show_log=False)
    result = ocr.ocr(filename, cls=False)[0]

    tboxes: list[TextBox] = []
    for box, [text, _] in result:
        p1, p2, _, p4 = box

        w = dist(p1, p2)
        h = dist(p1, p4)

        x1, y1 = p1
        x2, y2 = x1 + w, y1 + h

        tbox = TextBox(x1, y1, x2, y2, text)
        tboxes.append(tbox)

    if not paragraph or len(tboxes) < 2:
        return tboxes

    def merge(box1: TextBox, box2: TextBox) -> bool:
        if box2.y1 - box1.y2 < box2.height and box2.x2 > box1.x1 and box2.x1 < box1.x2:
            box1.x1 = min(box1.x1, box2.x1)
            box1.x2 = max(box1.x2, box2.x2)
            box1.y2 = box2.y2
            box1.text += f' {box2.text}'

            return True

        return False

    new_tboxes = [tboxes.pop(0)]
    for tbox in tboxes:
        for new_tbox in new_tboxes:
            if merge(new_tbox, tbox):
                break
        else:
            new_tboxes.append(tbox)

    return new_tboxes
