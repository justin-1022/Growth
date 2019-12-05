#general purpose button class using tkinter
#sticky makes the button latch, otherwise its one press
#if the button is sticky, f is assumed to be continuous and
#should be disableable by calling again (with different arguments)

class Button:
    buttonDict = {}
    def __init__(self, x, y, width, height, f, name, color="black", altColor="grey", sticky=False):
        self.id = random.randint(1, 1000000000)
        self.f = f
        self.name = name
        #when clicked button swaps to alt color
        self.color = color
        self.drawColor = color
        self.altColor = altColor
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.isClicked = False

        self.sticky = sticky #if true button will stay clicked until clicked again

        Button.buttonDict[name] = self

    def onClick(self, **kwargs):
        self.isClicked = True
        self.drawColor = self.altColor
        self.f(**kwargs)

    def clickCheck(self, xC, yC):
        if (xC >= self.x and xC <= self.x + self.width and
            yC >= self.y  and yC <= self.y + self.height:
            return True

        else:
            return False

    def onRelease(self, **kwargs):
        self.isClicked = False
        self.drawColor = self.color

        if self.sticky:
            self.f(**kwargs)

    def update(self, xC, yC, **kwargs):
        if not self.sticky:
            if self.clickCheck(xC, yC) and not self.isClicked:
                self.onClick(**kwargs)

            else:
                self.onRelease()

        else:
            if self.clickCheck(xC, yC):
                if not self.isClicked:
                    self.onClick(**kwargs)

                else:
                    self.onRelease(**kwargs)


    def draw(self, canvas):
        canvas.create_rect(self.x, self.y,
            self.x + self.width, self.y + self.height, fill=self.drawColor)
