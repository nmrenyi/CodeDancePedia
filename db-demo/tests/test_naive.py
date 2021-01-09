"""Naive test file
    By Liu Chang
"""


def add(operand_x, operand_y):
    """

    Args:
        operand_x: operand_x
        operand_y: operand_y

    Returns: sum of x and y

    """
    return operand_x + operand_y


def test_naive():
    """A naive test to test pytest function
    """
    assert add(3, 2) == 5
