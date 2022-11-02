import googletrans
from wand.image import Image
from imgtrans.format import format_tboxes
from imgtrans.textbox import TextBox

def rectangle(image: Image, tboxes: list[TextBox], transparent: bool = False):
    from wand.drawing import Drawing, Color

    with Drawing() as draw:
        draw.stroke_color = Color('blue')
        draw.fill_color = Color('white')
        if transparent:
            draw.fill_opacity = 0
        for (x1, y1, x2, y2), _ in format_tboxes(tboxes):
            draw.rectangle(left=x1, top=y1, right=x2, bottom=y2)
        draw(image)

    return image

def translate(image: Image, tboxes: list[TextBox]):
    from wand.font import Font
    from . import constant

    font = Font(constant.FONT_PATH)
    for (x1, y1, x2, y2), text in format_tboxes(tboxes):
        text = googletrans.Translator().translate(text.lower(), dest='vi').text  # type: ignore
        # draw to bounding box
        image.caption(
            text,
            left=int(x1),
            top=int(y1),
            width=int(x2-x1),
            height=int(y2-y1),
            font=font,
            gravity='center'
        )

    return image
