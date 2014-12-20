# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from django import template
from django.utils.translation import ugettext_lazy as _

from horizon import messages
from horizon import tabs

from openstack_dashboard import api
from openstack_dashboard.api import ceilometer
from openstack_dashboard.api import ironic


class GlobalStatsTab(tabs.Tab):
    name = _("Stats")
    slug = "stats"
    template_name = ("admin/metering/stats.html")
    preload = False

    @staticmethod
    def _get_flavor_names(request):
        try:
            flavors = api.nova.flavor_list(request, None)
            return [f.name for f in flavors]
        except Exception:
            return ['m1.tiny', 'm1.small', 'm1.medium',
                    'm1.large', 'm1.xlarge']

    def get_context_data(self, request):
        meters = ceilometer.Meters(request)
        if not meters._ceilometer_meter_list:
            msg = _("There are no meters defined yet.")


        nodes = ironic.get_node_names(request)
        node_list = []

        for node in nodes:
            node_info = ironic.get_node_info(request,node.uuid).driver_info
            node_ip = node_info['ipmi_address']
            node_list.append({'node_uuid': node.uuid, 'node_ip': node_ip})

        context = {
            'nova_meters': meters.list_nova(),
            'neutron_meters': meters.list_neutron(),
            'glance_meters': meters.list_glance(),
            'cinder_meters': meters.list_cinder(),
            'swift_meters': meters.list_swift(),
            'kwapi_meters': meters.list_kwapi(),
            'ironic_meters': meters.list_ironic(),
            'node_list': node_list
        }

        return context


class DailyReportTab(tabs.Tab):
    name = _("Daily Report")
    slug = "daily_report"
    template_name = ("admin/metering/daily.html")

    def get_context_data(self, request):
        context = template.RequestContext(request)
        return context

class hardwareevent(tabs.Tab):
    name = _("hardware Report")
    slug = "heardware_report"
    template_name = ("admin/metering/hardware_event.html")

    def get_context_data(self, request):
        context = template.RequestContext(request)
        meters = ceilometer.Meters(request)
        nodes=ironic.get_node_names(request)
        node_list={}
	
        for node in nodes:
            driver_info=ironic.get_node_info(request,node.uuid).driver_info
            driver_ip=driver_info['ipmi_address']

            node_list[node.uuid] =  driver_ip
        if not meters._ceilometer_meter_list:
            msg = _("There are no meters defined yet.")
        context['node_list'] = node_list
        return context

class BarementalTab(tabs.Tab):
    name = _("Baremental Tab")
    slug = "baremental_tab"
    template_name = ("admin/metering/baremental.html")

    def get_context_data(self, request):
        context = template.RequestContext(request)
        meters = ceilometer.Meters(request)
        if not meters._ceilometer_meter_list:
            msg = _("There are no meters defined yet.")
            messages.warning(request, msg)

        nodes = ironic.get_node_names(request)
        node_list = []

        for node in nodes:
            node_info = ironic.get_node_info(request,node.uuid).driver_info
            node_ip = node_info['ipmi_address']
            node_username = node_info['ipmi_username']

            node_list.append({'node_uuid': node.uuid, 'node_ip': node_ip, 'node_username': node_username})
        context['node_list'] = node_list
        return context

class CeilometerOverviewTabs(tabs.TabGroup):
    slug = "ceilometer_overview"
    tabs = (BarementalTab, DailyReportTab, GlobalStatsTab, hardwareevent)
    sticky = True

