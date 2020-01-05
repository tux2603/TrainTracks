#!/usr/bin/env python

from abc import ABC
from enum import Enum


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    NONE = -1

    def rotate(self, amount):
        if self == Direction.NONE:
            return Direction.NONE 
        else:
            return Direction((self.value + (amount % 4) + 4) % 4)

    def reverse(self):
        if  self == Direction.NONE:
            return Direction.NONE 
        else:
            return Direction((self.value + 2) % 4)


class Cell(ABC):
    def __init__(self):
        pass

    def enter(self, direction):
        pass

class Junction(Cell):
    class _Rail(Enum):
        BASE = 0
        DEFAULT_ARM = 1
        SECONDARY_ARM = 2
        NONE = -1

    class Type(Enum):
        LAZY = 0
        SPRUNG = 1
        ALTERNATING = 2
        ONE_WAY = 3

    # State descriptions for the different junctions
    _junctionStates = {
        Type.LAZY: (
            {
                _Rail.BASE: (_Rail.DEFAULT_ARM, 0),
                _Rail.DEFAULT_ARM: (_Rail.BASE, 0),
                _Rail.SECONDARY_ARM: (_Rail.BASE, 1)
            },

            {
                _Rail.BASE: (_Rail.SECONDARY_ARM, 0),
                _Rail.DEFAULT_ARM: (_Rail.BASE, 0),
                _Rail.SECONDARY_ARM: (_Rail.BASE, 1)
            }
        ),

        Type.SPRUNG: (
            {
                _Rail.BASE: (_Rail.DEFAULT_ARM, 0),
                _Rail.DEFAULT_ARM: (_Rail.BASE, 0),
                _Rail.SECONDARY_ARM: (_Rail.BASE, 0)
            },

            {
                _Rail.BASE: (_Rail.DEFAULT_ARM, 0),
                _Rail.DEFAULT_ARM: (_Rail.BASE, 0),
                _Rail.SECONDARY_ARM: (_Rail.BASE, 0)
            }
        ),

        Type.ALTERNATING: (
            {
                _Rail.BASE: (_Rail.DEFAULT_ARM, 1),
                _Rail.DEFAULT_ARM: (_Rail.NONE, 0),
                _Rail.SECONDARY_ARM: (_Rail.NONE, 0)
            },

            {
                _Rail.BASE: (_Rail.SECONDARY_ARM, 0),
                _Rail.DEFAULT_ARM: (_Rail.NONE, 1),
                _Rail.SECONDARY_ARM: (_Rail.NONE, 1)
            }
        ),

        Type.ONE_WAY: (
            {
                _Rail.BASE: (_Rail.NONE, 0),
                _Rail.DEFAULT_ARM: (_Rail.BASE, 0),
                _Rail.SECONDARY_ARM: (_Rail.BASE, 0)
            },

            {
                _Rail.BASE: (_Rail.NONE, 0),
                _Rail.DEFAULT_ARM: (_Rail.BASE, 0),
                _Rail.SECONDARY_ARM: (_Rail.BASE, 0)
            }
        )
    }

    def __init__(self, junctionType, base, defaultArm, secondaryArm):
        # Setup the state information
        self.junctionType = junctionType
        self.currentState = 0

        # Set the arms
        self.baseDirection = base
        self.defaulArmDirection = defaultArm
        self.secondaryArmDirection = secondaryArm


    def enter(self, direction):
        # Get what rail we came in on
        enterRail = Junction._Rail.NONE

        if direction == self.baseDirection:
            enterRail = Junction._Rail.BASE
        elif direction == self.defaulArmDirection:
            enterRail = Junction._Rail.DEFAULT_ARM
        elif direction == self.secondaryArmDirection:
            enterRail = Junction._Rail.SECONDARY_ARM

        # Throw an error if we're trying to come in on an invalid direction
        if enterRail == Junction._Rail.NONE:
            raise Exception('{} is not a valid direction to enter this rail junction.'.format(direction))

        # Get what what rail to go back out on
        exitRail = Junction._junctionStates[self.junctionType][self.currentState][enterRail][0]

        # Throw an error if we're trying to come in on an invalid direction
        if enterRail == Junction._Rail.NONE:
            raise Exception('{} is not a valid direction to enter this rail junction.'.format(direction))

        # Set the new state
        self.currentState = Junction._junctionStates[self.junctionType][self.currentState][enterRail][1]

        # Return the direction of the rail that the train exited on
        if exitRail == Junction._Rail.BASE:
            return self.baseDirection
        elif exitRail == Junction._Rail.DEFAULT_ARM:
            return self.defaulArmDirection
        else:
            return self.secondaryArmDirection


# ##### UNIT TESTS #####
if __name__ == '__main__':
    ########### START ROTATION CHECKS ##########
    print("Testing rotations")
    a = Direction.UP
    a = a.rotate(1)
    assert a == Direction.RIGHT, 'Clockwise rotation failed'

    a = a.rotate(-2)
    assert a == Direction.LEFT, 'Counter clockwise rotation failed'

    b = Direction.UP
    assert b.value == 0, 'Base enum values modified'

    b = b.rotate(10)
    assert b == Direction.DOWN, 'Rotation greater than 360 degrees failed'

    a = a.rotate(2).rotate(1)
    assert a == Direction.DOWN, 'Multiple rotations failed'

    c = Direction.NONE
    c = c.rotate(3)
    assert c == Direction.NONE, 'Direction.NONE shouldn\'t rotate'
    print("Rotation check complete")
    ########### END ROTATION CHECKS ##########
