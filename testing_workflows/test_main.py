from main import square
import pytest

@pytest.mark.parametrize('inp_out', [[1, 1], [2,3], [3, 9]])
def test_square(inp_out):
    assert square(inp_out[0]) == inp_out[1]