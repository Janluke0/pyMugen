from collections import namedtuple

Box = namedtuple("Box",["x0","y0","x1","y1"])
LOOP_START = "LOOP START"

class AnimationElement:
    def __init__(self
                , collision_boxes
                , attack_boxes
                , group_number
                , image_number
                , x_offset
                , y_offset
                , time
                , effects):
        super().__init__()
        self.collision_boxes = collision_boxes
        self.attack_boxes = attack_boxes
        self.group_number = group_number
        self.image_number = image_number
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.time = time
        self.effects = effects
    def __repr__(self):
        out = f"AnimationElement(collision_boxes={self.collision_boxes}, attack_boxes={self.attack_boxes}"
        out += f", group_number={self.group_number}, image_number={self.image_number}, x_offset={self.x_offset}"
        out += f", y_offset={self.y_offset}, time={self.time}, effects={self.effects})"
        return out

class Action:
    def __init__(self
                , code
                , animation_elements=None):
        """
            code: int
            animation_elements: List[AnimationElement or LOOP_START]
        """
        super().__init__()
        self.code = code
        self.animation_elements = [] if animation_elements is None else animation_elements

    def __repr__(self):
        out = f"Action(code={self.code}, animation_elements={self.animation_elements})"
        return out