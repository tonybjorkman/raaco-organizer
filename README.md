# raaco-organizer
Script for creating printable A4 PDF folding-labels for electrical components fitting Raaco storage drawers. Creates two types of labels, drawer front labels and folded compartment labels inside the drawers.
## Usage
When properly configured, the only input required is component values, type of component and drawer size(#compartments and #folds).

Declare you component collection under raaco_organizer.py, example of how a large series of resistor is added and printed to pdf is shown below.
```
drawer_cfg = cabinet.DrawerConfig(2, 3)
components_R = components.ComponentCollection()
components_R.insert_values_as_decades(
    [1, 1.2, 1.5, 1.8, 2, 2.2, 2.4, 2.7, 3, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]
    , [1, 10, 100, 1000, 10000, 100000], "resistor")
components_R.insert_values([1 * 10 ** 6, 1.5 * 10 ** 6, 2 * 10 ** 6, 3 * 10 ** 6], "resistor")
resistors = components_R.get_component_list()
drawers_R = cabinet.DrawerCollection(drawer_cfg)
drawers_R.insert_list(resistors)

cabinet.load(drawers_R)
s = painter.SheetStack()
s.process_cabinet(cabinet)
```

## Features
* resistor color coding according to IEC 60062:2016
* custom icons for front labels
* configurable number of compartments in each drawer
* configurable number of folds in each compartment

Labels from A4 paper, cut out, folded and put into the raaco drawers
![Finished labels](https://github.com/tonybjorkman/raaco-organizer/blob/master/doc/finished_labels.jpg)

Raw A4 PDF printout
![Raw labels](https://github.com/tonybjorkman/raaco-organizer/blob/master/doc/single%20page%20result.png)
