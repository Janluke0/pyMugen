from .utils.parser import parse 

def from_file(fname):
    parsed = parse(fname)
    for s in parsed:
        print(s)
        for v in parsed[s]:
            print("\t", v, "=", parsed[s][v])
