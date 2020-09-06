try:
    from . import context
except:
    import context 
from pymugen.formats.cns import parse_cns


if __name__ == "__main__":
    a,b = parse_cns("tests/test_data/G6_Luffy/Luffy.cns", 'latin-1')
    print(b)
    a,b = parse_cns("tests/test_data/G6_Luffy/tag_system.cns", 'latin-1')
    print(b)
    print()
    a,b = parse_cns("tests/test_data/kfm/kfm.cns")
    print(a,b)