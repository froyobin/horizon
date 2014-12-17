# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging

from django.conf import settings
from heatclient import client as heat_client

from horizon.utils import functions as utils
from horizon.utils.memoized import memoized  # noqa
from openstack_dashboard.api import base
from ironicclient import client as ironic_client
LOG = logging.getLogger(__name__)
# #
# #
# # def format_parameters(params):
# #     parameters = {}
# #     for count, p in enumerate(params, 1):
# #         parameters['Parameters.member.%d.ParameterKey' % count] = p
# #         parameters['Parameters.member.%d.ParameterValue' % count] = params[p]
# #     return parameters
# #
#
# @memoized
# def heatclient(request, password=None):
#     api_version = "1"
#     insecure = getattr(settings, 'OPENSTACK_SSL_NO_VERIFY', False)
#     cacert = getattr(settings, 'OPENSTACK_SSL_CACERT', None)
#     endpoint = base.url_for(request, 'orchestration')
#     LOG.debug('heatclient connection created using token "%s" and url "%s"' %
#               (request.user.token.id, endpoint))
#     kwargs = {
#         'token': request.user.token.id,
#         'insecure': insecure,
#         'ca_file': cacert,
#         'username': request.user.username,
#         'password': password
#         # 'timeout': args.timeout,
#         # 'ca_file': args.ca_file,
#         # 'cert_file': args.cert_file,
#         # 'key_file': args.key_file,
#     }
#     client = heat_client.Client(api_version, endpoint, **kwargs)
#     client.format_parameters = format_parameters
#     return client


# def stacks_list(request, marker=None, sort_dir='desc', sort_key='created_at',
#                 paginate=False):
#     limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
#     page_size = utils.get_page_size(request)
#
#     if paginate:
#         request_size = page_size + 1
#     else:
#         request_size = limit
#
#     kwargs = {'sort_dir': sort_dir, 'sort_key': sort_key}
#     if marker:
#         kwargs['marker'] = marker
#
#     stacks_iter = heatclient(request).stacks.list(limit=request_size,
#                                                   **kwargs)
#
#     has_prev_data = False
#     has_more_data = False
#     stacks = list(stacks_iter)
#
#     if paginate:
#         if len(stacks) > page_size:
#             stacks.pop()
#             has_more_data = True
#             if marker is not None:
#                 has_prev_data = True
#         elif sort_dir == 'asc' and marker is not None:
#             has_more_data = True
#         elif marker is not None:
#             has_prev_data = True
#     return (stacks, has_more_data, has_prev_data)


def get_node_names(request):

    auth_url=base.url_for(request, 'identity'),
    kwargs = {
        'os_auth_token': request.user.token.id,
        'ironic_url':'http://223.3.73.169:6385/',
        #'ironic_url':auth_url,
        # 'timeout': args.timeout,
        # 'ca_file': args.ca_file,
        # 'cert_file': args.cert_file,
        # 'key_file': args.key_file,
    }
    client = ironic_client.get_client(1,**kwargs)
    return client.node.list()

def get_node_info(request,uuid):
    auth_url=base.url_for(request, 'identity'),
    kwargs = {
        'os_auth_token': request.user.token.id,
        'ironic_url':'http://223.3.73.169:6385/',
        #'ironic_url':auth_url,
        # 'timeout': args.timeout,
        # 'ca_file': args.ca_file,
        # 'cert_file': args.cert_file,
        # 'key_file': args.key_file,
    }
    client = ironic_client.get_client(1,**kwargs)
    return client.node.get(uuid)
