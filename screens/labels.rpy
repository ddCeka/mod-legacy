
# =============
# LABELS SCREEN
# =============
screen mod_labels():
    style_prefix "mod"
    default thumbnailScale = 24
    default movingLabelName = None
    default colWidth = [mod.scaleX(20), mod.scaleX(20)]
    
    hbox:
        xfill True
        hbox:
            spacing mod.scalePxInt(5)
            if mod.Loader.loadedFile or len(mod.Loader.rememberedLabels) > 0:
                text "Remembered labels: "+str(len(mod.Loader.rememberedLabels)) yalign 0.5
                textbutton "\uf057" style_suffix "icon_button" action If(mod.Loader.unsavedChanges, mod.Confirm('This will clear the list below, are you sure?', Function(mod.Loader.clearLabels)), Function(mod.Loader.clearLabels))
            else:
                text "Load a file or add labels using the search option"

        hbox:
            xalign 1.0
            if mod.Settings.labelsView == 'list':
                textbutton "\uf302" style_suffix "icon_button" tooltip 'Show thumbnails' action SetField(mod.Settings, 'labelsView', 'thumbnails')
            else:
                textbutton "\uf022" style_suffix "icon_button" tooltip 'Show list' action SetField(mod.Settings, 'labelsView', 'list')
    frame style_suffix "seperator" ysize mod.scalePxInt(2) yoffset mod.scalePxInt(5)
    
    if len(mod.Loader.rememberedLabels) > 0:
        # =========
        # LIST VIEW
        # =========
        if mod.Settings.labelsView == 'list':
            hbox: # Headers
                yoffset mod.scaleY(0.5)
                hbox xsize colWidth[0]:
                    hbox:
                        label "Name"
                        textbutton '\uf15d' style_suffix 'icon_inlinebutton' tooltip 'Sort alphabetically' action Function(mod.Loader.sortLabels)
                        textbutton '\uf881' style_suffix 'icon_inlinebutton' tooltip 'Sort reversed alphabetically' action Function(mod.Loader.sortLabels, reverse=True)
                label "Replay" xsize colWidth[1]

            viewport:
                yoffset mod.scaleY(0.5)
                xfill True
                yfill True
                mousewheel True
                draggable True
                scrollbars "vertical"
                spacing mod.scalePxInt(10)

                # Results
                vbox:
                    for labelName,props in mod.Loader.rememberedLabels.items():
                        hbox:
                            hbox xsize colWidth[0]:
                                if 'name' in props:
                                    text mod.scaleText(props['name'], 20) substitute False
                                else:
                                    text mod.scaleText(labelName, 20) substitute False
                            hbox xsize colWidth[1]:
                                hbox:
                                    use mod_iconbutton('\uf144', 'Play', action=Show('mod_replay', labelName=labelName), inline=True)
                                    use mod_iconbutton('\uf064', 'Jump', action=Show('mod_jump', labelName=labelName), inline=True)
                            hbox:
                                use mod_iconbutton('\uf044', 'Edit', action=Show('mod_remember_var', varName=labelName, rememberType='label', defaultName=If('name' in props, props['name'], labelName)), inline=True)
                                use mod_iconbutton('\uf146', 'Remove', action=mod.Confirm('Are you sure you want to remove this label?', Function(mod.Loader.forgetLabel, labelName), title='Remove label'), inline=True)
                                if movingLabelName:
                                    if movingLabelName == labelName:
                                        use mod_iconbutton('\uf05e', 'Cancel', action=SetLocalVariable('movingLabelName', None), inline=True)
                                    else:
                                        use mod_iconbutton('\uf05b', 'Before this', action=[Function(mod.Loader.changeLabelPos, movingLabelName, labelName),SetLocalVariable('movingLabelName', None)], inline=True)
                                else:
                                    use mod_iconbutton('\uf0dc', 'Move', action=SetLocalVariable('movingLabelName', labelName), inline=True)

        # ===============
        # THUMBNAILS VIEW
        # ===============
        else:
            vpgrid:
                yoffset mod.scaleY(1)
                xfill True
                yfill True
                mousewheel True
                draggable True
                scrollbars "vertical"
                cols 4
                spacing 10

                for labelName,props in mod.Loader.rememberedLabels.items():
                    vbox:
                        button:
                            xsize mod.scaleX(thumbnailScale) ysize mod.scaleY(thumbnailScale)
                            action Show('mod_replay', labelName=labelName)
                            add Transform(modLabelImage(modLabel(labelName)), alpha=.7)
                            if 'name' in props:
                                text mod.scaleText(props['name'], thumbnailScale-2) color If(renpy.has_label(labelName), '#fff', '#d00') xalign .5 yalign 1.0 substitute False
                            else:
                                text mod.scaleText(labelName, thumbnailScale-2) color If(renpy.has_label(labelName), '#fff', '#d00') xalign .5 yalign 1.0 substitute False

                        hbox:
                            ypos -5
                            xsize mod.scaleX(thumbnailScale)
                            hbox:
                                textbutton "\uf144" style_suffix "icon_button" tooltip 'Replay' action Show('mod_replay', labelName=labelName)
                                textbutton "\uf064" style_suffix "icon_button" tooltip 'Jump' action Show('mod_jump', labelName=labelName)
                            hbox:
                                xalign 1.0
                                textbutton "\uf044" style_suffix "icon_button" tooltip 'Edit' action Show('mod_remember_var', varName=labelName, rememberType='label', defaultName=If('name' in props, props['name'], labelName))
                                textbutton "\uf146" style_suffix "icon_button" tooltip 'Remove' action mod.Confirm('Are you sure you want to remove this label?', Function(mod.Loader.forgetLabel, labelName), title='Remove label')
                                if movingLabelName:
                                    if movingLabelName == labelName:
                                        textbutton '\uf05e' style_suffix 'icon_button' tooltip 'Cancel' action SetLocalVariable('movingLabelName', None)
                                    else:
                                        textbutton '\uf05b' style_suffix 'icon_button' tooltip 'Before this' action [Function(mod.Loader.changeLabelPos, movingLabelName, labelName),SetLocalVariable('movingLabelName', None)]
                                else:
                                    textbutton '\uf0dc' style_suffix 'icon_button' tooltip 'Move'  action SetLocalVariable('movingLabelName', labelName)

                # Fill up till we have 4 columns (this is needed since Ren'Py 7.5)
                for i in range(4 - len(mod.Loader.rememberedLabels) % 4):
                    null
            

    else:
        vbox:
            yoffset mod.scaleY(1.5)
            xalign 0.5
            label "There are no remembered labels" xalign 0.5

# =============
# REPLAY SCREEN
# =============
screen mod_replay(labelName):
    layer If('mod' in config.layers, 'mod', 'overlay')
    style_prefix "mod"
    default errorMessage = None

    use mod_dialog('Start a replay', closeAction=Hide('mod_replay'), modal=True):
        if renpy.has_label(labelName):
            text 'You can end the replay by pressing Alt+M or by choosing "End Replay" in the game menu'
        else:
            text 'The selected label does not exist'

        if errorMessage != None:
            null height mod.scalePxInt(10)
            text errorMessage style_suffix "error_text"

        hbox:
            yoffset mod.scalePxInt(15) xalign .5
            if renpy.has_label(labelName):
                key 'K_KP_ENTER' action modReplay(labelName, Hide('mod_replay'), 'errorMessage')
                key 'K_RETURN' action modReplay(labelName, Hide('mod_replay'), 'errorMessage')
                textbutton "Start" style_suffix "primary_button" action modReplay(labelName, Hide('mod_replay'), 'errorMessage')
                null width mod.scalePxInt(10)
            textbutton "Cancel" action Hide('mod_replay')

# ===========
# JUMP SCREEN
# ===========
screen mod_jump(labelName):
    layer If('mod' in config.layers, 'mod', 'overlay')
    style_prefix "mod"

    use mod_dialog('Jump to label', closeAction=Hide('mod_jump'), modal=True):
        if renpy.has_label(labelName):
            text 'You are about to jump to a label, this will affect your game' color '#990000' bold True xalign .5
            text 'If you want to play the label without it affecting your game, go back and choose the replay option' xalign .5
            null height 10
            text '(Only use this option if you know what you\'re doing. Your game will continue from the label you\'re jumping to)' color '#AAA' style_suffix 'text_small' xalign .5
        else:
            text 'The selected label does not exist'

        hbox:
            yoffset mod.scalePxInt(15) xalign .5
            if renpy.has_label(labelName):
                key 'K_KP_ENTER' action [Hide('mod_jump'),Hide('mod_main'),Jump(labelName)]
                key 'K_RETURN' action [Hide('mod_jump'),Hide('mod_main'),Jump(labelName)]
                textbutton "Jump" style_suffix "primary_button" action [Hide('mod_jump'),Hide('mod_main'),Jump(labelName)]
                null width mod.scalePxInt(10)
            textbutton "Cancel" action Hide('mod_jump')

# ==================
# REPLAY JUMP SCREEN
# ==================
screen mod_replay_jump(jumpTo, choiceName=None, dialogTitle='Next label'):
    layer If('mod' in config.layers, 'mod', 'overlay')
    style_prefix 'mod'
    default errorMessage = None

    use mod_dialog(dialogTitle, Hide('mod_replay_jump'), modal=True):
        if choiceName:
            hbox:
                label 'Choice '
                text choiceName
        hbox:
            label 'Next label '
            text jumpTo

        vbox:
            yoffset mod.scalePxInt(15)
            spacing mod.scalePxInt(15)

            if errorMessage != None:
                text errorMessage style_suffix "error_text"

            vbox:
                text 'Playing the label will {b}not{/b} affect your current gameplay (it starts in replay mode)\nand you will return here after ending the replay (press Alt+M)' text_align .5

            hbox: # Buttons
                xalign 0.5
                spacing mod.scalePxInt(20)

                use mod_iconbutton('\uf144', '{u}P{/u}lay', modReplay(jumpTo, Hide('mod_replay_jump'), 'errorMessage'))
                key 'alt_K_p' action modReplay(jumpTo, Hide('mod_replay_jump'), 'errorMessage')
                use mod_iconbutton('\uf328', '{u}R{/u}emember', [Hide('mod_replay_jump'),Show('mod_remember_var', varName=jumpTo, rememberType='label')])
                key 'alt_K_r' action [Hide('mod_replay_jump'),Show('mod_remember_var', varName=jumpTo, rememberType='label')]
                textbutton "Cancel" action Hide('mod_replay_jump')
