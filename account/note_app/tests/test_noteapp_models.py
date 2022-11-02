import pytest
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db


class TestNoteModel:
    def test_model(self):
        obj = mixer.blend('note_app.Notes')
        assert obj.id == 1, 'should save an instance'
