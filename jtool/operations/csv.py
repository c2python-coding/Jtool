from jtool.execution.registry import register_command
from jtool.utils.errorhandling import raise_error
from jtool.utils.func_asserts import lambda_type


@register_command("column")
def EXTRACT_COLUMN(col_name):
    '''extracts a particular column from csv
    col_name is column header on the first row of the csv file'''
    row_idx = lambda row, col: row.index(col) if col in row else raise_error(col, "column header not found")
    return lambda data: [row[row_idx(data[0], col_name)] for row in data][1:]




