import pytest
from db_base64 import DbBase64

@pytest.fixture
def prepare_data():
    db_base64 = DbBase64()
    db_base64.debug = False
    return db_base64


@pytest.mark.parametrize("input_text, expected_sum", [
    ('Man', 'TWFu'),
    ('Ma', 'TWE='),
    ('M', 'TQ=='),
    ('Nowa praca ', 'Tm93YSBwcmFjYSA=')
])
def test_base64(prepare_data, input_text, expected_sum):
    result = prepare_data.ascii_to_base64(input_text)
    assert expected_sum == result
