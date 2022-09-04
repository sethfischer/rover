"""Final assembly."""

import cadquery as cq

from osr_mechanical.frame import Frame

frame = Frame()

final = cq.Assembly().add(frame.cq_object, name="frame")
