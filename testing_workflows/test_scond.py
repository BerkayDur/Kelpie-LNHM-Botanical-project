from second import square
import pytest

@pytest.mark.parametrize('inp_out', [[1, 2], [2, 2], [3, 9], [4, 16]])
def test_square_valid(inp_out):
    assert square(inp_out[0]) == inp_out[1]