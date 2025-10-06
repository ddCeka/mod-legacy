
style modSay_text:
    font "DejaVuSans.ttf"

style modSay_frame is mod_default:
    ypadding 0

transform mod_textboxSettingFade:
    on show:
        alpha 0.0
        linear 0.2 alpha 1.0
    on hide:
        alpha 1.0
        linear 0.2 alpha 0.0

screen mod_say(who, what):
    style_prefix 'modSay'

    vbox:
        xfill True
        yalign 1.0

        if who and mod.TextBox.Settings.whoShown:
            frame:
                xfill True
                xpadding mod.TextBox.whoXPadding
                background mod.TextBox.whoBackground
                text who id 'who'

        frame:
            xfill True
            background mod.TextBox.whatBackground

            hbox:
                spacing 20
                yminimum mod.TextBox.textHeight

                if mod.TextBox.Settings.sideImageShown and mod.TextBox.Settings.sideImagePos == 'left':
                    add mod.TextBox.sideImage

                frame:
                    xsize If(mod.TextBox.Settings.sideImageShown, config.screen_width-mod.TextBox.textHeight, config.screen_width)-(mod.TextBox.Settings.whatXPadding*2)
                    xpadding mod.TextBox.whatXPadding
                    text what id 'what'

                if mod.TextBox.Settings.sideImageShown and mod.TextBox.Settings.sideImagePos == 'right':
                    add mod.TextBox.sideImage


# =====================
# TEXTREPL. MAIN SCREEN
# =====================
screen mod_textboxCustomizations():
    style_prefix "mod"
    default colWidth = [mod.scaleX(20), mod.scaleX(60)]
    default textboxPages = modPages(len(mod.Loader.textboxCustomizations), itemsPerPage=22)

    hbox:
        spacing mod.scalePxInt(5)
        use mod_iconbutton('\uf067', 'Add', action=Function(mod.TextBox.openCustomizer, beforeOpenAction=Hide('mod_main'), afterCloseAction=mod.Open()))
        use mod_checkbox(checked=mod.TextBox.enabled, text='Enabled', action=ToggleField(mod.TextBox, 'enabled', True, False))
        if not mod.TextBox.enabled:
            text 'Custom textboxes are currently disabled, settings will not have any effect' yalign .5
    frame style_suffix "seperator" ysize mod.scalePxInt(2) yoffset mod.scalePxInt(5)

    if len(mod.Loader.textboxCustomizations) > 0:
        # PAGES
        fixed ysize mod.scalePxInt(50):
            hbox xalign .5 yoffset 4:
                use mod_pages(textboxPages)
            hbox xalign 1.0 yalign .5:
                text 'Customizations: {}'.format(len(mod.Loader.textboxCustomizations))

        hbox: # Headers
            yoffset mod.scaleY(1)
            label "Character" xsize colWidth[0]

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
                for charVarName in list(mod.Loader.textboxCustomizations.keys())[textboxPages.pageStartIndex:textboxPages.pageEndIndex]:
                    hbox:
                        hbox xsize colWidth[0]:
                            if charVarName == 'None':
                                text 'Any'
                            else:
                                text mod.scaleText(renpy.substitute('[{0}] ({0})'.format(charVarName)), 18)

                        hbox xsize colWidth[1]:
                            hbox:
                                use mod_iconbutton('\uf304', 'Edit', action=Function(mod.TextBox.openCustomizer, charVarName=charVarName, beforeOpenAction=Hide('mod_main'), afterCloseAction=mod.Open()), inline=True)
                                use mod_iconbutton('\uf146', 'Remove', mod.Confirm('Are you sure you want to remove this customization?', Function(mod.Loader.setTextboxCustomization, None, charVarName), title='Remove textbox customization'), inline=True)
    
    else:
        vbox:
            yoffset mod.scaleY(1.5)
            xalign 0.5
            label "There are no customizations yet" xalign 0.5
            null height mod.scalePxInt(15)
            text "Here you can customize the textbox for each or all characters" xalign .5
            text "Use the add button a the left top to start customizing" xalign .5


screen mod_textboxCustomizer(charVarName=None):
    layer If('mod' in config.layers, 'mod', 'overlay')
    style_prefix "mod"
    modal True

    on 'show' action Function(mod.TextBox.Settings.enableTemp, charVarName=charVarName)

    use mod_dialog(title='Textbox customizer', closeAction=Function(mod.TextBox.closeCustomizer)):
        vpgrid: # We need a vpgrid, because a viewport takes up all available height
            cols 1
            draggable True
            mousewheel True
            scrollbars "vertical"
            
            vbox spacing mod.scalePxInt(10):
                hbox spacing mod.scalePxInt(10):
                    # Character picker
                    vbox:
                        hbox:
                            text '\uf007' style_suffix 'icon'
                            label 'Character'
                        hbox:
                            if mod.TextBox.previewCharacter == mod.TextBox.demoCharacter:
                                text 'Any' yalign .5
                            else:
                                text '[{0}] ({0})'.format(mod.TextBox.previewCharacterVarName) yalign .5
                            textbutton '\uf304' style_suffix 'icon_button' action Show('mod_textboxCharacterPicker')
                            textbutton '\uf2ed' style_suffix 'icon_button' action SetField(mod.TextBox, 'previewCharacter', None) sensitive (mod.TextBox.previewCharacter != mod.TextBox.demoCharacter)
                            textbutton '\uf128' style_suffix 'icon_button' action mod.Confirm('Select a character to apply the customization to.\n"Any" is applied to any character that doensn\'t have it\'s own customizations.', title='Character selection')

                    vbox:
                        label 'Mode'
                        hbox:
                            textbutton If(mod.TextBox.Settings.customSayScreen, 'Full', 'Light') action ToggleField(mod.TextBox.Settings, 'customSayScreen', True, False)
                            textbutton '\uf128' style_suffix 'icon_button' action mod.Confirm('{b}Full{/b} = Use a fully customizable textbox\n{b}Light{/b} = Use the original textbox (some customization may not work)', title='Textbox mode') yalign .5

                # Namebox settings
                vbox:
                    hbox:
                        text '\uf5b7' style_suffix 'icon'
                        label 'Namebox'
                        if mod.TextBox.Settings.customSayScreen:
                            use mod_checkbox(checked=mod.TextBox.Settings.whoShown, text='Enabled', inline=True, action=ToggleField(mod.TextBox.Settings, 'whoShown', True, False))
                        
                    showif not mod.TextBox.Settings.customSayScreen or mod.TextBox.Settings.whoShown:
                        hbox spacing mod.scalePxInt(15) at mod_textboxSettingFade:
                            vbox:
                                text 'Text'
                                frame background Solid('#0002'):
                                    has vbox
                                    hbox spacing mod.scalePxInt(10):
                                        vbox:
                                            hbox: # Bold
                                                use mod_checkbox(checked=mod.TextBox.Settings.whoBold, text='Bold', action=ToggleField(mod.TextBox.Settings, 'whoBold', True, False))
                                                textbutton '\uf2ed' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whoBold', None) sensitive isinstance(mod.TextBox.Settings.whoBold, bool) yalign .5
                                            hbox: # Italic
                                                use mod_checkbox(checked=mod.TextBox.Settings.whoItalic, text='Italic', action=ToggleField(mod.TextBox.Settings, 'whoItalic', True, False))
                                                textbutton '\uf2ed' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whoItalic', None) sensitive isinstance(mod.TextBox.Settings.whoItalic, bool) yalign .5
                                            hbox: # Color
                                                use mod_iconbutton('\uf53f', 'Color', Show('mod_colorpicker', callback=modTextBoxSettingCallback('whoColor'), onClose=Hide('mod_colorpicker'), defaultColor=mod.TextBox.Settings.whoColor))
                                                if mod.TextBox.Settings.whoColor:
                                                    frame yalign .5:
                                                        background mod.TextBox.Settings.whoColor
                                                        text ''
                                                textbutton '\uf2ed' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whoColor', None) sensitive bool(mod.TextBox.Settings.whoColor) yalign .5
                                        vbox:
                                            if mod.TextBox.Settings.customSayScreen:
                                                text '{size=-4}Alignment{/size}'
                                                hbox: # Alignment
                                                    textbutton '\uf036' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whoXAlign', 0.0)
                                                    textbutton '\uf037' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whoXAlign', 0.5)
                                                    textbutton '\uf038' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whoXAlign', 1.0)
                                            text '{size=-4}Size{/size}'
                                            hbox: # Size
                                                textbutton '\uf068' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whoSize', mod.max(mod.TextBox.Settings.whoSize-2, 12))
                                                text '[mod.TextBox.Settings.whoSize]' yalign .5
                                                textbutton '\uf067' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whoSize', mod.min(mod.TextBox.Settings.whoSize+2, 100))
                                                textbutton '\uf0e2' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whoSize', modTextBoxSettings.defaultValues['whoSize'])
                                    hbox spacing mod.scalePxInt(5): # Change font
                                        use mod_iconbutton('\uf031', 'Font', action=Show('mod_textboxFontPicker', settingName='whoFont', defaultSelected=mod.TextBox.Settings.whoFont))
                                        if not mod.TextBox.Settings.customSayScreen:
                                            textbutton '\uf2ed' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whoFont', None) sensitive (mod.TextBox.Settings.whoFont != None) yalign .5
                                        if mod.TextBox.Settings.customSayScreen or mod.TextBox.Settings.whoFont != None:
                                            text (mod.TextBox.Settings.whoFont or list(modTextBoxSettings.fontOptions.keys())[0]) font mod.TextBox.whoFont yalign .5

                            vbox:
                                text 'Border'
                                frame background Solid('#0002'):
                                    has vbox
                                    use mod_checkbox(checked=mod.TextBox.Settings.whoOutlinesEnabled, text='Enabled', action=ToggleField(mod.TextBox.Settings, 'whoOutlinesEnabled', True, False))
                                    hbox: # Color
                                        use mod_iconbutton('\uf53f', 'Color', Show('mod_colorpicker', callback=modTextBoxSettingCallback('whoOutlinesColor'), onClose=Hide('mod_colorpicker'), defaultColor=mod.TextBox.Settings.whoOutlinesColor))
                                        if mod.TextBox.Settings.whoOutlinesColor:
                                            frame yalign .5:
                                                background mod.TextBox.Settings.whoOutlinesColor
                                                text ''
                                    text '{size=-4}Size{/size}'
                                    hbox: # Size
                                        textbutton '\uf068' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whoOutlinesWidth', mod.max(mod.TextBox.Settings.whoOutlinesWidth-1, 1))
                                        text '[mod.TextBox.Settings.whoOutlinesWidth]' yalign .5
                                        textbutton '\uf067' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whoOutlinesWidth', mod.min(mod.TextBox.Settings.whoOutlinesWidth+1, 10))
                                        textbutton '\uf0e2' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whoOutlinesWidth', modTextBoxSettings.defaultValues['whoOutlinesWidth'])

                            showif mod.TextBox.Settings.customSayScreen:
                                vbox at mod_textboxSettingFade:
                                    text 'Background'
                                    frame background Solid('#0002'):
                                        has vbox
                                        use mod_checkbox(checked=mod.TextBox.Settings.whoBackgroundEnabled, text='Enabled', action=ToggleField(mod.TextBox.Settings, 'whoBackgroundEnabled', True, False))
                                        hbox: # Color
                                            use mod_iconbutton('\uf53f', 'Color', Show('mod_colorpicker', callback=modTextBoxSettingCallback('whoBackground'), onClose=Hide('mod_colorpicker'), defaultColor=mod.TextBox.Settings.whoBackground))
                                            frame yalign .5:
                                                background mod.TextBox.Settings.whoBackground
                                                text ''
                                        use mod_checkbox(checked=mod.TextBox.Settings.whoBackgroundGradient, text='Gradient', action=ToggleField(mod.TextBox.Settings, 'whoBackgroundGradient', True, False))
                                        hbox: # Character color
                                            use mod_checkbox(checked=mod.TextBox.Settings.whoBackgroundCharacterColor, text='Character color', action=ToggleField(mod.TextBox.Settings, 'whoBackgroundCharacterColor', True, False))
                                            textbutton '\uf128' style_suffix 'icon_button' action mod.Confirm('Use the character\'s name color (when available)\n{size=-5}{alpha=.9}Note: This still uses the transparency/alpha from the color you\'ve set{/alpha}{/size}', title='Character color') yalign .5

                # Textbox settings
                vbox:
                    hbox:
                        text '\uf086' style_suffix 'icon'
                        label 'Text'

                    hbox spacing mod.scalePxInt(15):
                        vbox:
                            text 'Text'
                            frame background Solid('#0002'):
                                has vbox
                                hbox spacing mod.scalePxInt(10):
                                    vbox:
                                        hbox: # Bold
                                            use mod_checkbox(checked=mod.TextBox.Settings.whatBold, text='Bold', action=ToggleField(mod.TextBox.Settings, 'whatBold', True, False))
                                            textbutton '\uf2ed' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whatBold', None) sensitive isinstance(mod.TextBox.Settings.whatBold, bool) yalign .5
                                        hbox: # Italic
                                            use mod_checkbox(checked=mod.TextBox.Settings.whatItalic, text='Italic', action=ToggleField(mod.TextBox.Settings, 'whatItalic', True, False))
                                            textbutton '\uf2ed' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whatItalic', None) sensitive isinstance(mod.TextBox.Settings.whatItalic, bool) yalign .5
                                        hbox: # Color
                                            use mod_iconbutton('\uf53f', 'Color', Show('mod_colorpicker', callback=modTextBoxSettingCallback('whatColor'), onClose=Hide('mod_colorpicker'), defaultColor=mod.TextBox.Settings.whatColor))
                                            if mod.TextBox.Settings.whatColor:
                                                frame yalign .5:
                                                    background mod.TextBox.Settings.whatColor
                                                    text ''
                                            textbutton '\uf2ed' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whatColor', None) sensitive bool(mod.TextBox.Settings.whatColor) yalign .5
                                    vbox:
                                        if mod.TextBox.Settings.customSayScreen:
                                            text '{size=-4}Alignment{/size}'
                                            hbox: # Alignment
                                                textbutton '\uf036' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whatAlign', 0.0)
                                                textbutton '\uf037' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whatAlign', 0.5)
                                                textbutton '\uf038' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whatAlign', 1.0)
                                        text '{size=-4}Size{/size}'
                                        hbox: # Size
                                            textbutton '\uf068' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whatSize', mod.max(mod.TextBox.Settings.whatSize-2, 12))
                                            text '[mod.TextBox.Settings.whatSize]' yalign .5
                                            textbutton '\uf067' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whatSize', mod.min(mod.TextBox.Settings.whatSize+2, 100))
                                            textbutton '\uf0e2' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whatSize', modTextBoxSettings.defaultValues['whatSize'])
                                hbox: # Character color
                                    use mod_checkbox(checked=mod.TextBox.Settings.whatColorFromCharacter, text='Character color', action=ToggleField(mod.TextBox.Settings, 'whatColorFromCharacter', True, False))
                                    textbutton '\uf128' style_suffix 'icon_button' action mod.Confirm('Use the character\'s name color (when available)\n{size=-5}{alpha=.9}Note: This still uses the transparency/alpha from the color you\'ve set{/alpha}{/size}', title='Character color') yalign .5
                                hbox spacing mod.scalePxInt(5): # Change font
                                    use mod_iconbutton('\uf031', 'Font', action=Show('mod_textboxFontPicker', settingName='whatFont', defaultSelected=mod.TextBox.Settings.whatFont))
                                    if not mod.TextBox.Settings.customSayScreen:
                                        textbutton '\uf2ed' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whatFont', None) sensitive (mod.TextBox.Settings.whatFont != None) yalign .5
                                    if mod.TextBox.Settings.customSayScreen or mod.TextBox.Settings.whatFont != None:
                                        text (mod.TextBox.Settings.whatFont or list(modTextBoxSettings.fontOptions.keys())[0]) font mod.TextBox.whatFont yalign .5
                        
                        vbox:
                            text 'Border'
                            frame background Solid('#0002'):
                                has vbox
                                use mod_checkbox(checked=mod.TextBox.Settings.whatOutlinesEnabled, text='Enabled', action=ToggleField(mod.TextBox.Settings, 'whatOutlinesEnabled', True, False))
                                hbox: # Color
                                    use mod_iconbutton('\uf53f', 'Color', Show('mod_colorpicker', callback=modTextBoxSettingCallback('whatOutlinesColor'), onClose=Hide('mod_colorpicker'), defaultColor=mod.TextBox.Settings.whatOutlinesColor))
                                    if mod.TextBox.Settings.whatOutlinesColor:
                                        frame yalign .5:
                                            background mod.TextBox.Settings.whatOutlinesColor
                                            text ''
                                text '{size=-4}Size{/size}'
                                hbox: # Size
                                    textbutton '\uf068' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whatOutlinesWidth', mod.max(mod.TextBox.Settings.whatOutlinesWidth-1, 1))
                                    text '[mod.TextBox.Settings.whatOutlinesWidth]' yalign .5
                                    textbutton '\uf067' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whatOutlinesWidth', mod.min(mod.TextBox.Settings.whatOutlinesWidth+1, 10))
                                    textbutton '\uf0e2' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whatOutlinesWidth', modTextBoxSettings.defaultValues['whatOutlinesWidth'])
                        
                        showif mod.TextBox.Settings.customSayScreen:
                            vbox at mod_textboxSettingFade:
                                text 'Background'
                                frame background Solid('#0002'):
                                    has vbox
                                    use mod_checkbox(checked=mod.TextBox.Settings.whatBackgroundEnabled, text='Enabled', action=ToggleField(mod.TextBox.Settings, 'whatBackgroundEnabled', True, False))
                                    hbox: # Color
                                        use mod_iconbutton('\uf53f', 'Color', Show('mod_colorpicker', callback=modTextBoxSettingCallback('whatBackground'), onClose=Hide('mod_colorpicker'), defaultColor=mod.TextBox.Settings.whatBackground))
                                        frame yalign .5:
                                            background Solid(mod.TextBox.Settings.whatBackground)
                                            text ''
                                    use mod_checkbox(checked=mod.TextBox.Settings.whatBackgroundGradient, text='Gradient', action=ToggleField(mod.TextBox.Settings, 'whatBackgroundGradient', True, False))
                                    hbox: # Character color
                                        use mod_checkbox(checked=mod.TextBox.Settings.whatBackgroundCharacterColor, text='Character color', action=ToggleField(mod.TextBox.Settings, 'whatBackgroundCharacterColor', True, False))
                                        textbutton '\uf128' style_suffix 'icon_button' action mod.Confirm('Use the character\'s name color (when available)\n{size=-5}{alpha=.9}Note: This still uses the transparency/alpha from the color you\'ve set{/alpha}{/size}', title='Character color') yalign .5

                        showif mod.TextBox.Settings.customSayScreen:
                            vbox at mod_textboxSettingFade:
                                text 'General'
                                frame background Solid('#0002'):
                                    has vbox
                                    text '{size=-4}Height{/size}'
                                    hbox: # Height
                                        textbutton '\uf068' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whatHeight', mod.max(mod.TextBox.Settings.whatHeight-10, 50))
                                        text '[mod.TextBox.Settings.whatHeight]' yalign .5
                                        textbutton '\uf067' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whatHeight', mod.min(mod.TextBox.Settings.whatHeight+10, 450))
                                        textbutton '\uf0e2' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whatHeight', modTextBoxSettings.defaultValues['whatHeight'])

                # Sideimage settings
                showif mod.TextBox.Settings.customSayScreen:
                    vbox at mod_textboxSettingFade:
                        hbox:
                            text '\uf3e0' style_suffix 'icon'
                            label 'Side image'
                            use mod_checkbox(checked=mod.TextBox.Settings.sideImageShown, text='Enabled', inline=True, action=ToggleField(mod.TextBox.Settings, 'sideImageShown', True, False))
                        
                        showif mod.TextBox.Settings.sideImageShown:
                            hbox at mod_textboxSettingFade:
                                text 'Position: ' yalign .5
                                hbox:
                                    textbutton '\uf053' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'sideImagePos', 'left')
                                    textbutton '\uf054' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'sideImagePos', 'right')

        hbox:
            xalign 1.0
            spacing mod.scalePxInt(10)
            yoffset mod.scalePxInt(10)

            use mod_iconbutton('\uf128', 'Help', Show('mod_textboxCustomizerHelp'))
            use mod_iconbutton('\uf06e', 'Preview', Jump('mod_textboxCustomizer'))
            use mod_iconbutton('\uf00c', 'Apply', Function(mod.TextBox.closeCustomizer, save=True))
            use mod_iconbutton('\uf05e', 'Cancel', Function(mod.TextBox.closeCustomizer))


screen mod_textboxCustomizerHelp():
    layer If('mod' in config.layers, 'mod', 'overlay')
    style_prefix "mod"

    use mod_dialog(title='Textbox customizer', closeAction=Hide('mod_textboxCustomizerHelp'), modal=True):
        text 'This feature enabled you to customize the textbox displaying the game\'s dialogue.\nWhen changing settings, some will show immediately and for some you\'ll have to press the Preview button.'
        null height mod.scalePxInt(10)
        label 'Legend'
        hbox:
            text '\uf2ed' style_suffix 'icon'
            text 'Erase the value (use the game\'s value)'
        hbox:
            text '\uf0e2' style_suffix 'icon'
            text 'Reset value (back to initial value)'
        hbox:
            text '\uf146' style_suffix 'icon'
            text 'Using the game\'s value'
        hbox:
            text '\uf14a' style_suffix 'icon'
            text 'Enabled'
        hbox:
            text '\uf0c8' style_suffix 'icon'
            text 'Disabled'


screen mod_textboxCharacterPicker():
    layer If('mod' in config.layers, 'mod', 'overlay')
    style_prefix "mod"
    default charFilterInput = Input(autoFocus=True)

    use mod_dialog(title='Found '+str(len(mod.TextRepl.characters))+' characters', closeAction=Hide('mod_textboxCharacterPicker'), modal=True):
        text 'Selecter a character'

        hbox:
            spacing 5
            text "Filter: " yalign .5
            button:
                style_suffix 'inputframe'
                xminimum mod.scalePxInt(350)
                key_events True
                action charFilterInput.Enable()
                input value charFilterInput

        viewport:
            ysize mod.scalePxInt(250)
            xsize mod.scalePxInt(450)
            draggable True
            mousewheel True
            scrollbars "vertical"

            vbox:
                for varName in mod.TextRepl.characters:
                    if eval(varName) and eval(varName).name and str(charFilterInput).lower() in renpy.substitute(eval(varName).name).lower():
                        textbutton '[{0}] ({0})'.format(varName) xfill True action [Hide('mod_textboxCharacterPicker'),SetField(mod.TextBox, 'previewCharacter', varName)]


screen mod_textboxFontPicker(settingName, defaultSelected=None):
    layer If('mod' in config.layers, 'mod', 'overlay')
    style_prefix "mod"
    default selectedFont = (defaultSelected or list(modTextBoxSettings.fontOptions.keys())[0])
    default fontSize = 30
    
    use mod_dialog(title='Pick a font', closeAction=Hide('mod_textboxFontPicker'), modal=True):
        hbox spacing mod.scalePxInt(20):
            vbox:
                label 'Available fonts'
                for name,fontFile in modTextBoxSettings.fontOptions.items():
                    if renpy.loadable(fontFile):
                        textbutton name text_font fontFile action SetScreenVariable('selectedFont', name)

            vbox:
                label 'Preview'
                hbox:
                    text 'Fontsize: [fontSize]' yalign .5
                    textbutton '\uf068' style_suffix 'icon_button' action SetScreenVariable('fontSize', mod.max(fontSize-2, 12))
                    textbutton '\uf067' style_suffix 'icon_button' action SetScreenVariable('fontSize', mod.min(fontSize+2, 60))
                null height mod.scalePxInt(20)
                text "Here's some example text to show you this font." font modTextBoxSettings.fontOptions[selectedFont] size fontSize
                text "And also some bold text to show." bold True font modTextBoxSettings.fontOptions[selectedFont] size fontSize
                text "Also some italic while we're at it" italic True font modTextBoxSettings.fontOptions[selectedFont] size fontSize

        hbox:
            spacing mod.scalePxInt(10)
            xalign 1.0
            use mod_iconbutton('\uf00c', 'Select', action=[SetField(mod.TextBox.Settings, settingName, selectedFont),Hide('mod_textboxFontPicker')])
            use mod_iconbutton('\uf05e', 'Cancel', action=Hide('mod_textboxFontPicker'))


label mod_textboxCustomizer(charVarName=None):
    show screen mod_textboxCustomizer (charVarName)
    mod.TextBox.previewCharacter "Here's some text for testing purposes...\nAlso another line of text to fill up this space"
    return

label mod_textboxCustomizer_return:
    return
