
from core.retry_manager import should_retry, MAX_RETRIES


def test_pass_should_not_retry():
    assert should_retry(1, "PASS") is False


def test_fail_should_retry_first_attempt():
    assert should_retry(1, "FAIL") is True


def test_fail_should_retry_second_attempt():
    assert should_retry(2, "FAIL") is True


def test_fail_should_not_retry_after_maximum():
    assert should_retry(MAX_RETRIES + 1, "FAIL") is False


def test_max_retries_is_two():
    assert MAX_RETRIES == 2
