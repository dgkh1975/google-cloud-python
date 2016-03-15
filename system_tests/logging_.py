# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time

import unittest2

from gcloud import _helpers
from gcloud.environment_vars import TESTS_PROJECT
from gcloud import logging


DEFAULT_LOGGER_NAME = 'system-tests-%d' % (1000 * time.time(),)


class Config(object):
    """Run-time configuration to be modified at set-up.

    This is a mutable stand-in to allow test set-up to modify
    global state.
    """
    CLIENT = None


def setUpModule():
    _helpers.PROJECT = TESTS_PROJECT
    Config.CLIENT = logging.Client()


class TestLogging(unittest2.TestCase):

    def setUp(self):
        self.to_delete = []

    def tearDown(self):
        for doomed in self.to_delete:
            doomed.delete()

    def test_log_text(self):
        TEXT_PAYLOAD = 'System test: test_log_text'
        logger = Config.CLIENT.logger(DEFAULT_LOGGER_NAME)
        self.to_delete.append(logger)
        logger.log_text(TEXT_PAYLOAD)
        time.sleep(2)
        entries, _ = logger.list_entries()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].payload, TEXT_PAYLOAD)

    def test_log_struct(self):
        JSON_PAYLOAD = {
            'message': 'System test: test_log_struct',
            'weather': 'partly cloudy',
        }
        logger = Config.CLIENT.logger(DEFAULT_LOGGER_NAME)
        self.to_delete.append(logger)
        logger.log_struct(JSON_PAYLOAD)
        time.sleep(2)
        entries, _ = logger.list_entries()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].payload, JSON_PAYLOAD)
