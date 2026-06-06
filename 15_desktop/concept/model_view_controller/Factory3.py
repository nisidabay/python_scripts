#!/usr/bin/python3
class Button:
    html = ""

    def get_html(self):
        return self.html


class Image(Button):
    html = "<img></img>"


class Input(Button):
    html = "<input></input>"


class Flash(Button):
    html = "<obj></obj>"


class ButtonFactory():
    @staticmethod
    def create_button(kind):
        targetclass = kind.capitalize()
        return globals()[targetclass]()


if __name__ == "__main__":
    button_obj = ButtonFactory()
    button = ['image', 'input', 'flash']
    for b in button:
        print(button_obj.create_button(b).get_html())
