# -*- coding: utf-8 -*-

# Octowire Framework
# Copyright (c) ImmunIT - Jordan Ovrè / Paul Duncan
# License: Apache 2.0
# Paul Duncan / Eresse <pduncan@immunit.ch>
# Jordan Ovrè / Ghecko <jovre@immunit.ch>

from octowire_framework.module.AModule import AModule
from octowire.i2c import I2C


class Scan(AModule):
    def __init__(self, owf_config):
        super(Scan, self).__init__(owf_config)
        self.meta.update({
            'name': 'I2C scan',
            'version': '1.0.0',
            'description': 'Scan for I2C slave devices',
            'author': 'Jordan Ovrè / Ghecko <jovre@immunit.ch>, Paul Duncan / Eresse <pduncan@immunit.ch>'
        })
        self.options = {
            "i2c_bus": {"Name": "i2c_bus", "Value": "", "Required": True, "Type": "int",
                        "Description": "The octowire I2C device (0=I2C0 or 1=I2C1)", "Default": 0},
            "i2c_baudrate": {"Name": "i2c_baudrate", "Value": "", "Required": True, "Type": "int",
                             "Description": "set I2C baudrate in Hz (100000=100kHz)\n"
                                            "Supported values: 100kHz or 400kHz",
                             "Default": 400000},
        }

    def scan(self):
        bus_id = self.options["i2c_bus"]["Value"]
        i2c_baudrate = self.options["i2c_baudrate"]["Value"]

        # Set and configure I2C interface
        i2c_interface = I2C(serial_instance=self.owf_serial, bus_id=bus_id)
        i2c_interface.configure(baudrate=i2c_baudrate)

        slave_devices = i2c_interface.scan()
        self.logger.handle("Found {} slave device(s):".format(len(slave_devices)), self.logger.RESULT)
        for device_addr in slave_devices:
            self.logger.handle("    -> {} ({})".format(hex(device_addr), device_addr), self.logger.DEFAULT)
        return slave_devices

    def run(self, return_value=False):
        """
        Main function.
        Print/return the I2C slave addresses.
        :return: Nothing or bytes, depending of the 'return_value' parameter.
        """
        # If detect_octowire is True then Detect and connect to the Octowire hardware. Else, connect to the Octowire
        # using the parameters that were configured. It sets the self.owf_serial variable if the hardware is found.
        self.connect()
        if not self.owf_serial:
            return None
        try:
            slave_devices = self.scan()
            if return_value:
                return slave_devices
            return None
        except (Exception, ValueError) as err:
            self.logger.handle(err, self.logger.ERROR)
