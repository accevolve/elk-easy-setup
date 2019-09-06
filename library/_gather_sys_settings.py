#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This library should be saved to the 'library/' folder relative to your playbooks/inventory

import os
import resource
from subprocess import Popen, PIPE

def _gather_limits_info(module):

    # get limits info
    _limits = dict()
    _limits['nproc_soft'], _limits['nproc_hard'] = resource.getrlimit(resource.RLIMIT_NPROC)
    _limits['memlock_soft'], _limits['memlock_hard'] = resource.getrlimit(resource.RLIMIT_MEMLOCK)
    _limits['nofile_soft'], _limits['nofile_hard'] = resource.getrlimit(resource.RLIMIT_NOFILE)

    return _limits

def _gather_sysctl_info(module):

    # get sysctl info
    _sysctl = dict()
    with open('/proc/sys/vm/swappiness') as f:
        _sysctl['vm.swappiness'] = int(f.read())
    with open('/proc/sys/vm/max_map_count') as f:
        _sysctl['vm.max_map_count'] = int(f.read())

    return _sysctl

def _gather_mount_info(module):

    # get mount info
    _mount = dict()
    dirs = module.params['mount_dirs']
    if not dirs or len(dirs) < 1:
        return dirs

    _mount['scheduler'] = dict()
    _mount['filesystem'] = dict()

    for d in dirs:

        # for debug
        debug_key = '%s[debug-info]' % d

        # get device source
        cmd1 = 'findmnt -n -o SOURCE --target %s' % d
        p = Popen(cmd1, stdout=PIPE, stderr=PIPE, shell=True)
        output, err = p.communicate()
        rc = p.returncode
        if rc != 0:
            #raise Exception(err)
            _mount['scheduler'][debug_key] = '[%s, %s, %s]' % (rc, output, err)
            continue

        # get device
        source = output.strip()
        source_postfix = source.split('/')[2]

        # get scheduler
        sched_path = '/sys/block/%s/queue/scheduler' % source_postfix
        if not os.path.isfile(sched_path):
            real_dev = source_postfix.rstrip('0123456789')
            sched_path = '/sys/block/%s/queue/scheduler' % real_dev
        with open(sched_path) as f:
            sched = f.read().strip()
            _mount['scheduler'][debug_key] = sched # for debug
            _mount['scheduler'][d] = next(x for x in sched.split() if x.startswith('['))

        # get filesystem info
        cmd2 = 'findmnt -n -o FSTYPE --target %s' % d
        p = Popen(cmd2, stdout=PIPE, stderr=PIPE, shell=True)
        output, err = p.communicate()
        rc = p.returncode
        if rc != 0:
            #raise Exception(err)
            _mount['filesystem'][debug_key] = '[%s, %s, %s]' % (rc, output, err)
            continue

        _mount['filesystem'][d] = output.strip()

    return _mount

def _gather_facts(module):
    # facts
    _facts = {'ansible_facts': {}}

    _facts['ansible_facts']['_limits'] = _gather_limits_info(module)
    _facts['ansible_facts']['_sysctl'] = _gather_sysctl_info(module)
    if 'mount_dirs' in module.params:
        _facts['ansible_facts']['_mount'] = _gather_mount_info(module)

    return _facts

def main():
    module = AnsibleModule(
        argument_spec = dict(
            mount_dirs=dict(type=list, default=None, required=False),
        ),
        supports_check_mode = True,
    )

    data = _gather_facts(module)
    module.exit_json(**data)

from ansible.module_utils.basic import *
main()
