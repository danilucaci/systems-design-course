"""Two-node register histories. CP uses a fixed primary and deliberately has no failover."""
class Unavailable(Exception): pass


class Register:
    def __init__(self,mode):
        if mode not in ('cp','ap'): raise ValueError('choose cp or ap')
        self.mode=mode; self.connected=True
        self.states={'A':(0,'A',0),'B':(0,'A',0)}

    def read(self,node):
        if node not in self.states: raise ValueError('unknown node')
        if self.mode=='cp':
            if node=='B' and not self.connected: raise Unavailable('cannot reach the fixed primary')
            return self.states['A'][2]
        return self.states[node][2]

    def write(self,node,value):
        if node not in self.states: raise ValueError('unknown node')
        if self.mode=='cp':
            if node=='B' and not self.connected: raise Unavailable('cannot reach the fixed primary')
            destination='A'
        else: destination=node
        previous=self.states[destination]
        self.states[destination]=(previous[0]+1,destination,value)
        if self.connected: self.heal()

    def partition(self): self.connected=False

    def heal(self):
        winner=self.states['A'] if self.mode=='cp' else max(self.states.values(),key=lambda value:value[:2])
        self.states={'A':winner,'B':winner}; self.connected=True
