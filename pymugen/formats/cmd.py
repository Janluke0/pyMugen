#TODO
from .cns import parse_cns

def from_file(path,encoding=None):
    a = parse_cns(path, encoding)
    commands = []
    with open(path,"r",encoding=encoding) as f:
        cmd = None
        for l in f.readlines():
            if l.strip() == "" or l.strip().startswith(";"):
                continue
            if l.strip().startswith("[") and cmd is not None:
                commands.append(cmd)
                cmd = None
            if l.strip() == "[Command]":
                cmd = {}
            if "=" in l and cmd is not None:
                k,v = l.strip().split("=")
                cmd[k.strip()] = v.split(";")[0].replace("\"","").strip()
    return a, {
                c['name'] : 
                (c['command'], int(c['time']) if 'time' in c else None) 
                for c in commands
            }