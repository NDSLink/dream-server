
from app import app
from pytest import fixture
from constants import DREAMING_POKEMON_RESPONSE, PLAYSTATUS, SAVEDATA_DOWNLOAD, SLEEPILY_BITLIST, WAKE_UP_AND_DOWNLOAD, PUT_POKE_TO_SLEEP_RESPONSE, WORLDBATTLE_DOWNLOAD

@fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    yield client

def test_playstatus(client):
    response = client.get('/dsio/gw', query_string={'gsid': '1', 'p': PLAYSTATUS})
    assert response.data == WAKE_UP_AND_DOWNLOAD or response.data == PUT_POKE_TO_SLEEP_RESPONSE or response.data == b'\x08'

def test_worldbattle(client):
    response = client.get('/dsio/gw', query_string={'gsid': '1', 'p': WORLDBATTLE_DOWNLOAD})
    assert response.status_code == 502 or response.data == DREAMING_POKEMON_RESPONSE

def test_sleepily_bitlist(client):
    response = client.get('/dsio/gw', query_string={'gsid': '1', 'p': SLEEPILY_BITLIST})
    assert response.data.startswith(b"\x00\x00\x00\x00" + (b"\x00" * 0x7C))

