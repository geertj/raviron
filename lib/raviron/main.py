#
# This file is part of Raviron. Raviron is free software available under
# the terms of the MIT license. See the file "LICENSE" that was provided
# together with this source file for the licensing terms.
#
# Copyright (c) 2015 the Raviron authors. See the file "AUTHORS" for a
# complete list.

"""Ravello Ironic command-line utility.

Usage:
  raviron [options] proxy-create
  raviron [options] proxy-run
  raviron [options] node-create [-c <cpus>] [-m <memory>]
                                [-D <disk>] [-n <count>]
  raviron [options] node-dump
  raviron [options] node-list [--all [--cached]]
  raviron [options] node-start <node>
  raviron [options] node-stop <node>
  raviron [options] node-reboot <node>
  raviron [options] node-get-boot-device <node>
  raviron [options] node-set-boot-device <node> <bootdev>
  raviron [options] node-get-macs <node> [--cached]
  raviron [options] fixup-network
  raviron [options] fixup-nodes
  raviron --help

Command help:
  proxy-create          Create SSH->Ravello API proxy.
  proxy-run             Run the API proxy.
  node-create           Create a new node.
  node-dump             Dump node definitions to specified file.
  node-list             List running nodes (--all lists all).
  node-start            Start a node.
  node-stop             Stop a node.
  node-reboot           Reboot a node.
  node-get-boot-device  Return boot device for <node>.
  node-set-boot-device  Set boot device for <node> to <bootdev>.
                        The boot device may be "hd" or "network".
  node-get-macs         Return MAC addresses for <node>.
  fixup-network         Fix Ravello network settings after one or
                        more nodes were deployed.
  fixup-nodes           Fix on-node settings after they were deployed
                        or network settings have changed.
                        NOTE: run this command *after* fixup-network!

Options:
  -d, --debug       Enable debugging.
  -v, --verbose     Be verbose (shows logging output on stdout)
  -u <username>, --username=<username>
                    Ravello API username.
  -p <password>, --password=<password>
                    Ravello API password.
  -a <application>, --application=<application>
                    The Ravello application name.
  --all             List all nodes.
  --cached          Allow use of cached information.

Options for `node-create`:
  -c <cpus>, --cpus=<cpus>
                    The number of CPUs. [default: 2]
  -m <memory>, --memory=<memory>
                    The amount of memory in MB. [default: 8192]
  -D <disk>, --disk=<disk>
                    The size of the disk in GB. [default: 60]
  -n <count>, --count=<count>
                    The number of nodes to create. [default: 1]
"""

import sys
import docopt

from . import proxy, node, fixup, logging, factory


def _main():
    """Raviron main entry point."""
    args = docopt.docopt(__doc__)
    env = factory.get_environ(args)

    if args['proxy-create']:
        proxy.do_create(env)
    elif args['proxy-run']:
        proxy.do_run(env)
    elif args['node-create']:
        node.do_create(env)
    elif args['node-dump']:
        node.do_dump(env)
    elif args['node-list'] and not args.get('--all'):
        node.do_list_running(env, False)
    elif args['node-list']:
        node.do_list_all(env)
    elif args['node-start']:
        node.do_start(env, args['<node>'])
    elif args['node-stop']:
        node.do_stop(env, args['<node>'])
    elif args['node-reboot']:
        node.do_reboot(env, args['<node>'])
    elif args['node-get-boot-device']:
        node.do_get_boot_device(env, args['<node>'])
    elif args['node-set-boot-device']:
        node.do_set_boot_device(env, args['<node>'], args['<bootdev>'])
    elif args['node-get-macs']:
        node.do_get_macs(env, args['<node>'], False)
    elif args['fixup-network']:
        fixup.do_network(env)
    elif args['fixup-nodes']:
        fixup.do_nodes(env)


def main():
    """Main wrapper function. Calls _main() and handles exceptions."""
    try:
        _main()
    except Exception as e:
        log = logging.get_logger()
        log.error('Uncaught exception:', exc_info=True)
        if logging.get_debug():
            raise
        sys.stdout.write('Error: {!s}\n'.format(e))
        sys.exit(1)


if __name__ == '__main__':
    main()
