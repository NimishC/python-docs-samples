# Copyright 2018, Google, LLC.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import json

from mock import MagicMock, patch

import main

@patch('main.PROJECT_ID')
@patch('main.billing')
def test_disable_billing(billing_mock, PROJECT_ID):
    PROJECT_ID = 'my-project'
    PROJECT_NAME = f'projects/{PROJECT_ID}'

    data = {"budgetAmount": 400, "costAmount": 500}

    pubsub_message = {
        "data": base64.b64encode(bytes(json.dumps(data), 'utf-8')),
        "attributes": {}
    }

    projects_mock = MagicMock()
    projects_mock.projects = MagicMock(return_value=projects_mock)
    projects_mock.getBillingInfo = MagicMock(return_value=projects_mock)
    projects_mock.updateBillingInfo = MagicMock(return_value=projects_mock)
    projects_mock.execute = MagicMock(return_value={'billingEnabled': True})

    discovery_mock.build = MagicMock(return_value=projects_mock)

    main.stop_billing(pubsub_message, None)

    assert projects_mock.getBillingInfo.called_with(name=PROJECT_NAME)
    assert projects_mock.updateBillingInfo.called_with(
        name=PROJECT_NAME,
        body={'billingAccountName': ''}
    )
    assert projects_mock.execute.call_count == 2
