class TextBox():
    def __init__(self, x1: float, y1: float, x2: float, y2: float, text: str) -> None:
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.text = text

    def __iter__(self):
        return iter((self.x1, self.y1, self.x2, self.y2))

    @property
    def width(self) -> int:
        return int(self.x2 - self.x1)

    @property
    def height(self) -> int:
        return int(self.y2 - self.y1)

    @property
    def left(self) -> int:
        return int(self.x1)

    @property
    def top(self) -> int:
        return int(self.y1)
