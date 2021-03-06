from user_cv_builder import (UserCVBuilder, UserCV,
                             CampusNetExamResultMapper)
from mock import MagicMock, Mock
from pytest import yield_fixture


class FakeCampusNetClient(object):
    def user(self):
        return MagicMock(first_name='Don', last_name='Duck')

    def grades(self):
        return [MagicMock()]


@yield_fixture
def cn_client():
    yield FakeCampusNetClient()


def test_build_with_correct_values(monkeypatch, cn_client):
    mapped_exam_result = MagicMock()
    user_cv_init_mock = Mock(return_value=None)
    monkeypatch.setattr(UserCV, '__init__', user_cv_init_mock)
    monkeypatch.setattr(CampusNetExamResultMapper,
                        'mapped_exam_result',
                        lambda x: mapped_exam_result)
    UserCVBuilder(cn_client).build()
    user_cv_init_mock.assert_called_with('Don', 'Duck', [mapped_exam_result])


def test_build_returns_user_cv(monkeypatch, cn_client):
    monkeypatch.setattr(CampusNetExamResultMapper,
                        'mapped_exam_result',
                        lambda x: x)
    campus_net_client = FakeCampusNetClient()
    user_cv = UserCVBuilder(campus_net_client).build()
    assert type(user_cv) == UserCV
