"""Data for Vehicle Management Computer GPIO header pinout diagram."""

legend = [
    ("Pin №", "pin"),
    ("Power 5V", "pwr5v"),
    ("Power 3V3", "pwr3v3"),
    ("Ground", "gnd"),
    ("Interface", "interface"),
    ("Peripheral", "peri"),
    ("Protocol converter", "proconv"),
    ("No connection", "nc"),
]

pin_body = {"body": {"width": 40}}
interface_body = {"body": {"width": 100}}
peripheral_body = {"body": {"width": 100}}

odd_pins = [
    [
        ("1", "pin", pin_body),
        ("3V3", "pwr3v3", interface_body),
    ],
    [
        ("3", "pin", pin_body),
        ("I2C1 SDA", "interface", interface_body),
        ("I2C header", "peri", peripheral_body),
    ],
    [
        ("5", "pin", pin_body),
        ("I2C1 SCL", "interface", interface_body),
        ("I2C header", "peri", peripheral_body),
    ],
    [
        ("7", "pin", pin_body),
        ("GPIO4 DO", "interface", interface_body),
        ("I2C header", "peri", peripheral_body),
    ],
    [
        ("9", "pin", pin_body),
        ("GND", "gnd", interface_body),
    ],
    [
        ("11", "pin", pin_body),
        ("GPIO17 DO", "interface", interface_body),
        ("RSL", "peri", peripheral_body),
    ],
    [
        ("13", "pin", pin_body),
        ("NC", "nc", interface_body),
    ],
    [
        ("15", "pin", pin_body),
        ("NC", "nc", interface_body),
    ],
    [
        ("17", "pin", pin_body),
        ("3V3", "pwr3v3", interface_body),
    ],
    [
        ("19", "pin", pin_body),
        ("SPI0 MOSI", "interface", interface_body),
    ],
    [
        ("21", "pin", pin_body),
        ("SPI0 MISO", "interface", interface_body),
    ],
    [
        ("23", "pin", pin_body),
        ("SPI0 SCLK", "interface", interface_body),
    ],
    [
        ("25", "pin", pin_body),
        ("GND", "gnd", interface_body),
    ],
    [
        ("27", "pin", pin_body),
        ("I2C ID_SD", "interface", interface_body),
        ("ID EEPROM", "peri", peripheral_body),
    ],
    [
        ("29", "pin", pin_body),
        ("NC", "nc", interface_body),
    ],
    [
        ("31", "pin", pin_body),
        ("NC", "nc", interface_body),
    ],
    [
        ("33", "pin", pin_body),
        ("NC", "nc", interface_body),
    ],
    [
        ("35", "pin", pin_body),
        ("NC", "nc", interface_body),
    ],
    [
        ("37", "pin", pin_body),
        ("NC", "nc", interface_body),
    ],
    [
        ("39", "pin", pin_body),
        ("GND", "gnd", interface_body),
    ],
]

even_pins = [
    [
        ("2", "pin", pin_body),
        ("5V", "pwr5v", interface_body),
    ],
    [
        ("4", "pin", pin_body),
        ("5V", "pwr5v", interface_body),
    ],
    [
        ("6", "pin", pin_body),
        ("GND", "gnd", interface_body),
    ],
    [
        ("8", "pin", pin_body),
        ("UART TXD", "interface", interface_body),
        ("UART", "peri", peripheral_body),
    ],
    [
        ("10", "pin", pin_body),
        ("UART RXD", "interface", interface_body),
        ("UART", "peri", peripheral_body),
    ],
    [
        ("12", "pin", pin_body),
        ("NC", "nc", interface_body),
    ],
    [
        ("14", "pin", pin_body),
        ("GND", "gnd", interface_body),
    ],
    [
        ("16", "pin", pin_body),
        ("NC", "nc", interface_body),
    ],
    [
        ("18", "pin", pin_body),
        ("NC", "nc", interface_body),
    ],
    [
        ("20", "pin", pin_body),
        ("GND", "gnd", interface_body),
    ],
    [
        ("22", "pin", pin_body),
        ("NC", "nc", interface_body),
    ],
    [
        ("24", "pin", pin_body),
        ("SPI0 CE0", "interface", interface_body),
        ("UART{A,B}", "proconv", peripheral_body),
    ],
    [
        ("26", "pin", pin_body),
        ("SPI0 CE1", "interface", interface_body),
        ("CAN", "proconv", peripheral_body),
    ],
    [
        ("28", "pin", pin_body),
        ("I2C ID_SC", "interface", interface_body),
        ("ID EEPROM", "peri", peripheral_body),
    ],
    [
        ("30", "pin", pin_body),
        ("GND", "gnd", interface_body),
    ],
    [
        ("32", "pin", pin_body),
        ("NC", "nc", interface_body),
    ],
    [
        ("34", "pin", pin_body),
        ("GND", "gnd", interface_body),
    ],
    [
        ("36", "pin", pin_body),
        ("NC", "nc", interface_body),
    ],
    [
        ("38", "pin", pin_body),
        ("NC", "nc", interface_body),
    ],
    [
        ("40", "pin", pin_body),
        ("NC", "nc", interface_body),
    ],
]
