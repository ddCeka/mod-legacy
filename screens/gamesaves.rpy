
screen mod_gamesaves():
    style_prefix 'mod'
    default slotRegEx = '([0-9]+|quick)-([0-9]+)'

    hbox:
        vbox xsize mod.scaleX(23):
            hbox xsize mod.scaleX(23):
                label 'Quick resume' yalign .5
                textbutton "\uf128" style_suffix "icon_button" xalign 1.0 tooltip "Explain quick resume" action mod.Confirm("""The game will immediately load this save after starting the game\nThis skips the title screen and menu, you're directly back in the game\n\n{b}IMPORTANT:{/b} This save will be deleted after it has been loaded""", title='Quick resume')
            use mod_gamesaves_button('_reload-1')

            null height mod.scalePxInt(10)

            label 'Newest save'
            use mod_gamesaves_button(renpy.newest_slot(slotRegEx))

        frame style_suffix "vseperator" xsize mod.scalePxInt(2)

        vbox:
            fixed ysize mod.scalePxInt(50):
                hbox yalign .5:
                    text mod.Gamesaves.pageName yalign .5 substitute False style_suffix 'label_text'
                    textbutton "\uf304" style_suffix "icon_button" xalign 1.0 tooltip "Rename page" action Show('mod_gamesaves_pagename')

                # PAGES
                hbox xalign 1.0:
                    textbutton "\uf049" style_suffix 'icon_button' sensitive (mod.Gamesaves.page != 1) action SetField(mod.Gamesaves, 'page', 1) yalign .5 tooltip 'Go to first page'
                    textbutton "\uf048" style_suffix 'icon_button' sensitive (mod.Gamesaves.page != mod.Gamesaves.prevPage) action SetField(mod.Gamesaves, 'page', mod.Gamesaves.prevPage) yalign .5 tooltip 'Go to previous page'

                    textbutton 'A' sensitive ('auto' != mod.Gamesaves.page) action SetField(mod.Gamesaves, 'page', 'auto') tooltip 'Go to auto save page'
                    textbutton 'Q' sensitive ('quick' != mod.Gamesaves.page) action SetField(mod.Gamesaves, 'page', 'quick') tooltip 'Go to quick save page'
                    for page in mod.Gamesaves.pageRange:
                        textbutton If(page<10, '0[page]', '[page]') sensitive (page != mod.Gamesaves.page) action SetField(mod.Gamesaves, 'page', page)

                    textbutton "\uf051" style_suffix 'icon_button' action SetField(mod.Gamesaves, 'page', mod.Gamesaves.nextPage) yalign .5 tooltip 'Go to next page'
                    textbutton "\uf246" style_suffix 'icon_button' action Show('mod_gamesaves_pagenumber') yalign .5 tooltip 'Enter page number'

            frame style_suffix "seperator" ysize mod.scalePxInt(2)
            
            vpgrid:
                xfill True yfill True
                cols 3
                mousewheel True
                draggable True
                scrollbars "vertical"
                spacing mod.scalePxInt(15)

                for position in range(1,10):
                    use mod_gamesaves_button('{}-{}'.format(mod.Gamesaves.page, position))


screen mod_gamesaves_button(slot):
    default thumbnailScale = 23

    vbox:
        button:
            xsize mod.scaleX(thumbnailScale) ysize mod.scaleY(thumbnailScale)
            if renpy.can_load(slot):
                action Function(mod.Gamesaves.load, slot)
                add modGameSaves.SlotScreenshot(slot) xalign .5 yalign .5
                label mod.Gamesaves.slotTime(slot) xalign .5
                text mod.Gamesaves.slotName(slot) xalign .5 yalign 1.0 substitute False text_align .5
            else:
                action Function(mod.Gamesaves.save, slot)
                text 'Empty' xalign .5 yalign .5

        hbox xsize mod.scaleX(thumbnailScale):
            hbox:
                textbutton "\uf093" style_suffix "icon_button" tooltip 'Load game' action If(renpy.can_load(slot), Function(mod.Gamesaves.load, slot), None)
                textbutton "\uf019" style_suffix "icon_button" tooltip 'Save game' action Function(mod.Gamesaves.save, slot)

            hbox xalign 1.0:
                textbutton "\uf56f" style_suffix "icon_button" tooltip 'Move save' action If(renpy.can_load(slot), Function(mod.Gamesaves.move, slot), None)
                textbutton "\uf0c5" style_suffix "icon_button" tooltip 'Copy save' action If(renpy.can_load(slot), Function(mod.Gamesaves.copy, slot), None)
                textbutton "\uf2ed" style_suffix "icon_button" tooltip 'Delete save' action If(renpy.can_load(slot), Function(mod.Gamesaves.delete, slot), None)


screen mod_gamesaves_selectslot(defaultPage, defaultPosition, callback, confirmButtonText='OK'):
    layer If('mod' in config.layers, 'mod', 'overlay')
    style_prefix "mod"
    
    default inputs = InputGroup([
            ('page', Input(text=defaultPage)),
            ('position', Input(text=defaultPosition)),
        ],
        focusFirst=True,
        onSubmit=[Function(callback, GetScreenInput('page', 'inputs'), GetScreenInput('position', 'inputs')),Hide('mod_gamesaves_selectslot')],
    )

    key 'K_TAB' action inputs.NextInput()
    key 'shift_K_TAB' action inputs.PreviousInput()

    use mod_dialog(title='Select save slot', closeAction=Hide('mod_gamesaves_selectslot'), modal=True):
        text "Page:"
        button:
            xminimum mod.scalePxInt(450)
            key_events True
            action inputs.page.Enable()
            input value inputs.page allow '0123456789'

        text "Position:"
        button:
            xminimum mod.scalePxInt(450)
            key_events True
            action inputs.position.Enable()
            input value inputs.position allow '123456789' length 1

        hbox:
            yoffset mod.scalePxInt(15)
            align (1.0,1.0)
            textbutton confirmButtonText style_suffix "primary_button" action inputs.onSubmit
            null width mod.scalePxInt(10)
            textbutton "Cancel" action Hide('mod_gamesaves_selectslot')


screen mod_gamesaves_pagenumber():
    layer If('mod' in config.layers, 'mod', 'overlay')
    style_prefix "mod"
    
    default pageInput = Input(text=str(mod.Gamesaves.page), autoFocus=True, onEnter=[mod.Gamesaves.SetPage(GetScreenInput('pageInput')),Hide('mod_gamesaves_pagenumber')])

    use mod_dialog(title='Enter a page number', closeAction=Hide('mod_gamesaves_pagenumber'), modal=True):
        text "Page:"
        button:
            style_suffix 'inputframe'
            xminimum mod.scalePxInt(350)
            key_events True
            action pageInput.Enable()
            input value pageInput allow '0123456789'

        hbox:
            yoffset mod.scalePxInt(15)
            align (1.0,1.0)
            textbutton 'Open' style_suffix "primary_button" action pageInput.onEnter
            null width mod.scalePxInt(10)
            textbutton "Cancel" action Hide('mod_gamesaves_pagenumber')


screen mod_gamesaves_pagename():
    layer If('mod' in config.layers, 'mod', 'overlay')
    style_prefix "mod"
    
    default pageNameInput = Input(text=mod.Gamesaves.pageName, autoFocus=True, onEnter=[mod.Gamesaves.SetPageName(GetScreenInput('pageNameInput')),Hide('mod_gamesaves_pagename')])

    use mod_dialog(title='Change page name', closeAction=Hide('mod_gamesaves_pagename'), modal=True):
        text "Page name:"
        button:
            style_suffix 'inputframe'
            xminimum mod.scalePxInt(350)
            key_events True
            action pageNameInput.Enable()
            input value pageNameInput length 50

        hbox:
            yoffset mod.scalePxInt(15)
            align (1.0,1.0)
            textbutton 'Change' style_suffix "primary_button" action pageNameInput.onEnter
            null width mod.scalePxInt(10)
            textbutton "Cancel" action Hide('mod_gamesaves_pagename')

screen mod_gamesaves_savename(callback):
    layer If('mod' in config.layers, 'mod', 'overlay')
    style_prefix "mod"
    
    default inputSaveName = Input(autoFocus=True, onEnter=[Function(callback, GetScreenInput('inputSaveName')),Hide('mod_gamesaves_savename')])

    use mod_dialog(title='Save description', closeAction=Hide('mod_gamesaves_savename'), modal=True):
        text "Save name:"
        button:
            style_suffix 'inputframe'
            xminimum mod.scalePxInt(350)
            key_events True
            action inputSaveName.Enable()
            input value inputSaveName length 150

        hbox:
            yoffset mod.scalePxInt(15)
            align (1.0,1.0)
            textbutton 'Save' style_suffix "primary_button" action inputSaveName.onEnter
            null width mod.scalePxInt(10)
            textbutton "Cancel" action Hide('mod_gamesaves_savename')
