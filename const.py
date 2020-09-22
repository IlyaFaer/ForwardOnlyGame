"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Constants common for the whole Game.
"""
from panda3d.core import BitMask32

MOUSE_MASK = BitMask32(0x1)
SHOT_RANGE_MASK = BitMask32(0x4)
NO_MASK = BitMask32.allOff()

MOD_DIR = "models/bam/"
