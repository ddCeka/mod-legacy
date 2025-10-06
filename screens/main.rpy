
screen mod_overlay():
    layer If('mod' in config.layers, 'mod', 'overlay')
    style_prefix "mod"

    key "alt_K_m" action mod.Open()
    if mod.Settings.quickResumeSaveHotKey:
        key "alt_K_q" action mod.Gamesaves.Save('_reload-1', name='', overwrite=True, notify='Quick resume saved')
    if mod.Settings.quickSaveHotKey:
        key "alt_K_s" action QuickSave()
    if mod.Settings.quickLoadHotKey:
        key "alt_K_l" action QuickLoad()
    if mod.Settings.consoleHotKey:
        key "alt_K_o" action mod.OpenConsole()
    # Prevent the Shift+O when console is disabled
    if not config.console and not config.developer:
        key "shift_K_o" action NullAction()

    if mod.Settings.showWatchPanel:
        # Watchpanel toggle key
        if mod.Settings.watchpanelToggleKey and isinstance(mod.Settings.watchpanelToggleKey, basestring):
            key "K_{}".format(mod.Settings.watchpanelToggleKey[0].lower()) action ToggleField(mod.Settings, 'collapsedWatchPanel', True, False)

        if mod.Settings.collapsedWatchPanel:
            if not mod.Settings.watchpanelHideToggleButton or not mod.Settings.watchpanelToggleKey:
                if mod.Settings.watchPanelPos == 'r': # Position right
                    textbutton "\uf053" style_suffix "icon_button" align (1.0, 0.0) action SetField(mod.Settings, 'collapsedWatchPanel', False)
                else:
                    textbutton "\uf054" style_suffix "icon_button" align (0.0, 0.0) action SetField(mod.Settings, 'collapsedWatchPanel', False)
        else:
            use mod_watchpanel

    # Detection notifications
    use mod_notifications

    # Show the touch buttton
    if mod.Settings.touchEnabled or (renpy.variant("touch") and not mod.gestureInitialized):
        drag:
            draggable True
            if mod.Settings.touchPosition:
                pos mod.Settings.touchPosition
            else:
                align (.0025,1.0)
            clicked mod.Open()
            dragged mod.touchDragged

            idle_child Transform('mod/images/logo.png', alpha=.8)
            hover_child 'mod/images/logo.png'


# ===========
# MAIN SCREEN
# ===========
screen mod_main():
    layer If('mod' in config.layers, 'mod', 'overlay')
    style_prefix "mod"
    modal True

    key "ctrl_K_n" action Function(mod.Loader.clear)
    key "ctrl_K_o" action mod.Loader.Load()
    key "ctrl_K_s" action mod.Loader.Save()
    key 'K_ESCAPE' action Hide('mod_main')

    frame:
        at mod_fadeinout
        xfill True yfill True
        xmargin mod.scalePxInt(-3) ymargin mod.scalePxInt(-3)

        hbox:
            align (1.0, 0.0)
            textbutton If(mod.Settings.showWatchPanel, '\uf06e', '\uf070') style_suffix "icon_togglebutton" tooltip "Toggle watchpanel" action ToggleField(mod.Settings, 'showWatchPanel', True, False) # Panel
            textbutton "\uf00d" style_suffix "red_icon_button" tooltip "Close mod" action Hide('mod_main')

        vbox:
            xfill True

            # Header
            vbox:
                ysize mod.scalePxInt(46)
                align (0.5, 0.0)
                text "Universal Ren'Py Mod" style_suffix "header_text" yalign .5

            # Tabs
            hbox:
                yoffset mod.scalePxInt(10)
                xfill True
                hbox:
                    use mod_tabbutton('Search', '\uf002', 'search')
                    use mod_tabbutton('Variables', '\uf121', 'variables')
                    use mod_tabbutton('Snapshots', '\uf030', 'snapshots')
                    use mod_tabbutton('Labels', '\uf02b', 'labels')
                    use mod_tabbutton('Renaming', '\uf4ff', 'textrepl')
                    use mod_tabbutton('Textboxes', '\uf044', 'textboxCustomizations')
                    use mod_tabbutton('Load/save', '\uf0c7', 'gamesaves')
                    use mod_tabbutton('Options', '\uf085', 'options')

                # File buttons
                hbox:
                    xalign 1.0
                    if GetTooltip('mod_main'):
                        text mod.scaleText(GetTooltip('mod_main'), 16) yalign 0.5
                    else:
                        if mod.Loader.loadedFile:
                            text mod.scaleText(renpy.substitute('Loaded: [mod.Loader.loadedFile]'), 16) yalign 0.5
                            if mod.Loader.unsavedChanges:
                                label "*" yalign 0.5
                        elif mod.Loader.unsavedChanges:
                            label "Unsaved" yalign 0.5
                    null width mod.scalePxInt(10)
                    textbutton "\uf15b" style_suffix "icon_button" tooltip "New (Ctrl+N)" action Function(mod.Loader.clear) # New
                    textbutton "\uf07c" style_suffix "icon_button" tooltip "Open (Ctrl+O)" action mod.Loader.Load() # Open
                    textbutton "\uf0c7" style_suffix "icon_button" tooltip "Save (Ctrl+S)" action mod.Loader.Save() # Save

            frame:
                style_suffix "tab_frame"
                has vbox

                if mod.Settings.currentScreen == 'search':
                    use mod_search()
                elif mod.Settings.currentScreen == 'variables':
                    use mod_variables()
                elif mod.Settings.currentScreen == 'snapshots':
                    use mod_snapshots()
                elif mod.Settings.currentScreen == 'labels':
                    use mod_labels()
                elif mod.Settings.currentScreen == 'textrepl':
                    use mod_textrepl()
                elif mod.Settings.currentScreen == 'textboxCustomizations':
                    use mod_textboxCustomizations()
                elif mod.Settings.currentScreen == 'gamesaves':
                    use mod_gamesaves()
                elif isinstance(mod.Settings.currentScreen, basestring) and mod.Settings.currentScreen.startswith('options'):
                    use mod_options_main(mod.Settings.currentScreen[8:])

# =========
# TABBUTTON
# =========
screen mod_tabbutton(title, icon, name):
    button:
        style_suffix "tab"
        hbox:
            text icon style_suffix 'icon' yalign .5
            null width 2
            label title yalign .5
        selected (isinstance(mod.Settings.currentScreen, basestring) and mod.Settings.currentScreen.startswith(name))
        action SetField(mod.Settings, 'currentScreen', name)

# ==============
# CONFIRM SCREEN
# ==============
screen mod_confirm(prompt, yes=None, no=None, title=None, modal=True, promptSubstitution=True):
    layer If('mod' in config.layers, 'mod', 'overlay')
    style_prefix "mod"

    use mod_dialog(title, closeAction=no, modal=modal):
        if promptSubstitution:
            text '[prompt]' xalign .5 text_align .5
        else:
            text '[prompt!q]' xalign .5 text_align .5

        hbox:
            yoffset mod.scalePxInt(15)
            xalign 0.5
            if yes:
                key 'K_KP_ENTER' action [Function(yes),Hide('mod_confirm')]
                key 'K_RETURN' action [Function(yes),Hide('mod_confirm')]
                textbutton "Yes" style_suffix "primary_button" action [Function(yes),Hide('mod_confirm')]
                null width mod.scalePxInt(20) # We don't use spacing on the hbox, because this will also space between `key` statements
                if no:
                    key 'K_ESCAPE' action [Function(no),Hide('mod_confirm')]
                    textbutton "No" action [Function(no),Hide('mod_confirm')]
                else:
                    key 'K_ESCAPE' action Hide('mod_confirm')
                    textbutton "No" action Hide('mod_confirm')
            else:
                key 'K_KP_ENTER' action Hide('mod_confirm')
                key 'K_RETURN' action Hide('mod_confirm')
                key 'K_ESCAPE' action Hide('mod_confirm')
                textbutton "OK" style_suffix "primary_button" action Hide('mod_confirm')

# ==========
# ICONBUTTON
# ==========
screen mod_iconbutton(icon, text, action=None, xsize=None, inline=False, sensitive=None):
    style_prefix 'mod'

    button:
        if inline:
            style_suffix 'inlinebutton'
        xsize xsize
        sensitive sensitive
        action action
        hbox:
            hbox xsize mod.scalePxInt(30): # We want this size fixed, to prevent resizing on icon change
                text icon style_suffix 'icon_button_text'
            text text style_suffix 'button_text' bold False
# We have this screen because in some cases updating the `icon` for `mod_iconbutton` won't work
screen mod_checkbox(checked, text, action=None, xsize=None, inline=False, sensitive=None):
    style_prefix 'mod'

    button:
        if inline:
            style_suffix 'inlinetogglebutton'
        else:
            style_suffix 'togglebutton'
        xsize xsize
        sensitive sensitive
        action action
        hbox:
            hbox xsize mod.scalePxInt(30): # We want this size fixed, to prevent resizing on icon change
                if checked:
                    text '\uf14a' style_suffix 'icon'
                elif checked == False:
                    text '\uf0c8' style_suffix 'icon'
                else:
                    text '\uf146' style_suffix 'icon'
            text text
# We have this screen because in some cases updating the `icon` for `mod_iconbutton` won't work
screen mod_radiobutton(checked, text, action=None, xsize=None):
    style_prefix 'mod'

    button:
        xsize xsize
        action action
        hbox:
            hbox xsize mod.scalePxInt(30): # We want this size fixed, to prevent resizing on icon change
                if checked:
                    text '\uf192' style_suffix 'icon'
                else:
                    text '\uf111' style_suffix 'icon'
            text text

# ======
# DIALOG
# ======
screen mod_dialog(title=None, closeAction=None, xsize=None, modal=False):
    layer If('mod' in config.layers, 'mod', 'overlay')
    style_prefix 'mod'

    if closeAction:
        key 'K_ESCAPE' action closeAction

    if modal:
        textbutton "" style_suffix "overlay" xfill True yfill True action NullAction() at mod_fadeinout

    drag:
        draggable True
        drag_handle (0, 0, 1.0, mod.scalePxInt(50))
        if renpy.variant('touch'):
            align (.5,.15)
        else:
            align (.5,.5)

        frame:
            at mod_fadeinout
            style_suffix 'dialog'
            align (.5,.5)
            xsize xsize
            has vbox

            hbox ysize mod.scalePxInt(46):
                add 'mod/images/mod_vertical.png' yalign .5 zoom mod.scaleFactor
                if title:
                    label title yalign .5 xoffset mod.scalePxInt(5)

            hbox ysize mod.scalePxInt(46) yoffset mod.scalePxInt(-46) xalign 1.0:
                showif closeAction:
                    textbutton '\uf00d' style_suffix 'red_icon_button' yalign .5 action closeAction

            vbox yoffset mod.scalePxInt(-23):
                transclude

# =====================
# SPLASHSCREEN OVERRIDE
# =====================
label mod_splashscreen:
    $ del config.label_overrides['splashscreen']
    if not mod.Settings.skipSplashscreen and renpy.has_label('splashscreen'):
        call _splashscreen

    return

# =============================================================================
# Pages screen to use inside other screens (pass modPages() object as argument)
# =============================================================================
screen mod_pages(pages):
    textbutton "\uf049" style_suffix 'icon_button' sensitive (pages.currentPage>1) action SetField(pages, 'currentPage', 1) yalign .5 tooltip 'Go to first page'
    textbutton "\uf048" style_suffix 'icon_button' sensitive (pages.currentPage>1) action SetField(pages, 'currentPage', pages.currentPage-1) yalign .5 tooltip 'Go to previous page'

    for page in pages.pageRange:
        textbutton If(page<10, '0[page]', '[page]') sensitive (page != pages.currentPage) action SetField(pages, 'currentPage', page)

    textbutton "\uf051" style_suffix 'icon_button' sensitive (pages.currentPage<pages.pageCount) action SetField(pages, 'currentPage', pages.currentPage+1) yalign .5 tooltip 'Go to next page'
    textbutton "\uf050" style_suffix 'icon_button' sensitive (pages.currentPage<pages.pageCount) action SetField(pages, 'currentPage', pages.pageCount) yalign .5 tooltip 'Go to last page'
