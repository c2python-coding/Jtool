
from html.parser import HTMLParser
from html import unescape


def convert_string(data):
    try:
        int_val = int(data)
        return int_val
    except ValueError:
        pass
    try:
        float_val = float(data)
        return float_val
    except ValueError:
        pass
    return unescape(data)


class Tag:

    def __init__(self, tagname, attrs):
        self.tagname = tagname
        self.attrs = {}
        for key, val in attrs.items():
            self.attrs.update({key: convert_string(val)})
        self.children = []
        self.parent = None

    def add_data(self, data):
        self.data = convert_string(data)

    def add_child(self, child_tag):
        assert child_tag not in self.children, f"Adding duplicate child tag to {str(self.tagname}}"
        assert child_tag.parent is None, f"{str(child_tag.tagname)} tag already assigned to parent"
        self.children.append(child_tag)
        child_tag.parent = self

    def to_dict(self):
        return_dict = {
            "type": self.tagname,
            "attrs": self.attrs}
        if self.children:
            return_dict["children"] = []
            for child in self.children:
                return_dict["children"].append(child.to_dict())
        return return_dict


class HTMLJSONParser(HTMLParser):

    def __init__(self):
        self.tag_stack = []
        self.root_tags = []
        super().__init__()

    def append_tag(newtag):
        if self.tagstack:
            target = self.tag_stack[-1].children
        else:
            target = self.root_tags
        target.append(newtag)

    def handle_starttag(self, tag, attrs):

    def handle_endtag(tag):
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)

    def handle_startendtag(self, tag, attrs):
        print("Encountered some data  :", data)
