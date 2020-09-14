from .utils.parser import parse

class State:
    def __init__(self
                , code
                , _type
                , move_type
                , physics
                , anim
                , velset=None
                , ctrl=None
                , poweradd=0
                , juggle=None
                , facep2=False
                , hitdefpersist=False
                , movehitpersist=False
                , hicountpersist=False
                , sprpriority=None):
        """
            code: int
                the state code

            _type: str ["S", "C" , "A" or "L"]
                the state type: 
                standing, crouching, in the air or lying down.

            move_type: str ["A", "I" or "H"]
                the type of move done by the state: 
                attack, idle or being hit. 

            physics: str ["S", "C", "A", "N" or "U"]
                physics to use in the state: 
                stand, crouch, air, none, unchanged

            anim: int 
                The animation code

            velset: (int, int)
                the initial velocity components

            ctrl: bool
                set or unset control to P1 (???)
                if None is left unchanged

            poweradd: int
                amount of power added (or removed) by the state  

            juggle: int
                TODO: undestand this juggling concept
                
            facep2: bool
                if true the player will be turned, if necessary, 
                to face the opponent          

            hitdefpersist: bool
                TODO:            

            movehitpersist: bool
                TODO:            

            hitcountpersist: bool
                TODO:                

            sprpriority: int
                sprite priority             
        """
        super().__init__()
        self.code = code
        self._type = _type
        self.move_type = move_type
        self.physics = physics
        self.anim = anim
        self.velset = velset
        self.ctrl = ctrl
        self.poweradd = poweradd
        self.juggle = juggle
        self.facep2 = facep2
        self.hitdefpersist = hitdefpersist
        self.movehitpersist = movehitpersist
        self.hicountpersist = hicountpersist
        self.sprpriority = sprpriority
        self.controllers = []

    def __repr__(self):
        out = f"State(code={self.code}, type={self._type}"
        out += f", movetype={self.move_type}, controllers={self.controllers})"
        return out

    @staticmethod
    def from_dict(d, code):
        return State(code
                    , None if 'type' not in d else d['type']
                    , "I" if 'movetype' not in d else d['movetype']
                    , "N" if 'physics' not in d else d['physics']
                    , None if 'anim' not in d else d['anim']
                    , velset=None if 'velset' not in d else d['velset'] 
                    , ctrl=None if 'ctrl' not in d else d['ctrl'] 
                    , poweradd=0 if 'poweradd' not in d else d['poweradd'] 
                    , juggle=None if 'juggle' not in d else d['juggle'] 
                    , facep2=False if 'facep2' not in d else d['facep2'] 
                    , hitdefpersist=False if 'hitdefpersist' not in d else d['hitdefpersist'] 
                    , movehitpersist=False if 'movehitpersist' not in d else d['movehitpersist'] 
                    , hicountpersist=False if 'hicountpersist' not in d else d['hicountpersist'] 
                    , sprpriority=False if 'sprpriority' not in d else d['sprpriority'] 
            )
class StateController:
    def __init__(self
                , state_code
                , name
                , _type
                , triggers 
                , args):
        """
            state_code: int
                the relative state
            name: str
                should be unique between state controller of the same state
            _type: str 
            triggers: List[Trigger]
            args: dict
                depends by the controller type
        """
        super().__init__()
        self.state_code = state_code
        self.name = name
        self._type = _type
        self.triggers = triggers
        self.args = args

    def __repr__(self):
        out = f"StateController(state={self.state_code}, name={self.name}"
        out += f", type={self._type}, triggers={self.triggers}"
        out += f", args={self.args})"
        return out


"""   
# for now just focus on reading files the following
# will be useful when try to build a engine
class CtrlSet:
    def __init__(self, args):
        super().__init__()
        if "value" not in args:
            raise ValueError("Required argument 'value' is missing")
        self.enable_control = int(args['value']) == 1

    def run(self):
        pass
"""

def parse_cns(fname, encoding=None):
    parsed = parse(fname, encoding)
    states = []
    orphan_ctrls = []
    unamed_ctrls = 0
    #parse state
    for s_name in parsed.sections():
        if "Statedef" in s_name:
            se = parsed[s_name]
            code = int(s_name.split(" ")[1].strip())
            states.append(State.from_dict(se,code))
    # parse state controller
    for s_name in parsed.sections():
        if "State " in s_name:
            try:
                state_code, ctrl_name = s_name.split(",")
            except ValueError:
                state_code, ctrl_name = s_name, f"anon_{unamed_ctrls}"
                unamed_ctrls += 1
            state_code = int(state_code.split()[1].strip())
            se = parsed[s_name]
            triggers = []
            #parse triggers
            opts = {k:se[k] for k in se}
            t_all = None
            for k,v in opts.items():
                if k.startswith("trigger"):
                    t_code = k.replace("trigger","").strip().lower()
                    if t_code == "all":
                        t_all = [v]
                    else:
                        n = int(t_code)
                        t = [v]
                        if t_all is not None:
                            t.append(t_all)
                        if len(triggers) < n:
                            triggers.append(t)
                        else:
                            triggers[-1].append(t)
            args = {k:v for k,v in opts.items() 
                    if not k.startswith("trigger") and k !='type'} 
            ctrl = StateController(state_code, ctrl_name.strip(), se['type'], triggers, args)
            try:
                state = next((s for s in states if s.code == state_code))
                state.controllers.append(ctrl)
            except StopIteration:
                orphan_ctrls.append(ctrl) 
                
    return states, orphan_ctrls
