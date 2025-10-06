
# =====================
# TEXTREPL. MAIN SCREEN
# =====================
screen mod_textrepl():
    style_prefix "mod"
    default movingOriginal = None
    default colWidth = [mod.scaleX(20), mod.scaleX(20), mod.scaleX(13)]
    
    hbox:
        xfill True
        hbox:
            spacing 5
            if mod.Loader.loadedFile or len(mod.TextRepl.replacements) > 0:
                text "Text replacements: "+str(len(mod.TextRepl.replacements)) yalign 0.5
                textbutton "\uf057" style_suffix "icon_button" action If(mod.Loader.unsavedChanges, mod.Confirm('This will clear the list below, are you sure?', Function(mod.TextRepl.clearReplacements), title='Clear list'), Function(mod.TextRepl.clearReplacements))
            else:
                text "Load a file or add text replacements using the buttons on the right"

        hbox:
            xalign 1.0
            textbutton "\uf4ff" sensitive (not mod.TextRepl.incompatible) style_suffix "icon_button" tooltip 'Rename a character' action Show('mod_rename_character')
            textbutton "\uf067" sensitive (not mod.TextRepl.incompatible) style_suffix "icon_button" tooltip 'Add text replacement' action Show('mod_add_textrepl')
    frame style_suffix "seperator" ysize mod.scalePxInt(2) yoffset mod.scalePxInt(5)
    
    if len(mod.TextRepl.replacements) > 0:
        # PAGES
        fixed ysize mod.scalePxInt(50):
            hbox xalign .5 yoffset 4:
                textbutton "\uf049" style_suffix 'icon_button' sensitive (mod.TextRepl.currentPage>1) action SetField(mod.TextRepl, 'currentPage', 1) yalign .5 tooltip 'Go to first page'
                textbutton "\uf048" style_suffix 'icon_button' sensitive (mod.TextRepl.currentPage>1) action SetField(mod.TextRepl, 'currentPage', mod.TextRepl.currentPage-1) yalign .5 tooltip 'Go to previous page'

                for page in mod.TextRepl.pageRange:
                    textbutton If(page<10, '0[page]', '[page]') sensitive (page != mod.TextRepl.currentPage) action SetField(mod.TextRepl, 'currentPage', page)

                textbutton "\uf051" style_suffix 'icon_button' sensitive (mod.TextRepl.currentPage<mod.TextRepl.pageCount) action SetField(mod.TextRepl, 'currentPage', mod.TextRepl.currentPage+1) yalign .5 tooltip 'Go to next page'
                textbutton "\uf050" style_suffix 'icon_button' sensitive (mod.TextRepl.currentPage<mod.TextRepl.pageCount) action SetField(mod.TextRepl, 'currentPage', mod.TextRepl.pageCount) yalign .5 tooltip 'Go to last page'

        # Headers
        hbox:
            hbox xsize colWidth[0]:
                hbox:
                    label "Original"
                    textbutton '\uf15d' style_suffix 'icon_inlinebutton' tooltip 'Sort alphabetically' action Function(mod.TextRepl.sortReplacements)
                    textbutton '\uf881' style_suffix 'icon_inlinebutton' tooltip 'Sort reversed alphabetically' action Function(mod.TextRepl.sortReplacements, reverse=True)
            hbox xsize colWidth[1]:
                hbox:
                    label "Replacement"
                    textbutton '\uf15d' style_suffix 'icon_inlinebutton' tooltip 'Sort alphabetically' action Function(mod.TextRepl.sortReplacements, sortReplacement=True)
                    textbutton '\uf881' style_suffix 'icon_inlinebutton' tooltip 'Sort reversed alphabetically' action Function(mod.TextRepl.sortReplacements, sortReplacement=True, reverse=True)
            label "Case insensitive" xsize colWidth[2]

        # Results
        viewport:
            yoffset mod.scaleY(0.5)
            xfill True
            yfill True
            mousewheel True
            draggable True
            scrollbars "vertical"
            spacing mod.scalePxInt(10)

            vbox:
                for original,replacement in list(mod.TextRepl.replacements.items())[mod.TextRepl.pageStartIndex:mod.TextRepl.pageEndIndex]:
                    hbox:
                        hbox xsize colWidth[0]:
                            text mod.scaleText(replacement.original, 18) substitute False
                        hbox xsize colWidth[1]:                            
                            text mod.scaleText(replacement.replacement, 18) substitute False
                        hbox xsize colWidth[2]:
                            text mod.scaleText(If(replacement.caseInsensitive, 'Yes', 'No'), 5)
                        hbox:
                            if replacement.characterVar:
                                use mod_iconbutton('\uf044', 'Edit', Show('mod_add_textrepl', characterVar=replacement.characterVar, defaultReplacement=replacement.replacement), inline=True)
                            else:
                                use mod_iconbutton('\uf044', 'Edit', Show('mod_add_textrepl', defaultOriginal=replacement.original, defaultReplacement=replacement.replacement, defaultCaseInsensitive=replacement.caseInsensitive, defaultReplacePartialWords=replacement.replacePartialWords), inline=True)
                            use mod_iconbutton('\uf146', 'Remove', mod.Confirm('Are you sure you want to remove this text replacement?', Function(mod.TextRepl.delReplacement, original), title='Remove text replacement'), inline=True)
                            if movingOriginal:
                                if movingOriginal == replacement.original:
                                    use mod_iconbutton('\uf05e', 'Cancel', action=SetLocalVariable('movingOriginal', None), inline=True)
                                else:
                                    use mod_iconbutton('\uf05b', 'Before this', action=[Function(mod.TextRepl.changePos, movingOriginal, replacement.original),SetLocalVariable('movingOriginal', None)], inline=True)
                            else:
                                use mod_iconbutton('\uf0dc', 'Move', action=SetLocalVariable('movingOriginal', replacement.original), inline=True)

    else:
        vbox:
            yoffset mod.scaleY(1.5)
            xalign 0.5
            if mod.TextRepl.incompatible:
                label "Text replacement is not compatible with the used Ren'Py version" text_color "#f42929" xalign 0.5
            else:
                label "There are no text replacements" xalign 0.5

# ==================
# CHARACTER RENAMING
# ==================
screen mod_rename_character():
    layer If('mod' in config.layers, 'mod', 'overlay')
    style_prefix "mod"
    default charFilterInput = Input(autoFocus=True)

    textbutton "" style_suffix "overlay" xfill True yfill True action NullAction() at mod_fadeinout

    use mod_dialog(title='Found '+str(len(mod.TextRepl.characters))+' characters', closeAction=Hide('mod_rename_character'), modal=True):
        text 'Selecter a character to rename'

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
                        textbutton '[{0}] ({0})'.format(varName) xfill True action [Hide('mod_rename_character'),Show('mod_add_textrepl', characterVar=varName)]

# ====================
# Add text replacement
# ====================
screen mod_add_textrepl(characterVar=None, defaultOriginal='', defaultReplacement='', defaultCaseInsensitive=False, defaultReplacePartialWords=False, blockOriginal=False):
    layer If('mod' in config.layers, 'mod', 'overlay')
    style_prefix "mod"
    default caseInsensitive = defaultCaseInsensitive
    default replacePartialWords = defaultReplacePartialWords
    default inputs = InputGroup(
        [
            ('original', Input(text=(characterVar and eval(characterVar).name or defaultOriginal), editable=(not (characterVar or blockOriginal)))),
            ('replacement', Input(text=defaultReplacement)),
        ],
        focusFirst=True,
        onSubmit=[mod.TextRepl.AddReplacement(GetScreenInput('original', 'inputs'), GetScreenInput('replacement','inputs'), modGetScreenVariable('characterVar'), modGetScreenVariable('caseInsensitive'), modGetScreenVariable('replacePartialWords')),Hide('mod_add_textrepl')]
    )

    key 'K_TAB' action inputs.NextInput()
    key 'shift_K_TAB' action inputs.PreviousInput()

    use mod_dialog(title='Add text replacement', closeAction=Hide('mod_add_textrepl'), modal=True):
        text "Original:"
        button:
            xminimum mod.scalePxInt(450)
            key_events True
            action If(characterVar or blockOriginal, None, inputs.original.Enable())
            input value inputs.original

        text "Replacement:"
        button:
            xminimum mod.scalePxInt(450)
            key_events True
            action inputs.replacement.Enable()
            input value inputs.replacement

        if not characterVar:
            use mod_checkbox(checked=caseInsensitive, text='Case insensitive', action=ToggleScreenVariable('caseInsensitive', True, False))
            hbox:
                use mod_checkbox(checked=replacePartialWords, text='Replace parts of words', action=ToggleScreenVariable('replacePartialWords', True, False))
                textbutton "\uf128" style_suffix "icon_button" yalign .5 tooltip "Explain partial replacements" action mod.Confirm("""When this option is enabled the original text will also match parts of words. Otherwise it will only match whole words\n\nExample:\nOriginal: {b}mod{/b}\nReplacement: {b}Universal Ren'Py Mod{/b}\n\nOption enabled:\n{b}modod{/b} will become {b}Universal Ren'Py Modod{/b}\n(notice the extra {b}od{/b} because we only replaced the {b}mod{/b} part)\n\nOption disabled:\n{b}modod{/b} will not be replace, because it doesn't match the original {b}mod{/b} as a whole word""", title='Partial replacements')

        hbox:
            yoffset mod.scalePxInt(15)
            align (1.0,1.0)
            textbutton "Add" sensitive bool(str(inputs.original) and str(inputs.replacement)) style_suffix "primary_button" action inputs.onSubmit
            null width mod.scalePxInt(10)
            textbutton "Cancel" action Hide('mod_add_textrepl')
