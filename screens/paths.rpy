
screen mod_paths():
    layer If('mod' in config.layers, 'mod', 'overlay')
    style_prefix 'mod'
    modal True
    default selectedStatementIndex = mod.PathDetection.selectedIndex
    default statements = mod.PathDetection.statements or []
    default selectedIndex = None

    use mod_dialog('Path options', Hide('mod_paths')):
        null height 10

        hbox:
            label '#' xsize mod.scalePxInt(40)
            label 'Active path' xsize mod.scalePxInt(250)
            label 'Code' xsize mod.scalePxInt(150)
            label 'Next label' xsize mod.scalePxInt(300)

        vpgrid: # We need a vpgrid, because a viewport takes up all available height
            cols 1
            draggable True
            mousewheel True
            scrollbars "vertical"

            for i,statement in enumerate(statements):
                hbox:
                    hbox xsize mod.scalePxInt(40):
                        if i < 9:
                            text If(selectedIndex==i, '{b}{u}'+str(i+1)+'{/u}{/b}', '{u}'+str(i+1)+'{/u}')
                            key 'alt_K_{}'.format(i+1) action ToggleScreenVariable('selectedIndex', i, None)
                        else:
                            text str(i+1)

                    hbox xsize mod.scalePxInt(250):
                        if i == selectedStatementIndex:
                            text 'True' color '#baed91'
                        else:
                            text 'False' color '#fea3aa'

                        if statement.condition != 'True':
                            null width mod.scalePxInt(10)
                            use mod_iconbutton('\uf560', If(selectedIndex==i, '{u}C{/u}ondition', 'Condition'), mod.Confirm(prompt=statement.condition, title='Visibility condition', modal=False, promptSubstitution=False), inline=True)
                            if selectedIndex==i:
                                key 'alt_K_c' action mod.Confirm(prompt=statement.condition, title='Visibility condition', modal=False, promptSubstitution=False)
                        elif selectedIndex==i:
                                key 'alt_K_c' action NullAction()

                    hbox xsize mod.scalePxInt(150):
                        if statement.code:
                            use mod_iconbutton('\uf121', If(selectedIndex==i, '{u}S{/u}how', 'Show'), mod.Confirm(prompt=statement.code, title='Choice code', modal=False, promptSubstitution=False), inline=True)
                            if selectedIndex==i:
                                key 'alt_K_s' action mod.Confirm(prompt=statement.code, title='Choice code', modal=False, promptSubstitution=False)
                        else:
                            text 'Not found'
                            if selectedIndex==i:
                                key 'alt_K_s' action NullAction()

                    hbox xsize mod.scalePxInt(300):
                        if statement.jumpTo:
                            use mod_iconbutton('\uf064', If(selectedIndex==i, 'L{u}a{/u}bel', mod.scaleText(statement.jumpTo, 14, 'mod_button_text')), Show('mod_replay_jump', jumpTo=statement.jumpTo), inline=True)
                            if selectedIndex==i:
                                key 'alt_K_a' action Show('mod_replay_jump', jumpTo=statement.jumpTo)
                        else:
                            text 'N/A'
                            if selectedIndex==i:
                                key 'alt_K_a' action NullAction()

                    hbox xsize mod.scalePxInt(150):
                        if statement.Action:
                            use mod_iconbutton('\uf25a', If(selectedIndex==i, '{b}S{u}e{/u}lect{/b}', 'Select'), [statement.Action,Hide('mod_paths')], inline=True)
                            if selectedIndex==i:
                                key 'alt_K_e' action [statement.Action,Hide('mod_paths')]
                                key 'K_KP_ENTER' action [statement.Action,Hide('mod_paths')]
                                key 'K_RETURN' action [statement.Action,Hide('mod_paths')]
                        else:
                            use mod_iconbutton('\uf25a', 'Select', inline=True)
                            textbutton "\uf128" style_suffix "mod_icon_inlinebutton" yalign .5 action mod.Confirm(title='Not forceable', prompt='This path cannot be force selected\nProbably because it\'s behind a call or jump')
