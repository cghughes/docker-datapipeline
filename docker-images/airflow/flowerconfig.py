# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""Default celery configuration."""
import ssl
from airflow.utils.log.logging_mixin import LoggingMixin

log = LoggingMixin().log

#broker_url = conf.get('celery', 'BROKER_URL')
broker_url = 'pyamqp://airflow:3point142@rabbit01:5672/airflow'
log.info('Using broker_url ' + broker_url)

#result_backend = conf.get('celery', 'RESULT_BACKEND')
result_backend = "db+mysql://root:3point142@maria01:3306/airflow"
log.info('Using result_backend ' + result_backend)

default_queue = "celery.inbound"
log.info('Using default_queue ' + default_queue)

worker_concurrency = "16"
log.info('Using worker_concurrency ' + worker_concurrency)

DEFAULT_CELERY_CONFIG = {
    'accept_content': ['json', 'pickle'],
    'event_serializer': 'json',
    'worker_prefetch_multiplier': 1,
    'task_acks_late': True,
    'task_default_queue': default_queue,
    'task_default_exchange': default_queue,
    'broker_url': broker_url,
    'broker_transport_options': {},
    'result_backend': result_backend,
    'worker_concurrency': worker_concurrency,
}

celery_ssl_active = False
