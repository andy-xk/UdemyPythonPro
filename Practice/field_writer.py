import re

numbers = [
    '12.1', '123.567567567', '12345678.12345', '1234567.123', '12345678912345.4545',
    '12.2e+12', '12.53434343434343e-21', '10000000001E12',
    '3434E-2', '3.45678e+009',
    '3.45454444-4', '344444433.3+4', '+0.44-04'
]
numbers.extend( [ '-'+i for i in numbers])

def parse_number(n):
    re_number = re.compile(r'([+-]*)(\d*)([.]*)(\d*)([eE][+-]*\d+$|$|[+-]\d+$)')
    number_match = re.match(re_number, str(n))
    return number_match

def get_field_string_of_number(n, width=8):
    m = parse_number(n)
    sign = m.group(1)
    real = m.group(2)
    point = m.group(3)
    decimals = m.group(4)
    scientific = m.group(5)
    # remove + sign
    if sign == '+' or sign == '+-' or sign == '-+':
        sign = ''
    # remove leading zeros in scientific notation
    scientific = re.sub(r'(?<=e|E|\-)\+*[0]+(?=\d)', '', scientific)
    # remove + in scientific notation
    scientific = re.sub(r'(?<=e|E)\+*(?=\d)', '', scientific)
    # only big E in scientific notation
    scientific = re.sub(r'e', r'E', scientific)
    # add E in scientific notation
    scientific = re.sub(r'(^^[\+\-]\d+)', r'E\1', scientific)
    len_of_required_strings = len(sign) + len(scientific)
    rest_of_chars = width - len_of_required_strings
    # format float to rest of chars length
    precision = rest_of_chars - len(real) - len(point)
    if precision > 1:
        decimals_float = round(float('0.'+decimals), precision)
        decimals_short = re.sub(r'\d*\.', '',  str(decimals_float))
        #float_str = "{0:.{}f}".format(foo, rest_of_chars)
        number_str = sign + real + point + decimals_short + scientific
    elif precision == 0 or precision == -1:
        number_str = sign + real + scientific
    else:
        number_str = sign + real + point + decimals + scientific
        digits = 13
        number_str = "{0:.{1}E}".format(float(number_str), digits)
        number_str = get_field_string_of_number(number_str)
    #print(number_str, "Rest", rest_of_chars, "Precision", precision)
    return "{0:>{1}s}".format(number_str, width)

def check_parsing(numbers):
    width = 8
    for n in numbers:
        field_str = parse_number(n)
        print(str(n), '=', n, '=>', field_str) 
    for n in numbers:
        field_str = parse_number(n)
        print(str(n), '=', n, '=>', field_str.groups()) 

def check_writer(numbers, width=8):
    for n in numbers:
        field_str = parse_number(n)
        print(str(n), '=', n, '=>', field_str.groups()) 
        print(get_field_string_of_number(str(n), width))


if __name__ == "__main__":
    #check_parsing(numbers)
    check_writer(numbers,width=16)