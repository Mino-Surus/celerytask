import pytest
from celery.exceptions import Retry
from code import process_data

@pytest.fixture
def celery_eager():
    process_data.app.conf.task_always_eager = True
    process_data.app.conf.task_eager_propagates = True
    
    yield
    
    process_data.app.conf.task_always_eager = False
    process_data.app.conf.task_eager_propagates = False


@pytest.mark.parametrize("test_id", [1, 5, 10, 50, 100])
def test_process_data_positive(celery_eager, test_id):
    result = process_data.delay(test_id)
    assert result.get() == f"Данные для id={test_id} обработаны"


def test_process_data_negative(celery_eager):
    with pytest.raises(Retry) as exc_info:
        process_data.delay(-1)
    
    original_exc = exc_info.value.exc
    assert isinstance(original_exc, ValueError)
    assert str(original_exc) == "Отрицательный id"


def test_process_data_zero(celery_eager):
    with pytest.raises(Retry) as exc_info:
        process_data.delay(0)
        
    original_exc = exc_info.value.exc
    assert isinstance(original_exc, RuntimeError)
    assert str(original_exc) == "Нулевой id запрещён"