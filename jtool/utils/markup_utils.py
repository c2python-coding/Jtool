from html.parser import HTMLParser
from .errorhandling import assert_with_data, raise_error
from .constants import PRETTY_INDENT as p_ind

TAG_KEY = "<tag>"
INNER_KEY = "<inner_content>"
PARENT_KEY = "<parent_key>"
SPECIAL_HTML_KEYS = [TAG_KEY, INNER_KEY, PARENT_KEY]
no_close_tags = ["img", "input", "br", "hr", "meta", "etc", "link", "source"]


def format_data(datastr, convert_to_nums=False):
    if datastr is None:
        return None
    testdata = datastr.replace("\n", "").replace(" ", "")
    if not testdata:
        return ""
    if convert_to_nums:
        try:
            intval = int(datastr)
            return intval
        except ValueError:
            pass
        try:
            floatval = float(datastr)
            return floatval
        except ValueError:
            pass
    returnarray = [x.strip() for x in datastr.split("\n")]
    returnstring = "\n".join(x for x in returnarray if x)
    return returnstring


class JSONHTMLParser(HTMLParser):

    def __init__(self):
        self.parsed = []
        self.tag_stack = []
        super().__init__()

    def get_open_tag(self):
        if self.tag_stack:
            return self.tag_stack[-1]
        return None

    def close_open_tag(self):
        self.tag_stack.pop()

    def open_new_tag(self, tagdict):
        append_target = self.parsed
        parent_tag = self.get_open_tag()
        if parent_tag:
            if INNER_KEY not in parent_tag:
                parent_tag[INNER_KEY] = []
            append_target = parent_tag[INNER_KEY]
        append_target.append(tagdict)
        self.tag_stack.append(tagdict)

    def handle_starttag(self, tag, attrs):
        newdict = {}
        for item in attrs:
            newdict[item[0]] = format_data(item[1], True)
        newdict[TAG_KEY] = tag
        self.open_new_tag(newdict)
        if tag in no_close_tags:
            self.close_open_tag()

    def handle_endtag(self, tag):
        ptag = self.get_open_tag()
        ptag_type = ptag[TAG_KEY]
        if not ptag:
            raise_error(ptag, "closed tag with no open")
        assert_with_data(ptag_type == tag, tag,
                         f"mismatched closed tag to {ptag_type}")
        self.close_open_tag()

    def handle_data(self, data):
        ctag = self.get_open_tag()
        if ctag:
            fmtcontent = format_data(data)
            if fmtcontent:
                if INNER_KEY not in ctag:
                    ctag[INNER_KEY] = []
                ctag[INNER_KEY].append(fmtcontent)

    def handle_startendtag(self, tag, attrs):
        newdict = {}
        for item in attrs:
            newdict[item[0]] = format_data(item[1], True)
        newdict[TAG_KEY] = tag
        self.open_new_tag(newdict)
        self.close_open_tag()


def parse_html(data):
    assert_with_data(isinstance(data, str), data,
                     "input to html parser is not string type")
    tparser = JSONHTMLParser()
    tparser.feed(data)
    result = tparser.parsed
    if len(result) == 1:
        result = result[0]
    return result


def make_tag(tagdata, indent=0):
    spacing = " "*indent
    if isinstance(tagdata, str):
        return [spacing + tagdata]
    assert_with_data(isinstance(tagdata, dict), tagdata,
                     "tag json representation malfored")
    assert_with_data(TAG_KEY in tagdata, tagdata,
                     "html json specification missing <tag>")
    attr_array = []
    attr_string = ""
    for item in tagdata:
        if item not in SPECIAL_HTML_KEYS:
            val = tagdata[item]
            if val is None:
                attr_array.append(item)
            else:
                attr_array.append(f"{item}=\"{tagdata[item]}\"")
    if attr_array:
        attr_string = " " + " ".join(attr_array)
    if INNER_KEY not in tagdata:
        endpart = "/>" if tagdata['<tag>'] not in no_close_tags else ">"
        return_array = [spacing +
                        f"<{tagdata['<tag>']}" + attr_string + endpart]
    else:
        openstring = [spacing + f"<{tagdata['<tag>']}" + attr_string + ">"]
        closestring = [spacing + f"</{tagdata['<tag>']}>"]
        contentarray = []
        for item in tagdata[INNER_KEY]:
            contentarray += make_tag(item, indent+p_ind)
        return_array = openstring+contentarray+closestring
    return return_array


def to_html(jsondata):
    assert_with_data(isinstance(jsondata, dict) or isinstance(
        jsondata, list), jsondata, "wrongly formatted html json")
    if isinstance(jsondata, list):
        html_array = []
        for item in jsondata:
            html_array += make_tag(item)
    elif isinstance(jsondata, dict):
        html_array = make_tag(jsondata)
    # fixes newlines without spaces following indents
    # by respliutting the string by newline, and setting
    # missing indents o the same indent as line above
    html_array = "\n".join([x for x in html_array]).split("\n")
    getspaces = lambda data: len(data)-len(data.lstrip())
    for idx in range(1, len(html_array)):
        tstring = html_array[idx].lstrip(" ")
        if tstring[0] != "<":
            above_indent = getspaces(html_array[idx-1])
            this_indent = getspaces(html_array[idx])
            if this_indent < above_indent:
                html_array[idx] = above_indent*" " + tstring
    return "\n".join([x for x in html_array])
