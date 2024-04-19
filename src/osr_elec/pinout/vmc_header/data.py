"""Data for Vehicle Management Computer GPIO header pinout diagram."""

legend = [
    ("Pin №", "pin"),
    ("Power 5V", "pwr5v"),
    ("Power 3V3", "pwr3v3"),
    ("Ground", "gnd"),
    ("Interface", "interface"),
    ("Peripheral", "peri"),
    ("No connection", "nc"),
]

pin_body = {"body": {"width": 40}}
peripheral_body = {"body": {"width": 100}}

odd_pins = [
    [
        ("1", "pin", pin_body),
        ("3V3", "pwr3v3"),
    ],
    [
        ("3", "pin", pin_body),
        ("NC", "nc"),
    ],
    [
        ("5", "pin", pin_body),
        ("NC", "nc"),
    ],
    [
        ("7", "pin", pin_body),
        ("GPIO4 DO", "interface"),
        ("RSL", "peri", peripheral_body),
    ],
    [
        ("9", "pin", pin_body),
        ("GND", "gnd"),
    ],
    [
        ("11", "pin", pin_body),
        ("NC", "nc"),
    ],
    [
        ("13", "pin", pin_body),
        ("NC", "nc"),
    ],
    [
        ("15", "pin", pin_body),
        ("NC", "nc"),
    ],
    [
        ("17", "pin", pin_body),
        ("3V3", "pwr3v3"),
    ],
    [
        ("19", "pin", pin_body),
        ("NC", "nc"),
    ],
    [
        ("21", "pin", pin_body),
        ("NC", "nc"),
    ],
    [
        ("23", "pin", pin_body),
        ("NC", "nc"),
    ],
    [
        ("25", "pin", pin_body),
        ("GND", "gnd"),
    ],
    [
        ("27", "pin", pin_body),
        ("I2C ID_SD", "interface"),
        ("ID EEPROM", "peri", peripheral_body),
    ],
    [
        ("29", "pin", pin_body),
        ("NC", "nc"),
    ],
    [
        ("31", "pin", pin_body),
        ("NC", "nc"),
    ],
    [
        ("33", "pin", pin_body),
        ("NC", "nc"),
    ],
    [
        ("35", "pin", pin_body),
        ("NC", "nc"),
    ],
    [
        ("37", "pin", pin_body),
        ("NC", "nc"),
    ],
    [
        ("39", "pin", pin_body),
        ("GND", "gnd"),
    ],
]

even_pins = [
    [
        ("2", "pin", pin_body),
        ("5V", "pwr5v"),
    ],
    [
        ("4", "pin", pin_body),
        ("5V", "pwr5v"),
    ],
    [
        ("6", "pin", pin_body),
        ("GND", "gnd"),
    ],
    [
        ("8", "pin", pin_body),
        ("UART TXD", "interface"),
        ("UART", "peri", peripheral_body),
    ],
    [
        ("10", "pin", pin_body),
        ("UART RXD", "interface"),
        ("UART", "peri", peripheral_body),
    ],
    [
        ("12", "pin", pin_body),
        ("NC", "nc"),
    ],
    [
        ("14", "pin", pin_body),
        ("GND", "gnd"),
    ],
    [
        ("16", "pin", pin_body),
        ("NC", "nc"),
    ],
    [
        ("18", "pin", pin_body),
        ("NC", "nc"),
    ],
    [
        ("20", "pin", pin_body),
        ("GND", "gnd"),
    ],
    [
        ("22", "pin", pin_body),
        ("NC", "nc"),
    ],
    [
        ("24", "pin", pin_body),
        ("NC", "nc"),
    ],
    [
        ("26", "pin", pin_body),
        ("NC", "nc"),
    ],
    [
        ("28", "pin", pin_body),
        ("I2C ID_SC", "interface"),
        ("ID EEPROM", "peri", peripheral_body),
    ],
    [
        ("30", "pin", pin_body),
        ("GND", "gnd"),
    ],
    [
        ("32", "pin", pin_body),
        ("NC", "nc"),
    ],
    [
        ("34", "pin", pin_body),
        ("GND", "gnd"),
    ],
    [
        ("36", "pin", pin_body),
        ("NC", "nc"),
    ],
    [
        ("38", "pin", pin_body),
        ("NC", "nc"),
    ],
    [
        ("40", "pin", pin_body),
        ("NC", "nc"),
    ],
]
