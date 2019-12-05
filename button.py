#general purpose button class using tkinter
#sticky makes the button latch, otherwise its one press
#if the button is sticky, f is assumed to be continuous and
#should be disableable by calling again (with different arguments)

#Tkinter button was somewhat inadequate

from header import *

class Button:
    buttonDict = {}
    def __init__(self, x, y, width, height, f, name, text="", color="lightblue", altColor="yellow", sticky=False):
        self.id = random.randint(1, 1000000000)
        self.f = f
        self.name = name
        self.text = text
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
        if not self.sticky:
            if not self.isClicked:
                self.isClicked = True
                self.drawColor = self.altColor

                return self.f(**kwargs)

        else:
            if not self.isClicked:
                self.isClicked = True
                self.drawColor = self.altColor

                return self.f(**kwargs)

            else:
                return self.onRelease(**kwargs)




    def clickCheck(self, xC, yC):
        if (xC >= self.x and xC <= self.x + self.width and
            yC >= self.y  and yC <= self.y + self.height):
            return True

        else:
            return False

    def onRelease(self, **kwargs):
        self.isClicked = False
        self.drawColor = self.color

        if self.sticky:
            return self.f(**kwargs)

    def update(self, xC, yC, **kwargs):
        if not self.sticky:
            if self.clickCheck(xC, yC) and not self.isClicked:
                returnVal = self.onClick(**kwargs)

            else:
                returnVal = self.onRelease()

        else:
            if self.clickCheck(xC, yC):
                if not self.isClicked:
                    returnVal = self.onClick(**kwargs)

                else:
                    returnVal = self.onRelease(**kwargs)

        return returnVal


    def draw(self, canvas):
        canvas.create_rectangle(self.x, self.y,
            self.x + self.width, self.y + self.height, fill=self.drawColor)

        if self.text != "":
            canvas.create_text(self.x + self.width/2, self.y + self.height/2,
                        text=self.text, font=("system", 7), justify="center")

class DataButton(Button):
    #making this sticky will probably break it
    def __init__(self, x, y, width, height, f, name, text="", color="lightblue", altColor="yellow", sticky=False):
        super().__init__(x, y, width, height, f, name, text="", color="lightblue", altColor="yellow", sticky=False)
        self.data = None

    def onClick(self, **kwargs):
        if not self.sticky:
            if not self.isClicked:
                self.isClicked = True
                self.drawColor = self.altColor

                return self.data

        else:
            if not self.isClicked:
                self.isClicked = True
                self.drawColor = self.altColor

                return self.data

            else:
                return self.onRelease(**kwargs)

    def onRelease(self, **kwargs):
        self.isClicked = False
        self.drawColor = self.color

        if self.sticky:
            return self.f(**kwargs)
