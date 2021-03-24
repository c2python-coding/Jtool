from jtool.execution.registry import register_command
from jtool.utils.errorhandling import raise_error
from jtool.utils.markup_utils import TAG_KEY, INNER_KEY, SPECIAL_HTML_KEYS
import re




def lambda_istag(tag):
    if isinstance(tag, dict) and TAG_KEY in tag:
        return tag
    if isinstance(tag, list):
        raise_error(tag, "recieved a list, expecting a tag structure")
    raise_error(tag, "wrongly formatted tag structure")

def lambda_ismarkup(markup):
    if isinstance(markup, str):
        return markup
    return lambda_istag(markup)
    

def lambda_hascontent(tag):
    if INNER_KEY in lambda_istag(tag):
        return tag
    raise_error(tag, "tag has no inner content")


def tag_matcher(tagdict, tagtype, attrdict):
    if isinstance(tagdict, dict):
        if tagtype and tagtype != tagdict[TAG_KEY]:
            return False
        for item in attrdict:
            if (item not in tagdict) or (attrdict[item] != tagdict[item]):
                return False
        return True
    return False


def tag_search(condition_lambda, tags):
    accum_array = []
    if isinstance(tags, list):
        for item in tags:
            accum_array += tag_search(condition_lambda, item)
    elif isinstance(tags, dict):
        if condition_lambda(tags):
            accum_array = [tags]
        if INNER_KEY in tags:
            accum_array += tag_search(condition_lambda, tags[INNER_KEY])
    return accum_array



@register_command("tagtype")
def TAGTYPE_OP():
    '''returns the htmltag'''
    return lambda tag: lambda_type(tag, dict)[lambda_member(TAG_KEY, tag)]


@register_command("tagattrs")
def TAGATTRS_OP():
    '''returns the tag attributes'''
    extract_attrs = lambda tag: {key: tag[key] for key in tag if key not in SPECIAL_HTML_KEYS}
    return lambda markup: extract_attrs(lambda_type(markup, dict))


@register_command("innerhtml")
def INNERHTML_OP():
    '''return an array of the tags inner content'''
    return lambda markup: lambda_hascontent(markup)[INNER_KEY]


@register_command("childtags")
def CHILDTAGS_OP():
    '''return an array of child tags, excluding inner html text'''
    tagfilter = lambda innerlist: [lambda_istag(tag) for tag in innerlist if isinstance(tag,dict)]
    return lambda ptag: tagfilter(ptag[INNER_KEY]) if INNER_KEY in lambda_istag(ptag) else []



def get_attr_dict(attrstring):
    # extra space will cause the attribute to process
    # instead of handling non empty buffers at the end of the line
    attrstring += " "
    keybuffer = []
    valbuffer = []
    accumulator = {}
    target = keybuffer
    match = None
    idx = 0
    while idx < len(attrstring):
        if match:
            if attrstring[idx] == match:
                match = None
            else:
                target.append(attrstring[idx])
        else:
            # escape stuff in quotes as one single entry
            if attrstring[idx] in ["'", "\""]:
                match = attrstring[idx]
            elif attrstring[idx] == "=":
                target = valbuffer
            elif attrstring[idx] == " ":
                if target is keybuffer:
                    # handles attributes without an = value
                    accumulator["".join(keybuffer)] = None
                    keybuffer.clear()
                else:
                    accumulator["".join(keybuffer)] = "".join(valbuffer)
                    keybuffer.clear()
                    valbuffer.clear()
                    target = keybuffer
            else:
                target.append(attrstring[idx])
        idx += 1
    if keybuffer or valbuffer:
        raise_error(attrstring, "wrongly formatted attribute spec")
    for key in accumulator:
        if not accumulator[key]:
            raise_error(key, "wrongly formatted attribute spec value")
    return accumulator



@register_command("findtags")
def FINDALL_OP(tagspec):
    '''finds all descendant tags by specification (tagtype arrt1=val1 attr2=val2) and returns an array'''
    tsplit = tagspec.partition(" ")
    if "=" not in tsplit[0]:
        f_type = tsplit[0]
        attr_string = tsplit[2]
    else:
        f_type = None
        attr_string = tagspec
    f_attrs = get_attr_dict(attr_string) if attr_string else {}
    matcher = lambda tag, tt=f_type, td=f_attrs: tag_matcher(lambda_ismarkup(tag), tt, td)
    return lambda markup: tag_search(matcher, markup) 
