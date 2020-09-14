try:
    from . import context
except:
    import context 

from  pymugen.formats import cmd
r = cmd.from_file('tests/test_data/kfm/kfm.cmd', 'utf-8-sig')
print(r)