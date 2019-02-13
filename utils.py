def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier


def print_header(col_width, columns):
    print(("+" + "-" * col_width) * len(columns) + "+")
    columns_row = ""
    for column in columns:
        columns_row += "|" + column.center(col_width, " ")
    print(columns_row + "|")
    print(("+" + "=" * col_width) * len(columns) + "+")


def print_row(cell_width, cells):
    row = ""
    for cell in cells:
        row += "|" + cell.center(cell_width, " ")
    print(row + "|")
    print(("+" + "-" * cell_width) * len(cells) + "+")


def format_percentage(percentage):
    return format(percentage, '.2f') + "%"
