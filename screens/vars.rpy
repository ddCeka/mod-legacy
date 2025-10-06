
# =====================
# VARIABLES MAIN SCREEN
# =====================
screen mod_variables():
    style_prefix "mod"
    default movingVarName = None
    default colWidth = [mod.scaleX(20), mod.scaleX(20), mod.scaleX(7), mod.scaleX(7), mod.scaleX(7)]
    
    hbox:
        spacing mod.scalePxInt(5)
        if mod.Loader.loadedFile or len(mod.Loader.rememberedVars) > 0:
            text "Remembered variables: "+str(len(mod.Loader.rememberedVars)) yalign 0.5
            textbutton "\uf057" style_suffix "icon_button" action If(mod.Loader.unsavedChanges, mod.Confirm('This will clear the list below, are you sure?', Function(mod.Loader.clearVars), title='Clear list'), Function(mod.Loader.clearVars))
        else:
            text "Load a file or add variables using the search option"
    frame style_suffix "seperator" ysize mod.scalePxInt(2) yoffset mod.scalePxInt(5)
    
    if len(mod.Loader.rememberedVars) > 0:
        hbox: # Headers
            yoffset mod.scaleY(1)
            hbox xsize colWidth[0]:
                hbox:
                    label "Name"
                    textbutton '\uf15d' style_suffix 'icon_inlinebutton' tooltip 'Sort alphabetically' action Function(mod.Loader.sortVars)
                    textbutton '\uf881' style_suffix 'icon_inlinebutton' tooltip 'Sort reversed alphabetically' action Function(mod.Loader.sortVars, reverse=True)
            label "Value" xsize colWidth[1]
            hbox xsize colWidth[2]:
                hbox:
                    label "Watch"
                    textbutton '{size=-8}\uf059{/size}' style_suffix 'icon_textbutton' action mod.Confirm('Add this variable to the watchpanel\nSo you can easily view and edit it during playing', title='Watch variable')
            hbox xsize colWidth[3]:
                hbox:
                    if mod.StoreMonitor.isAttached():
                        label "Freeze"
                        textbutton '{size=-8}\uf059{/size}' style_suffix 'icon_textbutton' action mod.Confirm('A frozen variable cannot change until you unfreeze it\nYou can only change it through mod\n{alpha=.8}{size=-5}Use with care. Freezing important variables could break stuff{/size}{/alpha}', title='Freeze variable')
                    else:
                        label "Freeze" text_color '#ff0000'
                        textbutton '{size=-8}\uf059{/size}' style_suffix 'icon_textbutton' action mod.Confirm('A frozen variable cannot change until you unfreeze it\nYou can only change it through mod\n{color=#ff0000}{b}mod failed to initialize this feature{/b}{/color}', title='Freeze variable')
            hbox xsize colWidth[4]:
                hbox:
                    if mod.StoreMonitor.isAttached():
                        label "Monitor"
                        textbutton '{size=-8}\uf059{/size}' style_suffix 'icon_textbutton' action mod.Confirm('You\'ll receive a notification when this variable changes', title='Monitor variable')
                    else:
                        label "Monitor" text_color '#ff0000'
                        textbutton '{size=-8}\uf059{/size}' style_suffix 'icon_textbutton' action mod.Confirm('You\'ll receive a notification when this variable changes\n{color=#ff0000}{b}mod failed to initialize this feature{/b}{/color}', title='Monitor variable')

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
                for varName,props in mod.Loader.rememberedVars.items():
                    hbox:
                        hbox xsize colWidth[0]:
                            if 'name' in props:
                                text mod.scaleText(props['name'], 20) substitute False
                            else:
                                text mod.scaleText(varName, 20) substitute False

                        hbox xsize colWidth[1]:
                            textbutton modVar(varName).getButtonValue(19) style_suffix 'inlinebutton' action Show('mod_modify_value', var=modVar(varName)) substitute False

                        hbox xsize colWidth[2]: # Watch
                            if mod.Loader.isWatchingVar(varName):
                                use mod_iconbutton('\uf06e', 'Yes', action=Function(mod.Loader.unwatchVar, varName), inline=True)
                            else:
                                use mod_iconbutton('\uf070', 'No', action=Show('mod_remember_var', varName=varName, rememberType='watchVar', defaultName=If('name' in props, props['name'], varName)), inline=True)

                        hbox xsize colWidth[3]: # Freeze
                            if mod.Loader.isFrozenVar(varName):
                                use mod_iconbutton('\uf2dc', 'Yes', action=Function(mod.Loader.unfreezeVar, varName), inline=True, sensitive=If(mod.Loader.freezableVar(varName), None, False))
                            else:
                                use mod_iconbutton('\uf043', 'No', action=Function(mod.Loader.freezeVar, varName), inline=True, sensitive=If(mod.Loader.freezableVar(varName), None, False))

                        hbox xsize colWidth[4]: # Monitor
                            if mod.Loader.isMonitoredVar(varName):
                                use mod_iconbutton('\uf0f3', 'Yes', action=Function(mod.Loader.unmonitorVar, varName), inline=True, sensitive=If(mod.Loader.monitorableVar(varName), None, False))
                            else:
                                use mod_iconbutton('\uf1f6', 'No', action=Function(mod.Loader.monitorVar, varName), inline=True, sensitive=If(mod.Loader.monitorableVar(varName), None, False))

                        hbox:
                            use mod_iconbutton('\uf044', 'Edit', action=Show('mod_remember_var', varName=varName, defaultName=If('name' in props, props['name'], varName)), inline=True)
                            use mod_iconbutton('\uf146', 'Remove', action=mod.Confirm('Are you sure you want to remove this variable?', Function(mod.Loader.forgetVar, varName), title='Remove variable'), inline=True)
                            if movingVarName:
                                if movingVarName == varName:
                                    use mod_iconbutton('\uf05e', 'Cancel', action=SetLocalVariable('movingVarName', None), inline=True)
                                else:
                                    use mod_iconbutton('\uf05b', 'Before this', action=[Function(mod.Loader.changeVarPos, movingVarName, varName),SetLocalVariable('movingVarName', None)], inline=True)
                            else:
                                use mod_iconbutton('\uf0dc', 'Move', action=SetLocalVariable('movingVarName', varName), inline=True)

    else:
        vbox:
            yoffset mod.scaleY(1.5)
            xalign 0.5
            label "There are no remembered variables" xalign 0.5

# ===================
# MODIFY VALUE SCREEN
# ===================
screen mod_modify_value(var):
    layer If('mod' in config.layers, 'mod', 'overlay')
    style_prefix "mod"

    default newValue = var.value
    default errorMessage = None
    default valueInput = Input(
        text=str(newValue),
        autoFocus=True,
        editable=var.isEditable,
        updateScreenVariable='newValue',
        onEnter=modSetVarValue(var, onSuccess=Hide('mod_modify_value'), screenErrorVariable='errorMessage', newValue=modGetScreenVariable('newValue')),
    )

    on "show" action [mod.Search.queryInput.Disable(),valueInput.Enable()]

    use mod_dialog(title=If(var.isEditable,'Modify variable','View variable'), closeAction=Hide('mod_modify_value'), modal=True):
            vbox xminimum mod.scalePxInt(450) # To force a minimum width on the dialog
            label "[var.name]"
            null height mod.scalePxInt(10)

            text "Value type: [var.varType]"
            if var.varType in ['string', 'int', 'float', 'boolean']:
                text "Value: " yalign .5
                if var.varType == 'boolean':
                    textbutton "[newValue]" sensitive var.isEditable action ToggleScreenVariable('newValue', True, False)
                elif var.varType in ['string', 'int', 'float']:
                    vpgrid:
                        cols 1
                        draggable True
                        mousewheel True
                        scrollbars "vertical"

                        button:
                            style_suffix 'inputframe'
                            xminimum mod.scalePxInt(450)
                            key_events True
                            sensitive var.isEditable
                            action valueInput.Enable()
                            input value valueInput allow If(var.varType=='string', '', If(var.varType=='float','.0123456789-','0123456789-'))

            if errorMessage != None:
                text errorMessage style_suffix "error_text"

            hbox:
                yoffset mod.scalePxInt(15)
                align (1.0,1.0)
                spacing mod.scalePxInt(10)

                if var.isEditable:
                    if var.varType != 'unsupported' and var.varType in ['string', 'boolean', 'int', 'float']:
                        textbutton "Change" style_suffix "primary_button" action valueInput.onEnter
                    textbutton "Delete" style_suffix 'red_button' align(0.0, 1.0) action [mod.Confirm('I hope you know what you\'re doing, are you sure you want to continue?', Function(var.delete), title='Deleting a variable'),Hide('mod_modify_value')]
                    textbutton "Cancel" action Hide('mod_modify_value')
                else:
                    textbutton "Close" action Hide('mod_modify_value')

# ==================
# ADD LIST/DICT ITEM
# ==================
screen mod_add_item(parentVar):
    layer If('mod' in config.layers, 'mod', 'overlay')
    style_prefix "mod"
    
    default itemVal = ''
    default inputs = InputGroup(
        [
            ('itemKey', Input(text=If(parentVar.varType=='dict', '', 'auto.'), editable=(parentVar.varType=='dict'))),
            ('itemVal', Input(updateScreenVariable='itemVal')),
        ],
        focusFirst=True,
        onSubmit=modSetVarValue(
            var=parentVar,
            onSuccess=Hide('mod_add_item'),
            screenErrorVariable='errorMessage',
            newValue=modGetScreenVariable('itemVal'),
            overruleVarType=modGetScreenVariable('valueTypes', modGetScreenVariable('valueTypeIndex')),
            operator=If(parentVar.varType=='list', 'append', '='),
            varChildKey=If(parentVar.varType=='dict', GetScreenInput('itemKey', 'inputs'), None),
        ),
    )
    default errorMessage = None
    default valueTypes = ['string', 'int', 'float', 'boolean']
    default valueTypeIndex = 0

    on 'show' action [mod.Search.queryInput.Disable(),Function(inputs.focus)]
    key 'K_TAB' action inputs.NextInput()
    key 'shift_K_TAB' action inputs.PreviousInput()

    use mod_dialog(title='Add item', closeAction=Hide('mod_add_item'), modal=True):
        label '[parentVar.name]'
        if parentVar.varType=='dict':
            text "Key:"
            button:
                xminimum mod.scalePxInt(450)
                key_events True
                action inputs.itemKey.Enable()
                input value inputs.itemKey
            null height mod.scalePxInt(10)

        hbox:
            text "Value type: " yalign .5
            textbutton valueTypes[valueTypeIndex] action SetScreenVariable('valueTypeIndex', (valueTypeIndex+1) % len(valueTypes))

        text "Value:"
        if valueTypes[valueTypeIndex] == 'boolean':
            textbutton "[itemVal]" action ToggleScreenVariable('itemVal', True, False)
        else:
            button:
                xminimum mod.scalePxInt(450)
                key_events True
                action inputs.itemVal.Enable()
                input value inputs.itemVal

        if errorMessage != None:
            text errorMessage style_suffix "error_text"

        hbox:
            yoffset mod.scalePxInt(15)
            align (1.0,1.0)
            textbutton "Add" sensitive bool(str(inputs.itemKey)) style_suffix "primary_button" action inputs.onSubmit
            null width mod.scalePxInt(10)
            textbutton "Cancel" action Hide('mod_add_item')

# ============
# REMEMBER VAR
# ============
screen mod_remember_var(varName, rememberType='var', defaultName=None):
    layer If('mod' in config.layers, 'mod', 'overlay')
    style_prefix "mod"
    
    if rememberType == 'label':
        default submitAction = Function(mod.Loader.rememberLabel, varName, GetScreenInput('displayNameInput'))
    elif rememberType == 'watchVar':
        default submitAction = Function(mod.Loader.watchVar, varName, GetScreenInput('displayNameInput'))
    else:
        default submitAction = Function(mod.Loader.rememberVar, varName, GetScreenInput('displayNameInput'))

    default displayNameInput = Input(text=If(defaultName, defaultName, varName), autoFocus=True, onEnter=[submitAction,Hide('mod_remember_var')])

    on 'show' action [mod.Search.queryInput.Disable(),displayNameInput.Enable()]

    use mod_dialog(title=If(rememberType=='label', 'Remember label', If(rememberType=='watchVar', 'Watch variable', 'Remember variable')), closeAction=Hide('mod_remember_var'), modal=True):
        text "Enter a name:"
        button:
            style_suffix 'inputframe'
            xminimum mod.scalePxInt(450)
            key_events True
            action displayNameInput.Enable()
            input value displayNameInput

        hbox:
            yoffset mod.scalePxInt(15)
            align (1.0,1.0)
            textbutton "Save" style_suffix "primary_button" action [submitAction,Hide('mod_remember_var')]
            null width mod.scalePxInt(10)
            textbutton "Cancel" action Hide('mod_remember_var')

# ===========
# SAVE SCREEN
# ===========
screen mod_save_file():
    layer If('mod' in config.layers, 'mod', 'overlay')
    style_prefix "mod"
    
    default filenameInput = Input(
        text=If(mod.Loader.loadedFile, mod.Loader.loadedFile[:-4], mod.Loader.stripSpecialChars(config.name)),
        autoFocus=True,
        onEnter=mod.Loader.Save(GetScreenInput('filenameInput'), Hide('mod_save_file'), 'errorMessage')
    )
    default errorMessage = None

    on 'show' action [mod.Search.queryInput.Disable(),filenameInput.Enable()]

    use mod_dialog(title='Save file', closeAction=Hide('mod_save_file'), modal=True):
        text "Enter a filename:"
        button:
            style_suffix 'inputframe'
            xminimum mod.scalePxInt(450)
            key_events True
            action filenameInput.Enable()
            input value filenameInput allow 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123465789-_ '

        if errorMessage != None:
            text errorMessage bold True color "#f42929"

        hbox:
            yoffset mod.scalePxInt(15)
            align (1.0,1.0)
            spacing mod.scalePxInt(10)
            textbutton "\uf128" style_suffix "icon_button" yalign .5 action mod.Confirm(""".mod files can be shared with anyone and are saved in two locations:\n\n{}\n{}""".format(mod.Loader.gameDir, mod.Loader.saveDir), title='mod files', promptSubstitution=False)
            textbutton "Save" style_suffix "primary_button" action filenameInput.onEnter
            textbutton "Cancel" action Hide('mod_save_file')

# ===========
# LOAD SCREEN
# ===========
screen mod_load_file():
    layer If('mod' in config.layers, 'mod', 'overlay')
    style_prefix "mod"
    default errorMessage = None

    use mod_dialog(title='Open file', closeAction=Hide('mod_load_file'), modal=True):
        text 'Select a file to load:'
        if len(mod.Loader.listFiles()) == 0:
            hbox:
                ysize mod.scalePxInt(300)
                xsize mod.scalePxInt(650)
                vbox align (.5,.5) spacing mod.scalePxInt(10):
                    label 'No .mod files found' xalign .5
                    text "Looking for files in:\n{}\n{}".format(mod.Loader.gameDir, mod.Loader.saveDir)
        else:
            viewport:
                ysize mod.scalePxInt(300)
                xsize mod.scalePxInt(650)
                draggable True
                mousewheel True
                scrollbars "vertical"

                vbox:
                    for filename,file in mod.Loader.listFiles().items():
                        hbox:
                            button:
                                xfill True right_margin mod.scalePxInt(45)
                                action mod.Loader.Load(filename, Hide('mod_load_file'), 'errorMessage')
                                vbox:
                                    label filename[:-4]
                                    text 'Modified: {}'.format(modTimeToText(file['mtime']))
                            textbutton '\uf2ed' xoffset -mod.scalePxInt(45) style_suffix 'icon_button' action mod.Confirm('Are you sure you want to delete this file? This cannot be undone', mod.Loader.Delete(filename), title='Confirm deletion')

            if errorMessage != None:
                text errorMessage bold True color "#f42929"

# ==================
# VAR CHANGED SCREEN
# ==================
screen mod_var_changed(varName, prevVal):
    layer If('mod' in config.layers, 'mod', 'overlay')
    style_prefix "mod"
    default var = modVar(varName)
    default prevValType = modVar.getValType(prevVal)
    default errorMessage = None

    use mod_dialog(title='Variable changed', closeAction=Hide('mod_var_changed'), modal=True):
        label 'Variable'
        text "[var.name]"

        if var.varType != prevValType:
            text "Type changed from [prevValType] to [var.varType]"
        else:
            text "Type: [var.varType]"
        null height mod.scalePxInt(10)

        label "Previous value"
        text "[prevVal]"
        null height mod.scalePxInt(10)
        label "New value"
        text "[var.value]"

        if errorMessage != None:
            text errorMessage style_suffix "error_text"

        hbox:
            yoffset mod.scalePxInt(15)
            align (1.0,1.0)
            if var.varType != 'unsupported':
                textbutton "Change" style_suffix "primary_button" action [Show('mod_modify_value', var=var),Hide('mod_var_changed')]
                null width mod.scalePxInt(10)
            textbutton "Revert" style_suffix 'red_button' align(0.0, 1.0) action modSetVarValue(var, onSuccess=Hide('mod_var_changed'), screenErrorVariable='errorMessage', newValue=prevVal)
            null width mod.scalePxInt(10)
            textbutton "Close" action Hide('mod_var_changed')
