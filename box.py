from constants import Axis
from constants import RotationType
from auxiliary_methods import *

class Box:
    def __init__(self, **context):
        self.reference = context['reference'] 
        self.inner_length = context['inner_length']
        self.inner_width = context['inner_width']
        self.inner_depth = context['inner_depth']
        self.capacity = context['max_weight']
        self.empty_weight = context['empty_weight']
        self.total_items = 0 # number of total items in one box
        self.items = [] # item in one box -- a blank list initially
        self.unplaced_items = []
        self.unfitted_items = [] # unfitted item in one box -- a blank list initially
        self.number_of_decimals = DEFAULT_NUMBER_OF_DECIMALS
        self.context = context #the complete dictionary for the box
        self.remaining_volume = float(self.get_volume())
    
    def format_numbers(self, number_of_decimals):
        self.inner_length = set_to_decimal(self.inner_length, number_of_decimals)
        self.inner_depth = set_to_decimal(self.inner_depth, number_of_decimals)
        self.inner_width = set_to_decimal(self.inner_width, number_of_decimals)
        self.capacity = set_to_decimal(self.capacity, number_of_decimals)
        self.number_of_decimals = number_of_decimals
    
    def get_volume(self):
        return set_to_decimal(
            self.inner_length * self.inner_depth * self.inner_width, self.number_of_decimals)
     
    def get_total_weight(self):
        total_weight = self.empty_weight
        
        for item in self.items:
            total_weight += item.weight
        
        return set_to_decimal(total_weight, self.number_of_decimals)
    
    def get_filling_ratio(self):
        total_filling_volume = 0
        total_filling_ratio = 0
        
        for item in self.items:
            total_filling_volume += item.get_volume()
            
        total_filling_ratio = total_filling_volume / self.get_volume()
        return set_to_decimal(total_filling_ratio, self.number_of_decimals)
    
    def can_hold_item_with_rotation(self, item, pivot): 
        """Evaluate whether one item can be placed into box with all optional orientations.
        Args:
            item: any item in item list.
            pivot: an (x, y, z) coordinate, the back-lower-left corner of the item will be placed at the pivot.
        Returns:
            a list containing all optional orientations. If not, return an empty list.
        """
        
        fit = False 
        valid_item_position = [0, 0, 0]
        item.position = pivot 
        rotation_type_list = [] 

        if self.get_total_weight() + item.weight > self.capacity:
            return rotation_type_list
        
        
        for i in range(0, len(RotationType.ALL)): 
            item.rotation_type = i 
            dimension = item.get_dimension() 
            if (
                pivot[0] + dimension[0] <= self.inner_length and  # x-axis
                pivot[1] + dimension[1] <= self.inner_width and  # y-axis
                pivot[2] + dimension[2] <= self.inner_depth     # z-axis
            ):
            
                fit = True
                
                for current_item_in_box in self.items: 
                    if intersect(current_item_in_box, item): 
                        fit = False
                        item.position = [0, 0, 0]
                        break 
                
                if fit: 
                    rotation_type_list.append(item.rotation_type) 
            
            else:
                continue 
        
        return rotation_type_list 

    def put_item(self, item, pivot, distance_3d): 
        """Evaluate whether an item can be placed into a certain box with which orientation. If yes, perform put action.
        Args:
            item: any item in item list.
            pivot: an (x, y, z) coordinate, the back-lower-left corner of the item will be placed at the pivot.
            distance_3d: a 3D parameter to determine which orientation should be chosen.
        Returns:
            Boolean variable: False when an item couldn't be placed into the box; True when an item could be placed and perform put action.
        """
        
        fit = False 
        rotation_type_list = self.can_hold_item_with_rotation(item, pivot)
        margins_3d_list = []
        margins_3d_list_temp = []
        margin_3d = []
        margin_2d = []
        margin_1d = []
        
        n = 0
        m = 0
        p = 0
        
        if not rotation_type_list:
            return fit 
        
        else:
            fit = True 
            
            rotation_type_number = len(rotation_type_list)
            
            if rotation_type_number == 1: 
                item.rotation_type = rotation_type_list[0] 
                self.remaining_volume -= float(item.get_volume())
                self.items.append(item)
                self.total_items += 1
                return fit 
            
            else: 
                for rotation in rotation_type_list: 
                    item.rotation_type = rotation
                    dimension = item.get_dimension()
                    margins_3d = [distance_3d[0] - dimension[0], 
                                 distance_3d[1] - dimension[1], 
                                 distance_3d[2] - dimension[2]]
                    margins_3d_temp = sorted(margins_3d)
                    margins_3d_list.append(margins_3d)
                    margins_3d_list_temp.append(margins_3d_temp)
                
                while p < len(margins_3d_list_temp):
                    margin_3d.append(margins_3d_list_temp[p][0])
                    p += 1
                
                p = 0
                while p < len(margins_3d_list_temp):
                    if margins_3d_list_temp[p][0] == min(margin_3d):
                        n += 1
                        margin_2d.append(margins_3d_list_temp[p][1])
                    
                    p += 1
                
                if n == 1:
                    p = 0
                    while p < len(margins_3d_list_temp):
                        if margins_3d_list_temp[p][0] == min(margin_3d):
                            item.rotation_type = rotation_type_list[p]
                            self.remaining_volume -= float(item.get_volume())
                            self.items.append(item)
                            self.total_items += 1
                            return fit 
                        
                        p += 1
                
                else:
                    p = 0
                    while p < len(margins_3d_list_temp):
                        if (
                            margins_3d_list_temp[p][0] == min(margin_3d) and
                            margins_3d_list_temp[p][1] == min(margin_2d)
                        ):
                            m += 1
                            margin_1d.append(margins_3d_list_temp[p][2])
                        
                        p += 1
                
                if m == 1:
                    p = 0
                    while p < len(margins_3d_list_temp):
                        if (
                            margins_3d_list_temp[p][0] == min(margin_3d) and
                            margins_3d_list_temp[p][1] == min(margin_2d)
                        ):
                            item.rotation_type = rotation_type_list[p]
                            self.remaining_volume -= float(item.get_volume())
                            self.items.append(item)
                            self.total_items += 1
                            return fit 
                        
                        p += 1
                
                else:
                    p = 0
                    while p < len(margins_3d_list_temp):
                        if (
                            margins_3d_list_temp[p][0] == min(margin_3d) and
                            margins_3d_list_temp[p][1] == min(margin_2d) and
                            margins_3d_list_temp[p][2] == min(margin_1d)
                        ):
                            item.rotation_type = rotation_type_list[p]
                            self.remaining_volume -= float(item.get_volume())
                            self.items.append(item)
                            self.total_items += 1
                            return fit 
                        
                        p += 1
        
    def string(self):
        return "%s(%sx%sx%s, max_weight:%s) vol(%s) item_number(%s) filling_ratio(%s)" % (
            self.reference, self.inner_length, self.inner_width, self.inner_depth, self.capacity,
            self.get_volume(), self.total_items, self.get_filling_ratio())

    def empty_box(self):
        self.unplaced_items = []
        self.unfitted_items = []
        self.items = []
        self.total_items = 0
        self.remaining_volume = float(self.get_volume())