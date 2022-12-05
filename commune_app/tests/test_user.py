import pytest
from commune_app.models import User


USER_NAME0 = "user0"
PASSWORD0 = "123456"
FIRST_NAME0 = "user"
LAST_NAME0 = "usery"
EMAIL0 = "user@gmail.com"
ID0 = 123456789

ID_NOT_IN_DB = 987654321

USER_NAME1 = "user1"
PASSWORD1 = "987654"
FIRST_NAME1 = "user"
LAST_NAME1 = "class"
EMAIL1 = "userclass@gmail.com"
ID1 = 209461581


@pytest.fixture
def user0():
    return User(
        username=USER_NAME0, password=PASSWORD0, id=ID0, first_name=FIRST_NAME0, last_name=LAST_NAME0, email=EMAIL0
        )


@pytest.fixture
@pytest.mark.django_db()
def my_user0(user0):
    user0.save()
    return user0


@pytest.mark.django_db()
class TestUser:

    def test_my_user0(self, my_user0):
        assert User.objects.get(id=my_user0.id)
        assert ID0 == my_user0.id
        assert USER_NAME0 == my_user0.username
        assert FIRST_NAME0 == my_user0.first_name
        assert LAST_NAME0 == my_user0.last_name
        assert EMAIL0 == my_user0.email

    def test_ID_not_db(self):
        with pytest.raises(Exception):
            User.objects.get(id=ID_NOT_IN_DB)

    def test_delete_user(self, my_user0):
        my_user0.delete()
        with pytest.raises(Exception):
            User.objects.get(id=my_user0.id)

    def test_create_user(self):
        new_user = User(
            username=USER_NAME1, password=PASSWORD1, id=ID1,
            first_name=FIRST_NAME1, last_name=LAST_NAME1, email=EMAIL1
            )
        new_user.save()
        assert new_user in User.objects.all()
