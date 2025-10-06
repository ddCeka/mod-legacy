
screen mod_choices():
    layer If('mod' in config.layers, 'mod', 'overlay')
    style_prefix 'mod'
    modal True
    default choices = mod.Choices.currentChoices or []
    default selectedIndex = None

    use mod_dialog('Choices', Hide('mod_choices')):
        null height 10
        hbox:
            label '#' xsize mod.scalePxInt(40)
            label 'Choice' xsize mod.scalePxInt(350)
            label 'Visible' xsize mod.scalePxInt(260)
            label 'Code' xsize mod.scalePxInt(150)
            label 'Next label' xsize mod.scalePxInt(300)

        vpgrid: # We need a vpgrid, because a viewport takes up all available height
            cols 1
            draggable True
            mousewheel True
            scrollbars "vertical"

            for i,choice in enumerate(choices):
                hbox:
                    hbox xsize mod.scalePxInt(40):
                        if i < 9:
                            text If(selectedIndex==i, '{b}{u}'+str(i+1)+'{/u}{/b}', '{u}'+str(i+1)+'{/u}')
                            key 'alt_K_{}'.format(i+1) action ToggleScreenVariable('selectedIndex', i, None)
                        else:
                            text str(i+1)

                    hbox xsize mod.scalePxInt(350):
                        hbox:
                            text mod.scaleText(choice.text, 14) substitute False
                            null width mod.scalePxInt(10)
                            if choice.text in mod.TextRepl.replacements:
                                textbutton '\uf044' style_suffix 'icon_inlinebutton' action Show('mod_add_textrepl', defaultOriginal=choice.text, defaultReplacement=mod.TextRepl.replacements[choice.text].replacement, blockOriginal=True)
                            else:
                                textbutton '\uf044' style_suffix 'icon_inlinebutton' action Show('mod_add_textrepl', defaultOriginal=choice.text, defaultReplacement=choice.text, blockOriginal=True)

                    hbox xsize mod.scalePxInt(260):
                        if choice.isVisible:
                            text 'True' color '#baed91'
                        else:
                            text 'False' color '#fea3aa'
                        if choice.condition != 'True':
                            null width mod.scalePxInt(10)
                            use mod_iconbutton('\uf560', If(selectedIndex==i, '{u}C{/u}ondition', 'Condition'), mod.Confirm(prompt=choice.condition, title='Visibility condition', modal=False, promptSubstitution=False), inline=True)
                            if selectedIndex==i:
                                key 'alt_K_c' action mod.Confirm(prompt=choice.condition, title='Visibility condition', modal=False, promptSubstitution=False)
                        elif selectedIndex==i:
                            key 'alt_K_c' action NullAction()

                    hbox xsize mod.scalePxInt(150):
                        if choice.code:
                            use mod_iconbutton('\uf121', If(selectedIndex==i, '{u}S{/u}how', 'Show'), mod.Confirm(prompt=choice.code, title='Choice code', modal=False, promptSubstitution=False), inline=True)
                            if selectedIndex==i:
                                key 'alt_K_s' action mod.Confirm(prompt=choice.code, title='Choice code', modal=False, promptSubstitution=False)
                        else:
                            text 'Not found'
                            if selectedIndex==i:
                                key 'alt_K_s' action NullAction()

                    hbox xsize mod.scalePxInt(300):
                        if choice.jumpTo:
                            use mod_iconbutton('\uf064', If(selectedIndex==i, 'L{u}a{/u}bel', mod.scaleText(choice.jumpTo, 14, 'mod_button_text')), Show('mod_replay_jump', jumpTo=choice.jumpTo, choiceName=choice.text), inline=True)
                            if selectedIndex==i:
                                key 'alt_K_a' action Show('mod_replay_jump', jumpTo=choice.jumpTo, choiceName=choice.text)
                        else:
                            text 'N/A'
                            if selectedIndex==i:
                                key 'alt_K_a' action NullAction()

                    hbox xsize mod.scalePxInt(150):
                        use mod_iconbutton('\uf25a', If(selectedIndex==i, '{b}S{u}e{/u}lect{/b}', 'Select'), [choice.Action,Hide('mod_choices')], inline=True)
                        if selectedIndex==i:
                            key 'alt_K_e' action [choice.Action,Hide('mod_choices')]
                            key 'K_KP_ENTER' action [choice.Action,Hide('mod_choices')]
                            key 'K_RETURN' action [choice.Action,Hide('mod_choices')]
