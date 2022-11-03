import googletrans
from wand.image import Image
from imgtrans.textbox import TextBox

def rectangle(image: Image, tboxes: list[TextBox], transparent: bool = False):
    from wand.drawing import Drawing, Color

    with Drawing() as draw:
        draw.stroke_color = Color('blue')
        draw.fill_color = Color('white')
        if transparent:
            draw.fill_opacity = 0
        for tbox in tboxes:
            x1, y1, x2, y2 = tbox
            draw.rectangle(left=x1, top=y1, right=x2, bottom=y2)
        draw(image)

    return image

def translate(image: Image, tboxes: list[TextBox]):
    from wand.font import Font
    from . import constant

    font = Font(constant.FONT_PATH)
    for tbox in tboxes:
        text = googletrans.Translator().translate(tbox.text.lower(), dest='vi').text  # type: ignore
        image.caption(
            text,
            left=tbox.left,
            top=tbox.top,
            width=tbox.width,
            height=tbox.height,
            font=font,
            gravity='center'
        )

    return image
