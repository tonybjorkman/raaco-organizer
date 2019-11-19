from math import log,floor
from decimal import Decimal
from PIL import Image, ImageDraw, ImageFont


class Component:
    def __init__(self, value,suffix):
        self.value = value
        self.suffix = suffix
        self.text = value

    def paint_graphics(self, width, height):
        return None

    def convert_prefix(self,value):
        prefixes = [(6,"M"),(3,"K"),(0,""),(-3,"m"),(-6,"u"),(-9,"n"),(-12,"p")]

        for pref in prefixes:
            if value >= 10**pref[0]:
                return str(round(value/10**pref[0],1)).rstrip("0").rstrip(".")+" "+pref[1]
            if value < 10**-12:
                return str(value / 10 ** -12).rstrip("0").rstrip(".") + " " + "p"



class Resistor(Component):
    def __init__(self, value):
        super().__init__(value,"Ω")
        self.text = self.convert_prefix(value) + self.suffix

# Paint resistor-codes that fills up the allowed space
    def paint_graphics(self,width,height):
        image = Image.new('RGB', (width,height), (255, 255, 255))
        draw = ImageDraw.Draw(image)

        # resistor color code

        offset = 0
        c_width = width/5
        c_height = 60
        for color in self.get_resistor_colors(1):
            draw.rectangle(((offset * c_width,
                             0),
                            ((offset + 1) * c_width,
                             c_height + 0)), fill=color,
                           outline="black", width=4)
            offset += 1

        return image

    def get_resistor_colors(self, tolerance_inx):
        digit_to_color = {
            -2: "silver",
            -1: "gold",
            0: "black",
            1: "brown",
            2: "red",
            3: "orange",
            4: "yellow",
            5: "green",
            6: "blue",
            7: "violet",
            8: "grey",
            9: "white"
        }

        #Cases:
        #1. 1ohm, should be blk-blk-brown-blk
        #2. 1.1ohm should be brown-brown-black-silver

        #-2 because first three values in 123ohm contains the multiple 100 for 1.23

        multiplier = floor(log(self.value, 10))-2

        scinot = '%E' % self.value
        value_digits = int(scinot.split('E')[0].rstrip('0').rstrip('.').replace(".",""))
        #make it into three digits
        while value_digits < 100:
            value_digits*=10

        color_digit_list = [int(dig) for dig in str(value_digits)]
        color_digit_list.append(multiplier)
        color_digit_list.append(tolerance_inx)
        return [digit_to_color.get(inx) for inx in color_digit_list]

class ZenerDiode(Component):
    def __init__(self, value):
        super().__init__(value,"V")
        self.text = self.convert_prefix(value) + self.suffix

    def paint_graphics(self,width,height):
        return None


class Capacitor(Component):
    def __init__(self, value):
        super().__init__(value,"F")
        self.text = self.convert_prefix(value) + self.suffix

    def paint_graphics(self,width,height):
        return None

class ComponentCollection:

    def __init__(self):
        self.componentlist = list()

    def component_factory(self,component_type,value):
        if component_type=="":
            return Component(value,"")
        elif component_type=="resistor":
            return Resistor(value)
        elif component_type=="capacitor":
            return Capacitor(value)
        elif component_type=="zenerdiode":
            return ZenerDiode(value)

    def insert_values_as_decades(self,values_per_decade,decades,component):
        self.componentlist = [self.component_factory(component,x * y) for x in decades for y in values_per_decade]

    def insert_values(self, valuelist, component=""):
        self.componentlist.extend([self.component_factory(component,x) for x in valuelist])

    def get_component_list(self):
        return self.componentlist





def main():
    r = ComponentCollection([1, 1.2, 1.5, 1.8], "Ω")


    c = Component(123,"ohm");
    print(str(c.get_resistor_colors(1)))


if __name__ == "__main__":
    main()