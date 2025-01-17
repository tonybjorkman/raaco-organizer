from interfaces import *
from PIL import Image,ImageDraw,ImageFont
import components

def cm_to_px( cm):
    return round(cm * 236.22)

def rotated_text(text,angle,font):
    image = Image.new('RGB', (1, 1), (255, 255, 255))
    draw_txt = ImageDraw.Draw(image)
    #width, height = draw_txt.textsize(text,font=font)
    bbox = font.getbbox(text)

    # Calculate text width and height from the bounding box
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    print("{} has width: {} height: {}".format(text,width,height))
    # TODO only a quick fix for the height to multiply with 2! 
    image2 = Image.new('RGB', (width, height*2), (255, 255, 255))
    draw_txt2 = ImageDraw.Draw(image2)
    draw_txt2.text((0, 0), text, font=font, fill=(0, 0, 0))
    image2=image2.rotate(angle)
    return image2

class DrawerConfig:
    def __init__(self,num_comp,num_folds):
        self.drawer_width=cm_to_px(5)
        self.drawer_height = cm_to_px(2.9)
        self.drawer_label_height = cm_to_px(1)
        self.drawer_depth = cm_to_px(13.3)
        self.drawer_compartments = num_comp
        self.compartment_num_folds = num_folds #max_folds
        self.drawer_component_icon = None
        self.drawer_align_comp_right = False # treat the front drawer compartment positioning as if there were 3 compartments.

        self.comp_width = None
        self.comp_height = None
        self.comp_fold_length = None
        self.recalculate_compartments()

    def set_drawer_3comp_front_layout(self,value):
        self.drawer_align_comp_right=value

    def recalculate_compartments(self):
        self.comp_width = int(self.drawer_depth / self.drawer_compartments - (self.drawer_compartments - 1) * cm_to_px(
            0.3))  # old cm_to_px(6.5)
        self.comp_height = self.drawer_height
        self.comp_fold_length = int(self.drawer_width / self.compartment_num_folds * 0.8)  # cm_to_px(1.3)

    def setDrawer(self,width,height,depth,num_comp):
        self.drawer_width=width
        self.drawer_height = height
        self.drawer_depth = depth
        self.drawer_compartments = num_comp
        self.recalculate_compartments()

    def set_drawer_icon(self,image):
        self.drawer_component_icon = image

    def setDrawerDepth(self,depth):
        self.drawer_depth=depth
        self.recalculate_compartments()

    def setCompartment(self,num_folds):
        self.compartment_num_folds = num_folds
        self.recalculate_compartments()

    def getCompartment(self):
        return Compartment(self)

    def getDrawer(self):
        return Drawer(self)

class Cabinet:
    def __init__(self):
        self.drawer_collections = list()

    def load(self,dcollection):
        self.drawer_collections.append(dcollection)

class DrawerCollection:
    def __init__(self,drawerCfg):
        self.drawers=list()
        self.drawerCfg=drawerCfg

    def insert_value(self, value):
        if not self.room_in_last_drawer():
            d = Drawer(self.drawerCfg)
            self.drawers.append(d)

        self.drawers[-1].insert(value)

    def insert_list(self,val_list):
        for e in val_list:
            self.insert_value(e)


    def room_in_last_drawer(self):
        if len(self.drawers) > 0:
            return self.drawers[-1].has_room()
        else:
            return False

    def get_compartments(self):
        comps=list()
        for d in self.drawers:
            for c in d.compartments:
                comps.append(c)

        return comps

    def get_drawers(self):
        return self.drawers

class Drawer(IPaintable):

    #There is a compartment which is not yet full or there is place for a new compartment
    #case 1: has no compartments
    #case 2: has compartment with 1 value
    #case 3: has compartment which is full
    #case 4: has maximum comaprtment but room in last one
    #case 5: has max comapartment and no space in last. completely full.

    def __init__(self,cabinetCfg):
        self.compartments=list()
        self.max_compartments=cabinetCfg.drawer_compartments
        self.width = cabinetCfg.drawer_width
        self.height = cabinetCfg.drawer_label_height
        self.cabin_cfg = cabinetCfg
        self.drawer_component_icon = cabinetCfg.drawer_component_icon



    def insert(self,value):
        if not self.has_room():
            raise ValueError("bad! tried to insert in already full drawer")

        #Do i need to create new compartment? case1+3
        if len(self.compartments) == 0 or not self.compartments[-1].has_room():
            self.compartments.append(Compartment(self.cabin_cfg))

        self.compartments[-1].insert(value)

    # this case only covers case5.
    def has_room(self):
        if len(self.compartments) == self.max_compartments and not self.compartments[-1].has_room():
            return False
        else:
            return True

    def paint(self):
        line_width=8
        side_padding=40
        line_height = 70
        image = Image.new('RGB', (self.width,self.height), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        fnt = ImageFont.truetype('C:\Windows\Fonts\FRAMDCN.TTF', 80)
        draw.rectangle(((1,1), (self.width,self.height)), outline="black", width=line_width)
        num_comp = len(self.compartments)
        if self.cabin_cfg.drawer_align_comp_right:
            num_comp = 3
            side_offset = int(self.width /3)*2
        else:
            side_offset = int(self.width/num_comp)
        comp_inx=0
        fold_inx=0
        comp_g_top_padding = 14 # to keep the comp_grap from being pasted on top of border

        for comp in self.compartments:
            for x in comp.folds:
                draw.text((side_padding+comp_inx*side_offset, line_height*fold_inx), x.component.text, font=fnt, fill=(0, 0, 0))

                txtsize= [220,0]#draw.textsize(x.component.text,fnt)
                comp_graph_height = int((self.height-comp_g_top_padding-line_width)/self.cabin_cfg.compartment_num_folds)
                comp_graph_width = int(self.width/self.max_compartments-txtsize[0]-side_padding-16)
                # paints optional graphics, for resistors its the color code
                comp_image = x.component.paint_graphics(comp_graph_width, comp_graph_height)
                fold_dist = txtsize[0]+10 #230 #Should be to the right of text. 0 is same as text.
                #possibly paint the component graphics onto the drawer
                if comp_image is not None:
                    image.paste(comp_image, (side_padding+comp_inx*side_offset+fold_dist, comp_g_top_padding+line_height*fold_inx))

                fold_inx+=1
            comp_inx+=1
            fold_inx=0

        if self.cabin_cfg.drawer_component_icon is not None:
            icon = self.cabin_cfg.drawer_component_icon
            icon = icon.resize((300,150))
            y_offset=0
            if self.cabin_cfg.drawer_align_comp_right:
                y_offset=-line_height/2
            image_at_drawer_center = (int(self.width/2-icon.width/2),
                                      int((self.height-line_height)/2-icon.height/2+line_height+y_offset))
            image.paste(icon,image_at_drawer_center,mask=icon.split()[3])

        return image

class Compartment(IPaintable):

    def __init__(self,cabinet_cfg):
        self.folds=list()
        self.max_folds = cabinet_cfg.compartment_num_folds
        self.width = cabinet_cfg.comp_width
        self.height = cabinet_cfg.comp_height
        self.fold_length = cabinet_cfg.comp_fold_length
        self.cabin_builder = cabinet_cfg

    def insert(self,value):
        if not self.has_room():
            raise ValueError("tried to insert in full Compartment")

        self.folds.append(Fold(value))

    # the folds of the compartment are not all occupied
    def has_room(self):
        return len(self.folds) < self.max_folds

    #calculate the full area that the compartment would use on a canvas
    #height and width relates to the standing A4 paper where the compartment will be cut out as height>width.
    def getPaintSize(self):
        height=int((self.height*2+self.fold_length)*self.max_folds+30)
        width=int(self.width)
        return width ,height

    def paint(self):
        w,h = self.getPaintSize()
        image = Image.new('RGB', (w,h), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        line_width=5
        side_padding=200

        fnt = ImageFont.truetype('C:\Windows\Fonts\FRAMDCN.TTF', 200)
        tiny_fnt = ImageFont.truetype('C:\Windows\Fonts\FRAMDCN.TTF', 170)

        indexf=0;

        for f in self.folds:
            #step per complete fold
            complete_foldstep = indexf*(self.height*2+self.fold_length)
            start = (1,1+complete_foldstep)
            stop = (self.width,1+self.height + complete_foldstep)
            draw.rectangle((start,stop),outline="black",width=line_width)
            
            if isinstance(f.component, components.Resistor):
                # resistor color code
                fold_dist=30
                offset=0
                c_width=120
                c_height=120
                for color in f.component.get_resistor_colors(1):
                    draw.rectangle(((890+offset*c_width,start[1]+fold_dist), (890+(offset+1)*c_width-10,start[1]+c_height+fold_dist)),fill=color, outline="black", width=line_width)
                    offset+=1

            #first title
            draw.text((start[0]+side_padding,start[1]+5),str(f.component.text),font=fnt,fill=(0,0,0))
            start = (1,stop[1]+self.fold_length)
            # TODO fix line below that i commented out 

            draw.rectangle(((start[0],stop[1]), (stop[0],start[1])), outline="black", width=line_width)
            
            #bottom_title
            draw.text((start[0] + side_padding, stop[1] + 5), str(f.component.text), font=tiny_fnt, fill=(0, 0, 0))
            stop = (self.width,start[1]+self.height)
            draw.rectangle((start, stop), outline="black", width=line_width)

            if isinstance(f.component, components.Resistor):
                # resistor color code
                offset=0
                c_width=120
                c_height=120
                for color in reversed(f.component.get_resistor_colors(1)):
                    draw.rectangle(((50+offset*c_width,stop[1]-c_height-fold_dist), (50+(offset+1)*c_width-10,stop[1]-fold_dist)),fill=color, outline="black", width=line_width)
                    offset+=1

            #rotated title
            rot_img = rotated_text(str(f.component.text),180,fnt)
            image.paste(rot_img,(stop[0]-rot_img.width-side_padding,stop[1]-rot_img.height-5))
            indexf+=1
        return image

class Fold:
    def __init__(self, component):
        self.component=component
