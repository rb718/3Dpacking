from .box import Box

class PackedShipmentBox:
    '''
    PackedShipmentBox: Class to store packed boxes. Has the to_dict method to send the response. 
    '''
    def __init__(self, box):
        self.box = box

    def to_dict(self):
        return {
            'weight': float(self.box.get_total_weight()),
            'box': self.box.context,
            'items': [item.context for item in self.box.items]
        }