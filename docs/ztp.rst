.. _ztp_module:

ztp -- Event-Driven Ansible source plugin for Zero-Touch Provisioning (ZTP)
=========================================================================

.. contents::
   :local:
   :depth: 1

Synopsis
--------

The `ztp` plugin uses Zero-Touch Provisioning (ZTP) as an event source to monitor network devices and retrieve relevant events. It listens for DHCP packets and extracts source MAC addresses and vendor class identifiers from the packets.

This script can be tested outside of ansible-rulebook by specifying environment variables for interface and filter criteria.

Parameters
----------

- **interface** (True, any, default: "eth0"):
    Network interface to listen on for DHCP packets.

- **filter** (True, any, default: "udp dst port 67"):
    Filter criteria to apply to the sniffer for packet capturing.

Notes
-----

.. note::
   - The plugin currently listens for DHCP packets and captures source MAC addresses and vendor class identifiers.

Examples
--------

Here is an example of how to use the `ztp` plugin:

.. code-block:: yaml+jinja

    - name: Monitor DHCP packets
      hosts: localhost
      sources:
        - elchico2007.eda.ztp:
            interface: eth0
            filter: udp dst port 67
      rules:
        - name: Process DHCP packets
          condition: event.src_mac is defined and event.vendor_class_identifier is defined
          action:
            debug:
              msg: "Received packet from {{ event.src_mac }} with vendor class identifier: {{ event.vendor_class_identifier }}"

Authors
~~~~~~~

- Luis Valle (@elchico2007)