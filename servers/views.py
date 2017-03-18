# Create your views here.
from string import letters, digits
from random import choice
from bisect import insort
from servers.models import Instance

from vrtManager.instance import wvmInstances, wvmInstance
from libvirt import libvirtError, VIR_DOMAIN_XML_SECURE
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from vrtManager.hostdetails import wvmHostDetails
from vrtManager.connection import CONN_SSH, CONN_TCP, CONN_TLS, CONN_SOCKET, connection_manager
from servers.models import Compute
from servers.forms import ComputeAddTcpForm, ComputeAddSshForm, ComputeEditHostForm, ComputeAddTlsForm, ComputeAddSocketForm

def servers(request):

    def get_hosts_status(hosts):
        """
        Function return all hosts all vds on host
        """
        all_hosts = []
        flag = 0
        for host in hosts:

            # instances
            errors = []
            instances = []
            time_refresh = 8000
            get_instances = []
            conn = None
            all_hosts.append({'id': host.id,
                              'name': host.name,
                              'hostname': host.hostname,
                              'status': connection_manager.host_is_up(host.type, host.hostname),
                              'type': host.type,
                              'login': host.login,
                              'password': host.password,
                              'instances': instances
                              })

            compute = Compute.objects.get(id=host.id)

            try:
                conn = wvmInstances(compute.hostname,
                                    compute.login,
                                    compute.password,
                                    compute.type)
                get_instances = conn.get_instances()
            except libvirtError as err:
                errors.append(err)

            for instance in get_instances:
                try:
                    inst = Instance.objects.get(compute_id=host.id, name=instance)
                    uuid = inst.uuid
                except Instance.DoesNotExist:
                    uuid = conn.get_uuid(instance)
                    inst = Instance(compute_id=host.id, name=instance, uuid=uuid)
                    inst.save()
                all_hosts[flag]['instances'].append({'name': instance,
                                                  'status': conn.get_instance_status(instance),
                                                  'uuid': uuid,
                                                  'memory': conn.get_instance_memory(instance),
                                                  'vcpu': conn.get_instance_vcpu(instance),
                                                  'has_managed_save_image': conn.get_instance_managed_save_image(instance)})
            flag=flag+1
        return all_hosts

    computes = Compute.objects.filter()
    hosts_info = get_hosts_status(computes)
    form = None


    if request.method == 'POST':
        if 'host_ssh_add' in request.POST:
            form = ComputeAddSshForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                new_ssh_host = Compute(name=data['name'],
                                       hostname=data['hostname'],
                                       type=CONN_SSH,
                                       login=data['login'])
                new_ssh_host.save()
                return HttpResponseRedirect(request.get_full_path())

    return render_to_response('servers.html',locals(),context_instance=RequestContext(request))


