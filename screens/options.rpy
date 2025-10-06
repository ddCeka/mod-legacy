
# ====================
# SETTINGS MAIN SCREEN
# ====================
screen mod_options_main(selectedOption=None):
    style_prefix "mod"
    default currentOption = selectedOption
    default buttonWidth = mod.scaleX(15)
    
    hbox:
        vbox:
            use mod_iconbutton('\uf0f3', 'Notifications', action=SetField(mod.Settings, 'currentScreen', 'options_notifications'), xsize=buttonWidth)
            use mod_iconbutton('\uf06e', 'Watch panel', action=SetField(mod.Settings, 'currentScreen', 'options_watchpanel'), xsize=buttonWidth)
            use mod_iconbutton('\uf0c7', 'Load/save', action=SetField(mod.Settings, 'currentScreen', 'options_gamesaves'), xsize=buttonWidth)
            use mod_iconbutton('\uf0ad', 'Miscellaneous', action=SetField(mod.Settings, 'currentScreen', 'options_misc'), xsize=buttonWidth)

        null width 5
        frame style_suffix "vseperator" xsize mod.scalePxInt(2)
        null width 5

        vbox:
            xfill True yfill True

            # if renpy.has_screen('mod_options_{}'.format(mod.Settings.currentScreen[8:])):
            #     use expression 'mod_options_{}'.format(mod.Settings.currentScreen[8:]) # THIS IS NOT AVAILABLE IN OLDER RENPY VERSIONS
            if mod.Settings.currentScreen[8:] == 'notifications':
                use mod_options_notifications()
            if mod.Settings.currentScreen[8:] == 'watchpanel':
                use mod_options_watchpanel()
            if mod.Settings.currentScreen[8:] == 'gamesaves':
                use mod_options_gamesaves()
            if mod.Settings.currentScreen[8:] == 'misc':
                use mod_options_misc()
            else:
                label 'Select an option on the left' align (.5,.05)

# =============
# NOTIFICATIONS
# =============
screen mod_options_notifications():
    style_prefix 'mod'

    vbox yfill True:
        vbox yoffset 20:
            use mod_options_settings({
                'showReplayNotification': {
                    'title': 'Replay notification',
                    'description': """This option makes mod display a notification when you're in a replay\nand gives the option to quickly end it""",
                    'effective': If(mod.Settings.showReplayNotification, 'On', 'Off'),
                    'options': {
                        'On': True,
                        'Off': False,
                    },
                },
                'showChoicesNotification': {
                    'title': 'Choices notification',
                    'description': """This option makes mod display a notification when it detected choices\n\nThis notification also reports the number of hidden choices\nand gives quick access to more options regarding the choices\n\nYou can open the choices dialog by pressing Alt+C""",
                    'effective': If(mod.Settings.showChoicesNotification, 'On', 'Off'),
                    'options': {
                        'On': True,
                        'Off': False,
                    },
                },
                'showPathsNotification': {
                    'title': 'Paths notification',
                    'description': """This option makes mod display a notification when it detected a path/if-statement\nand gives quick access to more options/infor regarding the paths\n\nYou can open the choices dialog by pressing Alt+A""",
                    'effective': If(mod.Settings.showPathsNotification, 'On', 'Off'),
                    'options': {
                        'On': True,
                        'Off': False,
                    },
                },
                'stopSkippingOnPathDetection': {
                    'title': 'Stop skipping on path detection',
                    'description': """When you're skipping content and this option is enabled, skipping will be canceled on path detection""",
                    'effective': If(mod.Settings.stopSkippingOnPathDetection, 'On', 'Off'),
                    'options': {
                        'On': True,
                        'Off': False,
                    },
                },
            })

# ==========
# WATCHPANEL
# ==========
screen mod_options_watchpanel():
    style_prefix 'mod'

    vbox yfill True:
        vbox yoffset 20:
            use mod_options_settings(modOrderedDict([
                ('showWatchPanel', {
                    'title': 'Enable watchpanel',
                    'effective': If(mod.Settings.showWatchPanel, 'Enabled', 'Disabled'),
                    'options': {
                        'On': True,
                        'Off': False,
                    },
                }),
                ('watchpanelToggleKey', {
                    'title': 'Toggle using M-key',
                    'description': """Quickly open/close the watchpanel using this key""",
                    'effective': If(mod.Settings.watchpanelToggleKey, 'On', 'Off'),
                    'options': {
                        'On': 'M',
                        'Off': '',
                    },
                }),
                ('watchpanelHideToggleButton', {
                    'title': 'Hide togglebutton',
                    'description': """This removes the arrow button in the top corner\nNote: This only works when "Toggle using M-key" is enabled""",
                    'effective': If(mod.Settings.watchpanelHideToggleButton, 'On', 'Off'),
                    'options': {
                        'On': True,
                        'Off': False,
                    },
                }),
                ('watchPanelPos', {
                    'title': 'Panel position',
                    'effective': If(mod.Settings.watchPanelPos=='r', 'Right', 'Left'),
                    'options': modOrderedDict([
                        ('Left', 'l'),
                        ('Right', 'r'),
                    ]),
                }),
            ]))

# =========
# LOAD/SAVE
# =========
screen mod_options_gamesaves():
    style_prefix 'mod'

    vbox yfill True:
        vbox yoffset 20:
            use mod_options_settings(modOrderedDict([
                ('askSaveName', {
                    'title': 'Ask name before saving',
                    'effective': If(mod.Settings.askSaveName, 'On', 'Off'),
                    'options': {
                        'On': True,
                        'Off': False,
                    },
                }),
                ('quickResumeSaveHotKey', {
                    'title': 'Save {b}quick resume{/b} with Alt+Q',
                    'effective': If(mod.Settings.quickResumeSaveHotKey, 'On', 'Off'),
                    'options': {
                        'On': True,
                        'Off': False,
                    },
                }),
                ('quickSaveHotKey', {
                    'title': '{b}Quick save{/b} with Alt+S',
                    'effective': If(mod.Settings.quickSaveHotKey, 'On', 'Off'),
                    'options': {
                        'On': True,
                        'Off': False,
                    },
                }),
                ('quickLoadHotKey', {
                    'title': 'Load last {b}quick save{/b} with Alt+L',
                    'effective': If(mod.Settings.quickLoadHotKey, 'On', 'Off'),
                    'options': {
                        'On': True,
                        'Off': False,
                    },
                }),
            ]))

# =============
# MISCELLANEOUS
# =============
screen mod_options_misc():
    style_prefix 'mod'

    vbox yfill True:
        vbox yoffset 20:
            use mod_options_settings(modOrderedDict([
                ('consoleHotKey', {
                    'title': 'Open console with Alt+O',
                    'description': """Open the Ren'Py console. Even when it's disabled in the Ren'Py config""",
                    'effective': If(mod.Settings.consoleHotKey, 'On', 'Off'),
                    'options': {
                        'On': True,
                        'Off': False,
                    },
                }),
                ('skipSplashscreen', {
                    'title': 'Skip splashscreen',
                    'description': """This option skips the splashscreen at the start of the game (if any) and takes you directly to the menu""",
                    'effective': If(mod.Settings.skipSplashscreen, 'On', 'Off'),
                    'options': {
                        'On': True,
                        'Off': False,
                    },
                }),
            ] + ([
                ('touchEnabled', { # We only show this option on non-touch devices
                    'title': 'Enable touch control',
                    'description': """This will show additional logo on screen that you can drag around and click to open mod\n{size=-6}{alpha=.9}When you disable this on a touch device, you're still able to open mod by drawing an U on screen (down-right-up){/alpha}{/size}""",
                    'effective': If(mod.Settings.touchEnabled, 'On', 'Off'),
                    'options': {
                        'On': True,
                        'Off': False,
                    },
                }),
            ] if not renpy.variant('touch') or mod.gestureInitialized else [])))

# ======================
# CREATE A SETTINGS GRID
# ======================
screen mod_options_settings(settings):
    style_prefix 'mod'

    grid 4 len(settings)+1:
        spacing 5

        hbox:
            label 'Setting' yalign .5
            textbutton '{size=-8}\uf059{/size}' style_suffix 'icon_textbutton' action mod.Confirm("""There are 2 settings levels:\n{b}Local{/b}: The setting for the current game\n{b}Global{/b}: The setting for all games (that don't have a local setting)\n\nThe value under {b}Effective{/b} is the setting used in the current game""", title='Settings explanation')
        label 'Effective' yalign .5
        label 'Local' yalign .5
        label 'Global' yalign .5

        for setting in settings:
            hbox yalign .5:
                text settings[setting]['title'] yalign .5
                if 'description' in settings[setting]:
                    textbutton '{size=-8}\uf059{/size}' style_suffix 'icon_textbutton' action mod.Confirm(settings[setting]['description'], title=settings[setting]['title'])
            text settings[setting]['effective'] yalign .5
            hbox:
                for option in settings[setting]['options']:
                    use mod_radiobutton(mod.Settings.get(setting, globalSetting=False)==settings[setting]['options'][option], option, SetmodSetting(setting, settings[setting]['options'][option]))
                use mod_iconbutton('\uf2ed', 'Clear', SetmodSetting(setting, None))
            hbox:
                for option in settings[setting]['options']:
                    use mod_radiobutton(mod.Settings.get(setting, globalSetting=True)==settings[setting]['options'][option], option, SetmodSetting(setting, settings[setting]['options'][option], globalSetting=True))
                use mod_iconbutton('\uf2ed', 'Default', SetmodSetting(setting, None, globalSetting=True))
