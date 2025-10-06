
transform mod_fadeinout:
    on show:
        alpha 0.0
        linear 0.3 alpha 1.0
    on hide:
        linear 0.3 alpha 0.0

style mod_default is default:
    background None
    hover_background None
    selected_background None
    selected_hover_background None
    insensitive_background None

    xalign .0 yalign .0
    xpadding 0 ypadding 0
    xmargin 0 ymargin 0
    spacing 0

style mod_overlay:
    background "#99999988"

style mod_frame is mod_default:
    background Frame(renpy.display.im.FactorScale('mod/images/dialog.png', mod.scaleFactor, bilinear=False), mod.scalePx(11), mod.scalePx(54), mod.scalePx(11), mod.scalePx(6))
    padding (mod.scalePxInt(7), mod.scalePxInt(5))
style mod_dialog is mod_frame:
    padding (mod.scalePxInt(10), mod.scalePxInt(5), mod.scalePxInt(10), mod.scalePxInt(15))
style mod_framecontent is mod_frame:
    background Frame(renpy.display.im.FactorScale(renpy.display.im.Crop('mod/images/dialog.png', (0,52,22,15)), mod.scaleFactor, bilinear=False), mod.scalePx(11), mod.scalePx(7), mod.scalePx(11), mod.scalePx(7))

style mod_seperator is mod_default:
    background "#0096ff"
    ysize 1
style mod_vseperator is mod_default:
    background "#0096ff"
    xsize 1

style mod_text is mod_default:
    font "DejaVuSans.ttf"
    size mod.scalePxInt(24)
    outlines [(1, "#000000", 0, 0)]
    color '#fff'
    text_align 0.0
    alt ''
style mod_icon is mod_text:
    font "mod/FontAwesome5Free-Solid-900.otf"
style mod_text_small is mod_text:
    size mod.scalePxInt(20)

style mod_error_text is mod_text:
    color "#ff0000"
    bold False
    outlines [(1, "#000000", 0, 0)]

style mod_label is mod_default:
    background None
    xpadding 0
    ypadding 0
    xalign .0
style mod_label_text is mod_text:
    bold False

style mod_input is mod_text:
    bold False
    color "#ddc3fe"
style mod_inputframe is mod_button

style mod_header_text is mod_text:
    color "#6c5789"
    bold False
    size mod.scalePxInt(30)
    outlines [(1, "#8f7ea5", 1, 1),(1, "#3b2658", -1, -1)]

style mod_button is mod_default:
    background Frame(renpy.display.im.FactorScale('mod/images/button_idle.png', mod.scaleFactor), mod.scalePx(11), mod.scalePx(28))
    hover_background Frame(renpy.display.im.FactorScale('mod/images/button_hover.png', mod.scaleFactor), mod.scalePx(11), mod.scalePx(28))
    selected_idle_background Frame(renpy.display.im.FactorScale('mod/images/button_hover.png', mod.scaleFactor), mod.scalePx(11), mod.scalePx(28))
    insensitive_background Transform(Frame(renpy.display.im.FactorScale('mod/images/button_idle.png', mod.scaleFactor), mod.scalePx(11), mod.scalePx(28)), alpha=.6)
    xpadding int((0.65 / 100.0) * config.screen_width)
    ypadding int((0.8 / 100.0) * config.screen_height)
    xminimum None yminimum None
    xmaximum None ymaximum None
    xmargin 0 ymargin 0
style mod_button_text is mod_text:
    bold False
    color "#fff"
    insensitive_color "#b1a9bc"

style mod_togglebutton is mod_button:
    selected_hover_background Frame(renpy.display.im.FactorScale('mod/images/button_idle.png', mod.scaleFactor), mod.scalePx(11), mod.scalePx(28))
style mod_togglebutton_text is mod_button_text

style mod_inlinetogglebutton is mod_inlinebutton:
    selected_hover_background Frame(renpy.display.im.FactorScale('mod/images/button_idle.png', mod.scaleFactor), mod.scalePx(11), mod.scalePx(28))
style mod_inlinetogglebutton_text is mod_inlinebutton_text

style mod_inlinebutton is mod_button:
    yoffset -mod.scalePxInt(4)
    ypadding mod.scalePxInt(4)
style mod_inlinebutton_text is mod_button_text

style mod_primary_button is mod_button:
    idle_background Frame(renpy.display.im.FactorScale('mod/images/button_primary.png', mod.scaleFactor), mod.scalePx(11), mod.scalePx(28))
style mod_primary_button_text is mod_button_text

style mod_red_button is mod_button:
    background Frame(renpy.display.im.FactorScale('mod/images/button_idle_red.png', mod.scaleFactor), mod.scalePx(11), mod.scalePx(28))
    hover_background Frame(renpy.display.im.FactorScale('mod/images/button_hover_red.png', mod.scaleFactor), mod.scalePx(11), mod.scalePx(28))
    selected_background Frame(renpy.display.im.FactorScale('mod/images/button_hover_red.png', mod.scaleFactor), mod.scalePx(11), mod.scalePx(28))
style mod_red_button_text is mod_button_text

style mod_icon_button is mod_button
style mod_icon_button_text is mod_button_text:
    font "mod/FontAwesome5Free-Solid-900.otf"
    bold False
    
style mod_icon_togglebutton is mod_togglebutton
style mod_icon_togglebutton_text is mod_togglebutton_text:
    font "mod/FontAwesome5Free-Solid-900.otf"
    bold False

style mod_icon_inlinebutton is mod_inlinebutton
style mod_icon_inlinebutton_text is mod_icon_button_text

style mod_icon_textbutton is mod_default
style mod_icon_textbutton_text is mod_icon_button_text:
    hover_color '#bde4ff'

style mod_red_icon_button is mod_red_button
style mod_red_icon_button_text is mod_red_button_text:
    font "mod/FontAwesome5Free-Solid-900.otf"
    bold False

style mod_tab is mod_button:
    background Frame(renpy.display.im.FactorScale('mod/images/tab_idle.png', mod.scaleFactor), mod.scalePx(11), mod.scalePx(48), mod.scalePx(11), 0)
    hover_background Frame(renpy.display.im.FactorScale('mod/images/tab_hover.png', mod.scaleFactor), mod.scalePx(11), mod.scalePx(48), mod.scalePx(11), 0)
    selected_background Frame(renpy.display.im.FactorScale('mod/images/tab_hover.png', mod.scaleFactor), mod.scalePx(11), mod.scalePx(48), mod.scalePx(11), 0)
style mod_tab_text is mod_button_text

style mod_tab_frame is mod_frame:
    background "#82828290"
    xfill True
    yfill True
    yoffset mod.scalePxInt(10)
    bottom_margin mod.scalePxInt(10)

style mod_vscrollbar:
    xsize mod.scalePxInt(20)
    left_bar Frame(renpy.display.im.FactorScale('mod/images/button_hover.png', mod.scaleFactor), mod.scalePx(11), mod.scalePx(28))
    right_bar Frame(renpy.display.im.FactorScale('mod/images/button_idle.png', mod.scaleFactor), mod.scalePx(11), mod.scalePx(28))
    thumb renpy.display.im.FactorScale('mod/images/thumb_idle.png', mod.scaleFactor)
    hover_thumb renpy.display.im.FactorScale('mod/images/thumb_hover.png', mod.scaleFactor)
    thumb_offset mod.scalePxInt(10)
    unscrollable 'hide'

# We cannot inherit `mod_vscrollbar`, because it will invert the scrollbar for some reason
style mod_vbar:
    xsize mod.scalePxInt(20)
    left_bar Frame(renpy.display.im.FactorScale('mod/images/button_hover.png', mod.scaleFactor), mod.scalePx(11), mod.scalePx(28))
    right_bar Frame(renpy.display.im.FactorScale('mod/images/button_idle.png', mod.scaleFactor), mod.scalePx(11), mod.scalePx(28))
    thumb renpy.display.im.FactorScale('mod/images/thumb_idle.png', mod.scaleFactor)
    hover_thumb renpy.display.im.FactorScale('mod/images/thumb_hover.png', mod.scaleFactor)
    thumb_offset mod.scalePxInt(10)
    unscrollable 'hide'

style mod_hbox is mod_default
style mod_vbox is mod_default  
style mod_imagebutton is mod_default
style mod_vpgrid is mod_default
