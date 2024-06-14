from extract_from_db import load_into_parquet
import pytest


@pytest.mark.parametrize('fake_data', [(1,), {'hi':1}, {2,4,522,3,3}, 'adb', 234, 23.0])
def test_load_into_parquet_invalid_data(fake_data):
    with pytest.raises(TypeError):
        load_into_parquet(fake_data, ['test', '2'])

@pytest.mark.parametrize('fake_cols', [(1,), {'hi':1}, {2,4,522,3,3}, 'adb', 234, 23.0])
def test_load_into_parquet_invalid_cols_type(fake_cols):
    with pytest.raises(TypeError):
        load_into_parquet(['1', 2], fake_cols)

@pytest.mark.parametrize('fake_cols', [['a', 2], ['a', 'b', 'c', 234.30], ['a', []]])
def test_load_into_parquet_invalid_cols_item_type(fake_cols):
    with pytest.raises(TypeError):
        load_into_parquet(['1', 2], fake_cols)