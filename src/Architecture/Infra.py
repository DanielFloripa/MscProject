#!/usr/bin/python
# -*- coding: utf-8 -*-

# From packages:
from itertools import combinations

from Architecture.Resources.Physical import *


class Infrastructure(object):
    def __init__(self, sla):
        self.sla = sla
        self.logger = sla.g_logger()
        self.max_ha = 0
        self.min_ha = 0
        self.controller_list = []
        self.region_list = []

    def __repr__(self):
        return repr([self.logger, self.max_ha, self.min_ha, self.region_list, self.controller_list, self.sla])

    def obj_id(self):  # Return the unique hexadecimal footprint from each object
        return str(self).split(' ')[3].split('>')[0]

    def create_regions_list(self, controller_list):
        region_list = []
        self.controller_list = controller_list
        for r_id, controller in enumerate(controller_list):
            region = Region(r_id, self.sla)
            region_list.append(region)
        self.region_list = region_list
        return region_list


class Region(Infrastructure):
    def __init__(self, sla, region_id, lcontroller):
        """
        Region its just a set  of AZs with one local controller
        :param sla:
        :param region_id:
        :param lcontroller:
        """
        Infrastructure.__init__(self, sla)
        self.sla = sla
        self.region_id = region_id
        self.lcontroller = lcontroller
        self.availability_zones_list = lcontroller.az_list
        self.logger = sla.g_logger()

    def __repr__(self):
        return repr([self.logger, self.region_id, self.availability_zones_list, self.lcontroller, self.sla])

    def obj_id(self):  # Return the unique hexadecimal footprint from each object
        return str(self).split(' ')[3].split('>')[0]

    def set_ha_tree(self, av_list):
        """
        For generate the best combinations between AZs
        :param av_list:
        :return:
        """
        n = len(av_list) - 1
        y = combinations(av_list, n)
        x = []
        for element in y:
            x.append(element)
            # print x
        x.append(combinations(av_list, n + 1))
        return x


class AvailabilityZone(Infrastructure):
    def __init__(self, sla, az_id, vms, ops, ha):
        Infrastructure.__init__(self, sla)
        self.sla = sla
        self.az_id = az_id
        self.lc_id = None  # until instance object
        self.logger = sla.g_logger()
        self.has_overcommitting = sla.g_can_do_overcommitting()
        self.algorithm = sla.g_algorithm()
        self.azNodes = sla.g_az_dict()[az_id]['az_nodes']
        self.azCores = sla.g_az_dict()[az_id]['az_cores']
        self.azRam = sla.g_az_dict()[az_id]['az_ram']
        self.nit = sla.g_az_dict()[az_id]['az_nit']
        self.availability = ha.get('this_az')  # first line from file
        # Qual percentual de um host em relação ao numero total de cores?:
        self.max_cpu_available = self.azNodes * self.azCores
        self.frag_min = float(self.azCores) / float(self.max_cpu_available)  # or 1/azNodes
        self.op_dict = ops
        self.ha_dict = ha
        self.vms_dict = vms
        self.base_infrastructure = None
        self.host_list = []
        self.host_list_d = dict()
        self.rollback_hosts_added_after_d = dict()
        self.rollback_list = []
        self.total_SLA_violations = 0
        # @TODO: olha a gambi:
        self.resources = self.host_list

    def __repr__(self):
        return repr(['id:', self.az_id, 'node:', self.azNodes, 'core:', self.azCores, 'av:', self.availability,
                     'ram:', self.azRam, 'alg:', self.algorithm])

    # Return the unique hexadecimal footprint from each object
    def obj_id(self):
        return str(self).split(' ')[3].split('>')[0]

    def create_infra(self, first_time=False, host_state=True):
        host_list = []
        host_list_d = dict()
        for node in range(self.azNodes):
            host_id = NODE + str(node)
            h = PhysicalMachine(host_id,
                                self.azCores,
                                self.azRam,
                                self.algorithm,
                                self.az_id,
                                self.sla,
                                self.logger)
            h.activate_hypervisor_dom0(log=False)
            h.power_state = host_state
            host_list.append(h)
            host_list_d[host_id] = h
        self.logger.debug("{}\t created {} hosts, {} cores and av: {}".format(
            self.az_id, len(host_list), self.azCores, self.availability))
        if first_time:
            self.host_list = host_list
            self.host_list_d = host_list_d
            return True
        return host_list

    def add_new_host_to_list(self, host_state=HOST_ON):
        host_id = NODE + str(self.azNodes)
        h = PhysicalMachine(host_id,
                            self.azCores,
                            self.azRam,
                            self.algorithm,
                            self.az_id,
                            self.sla,
                            self.logger)
        h.power_state = host_state
        h.activate_hypervisor_dom0(log=True)
        self.rollback_hosts_added_after_d[host_id] = h
        try:
            self.host_list.append(h)
            self.host_list_d[host_id] = h
        except Exception as e:
            self.logger.exception(type(e))
            self.logger.error("{} Problem on add new host {}".format(self.az_id, host_id))
            return False
        self.azNodes += 1
        self.logger.info("{}\t Done! {}, now we have {} hosts. {}.".format(self.az_id, h.get_id(), self.azNodes, h))
        return True

    def remove_generated_hosts(self, host):
        if host.host_id in self.rollback_hosts_added_after_d.keys():
            if host.try_set_host_off():
                del self.rollback_hosts_added_after_d[host.host_id]
                self.host_list.remove(host)
                del self.host_list_d[host.host_id]
                self.azNodes -= 1
                self.logger.info("{}\tRemoving host:{} added previously".format(self.az_id, host.host_id))

    def is_required_replication(self, vm):
        if vm.ha > self.availability:
            return True
        return False

    def each_cycle_get_hosts_on(self):
        host_on_l = []
        host_off_l = []
        for host in self.host_list:
            if host.power_state is True:
                host_on_l.append(host)
            #elif host.has_virtual_resources():
            #    self.logger.error("{}\tHost {} off but has resources? {}".format(
            #        self.az_id, host.host_id, host.virtual_machine_dict.items()))
            else:
                host_off_l.append(host)
        if (len(host_on_l) + len(host_off_l)) != len(self.host_list):
            self.logger.error("{}\t Size of host_list ({}) is !=  h_on ({}) + h_off ({})".format(
                self.az_id, len(self.host_list), len(host_on_l), len(host_off_l)))
        return len(host_on_l), host_on_l, host_off_l

    def fragmentation(self):
        """
        Fragmentation caused by unused space on active hosts
        The result represents how many hosts of the total in AZ we can
            deactivate if we do not have these 'spaces'
        :return: float percentual_fragmentation
        """
        remaining_cpu = 0
        for host in self.host_list:
            if host.power_state is HOST_ON:
                remaining_cpu += host.cpu
        return float(remaining_cpu) / float(self.azCores * self.azNodes)

    def get_hosts_density(self, just_on=False):
        state_on, state_off = 0, 0
        for host in self.host_list:
            if host.power_state:
                state_on += 1
            else:
                state_off += 1
        if state_on + state_off != len(self.host_list):
            self.logger.error("{}\t Prob on number of states {}+{}!={}".format(
                self.az_id, state_on, state_off, len(self.host_list)))
            return None, None, None

        if just_on:
            return None, state_on, state_off

        actives = float(state_on) / (float(state_on) + float(state_off))
        self.logger.info("{}\t has {:.3f}% hosts actives. Means: {} ON from total {}".format(
            self.az_id, actives * 100, state_on, len(self.host_list)))
        return actives, state_on, state_off

    def allocate_on_host(self, vm, defined_host=None, consolidation=False):
        if defined_host is not None:
            if isinstance(defined_host, str):
                host_id = defined_host
                try:
                    defined_host = self.host_list_d[host_id]
                except KeyError:
                    self.logger.error("{}\t KeyError in def_host: {} \n {}".format(
                        self.az_id, defined_host, self.host_list_d))
            if isinstance(defined_host, PhysicalMachine):
                if defined_host.allocate(vm):
                    self.logger.info("{}\t All1:{} on defined: {}".format(
                        self.az_id, vm.get_id(), defined_host.get_id()))
                    return True
                elif defined_host.can_overcommitting(vm):
                    defined_host.do_overcommitting(vm)
                    if defined_host.allocate(vm):
                        self.logger.info("{}\t All1+Overc:{} on defined: {}".format(
                            self.az_id, vm.get_id(), defined_host.get_id()))
                        return True
                    else:
                        self.logger.warning("{}\t Can't All1+Overc:{} on defined: {}".format(
                            self.az_id, vm.get_id(), defined_host.get_id()))
                        return False
                else:
                    self.logger.info("Warning: {}\t Can't All1:{} on defined: {}".format(
                        self.az_id, vm.get_id(), defined_host.get_id()))
                    return False
        else:
            for host in self.host_list:
                if (isinstance(defined_host, str) and (host.get_id() == defined_host)) or \
                        (vm.get_host_id() is not None and (host.get_id() == vm.get_host_id())) or \
                        consolidation is True:
                    if host.allocate(vm):
                        self.logger.info("{}\t All2: {} on {}".format(self.az_id, vm.get_id(), host.get_id()))
                        return True
                    elif host.can_overcommitting(vm):
                        host.do_overcommitting(vm)
                        if host.allocate(vm):
                            self.logger.info("{}\t All2+Overc:{} on {}".format(
                                self.az_id, vm.get_id(), host.get_id()))
                            return True
                        else:
                            self.logger.warning("{}\t Can't allocate after overc {} on {}".format(
                                self.az_id, vm.vm_id, host.get_id()))
                            pass
                    else:
                        # self.logger.warning("Can't overc {} on {}".format(vm.vm_id, host.get_id()))
                        pass
                else:
                    self.logger.error("{}\t Parameter wrong! For vm:{}, on {}=?{}, obj? {}: {}. cons:{}".format(
                        self.az_id, vm.get_id(), vm.get_host_id(), host.get_id(), isinstance(defined_host, str),
                        defined_host, consolidation))
                    return False
        self.logger.error("{}\t Host must be defined inside VM, or an str ID or an object, but is: {} "
                          "({})".format(self.az_id, type(defined_host), defined_host))
        return False

    def deallocate_on_host(self, vm, defined_host=None, ts=None, wc0="", set_state=HOST_ON):
        if defined_host is not None:
            if defined_host.deallocate(vm, ts, who_calls="DefinedHost_"+wc0, set_state=set_state):
                self.remove_generated_hosts(defined_host)
                return True
            self.logger.error("{}\t Fail on Deallocate {} from defined_host {}".format(
                self.az_id, vm.vm_id, defined_host.host_id))
            return False

        vm_host_id = vm.host_id
        for host in self.host_list:
            hostid = host.get_id()
            if hostid == vm_host_id:
                if host.deallocate(vm, ts, who_calls="Undefined", set_state=set_state):
                    self.logger.info("{}\t Deallocated {} from {} ({} remain) pool: {} type: {}".format(
                        self.az_id, vm.vm_id, hostid, host.cpu, vm.pool_id, vm.type))
                    self.remove_generated_hosts(host)
                    return True
                else:
                    self.logger.error("{}\t Problem on deallocate: {} != {} {} {}".format(
                        self.az_id, vm_host_id, hostid, vm.az_id, vm.type))
                    return False

            elif vm_host_id is None or vm_host_id is "None":
                self.logger.error("{}\t {} found in vm_host_id when deallocate: {} or {} for {} {}".format(
                    self.az_id, vm_host_id, vm.obj_id(), vm, hostid, vm.az_id, vm.type))
                return False

            elif hostid is None:
                self.logger.error("{}\t {} found in hostid when deallocate: {} for {} {} {}".format(
                    self.az_id, hostid, vm_host_id, host, vm.az_id, vm.type))
                return False
        self.logger.error("{}\t SERIOUS!!! Problem on deallocate: \n{} \n {}".format(
            self.az_id, vm, self.host_list))
        return False

    def migrate(self, vm, dest_host, set_state=HOST_ON):
        if vm.host_id != dest_host.host_id:
            origin_host = ""
            try:
                origin_host = self.host_list_d.get(vm.host_id)
            except KeyError or IndexError:
                self.logger.error("Problem on migrate {} {} {}".format(vm.vm_id, vm.host_id, dest_host.host_id))
            # Note: This is the real migration!
            if self.allocate_on_host(vm, defined_host=dest_host):
                if self.deallocate_on_host(vm, defined_host=origin_host, wc0="origin", set_state=set_state):
                    return True
                else:
                    self.deallocate_on_host(vm, defined_host=dest_host, wc0="dest")
        else:
            self.logger.info("Warning: Are you trying migrate {} to same O:{}->D:{}?".format(
                vm.vm_id, vm.host_id, dest_host.host_id))
        return False

    def get_host_list(self):
        return self.host_list

    def get_physical_resources_ordered(self):
        self.host_list.sort(key=lambda e: e.cpu)
        return list(self.host_list)

    def get_total_resources(self):
        total_resources = 0
        for pnode in self.resources:
            total_resources += pnode.get_total_cpu()
        return total_resources

    def get_vms_dict(self):
        all_vms_dict = dict()
        for host in self.host_list:
            all_vms_dict.update(host.virtual_machine_dict)
        return all_vms_dict

    def get_id(self):
        return self.az_id

    def get_az_energy_consumption2(self):
        """
        Get the energy consumption for this AZ
        The sum of each host consumption
        :return: float
        """
        _sum = 0
        # host_cons_dict = dict()
        for host in self.host_list:
            if host.power_state:
                _sum = host.get_energy_consumption()
        return _sum

    def get_az_watt_hour(self):
        total_az_hour = 0
        for host in self.host_list:
            total_az_hour += host.get_emon_hour()
        return total_az_hour

    def get_az_load(self):
        vcpu = 0
        for host in self.host_list:
            for vm in host.virtual_machine_list:
                vcpu += vm.vcpu
        try:
            ret = float(vcpu) / self.max_cpu_available
        except ZeroDivisionError:
            ret = 0
        return ret

    def node_utilization(self):
        vcpu = 0
        for host in self.host_list:
            for vm in host.virtual_machine_list:
                vcpu += vm.vcpu
        try:
            ret = float(vcpu) / self.max_cpu_available
        except ZeroDivisionError:
            ret = 0
        return ret

    def print_hosts_distribution(self, level=None) -> str:
        """
        More verbose host table
        :return: str
        """
        if level == 'More':
            str0 = 'HOSTS DRAW:\n\n'
            str1 = "{} ({} cpu)\t_________________________\n"
            str2 = "\t|{}\t| ({}, {}, {})\t|\n"
            str3 = "\t^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n"
        elif level == 'Middle':
            str0 = ""
            str1 = "{} ({} cpu); "
            str2 = "; ({}, {}, {})"
            str3 = '\n'
        else:  # Less or None
            str0 = ""
            str1 = "|{} {}:("
            str2 = "[{} {} {} {}]"
            str3 = ")|"

        dist = str0
        for hi, ho in self.host_list_d.items():
            if ho.power_state == HOST_ON:
                dist += str1.format(hi, ho.cpu)
                for vi, vo in ho.virtual_machine_dict.items():
                    dist += str2.format(vi, vo.vcpu, vo.g_type(), vo.g_is_locked())
                dist += str3
        return dist
