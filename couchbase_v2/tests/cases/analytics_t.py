#
# Copyright 2018, Couchbase, Inc.
# All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License")
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
#

from __future__ import print_function

import logging
from unittest import SkipTest

from couchbase_tests.base import RealServerTestCase, version_to_tuple
from parameterized import parameterized
import json
import time
import copy
from couchbase_core import JSON
from couchbase_core.analytics_ingester import AnalyticsIngester
from couchbase_core.analytics_ingester import BucketOperators
import traceback
from couchbase_tests.base import PYCBC_SERVER_VERSION
import os
import couchbase_v2

from couchbase_core.tests.analytics_harness import *
