"""
Functions in this file are stored here only to provide convinient way to convert
coordinates from numbers to Excel format
"""

def colToLetter(column : int) -> str | None:
    """
    This funciton is able to translate column number stored as a number into
    excel prioprietary column name like '`27`' -> '`aa`'

    If inputed value is not number or is smaller than 1 None is returned
    """

    if type(column) != int or column <= 0: return None

    letters = []

    while column % 26 > 0:
        r = column % 26
        letters.insert(0, chr(r+64))
        column //= 26
    
    return "".join(letters)


def letterToCol(letter: str) -> int | None:
    """
    This function allows to translate column name stored in excel format into 
    numeric value ex: '`aa`' -> '`27`'
    """

    if not letter.isalpha(): return None

    result = 0
    power = 0

    for l in range(len(letter)-1,-1,-1):
        result += 26**power * (ord(letter[l]) - 64)
        power += 1
    
    return result


def toExclNot(col: int, row: int) -> str | None:
    """ Translation from (4,5) to "D5" etc.  """
    return colToLetter(col) + str(row)
