
screen mod_colorpicker(callback, onClose, defaultColor=None):
    layer If('mod' in config.layers, 'mod', 'overlay')
    style_prefix "mod"
    modal True

    default colorPicker = modColorPicker(defaultColor)
    default colorPresets = [(0, 0, 0), (12, 19, 79), (29, 38, 125), (92, 70, 156), (212, 173, 252), (255, 255, 255)]

    use mod_dialog(title='Colorpicker', closeAction=onClose):
        label 'Current:'
        frame xsize mod.scalePxInt(230) ysize 30:
            background Solid(colorPicker.hex)
            text ''

        null height mod.scalePxInt(5)

        hbox: # Color presents
            spacing 3
            for preset in colorPresets:
                imagebutton:
                    idle Solid(Color((preset[0], preset[1], preset[2], 175)))
                    hover Solid(Color(preset))
                    xsize 20 ysize 20
                    action SetField(colorPicker, 'rgba', preset)

        null height mod.scalePxInt(10)

        hbox ysize mod.scalePxInt(250) xsize mod.scalePxInt(230):
            vbox:
                text "R" xalign .5 color '#ffadad' size 34 outlines [(2, '#222', 0, 0)]
                vbar xoffset 4:
                    value FieldValue(colorPicker, 'r', 255, step=1)
            vbox:
                text "G" xalign .5 color '#adffad' size 34 outlines [(2, '#222', 0, 0)]
                vbar xoffset 4:
                    value FieldValue(colorPicker, 'g', 255, step=1)
            vbox:
                text "B" xalign .5 color '#3572ff' size 34 outlines [(2, '#222', 0, 0)]
                vbar xoffset 4:
                    value FieldValue(colorPicker, 'b', 255, step=1)
            vbox:
                text "A" xalign .5 size 34 outlines [(2, '#222', 0, 0)]
                vbar xoffset 4:
                    value FieldValue(colorPicker, 'a', 1.0, step=.1)

        hbox yoffset 10:
            textbutton 'Apply' action [Function(callback, colorPicker.hex), onClose]
            textbutton 'Cancel' action onClose
