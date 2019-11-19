from PIL import Image, ImageDraw, ImageFont
import cabinet
import painter
import components
from pathlib import Path
# get an image

def build_capacitors():
    drawer_cfg = cabinet.DrawerConfig(3, 1)
    C_img_url = Path(__file__).parent / 'icons/C_ceramic.png'
    C_img = Image.open(C_img_url)
    drawer_cfg.set_drawer_icon(C_img)
    drawer_cfg.drawer_align_comp_right = False
    drawers_C = cabinet.DrawerCollection(drawer_cfg)

    components_C = components.ComponentCollection()
    components_C.insert_values_as_decades([1.0, 2.2, 4.7], [10 * 1e-12, 100 * 1e-12, 1e-9, 10 * 1e-9], "capacitor")
    capacitors = components_C.get_component_list()
    drawers_C.insert_list(capacitors)
    return drawers_C

def build_transistor():
    drawer_cfg = cabinet.DrawerConfig(3, 1)
    C_img_url = Path(__file__).parent / 'icons/Tnpn.png'
    C_img = Image.open(C_img_url)
    drawer_cfg.set_drawer_icon(C_img)
    drawer_cfg.drawer_align_comp_right = False
    drawers_C = cabinet.DrawerCollection(drawer_cfg)

    components_C = components.ComponentCollection()
    components_C.insert_values(["BC337","BC517","BC547B"],"")
    capacitors = components_C.get_component_list()
    drawers_C.insert_list(capacitors)
    return drawers_C

def build_resistors():
    drawer_cfg = cabinet.DrawerConfig(2, 3)

    components_R = components.ComponentCollection()
    components_R.insert_values_as_decades(
        [1, 1.2, 1.5, 1.8, 2, 2.2, 2.4, 2.7, 3, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]
        , [1, 10, 100, 1000, 10000, 100000], "resistor")
    components_R.insert_values([1 * 10 ** 6, 1.5 * 10 ** 6, 2 * 10 ** 6, 3 * 10 ** 6], "resistor")
    resistors = components_R.get_component_list()
    drawers_R = cabinet.DrawerCollection(drawer_cfg)
    drawers_R.insert_list(resistors)
    return drawers_R

def build(comp,folds,icon,valuelist):
    ''' Takes number of compartments, and the number of paper fold slots within these compartments '''
    drawer_cfg = cabinet.DrawerConfig(comp, folds)
    string = 'icons/'+icon+'.png'
    C_img_url = Path(__file__).parent / string
    C_img = Image.open(C_img_url)
    drawer_cfg.set_drawer_icon(C_img)
    drawer_cfg.drawer_align_comp_right = False
    drawers_C = cabinet.DrawerCollection(drawer_cfg)

    components_C = components.ComponentCollection()
    components_C.insert_values(valuelist,"")
    capacitors = components_C.get_component_list()
    drawers_C.insert_list(capacitors)
    return drawers_C

cabinet = cabinet.Cabinet()
# My component collection

# List all the components I have
drawers_R = build_resistors()
drawers_C = build_capacitors()
drawers_npn = build_transistor()
drawers_pnp = build(3,1,"Tnpn2",["BC327","BC516","BC557B"])

# Store drawers in the cabinet, ready to send the cabinet to the painter
cabinet.load(drawers_R)
cabinet.load(drawers_C)
cabinet.load(drawers_npn)
cabinet.load(drawers_pnp)

# create the PDFs to be printed
s = painter.SheetStack()
s.process_cabinet(cabinet)


