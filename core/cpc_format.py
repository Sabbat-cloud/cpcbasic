import re
import math

_pattern = re.compile(
    r'(!'
    r'|\\[ ]*\\'
    r'|&'
    r'|(?:\+)?'
    r'(?:\*\*Pt|\*\*\$|\*\*|PtPt|\$\$)?'
    r'(?:[#,]*#+[#,]*\.?[#]*|\.[#]+)'
    r'(?:\^\^\^\^)?'
    r'(?:[\+\-])?)'
)

def format_cpc_field(val, fmt):
    if fmt == '!':
        return str(val)[0] if str(val) else ""
    elif fmt.startswith('\\') and fmt.endswith('\\'):
        return str(val)[:len(fmt)]
    elif fmt == '&':
        return str(val)
        
    try:
        val = float(val)
    except:
        val = 0.0

    prefix_plus = False
    suffix_plus = False
    suffix_minus = False
    
    if fmt.startswith('+'):
        prefix_plus = True
        fmt = fmt[1:]
    if fmt.endswith('+'):
        suffix_plus = True
        fmt = fmt[:-1]
    elif fmt.endswith('-'):
        suffix_minus = True
        fmt = fmt[:-1]
        
    exp_format = False
    if fmt.endswith('^^^^'):
        exp_format = True
        fmt = fmt[:-4]
        
    fill_char = ' '
    currency = ''
    if fmt.startswith('**Pt'):
        fill_char = '*'
        currency = 'Pt'
        fmt = fmt[4:]
    elif fmt.startswith('**$'):
        fill_char = '*'
        currency = '$'
        fmt = fmt[3:]
    elif fmt.startswith('**'):
        fill_char = '*'
        fmt = fmt[2:]
    elif fmt.startswith('PtPt'):
        currency = 'Pt'
        fmt = fmt[4:]
    elif fmt.startswith('$$'):
        currency = '$'
        fmt = fmt[2:]
        
    digits_part = fmt
    if '.' in digits_part:
        int_part_fmt, frac_part_fmt = digits_part.split('.', 1)
        has_dot = True
    else:
        int_part_fmt, frac_part_fmt = digits_part, ""
        has_dot = False
        
    use_comma = ',' in int_part_fmt
    
    W_int = len(int_part_fmt)
    if fill_char == '*' and currency == 'Pt':
        W_int += 3
    elif fill_char == '*' and currency == '$':
        W_int += 3
    elif fill_char == '*' and not currency:
        W_int += 2
    elif not fill_char == '*' and currency == 'Pt':
        W_int += 2
    elif not fill_char == '*' and currency == '$':
        W_int += 2
        
    frac_places = len(frac_part_fmt)
    
    is_negative = val < 0
    abs_val = abs(val)
    
    exponent_str = ""
    if exp_format:
        if abs_val == 0:
            exponent = 0
        else:
            exponent = int(math.floor(math.log10(abs_val)))
            
        abs_val = abs_val / (10**exponent)
        abs_val = round(abs_val, frac_places)
        if abs_val >= 10.0:
            abs_val /= 10.0
            exponent += 1
            
        exponent_str = f"E{exponent:+03d}"
    else:
        abs_val = round(abs_val, frac_places)
        
    int_val = int(abs_val)
    if frac_places > 0:
        frac_str = f"{abs_val:.{frac_places}f}".split('.')[1]
    else:
        frac_str = ""
        
    int_str = str(int_val)
    if use_comma:
        parts = []
        while len(int_str) > 3:
            parts.insert(0, int_str[-3:])
            int_str = int_str[:-3]
        parts.insert(0, int_str)
        int_str = ",".join(parts)
        
    sign_str = ""
    trailing_sign_str = ""
    
    if suffix_minus:
        trailing_sign_str = "-" if is_negative else " "
        is_negative = False
    elif suffix_plus:
        trailing_sign_str = "-" if is_negative else "+"
        is_negative = False
        
    if prefix_plus:
        sign_str = "-" if is_negative else "+"
        is_negative = False
    else:
        if is_negative:
            sign_str = "-"
            is_negative = False
            
    content_len = len(int_str) + len(currency)
    if not prefix_plus:
        content_len += len(sign_str)
        
    if content_len > W_int:
        return f"%{val}"
        
    pad_len = max(0, W_int - content_len)
    padding = fill_char * pad_len
    
    assembled_int = padding + sign_str + currency + int_str
    
    res = assembled_int
    if has_dot:
        res += "." + frac_str
    res += exponent_str
    res += trailing_sign_str
    
    return res

def format_cpc_using(vals, fmt_str):
    if not vals:
        return fmt_str
        
    out = ""
    val_idx = 0
    
    while val_idx < len(vals):
        last_idx = 0
        found_field = False
        for m in _pattern.finditer(fmt_str):
            found_field = True
            
            literal = fmt_str[last_idx:m.start()]
            
            if val_idx < len(vals):
                out += literal
                field_fmt = m.group(0)
                out += format_cpc_field(vals[val_idx], field_fmt)
                val_idx += 1
            else:
                break
                
            last_idx = m.end()
            
        if not found_field:
            out += fmt_str
            break
            
        if val_idx >= len(vals):
            # Check if there are any remaining fields in the rest of the string
            # If not, we append the literal part.
            rest = fmt_str[last_idx:]
            if not _pattern.search(rest):
                out += rest
            break
            
    return out
