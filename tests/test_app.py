import pytest

def test_empyt_db(client):
    rv = client.get('/')
    assert b'No entries here so far' in rv.data
