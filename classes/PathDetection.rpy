
init python:
    class modPathDetectionClass(NonPicklable):
        lookAheadLimit = 20
        
        def nodeIsBlocking(self, node):
            """ Test if a node is blocking/waiting for user interaction """
            if hasattr(node, 'interact') and node.interact: 
                return True
            elif isinstance(node, renpy.ast.UserStatement) and hasattr(node, 'get_code') and callable(node.get_code): 
                code = node.get_code()
                if code == 'pause':
                    return True
            
            return False
        
        def nextNode(self, node):
            """ Find next node, even if it's a new label (jump/call) """
            if isinstance(node, renpy.ast.Call):
                if hasattr(node, 'label') and node.label:
                    return renpy.game.script.lookup(node.label)
            elif isinstance(node, renpy.ast.Jump):
                if hasattr(node, 'predict') and callable(node.predict):
                    predict = node.predict()
                    if len(predict) > 0 and isinstance(predict[0], renpy.ast.Node):
                        return predict[0]
            elif hasattr(node, 'next'):
                return node.next
        
        @property
        def nextIfStatement(self):
            try:
                current = renpy.game.script.lookup(renpy.game.context().current)
                forceableNode = True 
                
                
                if not self.nodeIsBlocking(current):
                    return None
                
                
                next = self.nextNode(current)
                for i in range(self.lookAheadLimit): 
                    if next:
                        if isinstance(next, renpy.ast.If): 
                            return (next, forceableNode)
                        elif self.nodeIsBlocking(next): 
                            break
                        elif isinstance(next, renpy.ast.Jump) or isinstance(next, renpy.ast.Call):
                            forceableNode = False 
                        
                        
                        next = self.nextNode(next)
                    else:
                        break 
            except:
                pass
            
            return None
        
        @property
        def pathIsNext(self):
            return bool(self.nextIfStatement)
        
        @property
        def statements(self):
            try:
                ifStatement = self.nextIfStatement
                if ifStatement:
                    statements = []
                    for i,item in enumerate(ifStatement[0].entries):
                        if len(item) >= 2:
                            statements.append(modPath(i, item, ifStatement[1]))
                    return statements
            except:
                pass
        
        @property
        def selectedIndex(self):
            for i,statement in enumerate(self.statements):
                if statement.isSelected:
                    return i
        
        @property
        def statementsCount(self):
            try:
                return len(self.statements)
            except:
                return 0

    class modPath(NonPicklable):
        """
        The `data` is a tuple that exists of 2 items
        0: Condition
        1: Nodes (code)
        """
        def __init__(self, index, data, forceable=False):
            self._m1_PathDetection__index = index
            self._m1_PathDetection__condition = data[0]
            self._m1_PathDetection__nodes = data[1]
            self._m1_PathDetection__forceable = forceable
            self._m1_PathDetection__code = None
            self._m1_PathDetection__jumpTo = None
        
        @property
        def forceable(self):
            return self._m1_PathDetection__forceable
        
        @property
        def isSelected(self):
            """ The condition for this statement is true? """
            try:
                return eval(self._m1_PathDetection__condition)
            except:
                return False
        
        @property
        def condition(self):
            return self._m1_PathDetection__condition
        
        @property
        def code(self):
            if self._m1_PathDetection__code == None:
                self._m1_PathDetection__code = ''
                if hasattr(self._m1_PathDetection__nodes, '__iter__'):
                    for content in self._m1_PathDetection__nodes:
                        if isinstance(content, renpy.ast.Python) and hasattr(content, 'code') and hasattr(content.code, 'source'):
                            if not content.code.source.startswith('renpy.pause(') and not content.code.source.startswith('ui.'): 
                                self._m1_PathDetection__code += content.code.source+'\n'
                self._m1_PathDetection__code = self._m1_PathDetection__code.strip()
            return self._m1_PathDetection__code
        
        @property
        def jumpTo(self):
            if self._m1_PathDetection__jumpTo == None:
                self._m1_PathDetection__jumpTo = ''
                for content in self._m1_PathDetection__nodes:
                    if isinstance(content, renpy.ast.Jump):
                        self._m1_PathDetection__jumpTo = content.target
                        break
            return self._m1_PathDetection__jumpTo
        
        @property
        def Action(self):
            if not self.forceable: return None
            
            class SetNode():
                def __init__(self, node):
                    self._m1_PathDetection__node = node
                
                def __call__(self):
                    try:
                        
                        targetIf = mod.PathDetection.nextIfStatement[0] if mod.PathDetection.nextIfStatement else None
                        
                        if targetIf:
                            if renpy.game.context().next_node == targetIf: 
                                renpy.game.context().next_node = self._m1_PathDetection__node
                            
                            else: 
                                import copy
                                
                                currentNode = copy.copy(renpy.game.context().next_node)
                                newChain = currentNode
                                
                                for i in range(mod.PathDetection.lookAheadLimit): 
                                    if not currentNode.next: break 
                                    
                                    if currentNode.next == targetIf: 
                                        currentNode.next = self._m1_PathDetection__node
                                        renpy.game.context().next_node = newChain
                                        break
                                    else: 
                                        currentNode.next = copy.copy(currentNode.next)
                                        currentNode = mod.PathDetection.nextNode(currentNode)
                    
                    except Exception as e:
                        print('mod: Failed to force path choice: {}'.format(e))
            
            if mod.Choices.isDisplayingChoice:
                return None
            
            return [SetNode(self._m1_PathDetection__nodes[0]),Return()]
