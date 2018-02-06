def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a + b for a in A for b in B]


digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits
squares = cross(rows, cols)  # unique id for each squares

# list of three different units[all rows, all cols, all squares]
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')])
# each sqaure has 3 units
units = dict((s, [u for u in unitlist if s in u]) for s in squares)
# each square has 20 peers
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in squares)


def assign(values, square, digit):
    """
    Eliminate all the other values (except digit) from values[square] and propagate.
    Return values, except return False if a contradiction is detected.
    """
    other_values = values[square].replace(digit, '')
    if all(eliminate(values, square, d2) for d2 in other_values):
        return values
    else:
        return False


def eliminate(values, square, digit):
    """
    Eliminate digit from values[square]; propagate when values or places <= 2.
    Return values, except return False if a contradiction is detected.
    """
    if digit not in values[square]:
        return values  # Already eliminated
    values[square] = values[square].replace(digit, '')

    # if a square is reduced to one value d2, then eliminate d2 from the peers
    if len(values[square]) == 0:
        return False  # Contradiction: removed last value
    elif len(values[square]) == 1:
        d2 = values[square]
        if not all(eliminate(values, s2, d2) for s2 in peers[square]):
            return False

    # if a unit is reduced to only one place for a digit, then put it there.
    for unit in units[square]:
        dplaces = [s for s in unit if digit in values[s]]

    if len(dplaces) == 0:
        return False  # Contradiction: no place for this value
    elif len(dplaces) == 1:
        # digit can only be in one place in unit; assign it there
        if not assign(values, dplaces[0], digit):
            return False
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '0' or '.' for empties.
    """
    chars = [c for c in grid if c in digits or c in '0.']
    assert len(chars) == 81
    return dict(zip(squares, chars))


def parse_grid(grid):
    """
    Convert grid to a dict of possible values, {square: digits}, or
    return False if a contradiction is detected.
    """
    # Initialize dictionary with every square can be any digit
    values = dict((s, digits) for s in squares)
    for square, digit in grid_values(grid).items():
        if digit in digits and not assign(values, square, digit):
            return False  # Fail if we can't assign digit to square
    return values


def display(values):
    """
    Display these values as a 2-D grid.
    """
    width = 1 + max(len(values[s]) for s in squares)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print ''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols)
        if r in 'CF': print line
    print


def main():
    easy_grid = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
    hard_grid = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    display(parse_grid(easy_grid))
    display(parse_grid(hard_grid))


if __name__ == '__main__':
    main()
