#general purpose button class using tkinter
#wait makes the button latch, otherwise its one press
#if the button is wait, will wait for a second click event before running f

#Tkinter button wasn't versatile enough so I made my own (superior) button

from header import *

class Button:
    buttonDict = {}
    def __init__(self, x, y, width, height, f, name, text="", wait=False, color="lightblue", altColor="yellow"):
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

        self.wait = wait #if true button will stay clicked until clicked again

        Button.buttonDict[name] = self
#        print("added", name)

    def onClick(self, **kwargs):
        if not self.wait:
            if not self.isClicked:
                self.isClicked = True
                self.drawColor = self.altColor

                return self.f(**kwargs)

        else:
            if not self.isClicked:
                self.isClicked = True
                self.drawColor = self.altColor

    def clickCheck(self, xC, yC):
        if (xC >= self.x and xC <= self.x + self.width and
            yC >= self.y  and yC <= self.y + self.height):
            return True

        else:
            return False

    def onRelease(self, **kwargs):
        self.isClicked = False
        self.drawColor = self.color

        if self.wait:
            return self.f(**kwargs)

    def update(self, xC, yC, **kwargs):
        if not self.wait:
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
    #making this wait will probably break it
    #f will not be called ever - set to None
    def __init__(self, x, y, width, height, f, name, text="", color="lightblue", altColor="yellow", wait=False):
        super().__init__(x, y, width, height, f, name, text="", color="lightblue", altColor="yellow", wait=False)
        self.data = None
        self.text = "No data"

    def onClick(self, **kwargs):
        if not self.wait:
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

        if self.wait:
            return self.data

    def draw(self, canvas):
        #changin how text is displayed
        canvas.create_rectangle(self.x, self.y,
            self.x + self.width, self.y + self.height, fill=self.drawColor)

        if self.text != "":
            canvas.create_text(self.x + self.width/2, self.y + self.height/2,
                        text=self.text, font=("system", 8), justify="left")
