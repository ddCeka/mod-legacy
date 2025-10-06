init 999:
    define config.hw_video = False
    define quick_menu = True
    define config.has_autosave = True

    define config.autosave_on_quit = True
    define config.autosave_on_choice = True
    define config.save_on_mobile_background = True

    define config.allow_skipping = True
    define config.rollback_enabled = True
    define config.hard_rollback_limit = 100
    define config.allow_underfull_grids = True
    define config.default_music_volume = 0.5
    define config.default_sfx_volume = 0.5
    define config.default_voice_volume = 0.5
    
    default persistent.mod_textbox = False
    default persistent.quickmenu = 1
    default persistent.qm_back = True
    default persistent.qm_history = False
    default persistent.qm_skip = False
    default persistent.qm_auto = False
    default persistent.qm_save = True
    default persistent.qm_load = True
    default persistent.qm_qsave = False
    default persistent.qm_qload = False
    default persistent.qm_prefs = True
    default persistent.qm_mod = False
    default persistent.qm_addon = True

    if persistent.mod_textbox == True:
        screen say(who, what):

            style_prefix "say"

            window:
                background Transform(style.window.background, alpha=persistent.dialogueBoxOpacity)

                if who is not None:

                    window:
                        style "namebox"
                        text who id "who"

                text what id "what"

            if not renpy.variant("small"):
                add SideImage() xalign 0.0 yalign 1.0

init 998 python:
    if not persistent.mod_textbox:
        persistent.say_window_alpha = 0.5
        persistent.dialogueBoxOpacity = 0.5

init -2 python:
    class GetInput(Action):
        def __init__(self,screen_name,input_id):
            self.screen_name=screen_name
            self.input_id=input_id
        def __call__(self):
            if renpy.get_widget(self.screen_name,self.input_id):
                return str(renpy.get_widget(self.screen_name,self.input_id).content)

init:
    $ config.gestures["n"] = "game_menu"
    $ config.gestures["s"] = "hide_windows"
    $ config.gestures["e"] = "skip"
    $ config.gestures["w"] = "rollback"
    $ config.gestures["n_s_n"] = "performance"
    $ config.gestures["e_w_e"] = "fast_skip"
    $ config.gestures["n_w_s"] = "console"
    $ quick_menu = True
    $ suppress_overlay = False

init python:
    for label in renpy.get_all_labels():
        renpy.game.persistent._seen_ever[label] = True
        renpy.game.seen_session[label] = True
        
    config.label_overrides["start"] = "addon_start"
    config.label_overrides["after_load"] = "addon_after_load"
    config.overlay_screens.append("quick_menu")
    gr = "{color=#00FF00}"
    red = "{color=#FF0000}"
    pur = "{color=#8a2be2}"

label addon_start:
    $ suppress_overlay = False
    $ quick_menu = True
    show screen quick_menu

    python:
        config.label_overrides.pop("start")
    jump start

label addon_after_load:
    $ suppress_overlay = False
    $ quick_menu = True
    show screen quick_menu
    
    python:
        config.label_overrides.pop("after_load")
    if renpy.has_label("after_load"):
        call after_load
    return

screen addon():

    style_prefix "addon" tag menu
    use game_menu(_("Addon"), scroll="viewport"):
        label "{u}{size=-18}Addon Extra{/size}{/u}"
        null height (4 * gui.pref_spacing)

        vbox:
            hbox:
                box_wrap True
                spacing 12
                vbox:
                    style_prefix "radio"
                    label ("HW Video")
                    textbutton ("Use Hardware") action SetVariable("config.hw_video", "True")
                    textbutton ("Use Software") action SetVariable("config.hw_video", "False")

                vbox:
                    style_prefix "radio"
                    label ("Powersave")
                    textbutton ("Enable") action Preference("gl powersave", True)
                    textbutton ("Disable") action Preference("gl powersave", False)
                    textbutton ("Auto") action Preference("gl powersave", "auto")

                vbox:
                    style_prefix "radio"
                    label _("Font Override")
                    textbutton _("Default") action Preference("font transform", None)
                    textbutton _("DejaVu Sans") action Preference("font transform", "dejavusans")
                    textbutton _("Opendyslexic") action Preference("font transform", "opendyslexic")

                vbox:
                    style_prefix "radio"
                    label _("High Contrast Text")
                    textbutton _("Enable") action Preference("high contrast text", "enable")
                    textbutton _("Disable") action Preference("high contrast text", "disable")

                vbox:
                    style_prefix "radio"
                    label _("Textbox Mod")
                    textbutton _("Enable") action SetVariable("persistent.mod_textbox", True)
                    textbutton _("Disable") action SetVariable("persistent.mod_textbox", False)
                
                vbox:
                    style_prefix "radio"
                    label ("Quick Menu")
                    textbutton "Standard" action SetVariable("persistent.quickmenu", 1)
                    textbutton "Icon" action SetVariable("persistent.quickmenu", 2)

            null height (4 * gui.pref_spacing)

            hbox:
                style_prefix "addon_text"
                label "Customize Quick Menu:"
            hbox:
                style_prefix "addon_text"
                box_wrap True
                spacing 15
                yalign .5
                vbox:
                    textbutton ("\"Back\":") action NullAction()
                    hbox:
                        if persistent.qm_back == False:
                            textbutton _("Off") action (SetVariable("persistent.qm_back",True))
                        else:
                            textbutton _("On") action (SetVariable("persistent.qm_back",False))

                null height (4 * gui.pref_spacing)

                vbox:
                    textbutton ("\"History\":") action NullAction()
                    hbox:
                        if persistent.qm_history == False:
                            textbutton _("Off") action (SetVariable("persistent.qm_history",True))
                        else:
                            textbutton _("On") action (SetVariable("persistent.qm_history",False))

                null height (4 * gui.pref_spacing)

                vbox:
                    textbutton ("\"Skip\":") action NullAction()
                    hbox:
                        if persistent.qm_skip == False:
                            textbutton _("Off") action (SetVariable("persistent.qm_skip",True))
                        else:
                            textbutton _("On") action (SetVariable("persistent.qm_skip",False))

                null height (4 * gui.pref_spacing)

                vbox:
                    textbutton ("\"Auto\":") action NullAction()
                    hbox:
                        if persistent.qm_auto == False:
                            textbutton _("Off") action (SetVariable("persistent.qm_auto",True))
                        else:
                            textbutton _("On") action (SetVariable("persistent.qm_auto",False))

                null height (4 * gui.pref_spacing)

                vbox:
                    textbutton ("\"Save\":") action NullAction()
                    hbox:
                        if persistent.qm_save == False:
                            textbutton _("Off") action (SetVariable("persistent.qm_save",True))
                        else:
                            textbutton _("On") action (SetVariable("persistent.qm_save",False))

                null height (4 * gui.pref_spacing)

                vbox:
                    textbutton ("\"Load\":") action NullAction()
                    hbox:
                        if persistent.qm_load == False:
                            textbutton _("Off") action (SetVariable("persistent.qm_load",True))
                        else:
                            textbutton _("On") action (SetVariable("persistent.qm_load",False))

                null height (4 * gui.pref_spacing)

                vbox:
                    textbutton ("\"Q.Save\":") action NullAction()
                    hbox:
                        if persistent.qm_qsave == False:
                            textbutton _("Off") action (SetVariable("persistent.qm_qsave",True))
                        else:
                            textbutton _("On") action (SetVariable("persistent.qm_qsave",False))

                null height (4 * gui.pref_spacing)

                vbox:
                    textbutton ("\"Q.Load\":") action NullAction()
                    hbox:
                        if persistent.qm_qload == False:
                            textbutton _("Off") action (SetVariable("persistent.qm_qload",True))
                        else:
                            textbutton _("On") action (SetVariable("persistent.qm_qload",False))

                null height (4 * gui.pref_spacing)

                vbox:
                    textbutton ("\"Prefs\":") action NullAction()
                    hbox:
                        if persistent.qm_prefs == False:
                            textbutton _("Off") action (SetVariable("persistent.qm_prefs",True))
                        else:
                            textbutton _("On") action (SetVariable("persistent.qm_prefs",False))

                null height (4 * gui.pref_spacing)

                vbox:
                    textbutton ("\"Mod\":") action mod.Open()
                    hbox:
                        if persistent.qm_mod == False:
                            textbutton _("Off") action (SetVariable("persistent.qm_mod",True))
                        else:
                            textbutton _("On") action (SetVariable("persistent.qm_mod",False))

            null height (4 * gui.pref_spacing)

            if persistent.mod_textbox == True:
                hbox:
                    box_wrap True
                    vbox:
                        label ("Textbox opacity")
                        style_prefix "addon_slider"
                        bar value FieldValue(persistent, "dialogueBoxOpacity", range=1.0)
                        hbox:
                            xfill True
                            text "{}%".format(int(persistent.dialogueBoxOpacity * 100)):
                                xcenter 0.5
                                ycenter 0.5

            null height (4 * gui.pref_spacing)

            hbox:
                box_wrap True
                vbox:
                    label ("Font Size")
                    style_prefix "addon_slider"
                    bar value Preference("font size")
                    hbox:
                        xfill True
                        textbutton _("50%"):
                            xalign 0.0
                            action Preference("font size", 0.50)
                        textbutton _("75%"):
                            xalign 0.25
                            action Preference("font size", 0.75)
                        textbutton _("100%"):
                            xalign 0.5
                            action Preference("font size", 1.0)
                        textbutton _("125%"):
                            xalign 0.75
                            action Preference("font size", 1.25)
                        textbutton _("150%"):
                            xalign 1.0
                            action Preference("font size", 1.5)
                    null height 10
                    hbox:
                        textbutton _("Reset"):
                            alt "reset font size"
                            action Preference("font size", 1.0)

            null height (4 * gui.pref_spacing)

            hbox:
                vbox:
                    label ("Gestures") style_prefix "addon_text"
                    text ("Up = Menu")
                    text ("Down = Hide")
                    text ("Left = Back")
                    text ("Right = Skip")
                    text ("Down-Right-Up = Open mod")
                    text ("Right-Left-Right = Fast-Skip to next choice")
                    text ("Up-Down-Up = Show Performance")
                    text ("Up-Left-Down = Console Screen (Type exit to close!)")
                
                null width 20

                hbox:
                    vbox:
                        style_prefix "addon_label_text"
                        textbutton _("Back to Game") action Return()

            null height (4 * gui.pref_spacing)

style game_menu_outer_frame is empty
style addon_label is gui_label
style addon_label_text is gui_label_text

style addon_outer_frame:
    bottom_padding 45
    top_padding 180
    background "#ff0"

style addon_text is addon_default:
    font "DejaVuSans.ttf"
    size int(config.screen_height / 34)
    outlines [(2, "#000000", 0, 0)]
    color '#fff'
    text_align 0.0

style addon_label_text:
    size gui.title_text_size
    yalign 0.0

style addon_label:
    xalign 0.5

style addon_slider:
    base_bar Frame("mod/images/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "mod/images/horizontal_[prefix_]thumb.png"
    xalign 0.5

screen quick_menu():
    variant "touch"
    key "alt_K_m" action [ If(suppress_overlay, SetVariable('quick_menu', True ), If(quick_menu, SetVariable('quick_menu', False ), SetVariable('quick_menu', True ))), SetVariable('suppress_overlay', False ) ]
    zorder 101
    if quick_menu:

        if persistent.quickmenu == 1:
            hbox:
                style_prefix "quick"

                xalign 0.5
                yalign 1.0
                
                if persistent.qm_back:
                    textbutton _("Back") action Rollback()
                if persistent.qm_skip:
                    textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
                if persistent.qm_history:
                    textbutton _("History") action ShowMenu('history')
                if persistent.qm_auto:
                    textbutton _("Auto") action Preference("auto-forward", "toggle")
                if persistent.qm_save:
                    textbutton _("Save") action ShowMenu('save')
                if persistent.qm_load:
                    textbutton _("Load") action ShowMenu('load')
                if persistent.qm_qsave:
                    textbutton _("Q.Save") action QuickSave()
                if persistent.qm_qload:
                    textbutton _("Q.Load") action QuickLoad()
                if persistent.qm_prefs:
                    textbutton _("Prefs") action ShowMenu('preferences')
                if persistent.qm_mod:
                    textbutton _("Mod") action mod.Open()
                if persistent.qm_addon:
                    textbutton _("Addon") action ShowMenu('addon')

        if persistent.quickmenu == 2:
            drag:
                draggable True
                xalign 0.0025
                yalign 0.97
                clicked ShowMenu('addon')
                dragged mod.touchDragged
                idle_child Transform('mod/images/menu.png', alpha=.5)
                hover_child 'mod/images/menu.png'

style quick_button:
    properties gui.button_properties("quick_button")

style quick_button_text:
    properties gui.button_text_properties("quick_button")

style quick_button_text:
    background None
    font "mod/FontAwesome5Free-Solid-900.otf"
    size int(config.screen_height / 32.5)
    idle_color "#8885"
    hover_color "#0F0F"
    insensitive_color "#4445"
    outlines [ (absolute(2), "#000A", absolute(0), absolute(0)) ]
    hover_outlines [ (absolute(2), "#000F", absolute(0), absolute(0)) ]

style say_dialogue:
    color "#FFFFFF"
    outlines [ (absolute(2), "#000", absolute(1), absolute(1)) ]

style say_label:
    outlines [ (absolute(2), "#000", absolute(1), absolute(1)) ]

style input_prompt:
    color "#FFFFFF"
    outlines [ (absolute(2), "#000", absolute(1), absolute(1)) ]

style input:
    color "#FFFFFF"
    outlines [ (absolute(2), "#000", absolute(1), absolute(1)) ]

style choice_button_text:
    size int(config.screen_height / 32.5)
    idle_color "#FFF"
    hover_color "#00FF00"
    insensitive_color "#808080FF"
    idle_outlines [ (absolute(5), "#FFF0", absolute(1), absolute(1)), (absolute(2), "#000", absolute(1), absolute(1)) ]
    hover_outlines [ (absolute(5), "#0F08", absolute(1), absolute(1)), (absolute(2), "#000", absolute(1), absolute(1)) ]
    insensitive_outlines [ (absolute(5), "#808080C0", absolute(1), absolute(1)), (absolute(2), "#000", absolute(1), absolute(1)) ]

style choice_button:
    background None
