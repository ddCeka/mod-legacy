
transform mod_choicesnotification_slide(width, position='l'):
    xoffset If(position == 'r', width, -width)
    on show:
        linear .2 xoffset 0
    on hide:
        linear .2 xoffset If(position == 'r', width, -width)

transform mod_notification_slide(width, position='l'):
    xoffset If(position == 'r', width, -width)
    linear .2 xoffset 0
    on hide:
        linear .2 xoffset If(position == 'r', width, -width)

# ===========
# MAIN SCREEN
# ===========
screen mod_watchpanel():
    layer If('mod' in config.layers, 'mod', 'overlay')
    style_prefix "mod"
    modal True
    default movingVarName = None

    frame:
        xalign If(mod.Settings.watchPanelPos == 'r', 1.0, 0.0)
        at mod_fadeinout
        xmargin -3 ymargin -3
        xsize mod.scaleX(15)
        yfill True
        has vbox
        xfill True

        hbox:
            xfill True ysize mod.scalePx(46)
            text "mod" style_suffix "header_text" yalign .5 xoffset mod.scalePx(3)
            hbox:
                xalign 1.0
                textbutton If(mod.Settings.watchPanelPos == 'r', "\uf054","\uf053") style_suffix "icon_button" tooltip 'Hide panel' action SetField(mod.Settings, 'collapsedWatchPanel', True)
                textbutton "\uf2d0" style_suffix "icon_button" tooltip 'Open mod' action mod.Open()
                textbutton "\uf00d" style_suffix "red_icon_button" tooltip 'Close panel' action SetField(mod.Settings, 'showWatchPanel', False)
        if GetTooltip('mod_overlay'):
            text GetTooltip('mod_overlay') xalign 1.0
        else:
            label 'Watchpanel' xalign .5
        null height 10

        vbox:
            #
            # Label monitor
            #
            label 'Last seen label'
            text mod.scaleText(mod.Search.lastLabel, 14) yalign 0.5 substitute False
            if renpy.has_label(mod.Search.lastLabel):
                hbox:
                    if not mod.Loader.hasLabel(mod.Search.lastLabel):
                        textbutton "\uf0fe" style_suffix "icon_button" yalign 0.5 tooltip 'Remember label' action Show('mod_remember_var', varName=mod.Search.lastLabel, rememberType='label')
                    textbutton "\uf144" style_suffix "icon_button" yalign 0.5 tooltip 'Replay label' action Show('mod_replay', labelName=mod.Search.lastLabel)
            frame xfill True ysize 10 ymargin 4 background Solid('#FFFFFF33')

            #
            # Choices detection
            #
            label 'Displaying choice?'
            if mod.Choices.isDisplayingChoice:
                hbox:
                    xfill True
                    text 'Yes ([mod.Choices.hiddenCount] hidden)'
                    textbutton '\uf03a' style_suffix 'icon_inlinebutton' xalign 1.0 tooltip 'Show choices' action Show('mod_choices')
            else:
                text 'No'
            frame xfill True ysize 10 ymargin 4 background Solid('#FFFFFF33')

            #
            # Path detection
            #
            label 'Detected path?'
            if mod.PathDetection.pathIsNext:
                hbox:
                    xfill True
                    text 'Yes'
                    textbutton '\uf03a' style_suffix 'icon_inlinebutton' xalign 1.0 tooltip 'Show options' action Show('mod_paths')
            else:
                text 'No'
            frame xfill True ysize 10 ymargin 4 background Solid('#FFFFFF33')

        #
        # Watching
        #
        if len(mod.Loader.watchedVars) == 0:
            text "There are no watched variables"
        else:
            vpgrid:
                yfill True
                xfill True
                mousewheel True
                draggable True
                scrollbars "vertical"
                cols 1

                for varName,varProps in mod.Loader.watchedVars.items():
                    vbox:
                        spacing 5
                        if 'name' in varProps:
                            text mod.scaleText(varProps['name'], 12) substitute False
                        else:
                            text mod.scaleText(varName, 12) substitute False
                        textbutton modVar(varName).getButtonValue(12) tooltip 'Modify value' action Show('mod_modify_value', var=modVar(varName)) substitute False
                        hbox:
                            textbutton "\uf044" style_suffix "icon_button" tooltip 'Change variable' action Show('mod_remember_var', varName=varName, rememberType='watchVar', defaultName=If('name' in varProps, varProps['name'], varName))
                            textbutton "\uf146" style_suffix "icon_button" tooltip 'Remove from list' action mod.Confirm('Are you sure you want to remove this variable?', Function(mod.Loader.unwatchVar, varName), title='Remove variable')
                            if movingVarName:
                                if movingVarName == varName:
                                    textbutton '\uf05e' style_suffix 'icon_button' tooltip 'Cancel' action SetLocalVariable('movingVarName', None)
                                else:
                                    textbutton '\uf05b' style_suffix 'icon_button' tooltip 'Before this' action [Function(mod.Loader.changeVarWatchPos, movingVarName, varName),SetLocalVariable('movingVarName', None)]
                            else:
                                textbutton '\uf0dc' style_suffix 'icon_button' tooltip 'Move' action SetLocalVariable('movingVarName', varName)
                        frame xfill True ysize 10 ymargin 4 background Solid('#FFFFFF33')

screen mod_notifications():
    layer If('mod' in config.layers, 'mod', 'overlay')
    style_prefix "mod"

    vbox:
        yoffset If(mod.Settings.showWatchPanel and mod.Settings.collapsedWatchPanel, mod.scalePxInt(45), 5) # We need some yoffset if the watchpanel togglebutton is there
        xalign If(mod.Settings.watchPanelPos == 'r', 1.0, 0.0)
        xoffset (If(mod.Settings.showWatchPanel and not mod.Settings.collapsedWatchPanel, mod.scaleX(15), 0) * If(mod.Settings.watchPanelPos == 'r', -1, 1)) # Offset notification when the panel is open, multiply by 1 or -1 for left or right panel

        # ==========
        # END REPLAY
        # ==========
        showif mod.Settings.showReplayNotification and _in_replay and (not mod.Settings.showWatchPanel or mod.Settings.collapsedWatchPanel):
            frame:
                style_suffix 'framecontent'

                vbox:
                    xsize mod.scalePxInt(250)
                    label 'You\'re in a replay'
                    key 'alt_K_e' action EndReplay(False)
                    use mod_iconbutton('\uf28d','{u}E{/u}nd replay', EndReplay(False))

        # ====================
        # Choices notification
        # ====================
        showif mod.Settings.showChoicesNotification and mod.Choices.isDisplayingChoice and (not mod.Settings.showWatchPanel or mod.Settings.collapsedWatchPanel):
            frame:
                style_suffix 'framecontent'
                at mod_choicesnotification_slide(mod.scalePxInt(250), mod.Settings.watchPanelPos)

                vbox:
                    xsize mod.scalePxInt(250)
                    label '{u}C{/u}hoices detected'
                    hbox:
                        xfill True
                        text '[mod.Choices.hiddenCount] hidden'
                        key 'alt_K_c' action Show('mod_choices')
                        textbutton '\uf03a' style_suffix 'icon_inlinebutton' xalign 1.0 action Show('mod_choices')

        # ==================
        # Paths notification
        # ==================
        showif mod.Settings.showPathsNotification and mod.PathDetection.pathIsNext and (not mod.Settings.showWatchPanel or mod.Settings.collapsedWatchPanel):
            if mod.Settings.stopSkippingOnPathDetection:
                on 'show' action modCancelSkipping()

            frame:
                style_suffix 'framecontent'
                at mod_choicesnotification_slide(mod.scalePxInt(250), mod.Settings.watchPanelPos)

                vbox:
                    xsize mod.scalePxInt(250)
                    label 'P{u}a{/u}th detected'
                    hbox:
                        xfill True
                        text '[mod.PathDetection.statementsCount] options'
                        key 'alt_K_a' action Show('mod_paths')
                        textbutton '\uf03a' style_suffix 'icon_inlinebutton' xalign 1.0 action Show('mod_paths')

        # ==================
        # TEMP NOTIFICATIONS
        # ==================
        for notif in mod.Notifications.notifications:
            button:
                style_suffix 'framecontent'
                at mod_notification_slide(mod.scalePxInt(250), mod.Settings.watchPanelPos)
                action notif

                vbox:
                    xsize mod.scalePxInt(250)
                    label mod.scaleText(notif.label, 240, style='mod_label_text', pixelTarget=True)
                    if notif.text:
                        text mod.scaleText(notif.text, 240, pixelTarget=True)
