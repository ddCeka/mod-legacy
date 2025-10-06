
init python:
    class modChoicesClass(NonPicklable):
        @property
        def isDisplayingChoice(self):
            try:
                current = renpy.game.context().current
                script = renpy.game.script.lookup(current)
                return isinstance(script, renpy.ast.Menu)
            except:
                return False
        
        @property
        def currentChoices(self):
            try:
                current = renpy.game.context().current
                script = renpy.game.script.lookup(current)
                if isinstance(script, renpy.ast.Menu): 
                    choices = []
                    for i,item in enumerate(script.items):
                        if len(item) >= 3 and item[2]:
                            choices.append(modChoice(i, item))
                    return choices
            except:
                pass
        
        @property
        def hiddenCount(self):
            count = 0
            for choice in self.currentChoices or []:
                if not choice.isVisible:
                    count += 1
            return count

    class modChoice(NonPicklable):
        """
        The tuple exists of 3 items
        0: The text
        1: Condition
        2: Choice content in a list
        """
        def __init__(self, index, choiceTuple):
            self._m1_choices__index = index
            self._m1_choices__choice = choiceTuple
            self._m1_choices__code = None
            self._m1_choices__jumpTo = None
        
        @property
        def isVisible(self):
            """ Is this choice available? """
            return eval(self.condition)
        
        @property
        def text(self):
            """ Get the option text (not translated!) """
            try:
                return renpy.exports.substitute(self._m1_choices__choice[0])
            except:
                return self._m1_choices__choice[0]
        
        @property
        def condition(self):
            return self._m1_choices__choice[1]
        
        @property
        def code(self):
            if self._m1_choices__code == None:
                self._m1_choices__code = ''
                if hasattr(self._m1_choices__choice[2], '__iter__'):
                    for content in self._m1_choices__choice[2]:
                        if isinstance(content, renpy.ast.Python) and hasattr(content, 'code') and hasattr(content.code, 'source'):
                            if not content.code.source.startswith('renpy.pause(') and not content.code.source.startswith('ui.'): 
                                self._m1_choices__code += content.code.source+'\n'
                self._m1_choices__code = self._m1_choices__code.strip()
            return self._m1_choices__code
        
        @property
        def jumpTo(self):
            if self._m1_choices__jumpTo == None:
                self._m1_choices__jumpTo = ''
                for content in self._m1_choices__choice[2]:
                    if isinstance(content, renpy.ast.Jump):
                        self._m1_choices__jumpTo = content.target
                        break
            return self._m1_choices__jumpTo
        
        @property
        def Action(self):
            return renpy.ui.ChoiceReturn(self.text, self._m1_choices__index)
