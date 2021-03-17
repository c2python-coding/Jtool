from jtool.execution.registry import register_command
from jtool.execution import runprogram
from jtool.utils.errorhandling import assert_with_data
from jtool.utils.func_asserts import lambda_type
import re


@register_command("unique")
def make_UNIQUE_op():
    '''selects unique values from list'''
    return lambda data: list(set(lambda_type(data, list)))

@register_command("refilter")
def make_FILTER_op(filterspec):
    '''regexp filter based on the syntax (selector=>regular_expression)'''
    assert_with_data("=>" in filterspec, filterspec,
                     "regexp filter must be in fhe form of selector=>regular_expression")
    fsplit = filterspec.split("=>")
    selector = fsplit[0]
    restr = fsplit[1]
    return lambda data, slct=selector, regexp=restr: data if re.search(restr, str(runprogram(data, slct) if slct else data)) else None
