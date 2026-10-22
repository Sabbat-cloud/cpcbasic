import re
import math

_token_pattern = re.compile(
    r'(_.'
    r'|!'
    r'|\\[ ]*\\'
    r'|&'
    r'|(?:\+)?'
    r'(?:\*\*Pt|\*\*\$|\*\*£|\*\*|PtPt|\$\$|££)?'
    r'(?:[#,]*#+[#,]*\.?[#]*|\.[#]+)'
    r'(?:\^\^\^\^)?'
    r'(?:[\+\-])?)'
)

def cpc_round_half_away(val, decimals=0):
    m = 10.0 ** decimals
    v = val * m
    r = math.copysign(math.floor(abs(v) + 0.5), v)
    return r / m if decimals > 0 else float(int(r))

def format_cpc_field(val, fmt):
    if fmt == '!':
        s = str(val)
        return s[0] if s else " "
    elif fmt.startswith('\\') and fmt.endswith('\\'):
        s = str(val)
        return s[:len(fmt)].ljust(len(fmt))
    elif fmt == '&':
        return str(val)
        
    try:
        val = float(val)
    except Exception:
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
    elif fmt.startswith('**£'):
        fill_char = '*'
        currency = '£'
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
    elif fmt.startswith('££'):
        currency = '£'
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
    if prefix_plus:
        W_int += 1
    if fill_char == '*' and currency == 'Pt':
        W_int += 3
    elif fill_char == '*' and currency in ('$', '£'):
        W_int += 3
    elif fill_char == '*' and not currency:
        W_int += 2
    elif fill_char != '*' and currency == 'Pt':
        W_int += 2
    elif fill_char != '*' and currency in ('$', '£'):
        W_int += 2
        
    frac_places = len(frac_part_fmt)
    
    is_negative = val < 0
    abs_val = abs(val)
    
    exponent_str = ""
    if exp_format:
        prefix_reserved = len(currency) + (0 if (suffix_plus or suffix_minus) else 1)
        digits_before_dp = max(0, W_int - prefix_reserved)
        if abs_val == 0:
            exponent = 0
            scaled = 0.0
        else:
            e10 = int(math.floor(math.log10(abs_val))) + 1
            exponent = e10 - digits_before_dp
            scaled = abs_val / (10.0 ** exponent)
            scaled = cpc_round_half_away(scaled, frac_places)
            limit = 10.0 ** digits_before_dp
            if scaled >= limit:
                scaled /= 10.0
                exponent += 1
        abs_val = scaled
        exponent_str = f"E{exponent:+03d}"
    else:
        abs_val = cpc_round_half_away(abs_val, frac_places)
        
    int_val = int(abs_val)
    if frac_places > 0:
        frac_str = f"{abs_val:.{frac_places}f}".split('.')[1]
    else:
        frac_str = ""
        
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

    if int_val == 0 and has_dot and W_int <= len(sign_str) + len(currency):
        int_str = ""
    else:
        int_str = str(int_val)

    if use_comma and not exp_format and len(int_str) > 3:
        parts = []
        while len(int_str) > 3:
            parts.insert(0, int_str[-3:])
            int_str = int_str[:-3]
        parts.insert(0, int_str)
        int_str = ",".join(parts)
            
    content_len = len(int_str) + len(currency) + len(sign_str)
        
    if content_len > W_int and not exp_format:
        res = "%" + sign_str + currency + int_str
        if has_dot:
            res += "." + frac_str
        res += exponent_str
        res += trailing_sign_str
        return res
        
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
    # Break fmt_str into segments: ('LIT', text) or ('FMT', spec)
    segments = []
    last_idx = 0
    for m in _token_pattern.finditer(fmt_str):
        if m.start() > last_idx:
            segments.append(('LIT', fmt_str[last_idx:m.start()]))
        tok = m.group(0)
        if tok.startswith('_') and len(tok) == 2:
            segments.append(('LIT', tok[1]))
        else:
            segments.append(('FMT', tok))
        last_idx = m.end()
    if last_idx < len(fmt_str):
        segments.append(('LIT', fmt_str[last_idx:]))

    has_fmt = any(kind == 'FMT' for kind, _ in segments)
    if not vals:
        return "".join(v for kind, v in segments if kind == 'LIT') if not has_fmt else ""

    if not has_fmt:
        return "".join(v for _, v in segments)

    out = ""
    val_idx = 0
    while val_idx < len(vals):
        for idx, (kind, text) in enumerate(segments):
            if kind == 'LIT':
                out += text
            else:
                if val_idx < len(vals):
                    out += format_cpc_field(vals[val_idx], text)
                    val_idx += 1
                    if val_idx >= len(vals):
                        # Append trailing literals up to next FMT
                        for k2, t2 in segments[idx + 1:]:
                            if k2 == 'LIT':
                                out += t2
                            else:
                                break
                        break
    return out
