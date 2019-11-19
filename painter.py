from PIL import Image,ImageDraw

class SheetStack:
    def __init__(self):
        self.compartmentSheets=list()
        self.frontLabelSheets=list()

    #takes a compartment as input
    def paint(self,paintables):
        for paintable in paintables:
            newpaint = paintable.paint()
            sheet = self.getUsableSheet(self.compartmentSheets,newpaint)
            sheet.canvas.paste(newpaint, (sheet.x_pos,sheet.y_pos))

    def process_cabinet(self,cabinet):
        for drawercollection in cabinet.drawer_collections:
            self.paint(drawercollection.get_compartments())
            self.paintFrontLabels(drawercollection.get_drawers())
        self.save_sheets()


    #takes a drawer as input
    def paintFrontLabels(self,paintables):
        for paintable in paintables:
            newpaint = paintable.paint()
            sheet = self.getUsableSheet(self.frontLabelSheets, newpaint)
            sheet.canvas.paste(newpaint, (sheet.x_pos,sheet.y_pos))


    def getUsableSheet(self,sheetList,image):
        if len(sheetList) == 0:
            sheetList.append(Sheet())
            return sheetList[-1]
        #cant grow to the side or down
        if image.width*2 + sheetList[-1].x_pos > sheetList[-1].width and image.height*2 + sheetList[-1].y_pos > sheetList[-1].height:
            sheetList.append(Sheet())
            return sheetList[-1]
        elif image.height*2 + sheetList[-1].y_pos > sheetList[-1].height:
            sheetList[-1].x_pos +=image.width
            sheetList[-1].y_pos = 0
            return sheetList[-1]
        else:
            sheetList[-1].y_pos += image.height
            return sheetList[-1]

    def save_sheets(self):
        i=0
        for s in self.compartmentSheets:
            s.canvas.save("img"+str(i)+".pdf")
            i+=1
        i = 0
        for f in self.frontLabelSheets:
            f.canvas.save("img-label" + str(i) + ".pdf")
            i += 1

class Sheet:
    def __init__(self):
        self.width=round(4962*0.95) #add margin
        self.height=round(7014*0.95) #add margin
        self.x_pos=0
        self.y_pos=0
        self.canvas = Image.new('RGB', (self.width, self.height), (255, 255, 255))




