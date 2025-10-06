
screen mod_snapshots():
    style_prefix "mod"
    default comparingSnapshotName = None
    default colWidth = [mod.scaleX(20), mod.scaleX(12), mod.scaleX(60)]
    default comparing = None
    default snapshotsPages = modPages(len(mod.Snapshots.snapshotNames), itemsPerPage=22)

    python:
        if len(mod.Snapshots.snapshotNames) != snapshotsPages.itemCount:
            SetField(snapshotsPages, 'itemCount', len(mod.Snapshots.snapshotNames))()

    hbox:
        spacing mod.scalePxInt(5)
        if comparing:
            use mod_iconbutton('\uf053', 'Back', action=SetLocalVariable('comparing', None))
            if len(comparing) > 1:
                text 'Comparing "{}" with "{}"'.format(comparing[0], comparing[1]) yalign .5
            else:
                text 'Comparing "{}" with "{}"'.format(comparing[0], 'Current variables') yalign .5
        else:
            use mod_iconbutton('\uf067', 'Create', action=Show('mod_snapshot_create'))
    frame style_suffix "seperator" ysize mod.scalePxInt(2) yoffset mod.scalePxInt(5)

    if comparing:
        if len(comparing) > 1:
            use mod_snapshots_comparison(comparing[0], comparing[1])
        else:
            use mod_snapshots_comparison(comparing[0])
    
    elif len(mod.Snapshots.snapshotNames) > 0:
        # PAGES
        fixed ysize mod.scalePxInt(50):
            hbox xalign .5 yoffset 4:
                use mod_pages(snapshotsPages)
            hbox xalign 1.0 yalign .5:
                text 'Snapshots: {}'.format(len(mod.Snapshots.snapshotNames))

        hbox: # Headers
            yoffset mod.scaleY(1)
            label "Name" xsize colWidth[0]
            label "Creation time" xsize colWidth[1]

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
                for name in mod.Snapshots.snapshotNames[snapshotsPages.pageStartIndex:snapshotsPages.pageEndIndex]:
                    hbox:
                        hbox xsize colWidth[0]:
                            text mod.scaleText(name, 18) substitute False

                        hbox xsize colWidth[1]:
                            text mod.Snapshots.getSnapshotTime(name)

                        hbox xsize colWidth[2]:
                            hbox:
                                if comparingSnapshotName: # Trying to compare?
                                    if comparingSnapshotName == name:
                                        use mod_iconbutton('\uf05e', 'Cancel', action=SetLocalVariable('comparingSnapshotName', None), inline=True)
                                    else:
                                        use mod_iconbutton('\uf362', 'Compare', action=[SetLocalVariable('comparing', [comparingSnapshotName,name]),SetLocalVariable('comparingSnapshotName', None)], inline=True)
                                else:
                                    use mod_iconbutton('\uf550', 'Show changes', SetLocalVariable('comparing', [name]), inline=True)
                                    use mod_iconbutton('\uf362', 'Compare with...', sensitive=(len(mod.Snapshots.snapshotNames) > 1), action=SetLocalVariable('comparingSnapshotName', name), inline=True)
                                    use mod_iconbutton('\uf146', 'Remove', mod.Confirm('Are you sure you want to remove this snapshot?', Function(mod.Snapshots.delete, name), title='Remove snapshot'), inline=True)

    else:
        vbox:
            yoffset mod.scaleY(1.5)
            xalign 0.5
            label "There are no snapshots yet" xalign 0.5
            null height mod.scalePxInt(15)
            text "Here you can create snapshots of all current variables and later use them to list all changed variables" xalign .5
            text "(snapshots can be compared to current variables or other snapshots)" xalign .5
            text "Note: Snapshots will be lost when closing the game" style_suffix 'text_small' xalign .5 yoffset mod.scalePxInt(10)


screen mod_snapshots_comparison(old, new=None):
    style_prefix "mod"

    default changes = mod.Snapshots.findChanges(old, new)
    default comparisonColWidth = [mod.scaleX(20), mod.scaleX(20), mod.scaleX(20)]
    default comparisonPages = modPages(len(changes), itemsPerPage=21)
    default compareDict = None
    default compareList = None

    if compareDict:
        hbox yoffset mod.scalePxInt(6):
            spacing mod.scalePxInt(5)
            use mod_iconbutton('\uf053', 'Back', action=SetLocalVariable('compareDict', None))
            text 'Comparing variable "{}"'.format(compareDict['old'].name) yalign .5
        frame style_suffix "seperator" ysize mod.scalePxInt(2) yoffset mod.scalePxInt(6)
        use mod_snapshots_dictCompare(compareDict)

    elif compareList:
        hbox yoffset mod.scalePxInt(6):
            spacing mod.scalePxInt(5)
            use mod_iconbutton('\uf053', 'Back', action=SetLocalVariable('compareList', None))
            text 'Comparing variable "{}"'.format(compareList['old'].name) yalign .5
        frame style_suffix "seperator" ysize mod.scalePxInt(2) yoffset mod.scalePxInt(6)
        use mod_snapshots_listCompare(compareList)

    elif len(changes) == 0:
        label "No changes were found" xalign 0.5 yoffset mod.scaleY(1.5)

    else:
        # PAGES
        fixed ysize mod.scalePxInt(50):
            hbox xalign .5 yoffset 4:
                use mod_pages(comparisonPages)
            hbox xalign 1.0 yalign .5:
                text 'Changes: {}'.format(len(changes))

        hbox: # Headers
            yoffset mod.scaleY(1)
            label "Name" xsize comparisonColWidth[0]
            label "Previous" xsize comparisonColWidth[1]
            label "New" xsize comparisonColWidth[2]

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
                for var in changes[comparisonPages.pageStartIndex:comparisonPages.pageEndIndex]:
                    hbox:
                        hbox xsize comparisonColWidth[0]:
                            text mod.scaleText(var['old'].name, 18) substitute False

                        hbox xsize comparisonColWidth[1]:
                            textbutton var['old'].getButtonValue(17) style_suffix 'inlinebutton' substitute False action Show('mod_modify_value', var=var['old'])

                        hbox xsize comparisonColWidth[2]:
                            textbutton var['new'].getButtonValue(17) style_suffix 'inlinebutton' substitute False action Show('mod_modify_value', var=var['new'])

                        hbox:
                            hbox:
                                # Remember
                                if mod.Loader.hasVar(var['new'].name):
                                    use mod_iconbutton('\uf328', 'Forget', Function(mod.Loader.forgetVar, var['new'].name), inline=True)
                                else:
                                    use mod_iconbutton('\uf46d', 'Remember', Show('mod_remember_var', varName=var['new'].name), inline=True)
                                # Watch
                                if mod.Loader.isWatchingVar(var['new'].name):
                                    use mod_iconbutton('\uf070', 'Unwatch', Function(mod.Loader.unwatchVar, var['new'].name), inline=True)
                                else:
                                    use mod_iconbutton('\uf06e', 'Watch', Show('mod_remember_var', varName=var['new'].name, rememberType='watchVar'), inline=True)
                                # List changes
                                if var['old'].varType == 'dict' and var['new'].varType == 'dict':
                                    use mod_iconbutton('\uf550', 'Show changes', SetLocalVariable('compareDict', var), inline=True)
                                elif var['old'].varType == 'list' and var['new'].varType == 'list':
                                    use mod_iconbutton('\uf550', 'Show changes', SetLocalVariable('compareList', var), inline=True)

screen mod_snapshots_dictCompare(compareVar):
    style_prefix "mod"

    default dictChanges = mod.Snapshots.findDictChanges(compareVar['old'].value, compareVar['new'].value)
    default dictComparisonColWidth = [mod.scaleX(20), mod.scaleX(20), mod.scaleX(20)]
    default dictComparisonPages = modPages(len(dictChanges), itemsPerPage=20)

    if len(dictChanges) == 0:
        label "No changes were found" xalign 0.5 yoffset mod.scaleY(1.5)
    
    else:
        # PAGES
        fixed ysize mod.scalePxInt(50):
            hbox xalign .5 yoffset 4:
                use mod_pages(dictComparisonPages)
            hbox xalign 1.0 yalign .5:
                text 'Changes: {}'.format(len(dictChanges))

        hbox: # Headers
            yoffset mod.scaleY(1)
            label "Name" xsize dictComparisonColWidth[0]
            label "Previous" xsize dictComparisonColWidth[1]
            label "New" xsize dictComparisonColWidth[2]

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
                for var in dictChanges[dictComparisonPages.pageStartIndex:dictComparisonPages.pageEndIndex]:
                    hbox:
                        hbox xsize dictComparisonColWidth[0]:
                            text mod.scaleText(var['old'].name, 18) substitute False

                        hbox xsize dictComparisonColWidth[1]:
                            textbutton var['old'].getButtonValue(17) style_suffix 'inlinebutton' substitute False action Show('mod_modify_value', var=var['old'])

                        hbox xsize dictComparisonColWidth[2]:
                            textbutton var['new'].getButtonValue(17) style_suffix 'inlinebutton' substitute False action NullAction()

screen mod_snapshots_listCompare(compareVar):
    style_prefix "mod"

    default listChanges = mod.Snapshots.findListChanges(compareVar['old'].value, compareVar['new'].value)
    default listComparisonColWidth = [mod.scaleX(15), mod.scaleX(70)]
    default listComparisonPages = modPages(len(listChanges), itemsPerPage=20)

    if len(listChanges) == 0:
        label "No changes were found" xalign 0.5 yoffset mod.scaleY(1.5)
    
    else:
        # PAGES
        fixed ysize mod.scalePxInt(50):
            hbox xalign .5 yoffset 4:
                use mod_pages(listComparisonPages)
            hbox xalign 1.0 yalign .5:
                text 'Changes: {}'.format(len(listChanges))

        hbox: # Headers
            yoffset mod.scaleY(1)
            label "Added/Remove" xsize listComparisonColWidth[0]
            label "Value" xsize listComparisonColWidth[1]

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
                for change in listChanges[listComparisonPages.pageStartIndex:listComparisonPages.pageEndIndex]:
                    hbox:
                        hbox xsize listComparisonColWidth[0]:
                            text change['type']

                        hbox xsize listComparisonColWidth[1]:
                            text mod.scaleText(str(change['val']), 68) substitute False


screen mod_snapshot_create():
    layer If('mod' in config.layers, 'mod', 'overlay')
    style_prefix "mod"

    default submitAction = Function(mod.Snapshots.create, name=GetScreenInput('nameInput'))
    default nameInput = Input(autoFocus=True, onEnter=[submitAction,Hide('mod_snapshot_create')])

    use mod_dialog(title='Create snapshot', closeAction=Hide('mod_snapshot_create'), modal=True):
        text "Enter a name:"
        button:
            style_suffix 'inputframe'
            xminimum mod.scalePxInt(450)
            key_events True
            action nameInput.Enable()
            input value nameInput

        hbox:
            yoffset mod.scalePxInt(15)
            align (1.0,1.0)
            textbutton "Create" style_suffix "primary_button" action [submitAction,Hide('mod_snapshot_create')]
            null width mod.scalePxInt(10)
            textbutton "Cancel" action Hide('mod_snapshot_create')

