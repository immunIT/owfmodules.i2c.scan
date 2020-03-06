from octowire_framework.module.AModule import AModule
from octowire.i2c import I2C


class Scan(AModule):
    def __init__(self, owf_config):
        super(Scan, self).__init__(owf_config)
        self.meta.update({
            'name': 'I2C scan',
            'version': '1.0.0',
            'description': 'Scan for I2C slave devices',
            'author': 'Jordan Ovrè <ghecko78@gmail.com> / Paul Duncan <eresse@dooba.io>'
        })
        self.options = [
            {"Name": "detect_octowire", "Value": "", "Required": True, "Type": "bool",
             "Description": "Detect and connect octowire hardware", "Default": True},
            {"Name": "i2c_bus", "Value": "", "Required": True, "Type": "int",
             "Description": "The octowire I2C device (0=I2C0 or 1=I2C1)", "Default": 0},
            {"Name": "i2c_baudrate", "Value": "", "Required": True, "Type": "int",
             "Description": "set I2C baudrate in Hz (100000=100kHz)\n"
                            "Supported values: 100kHz or 400kHz", "Default": 400000},
        ]

    def scan(self):
        bus_id = self.get_option_value("i2c_bus")
        i2c_baudrate = self.get_option_value("i2c_baudrate")

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
        # Detect and connect to the octowire hardware. Set the self.owf_serial variable if found.
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
