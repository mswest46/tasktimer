from unittest import TestCase
from nose.tools import assert_equals, assert_raises
import tasktimer.task as task
import mock
import os
import filecmp
from datetime import datetime

class TestTask(TestCase): 
    def setUp(self): 
        self.task = task.Task({task.ID_KEY: 1, 
            task.DESCRIPTION_KEY: "I'm a test case", 
            task.STATUS_KEY: task.PENDING,
            'created': datetime.now()})
    def tearDown(self): 
        pass
    def test_task_get(self): 
        assert_equals(self.task.get(task.ID_KEY), 1)
    def test_task_set(self): 
        self.task.set(task.ID_KEY, 2)
        assert_equals(self.task.get(task.ID_KEY), 2)
    def test_task_start(self): 
        self.task.start()
        assert_equals(self.task.get(task.STATUS_KEY), task.IN_PROGRESS)
    def test_task_finish(self): 
        self.task.finish()
        assert_equals(self.task.get(task.STATUS_KEY), task.COMPLETE)

