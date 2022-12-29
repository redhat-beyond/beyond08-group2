import pytest
from commune_app.all_models.users import User
from commune_app.all_models.chores import Chore
from commune_app.all_models.votes import Vote


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
EMAIL1 = "userclass1@gmail.com"
ID1 = 209461581

USER_NAME = "use"
PASSWORD = "123456789"
FIRST_NAME = "USE"
LAST_NAME = "MODEL"
EMAIL = "userclass2@gmail.com"
ID = 102030405

LONG_FIELD = "A" * 151
NOT_EMAIL = "user.com@[]"

CHORE_TITLE = "Dishes"
CHORE_DATE = (1997, 10, 19)
CHORE_BUDGET = 30
CHORE_DESCRIPTION = "Clean the Dishes"
CHORE_ASSIGN = "Elias"
CHORE_PASSED = False


@pytest.fixture
def user0():
    return User(
        username=USER_NAME0, password=PASSWORD0, id=ID0, first_name=FIRST_NAME0, last_name=LAST_NAME0, email=EMAIL0
    )


@pytest.fixture
def user1():
    return User(
        username=USER_NAME1, password=PASSWORD1, id=ID1, first_name=FIRST_NAME1, last_name=LAST_NAME1, email=EMAIL1
    )


@pytest.fixture
def user2():
    return User(
        username=USER_NAME, password=PASSWORD, id=ID, first_name=FIRST_NAME, last_name=LAST_NAME, email=EMAIL
    )


@pytest.fixture
def chore0(user0):
    return Chore(
        title=CHORE_TITLE,
        date=CHORE_DATE,
        budget=CHORE_BUDGET,
        description=CHORE_DESCRIPTION,
        assign_to=user0,
        passed=CHORE_PASSED
    )


@pytest.fixture
def vote0(user0, chore0):
    return Vote(user=user0, chore=chore0, approve=False)


@pytest.mark.django_db()
class TestVote:
    def test_new_vote(self, vote0, user0, chore0):
        assert vote0.user == user0
        assert vote0.chore == chore0
        assert vote0.approve == 0

    def test_passing_chore(self, user0, user1, user2, chore0):
        chore0.save()
        user0.save()
        user1.save()
        user2.save()

        # first vote
        Vote.create_new_vote(user1, chore0, True)

        # 1 user voted with yes
        assert len(Vote.objects.filter(chore=chore0, approve=True)) == 1
        assert len(Vote.objects.filter(chore=chore0, approve=False)) == 0

        # only 1 user voted, so no change in passed
        passedInt = Chore.objects.filter(title=CHORE_TITLE).first().passed
        assert passedInt == 0

        # second vote
        Vote.create_new_vote(user2, chore0, False)

        # 1 user voted with yes and another with no, and still only 2 votes, we need 3 to decide
        assert len(Vote.objects.filter(chore=chore0, approve=True)) == 1
        assert len(Vote.objects.filter(chore=chore0, approve=False)) == 1

        # only 2 users voted, so no change in passed
        assert Chore.objects.filter(title=CHORE_TITLE).first().passed == 0

        # third vote
        Vote.create_new_vote(user0, chore0, True)

        # 2 users voted with yes and 1 with no
        assert len(Vote.objects.filter(chore=chore0, approve=True)) == 2
        assert len(Vote.objects.filter(chore=chore0, approve=False)) == 1

        # all 3 users have voted, 2 votes yes and 1 voted no, passed should be true now
        passedInt = Chore.objects.filter(title=CHORE_TITLE).first().passed
        assert passedInt == 1
