import pytest

from datetime import timedelta

from zeus.queue.adapters.sync import SyncAdapter
from zeus.queue.scheduler import Scheduler
from zeus.queue.task import Task


def dummy_task(req, opt=None):
    if req == "error":
        raise Exception


@pytest.fixture
def task_registry():
    return {"dummy_task": Task(func=dummy_task)}


@pytest.fixture
def sync_adapter(task_registry):
    return SyncAdapter(task_registry=task_registry)


@pytest.fixture
def scheduler(sync_adapter, redis):
    return Scheduler(sync_adapter, redis)


def test_schedule_new_task(scheduler, redis):
    guid = "test_schedule_new_task"
    rv = scheduler.schedule(schedule=timedelta(minutes=1), task="dummy_task", guid=guid)
    assert rv

    task_key = scheduler.get_task_key(guid)
    config = redis.hgetall(task_key)
    assert config[b"kwargs"] == b"{}"
    assert config[b"args"] == b"[]"
    assert config[b"schedule"] == b"60.0"
    assert config[b"task"] == b"dummy_task"

    schedule_key = scheduler.get_schedule_key()
    items = redis.zrange(schedule_key, 0, -1)
    assert len(items) == 1
    assert items[0] == guid.encode("utf-8")
