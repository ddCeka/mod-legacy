
init python:
    def mod_searchResultColumns(var, subItem=0):
        """ We use this method because Ren'Py doesn't allow to `use` a screen inside itself in devmode """

        Button = renpy.display.behavior.Button # In case a game assigns something to variable Button (noticed in The Red Room)
        TextButton = renpy.display.behavior.TextButton # TextButton isn't global in older Ren'Py versions

        def mod_iconButton(icon, text, action):
            return Button(
                HBox(
                    HBox(Text(icon, style='mod_icon'), xsize=mod.scalePxInt(30)),
                    Text(text, style='mod_text'),
                    style='mod_hbox',
                ),
                action=action,
                style='mod_inlinebutton',
            )

        # Render label columns
        if mod.Search.searchType == 'labels':
            # Name
            yield Text(mod.scaleText(('-'*subItem)+var.name, 19), substitute=False, style='mod_text')
            # Playbutton
            yield HBox(
                mod_iconButton('\uf144', 'Play', Show('mod_replay', labelName=var.name)),
                mod_iconButton('\uf064', 'Jump', Show('mod_jump', labelName=var.name)),
                style='mod_hbox',
            )
            # Remember
            if mod.Loader.hasLabel(var.name):
                yield mod_iconButton('\uf46d', 'Yes', Function(mod.Loader.forgetLabel, var.name))
            else:
                yield mod_iconButton('\uf328', 'No', Show('mod_remember_var', varName=var.name, rememberType='label'))

        # Render variable columns
        elif mod.Settings.showUnsupportedVariables or var.isSupported:
            # Name
            yield Text(mod.scaleText(('-'*subItem)+var.name, 19), substitute=False, style='mod_text')
            # Value
            if var.isExpandable:
                yield HBox(
                    TextButton(If(var.expanded, "\uf0d7", "\uf0da"), action=ToggleField(var, 'expanded', True, False), style='mod_icon_inlinebutton', text_style='mod_icon_inlinebutton_text', text_substitute=False),
                    Null(width=5),
                    Text(var.getButtonValue(19), substitute=False, style='mod_text'),
                    style='mod_hbox',
                )
            else:
                yield TextButton(var.getButtonValue(18), action=Show('mod_modify_value', var=var), style='mod_inlinebutton', text_style='mod_inlinebutton_text', text_substitute=False)
            # Remember
            if mod.Loader.hasVar(var.name):
                yield mod_iconButton('\uf46d', 'Yes', Function(mod.Loader.forgetVar, var.name))
            else:
                yield mod_iconButton('\uf328', 'No', Show('mod_remember_var', varName=var.name))
            # Watch
            if mod.Loader.isWatchingVar(var.name):
                yield mod_iconButton('\uf06e', 'Yes', Function(mod.Loader.unwatchVar, var.name))
            else:
                yield mod_iconButton('\uf070', 'No', Show('mod_remember_var', varName=var.name, rememberType='watchVar'))

            # Childvariables
            if var.expanded and var.isExpandable:
                for childVar in var.children:
                    for c in mod_searchResultColumns(childVar, subItem=subItem+1):
                        yield c

                if var.varType in ['dict', 'list']:
                    yield TextButton(('-'*(subItem+1))+'Add item', action=Show('mod_add_item', parentVar=var), style='mod_inlinebutton', text_style='mod_inlinebutton_text', text_substitute=False)
                    yield Null()
                    yield Null()
                    yield Null()

# ==================
# SEARCH MAIN SCREEN
# ==================
screen mod_search():
    style_prefix "mod"

    hbox:
        xfill True
        hbox:
            spacing 5
            text "Search: " yalign .5
            hbox yalign .5:
                button:
                    style_suffix 'inputframe'
                    xminimum mod.scalePxInt(250)
                    key_events True
                    action mod.Search.queryInput.Enable()
                    input value mod.Search.queryInput
            text " in " yalign .5
            textbutton mod.Search.searchType yalign .5 selected False action [Show('mod_search_options'),mod.Search.queryInput.Disable()]
            textbutton "Search" style_suffix "primary_button" yalign .5 action Function(mod.Search.doSearch)
            textbutton "Reset" style_suffix "red_button" yalign .5 action Function(mod.Search.resetSearch)

            if mod.Search.searchType == 'labels':
                text 'Last seen: [mod.Search.lastLabel]' yalign 0.5
                if renpy.has_label(mod.Search.lastLabel):
                    if not mod.Loader.hasLabel(mod.Search.lastLabel):
                        textbutton "\uf0fe" style_suffix "icon_button" yalign 0.5 action Show('mod_remember_var', varName=mod.Search.lastLabel, rememberType='label')
                    textbutton "\uf144" style_suffix "icon_button" yalign 0.5 action Show('mod_replay', labelName=mod.Search.lastLabel)

        hbox xalign 1.0 yalign .5:
            textbutton 'R' text_color If(mod.Settings.searchRecursive, '#baed91', '#fea3aa') tooltip If(mod.Settings.searchRecursive, 'Recursive enabled', 'Recursive disabled') action ToggleField(mod.Settings, 'searchRecursive', True, False)
            textbutton 'P' text_color If(mod.Settings.searchPersistent, '#baed91', '#fea3aa') tooltip If(mod.Settings.searchPersistent, 'Persistent enabled', 'Persistent disabled') action ToggleField(mod.Settings, 'searchPersistent', True, False)
            textbutton 'O' text_color If(mod.Settings.searchObjects, '#baed91', '#fea3aa') tooltip If(mod.Settings.searchObjects, 'Object search enabled', 'Object search disabled') action ToggleField(mod.Settings, 'searchObjects', True, False)
            textbutton 'U' text_color If(mod.Settings.showUnsupportedVariables, '#baed91', '#fea3aa') tooltip If(mod.Settings.showUnsupportedVariables, 'Showing unsupported vars', 'Hiding unsupported vars') action ToggleField(mod.Settings, 'showUnsupportedVariables', True, False)
            textbutton 'W' text_color If(mod.Settings.useWildcardSearch, '#baed91', '#fea3aa') tooltip If(mod.Settings.useWildcardSearch, 'Wildcard search enabled', 'Wildcard search disabled') action ToggleField(mod.Settings, 'useWildcardSearch', True, False)
            
    frame style_suffix "seperator" ysize mod.scalePxInt(2) yoffset mod.scalePxInt(5)

    if len(mod.Search.results) > 0:
        # PAGES
        fixed ysize mod.scalePxInt(50):
            hbox xalign .5 yoffset 4:
                textbutton "\uf049" style_suffix 'icon_button' sensitive (mod.Search.currentPage>1) action SetField(mod.Search, 'currentPage', 1) yalign .5 tooltip 'Go to first page'
                textbutton "\uf048" style_suffix 'icon_button' sensitive (mod.Search.currentPage>1) action SetField(mod.Search, 'currentPage', mod.Search.currentPage-1) yalign .5 tooltip 'Go to previous page'

                for page in mod.Search.pageRange:
                    textbutton If(page<10, '0[page]', '[page]') sensitive (page != mod.Search.currentPage) action SetField(mod.Search, 'currentPage', page)

                textbutton "\uf051" style_suffix 'icon_button' sensitive (mod.Search.currentPage<mod.Search.pageCount) action SetField(mod.Search, 'currentPage', mod.Search.currentPage+1) yalign .5 tooltip 'Go to next page'
                textbutton "\uf050" style_suffix 'icon_button' sensitive (mod.Search.currentPage<mod.Search.pageCount) action SetField(mod.Search, 'currentPage', mod.Search.pageCount) yalign .5 tooltip 'Go to last page'
            hbox xalign 1.0 yalign .5:
                text 'Results: {}'.format(len(mod.Search.results))

        # RESULT
        vpgrid:
            yoffset mod.scaleY(0.5)
            xfill True
            yfill True
            mousewheel True
            draggable True
            scrollbars "vertical"
            cols If(mod.Search.searchType == 'labels', 3, 4)
            spacing mod.scalePxInt(10)

            # Headers
            label "Name" xminimum mod.scaleX(20)
            label If(mod.Search.searchType=='labels', "Replay","Value") xminimum mod.scaleX(20)
            label "Remember" xminimum mod.scaleX(5)
            if mod.Search.searchType!='labels':
                label "Watch" xminimum mod.scaleX(5)

            # Results
            for var in mod.Search.results[mod.Search.pageStartIndex:mod.Search.pageEndIndex]:
                for c in mod_searchResultColumns(var):
                    add c

    else: # No results
        vbox:
            yoffset mod.scaleY(1.5)
            xalign 0.5

            label "No results" xalign 0.5
            if mod.Search.searchRecursive:
                null height mod.scaleY(2)
                text "You're currently doing a recursive search, use the reset button to start over" xalign 0.5
                text "This means you're searching your previous results instead of everything" xalign 0.5 size 16

# =====================
# SEARCH OPTIONS SCREEN
# =====================
screen mod_search_options():
    layer If('mod' in config.layers, 'mod', 'overlay')
    style_prefix "mod"

    use mod_dialog('Search options', closeAction=Hide('mod_search_options'), modal=True):
        text 'Search type:'
        use mod_radiobutton(checked=(mod.Search.searchType=='variable names'), text='Variable names', action=[SetField(mod.Search, 'searchType', 'variable names'),Hide('mod_search_options')])
        use mod_radiobutton(checked=(mod.Search.searchType=='values'), text='Values', action=[SetField(mod.Search, 'searchType', 'values'),Hide('mod_search_options')])
        use mod_radiobutton(checked=(mod.Search.searchType=='labels'), text='Labels/Scenes', action=[SetField(mod.Search, 'searchType', 'labels'),Hide('mod_search_options')])

        null height 20
        text 'Other options:'
        hbox:
            use mod_checkbox(checked=mod.Settings.searchRecursive, text='Use recursive search', action=ToggleField(mod.Settings, 'searchRecursive', True, False))
            textbutton "\uf128" style_suffix "icon_button" yalign .5 tooltip "Explain resursive search" action mod.Confirm("""Enabling this feature means you'll search previous results until you reset\n\nExample:\nYou search for value {b}51{/b}, but get a lot of results\nWhen you know the value changed to (for example) {b}52{/b}, search for {b}52{/b}\nRecursive search will show all previous {b}51{/b} values that changed to {b}52{/b}""", title='Recursive search')
        hbox:
            use mod_checkbox(checked=mod.Settings.searchPersistent, text='Search in persistents', action=ToggleField(mod.Settings, 'searchPersistent', True, False))
            textbutton "\uf128" style_suffix "icon_button" yalign .5 tooltip "Explain persistents" action mod.Confirm("""Persistent variables are variables outside your save\n\nThose will stay the same regardless of the save you load,\nor even when you start a new game""", title='Persistent variables')
        hbox:
            use mod_checkbox(checked=mod.Settings.searchObjects, text='Search in objects/lists/dicts', action=ToggleField(mod.Settings, 'searchObjects', True, False))
            textbutton "\uf128" style_suffix "icon_button" yalign .5 tooltip "Explain object search" action mod.Confirm("""Objects, lists and dicts are essentually variables that contain variables\n\nFor example the object {b}player{/b} could contain the variable {b}name{/b}\nWhich is diplayed as {b}player.name{/b}""", title='search objects')
        hbox:
            use mod_checkbox(checked=mod.Settings.showUnsupportedVariables, text='Show unsupported variables', action=ToggleField(mod.Settings, 'showUnsupportedVariables', True, False))
            textbutton "\uf128" style_suffix "icon_button" yalign .5 tooltip "Explain unsupported variables" action mod.Confirm("""Show variables that mod cannot modify""", title='Unsupported variables')
        hbox:
            use mod_checkbox(checked=mod.Settings.useWildcardSearch, text='Use wildcard search', action=ToggleField(mod.Settings, 'useWildcardSearch', True, False))
            textbutton "\uf128" style_suffix "icon_button" yalign .5 tooltip "Explain wildcard search" action mod.Confirm("""Enabling this feature means results will exactly match the value you've entered. {b}Unless{/b} you use a wilcard.\n\nThere are 2 types of wildcards:\n{b}*{/b} : Will match any character\n{b}?{/b} : Matches any single character\n\nExample:\n{b}mod{/b} will only match exactly {b}mod{/b}\n{b}*mod*{/b} will also match {b}Hi, I'm mod! Who are you?{/b}\n{b}m*od{/b} will match {b}mod{/b}, {b}moood{/b} and {b}md{/b}\n{b}m?od{/b} will match {b}mod{/b}, but will NOT match {b}moood{/b} or {b}od{/b}""", title='Wildcard search')
