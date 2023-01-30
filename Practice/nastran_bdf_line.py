import argparse
import re
from functools import partial
from io import StringIO

def init_re():
    global re_comment
    re_comment = re.compile(r'^\$')
    global re_comma_separated 
    re_comma_separated = re.compile(r',')
    global re_long_format 
    re_long_format = re.compile(r'^\*')
    global re_empty_line
    re_empty_line = re.compile(r'^\s*$')

def parse(line):
    print(line)
    fields = []
    # if comment
    if re.match(re_comment, line):
        ltype = 'c'
        fields = [ line ]
    #if long format
    elif re.match(re_long_format, line):
        ltype = 'l'
        fields.append(line[0:8])
        line = line[8:]
        lfields = [l for l in iter(partial(StringIO(line).read, 16), '')]
        fields.extend(lfields)
    #if comma separated
    elif re.search(re_comma_separated, line):
        ltype = 'm'
        fields = line.split(',')
    #empty line
    elif re.match(re_empty_line, line):
        ltype = 'e'
        fields = [ line ]
    else:
        ltype = 's'
        fields = [l for l in iter(partial(StringIO(line).read, 8), '')]

    return (ltype, fields)

def get_bdf_line_of_fields(ltype, fields):
    if ltype == 'm':
        return ','.join(map(str, fields))
    else:
        return ''.join(map(str, fields))

def set_field(ltype, fields, field_number, field_value):
    if len(fields)<field_number:
        return ltype, fields
    if ltype == 's':
        fields[field_number-1]="{0:>8}".format(str(field_value))
    elif ltype == 'l':
        fields[field_number-1]="{0:>16}".format(str(field_value))
    elif ltype == 'm':
        fields[field_number-1]=str(field_value)
    # do nothing for comment and empty line
    # to do: what if you want to set fields of empty line?
    return ltype, fields

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--line", help="bdf line", type=str, required=True
    )
    parser.add_argument(
        "--output_type", help="Output type (str)", type=str, required=False,
        default='small'
    )

    args = parser.parse_args()

    line = args.line

    print(line, type(line))
    init_re()
    ltype, fields = parse(line)
    print(fields)
    print(get_bdf_line_of_fields(ltype, fields))
    set_field(ltype, fields, 2, 'NEW')
    print(get_bdf_line_of_fields(ltype, fields))




if __name__ == "__main__":
    main()
