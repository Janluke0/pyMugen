from configparser import ConfigParser
#TODO handle enconding
FILE_ENCODING = 'utf-8-sig' # kungfuman 
#FILE_ENCODING = 'latin-1' #for luffy 

#TODO: handle command duplicate sections
def parse(file, encoding=None):
    c = ConfigParser(interpolation=None,inline_comment_prefixes=[';'], strict=False)
    c.read(file, encoding=FILE_ENCODING if encoding is None else encoding)
    return c
