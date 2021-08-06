from .errorhandling import raise_error
import re


br_open = ["[","{","("]
br_close = ["]","}",")"]
q_chars = ["\"","'"]


def split_ranges(rangestring):
    crange = rangestring.split(" ")
    indicies = []
    for elem in crange:
        try:
            if "-" in elem:
                rangevals = elem.split("-")
                lval = int(rangevals[0].strip())
                rval = int(rangevals[1].strip())
                indicies += list(range(lval, rval+1))
            else:
                indicies.append(int(elem.strip()))
        except Exception:
            raise_error(rangestring, "invalid array selection specifier")
    return indicies

def validate_re(re_expression):
    try:
        re.compile(re_expression)
    except re.error as e:
        raise_error(re_expression, str(e))

def skip_quotes(data,index):
    tchar = data[index]
    assert tchar in q_chars
    eidx = index+1
    while not (data[eidx] == tchar and data[eidx-1] != "\\"):  #\"
        eidx+=1
        if eidx >= len(data):
            raise_error(data[index:index+50],f"end of text, unmatched quote at col {index}")
    return eidx

def match_bracket(data,index):
    tchar = data[index]
    br_stack = [tchar]
    assert tchar in br_open
    eidx = index+1
    while br_stack:
        cchar = data[eidx]
        if cchar in q_chars:
            eidx = skip_quotes(data,eidx)
        elif cchar in br_open:
            br_stack.append(cchar)
        elif cchar in br_close:
            brindex = br_open.index(br_stack[-1])
            if cchar != br_close[brindex]:
                raise_error(data[eidx:max(eidx+50,len(data))],f"unexpected {cchar} at {eidx}")
            else:
                br_stack.pop()
        eidx+=1
        if eidx >= len(data) and br_stack:
            raise_error(data[index:index+50],f"end of text, unmatched {tchar}")
    return eidx-1 # eidx will get incremented after last parenthesis


def parse_logical(data,startindex,endindex):
    idx = startindex
    buffer = ""
    elements = []
    while idx<endindex:
        tchar = data[idx]
        if tchar in q_chars:
            eidx = skip_quotes(data,idx)
            buffer += data[idx:eidx+1]
            idx=eidx
        elif tchar in br_open:
            eidx = match_bracket(data,idx)
            items = parse_logical(data,idx+1,eidx)
            buffer = buffer.strip().replace("\"","")
            if buffer:
                elements.append({buffer:items})
                buffer = ""
            else:
                elements.append(items)
            idx = eidx
        elif tchar == "," or tchar == "\n":
            if buffer:
                elements.append(buffer.strip().replace("\"",""))
                buffer = ""
        else:
            buffer+=tchar
        idx+=1
    if buffer:
        elements.append(buffer.strip())
    return elements
    

