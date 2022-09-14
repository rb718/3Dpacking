import copy
from .constants import RotationType
from .constants import Axis
from .constants import Criteria
from .item import Item
from .box import Box
from .auxiliary_methods import *
from .packedBox import PackedShipmentBox

class Packer:
    def __init__(self):
        self.boxes = [] 
        self.unplaced_items = []
        self.packaged_in_own_box = []
        self.placed_items = []
        self.unfit_items = []
        self.total_items = 0
        self.selected_box = None
        self.packing = []
        self.packaged_already = []
    
    def add_box(self, box):
        return self.boxes.append(box)
    
    def add_item(self, item): 
        """Add unplaced items into box's unplaced_items list.
        Args:
            item: an unplaced item.
        Returns:
            The unplaced item is added into box's unplaced_items list."""
        if item.packaged_already:
            self.packaged_already.append(item)
            return
        if not item.packaged_in_own_box:
            self.total_items += 1
            self.unplaced_items.append(item)
        else:
            self.packaged_in_own_box.append(item) 
    
    def pivot_dict(self, box, item):
        """For each item to be placed into a certain box, obtain a corresponding comparison parameter of each optional pivot that the item can be placed.
        Args:
            box: a box in box list that a certain item will be placed into.
            item: an unplaced item in item list.
        Returns:
            a pivot_dict contain all optional pivot point and their comparison parameter of the item.
            a empty dict may be returned if the item couldn't be placed into the box.
        """
        
        pivot_dict = {}
        can_put = False
        
        for axis in range(0, 3): 
            items_in_box = box.items 
            items_in_box_temp = items_in_box[:] 
            
            n = 0
            while n < len(items_in_box):
                pivot = [0, 0, 0] 
                
                if axis == Axis.LENGTH: # axis = 0/ x-axis
                    ib = items_in_box[n]
                    pivot = [ib.position[0] + ib.get_dimension()[0],
                            ib.position[1],
                            ib.position[2]]
                    try_put_item = box.can_hold_item_with_rotation(item, pivot) 
                    
                    if try_put_item: 
                        can_put = True
                        q = 0
                        q = 0
                        ib_neigh_x_axis = []
                        ib_neigh_y_axis = []
                        ib_neigh_z_axis = []
                        right_neighbor = False
                        front_neighbor = False
                        above_neighbor = False
                        
                        while q < len(items_in_box_temp):
                            if items_in_box_temp[q] == items_in_box[n]: 
                                q += 1 
                            
                            else:
                                ib_neighbor = items_in_box_temp[q]
                                
                                if (
                                    ib_neighbor.position[0] > ib.position[0] + ib.get_dimension()[0] and 
                                    ib_neighbor.position[1] + ib_neighbor.get_dimension()[1] > ib.position[1] and 
                                    ib_neighbor.position[2] + ib_neighbor.get_dimension()[2] > ib.position[2] 
                                ): 
                                    right_neighbor = True
                                    x_distance = ib_neighbor.position[0] - (ib.position[0] + ib.get_dimension()[0])
                                    ib_neigh_x_axis.append(x_distance)
                                    
                                elif (
                                    ib_neighbor.position[1] >= ib.position[1] + ib.get_dimension()[1] and 
                                    ib_neighbor.position[0] + ib_neighbor.get_dimension()[0] > ib.position[0] + ib.get_dimension()[0] and 
                                    ib_neighbor.position[2] + ib_neighbor.get_dimension()[2] > ib.position[2] 
                                ):
                                    front_neighbor = True
                                    y_distance = ib_neighbor.position[1] - ib.position[1]
                                    ib_neigh_y_axis.append(y_distance)
                                
                                elif (
                                    ib_neighbor.position[2] >= ib.position[2] + ib.get_dimension()[2] and 
                                    ib_neighbor.position[0] + ib_neighbor.get_dimension()[0] > ib.position[0] + ib.get_dimension()[0] and 
                                    ib_neighbor.position[1] + ib_neighbor.get_dimension()[1] > ib.position[1] 
                                ):
                                    above_neighbor = True
                                    z_distance = ib_neighbor.position[2] - ib.position[2]
                                    ib_neigh_z_axis.append(z_distance)
                                
                                q += 1 
                                
                        if not right_neighbor: 
                            x_distance = box.inner_length - (ib.position[0] + ib.get_dimension()[0])
                            ib_neigh_x_axis.append(x_distance)
                        
                        if not front_neighbor: 
                            y_distance = box.inner_width - ib.position[1]
                            ib_neigh_y_axis.append(y_distance)
                        
                        if not above_neighbor: 
                            z_distance = box.inner_depth - ib.position[2]
                            ib_neigh_z_axis.append(z_distance)
                        
                        distance_3D = [min(ib_neigh_x_axis), min(ib_neigh_y_axis), min(ib_neigh_z_axis)]
                        pivot_dict[tuple(pivot)] = distance_3D
                
                elif axis == Axis.WIDTH: # axis = 1/ y-axis
                    ib = items_in_box[n]
                    pivot = [ib.position[0],
                            ib.position[1] + ib.get_dimension()[1],
                            ib.position[2]]
                    try_put_item = box.can_hold_item_with_rotation(item, pivot) 
                    
                    if try_put_item: 
                        can_put = True
                        q = 0
                        ib_neigh_x_axis = []
                        ib_neigh_y_axis = []
                        ib_neigh_z_axis = []
                        right_neighbor = False
                        front_neighbor = False
                        above_neighbor = False
                        
                        while q < len(items_in_box_temp):
                            if items_in_box_temp[q] == items_in_box[n]: 
                                q += 1 
                            
                            else:
                                ib_neighbor = items_in_box_temp[q]
                                
                                if (
                                    ib_neighbor.position[0] >= ib.position[0] + ib.get_dimension()[0] and 
                                    ib_neighbor.position[1] + ib_neighbor.get_dimension()[1] > ib.position[1] + ib.get_dimension()[1] and 
                                    ib_neighbor.position[2] + ib_neighbor.get_dimension()[2] > ib.position[2] 
                                ):
                                    right_neighbor = True
                                    x_distance = ib_neighbor.position[0] - ib.position[0]
                                    ib_neigh_x_axis.append(x_distance)
                                
                                elif (
                                    ib_neighbor.position[1] > ib.position[1] + ib.get_dimension()[1] and 
                                    ib_neighbor.position[0] + ib_neighbor.get_dimension()[0] > ib.position[0] and 
                                    ib_neighbor.position[2] + ib_neighbor.get_dimension()[2] > ib.position[2] 
                                ):
                                    front_neighbor = True
                                    y_distance = ib_neighbor.position[1] - (ib.position[1] + ib.get_dimension()[1])
                                    ib_neigh_y_axis.append(y_distance)
                                
                                elif (
                                    ib_neighbor.position[2] >= ib.position[2] + ib.get_dimension()[2] and 
                                    ib_neighbor.position[0] + ib_neighbor.get_dimension()[0] > ib.position[0] and 
                                    ib_neighbor.position[1] + ib_neighbor.get_dimension()[1] > ib.position[1] + ib.get_dimension()[1] 
                                ):
                                    above_neighbor = True
                                    z_distance = ib_neighbor.position[2] - ib.position[2]
                                    ib_neigh_z_axis.append(z_distance)
                                
                                q += 1
                        
                        if not right_neighbor: 
                            x_distance = box.inner_length - ib.position[0]
                            ib_neigh_x_axis.append(x_distance)
                        
                        if not front_neighbor: 
                            y_distance = box.inner_width - (ib.position[1] + ib.get_dimension()[1])
                            ib_neigh_y_axis.append(y_distance)
                        
                        if not above_neighbor: 
                            z_distance = box.inner_depth - ib.position[2]
                            ib_neigh_z_axis.append(z_distance)
                        
                        distance_3D = [min(ib_neigh_x_axis), min(ib_neigh_y_axis), min(ib_neigh_z_axis)]
                        pivot_dict[tuple(pivot)] = distance_3D
            
                elif axis == Axis.HEIGHT: # axis = 2/ z-axis
                    ib = items_in_box[n]
                    pivot = [ib.position[0],
                            ib.position[1],
                            ib.position[2] + ib.get_dimension()[2]]
                    try_put_item = box.can_hold_item_with_rotation(item, pivot) 
                    
                    if try_put_item: 
                        can_put = True
                        q = 0
                        ib_neigh_x_axis = []
                        ib_neigh_y_axis = []
                        ib_neigh_z_axis = []
                        right_neighbor = False
                        front_neighbor = False
                        above_neighbor = False
                        
                        while q < len(items_in_box_temp):
                            if items_in_box_temp[q] == items_in_box[n]: 
                                q += 1 
                            
                            else:
                                ib_neighbor = items_in_box_temp[q]
                                
                                if (
                                    ib_neighbor.position[0] >= ib.position[0] + ib.get_dimension()[0] and 
                                    ib_neighbor.position[1] + ib_neighbor.get_dimension()[1] > ib.position[1] and 
                                    ib_neighbor.position[2] + ib_neighbor.get_dimension()[2] > ib.position[2] + ib.get_dimension()[2] 
                                ):
                                    right_neighbor = True
                                    x_distance = ib_neighbor.position[0] - ib.position[0]
                                    ib_neigh_x_axis.append(x_distance)
                                
                                elif (
                                    ib_neighbor.position[1] > ib.position[1] + ib.get_dimension()[1] and 
                                    ib_neighbor.position[0] + ib_neighbor.get_dimension()[0] > ib.position[0] and 
                                    ib_neighbor.position[2] + ib_neighbor.get_dimension()[2] > ib.position[2] + ib.get_dimension()[2] 
                                ):
                                    front_neighbor = True
                                    y_distance = ib_neighbor.position[1] - (ib.position[1] + ib.get_dimension()[1])
                                    ib_neigh_y_axis.append(y_distance)
                                
                                elif (
                                    ib_neighbor.position[2] >= ib.position[2] + ib.get_dimension()[2] and 
                                    ib_neighbor.position[1] + ib_neighbor.get_dimension()[1] > ib.position[1] and 
                                    ib_neighbor.position[0] + ib_neighbor.get_dimension()[0] > ib.position[0] 
                                ):
                                    above_neighbor = True
                                    z_distance = ib_neighbor.position[2] - ib.position[2]
                                    ib_neigh_z_axis.append(z_distance)
                                
                                q += 1
                                
                        if not right_neighbor: 
                            x_distance = box.inner_length - ib.position[0]
                            ib_neigh_x_axis.append(x_distance)
                        
                        if not front_neighbor: 
                            y_distance = box.inner_width - ib.position[1]
                            ib_neigh_y_axis.append(y_distance)
                        
                        if not above_neighbor: 
                            z_distance = box.inner_depth - (ib.position[2] + ib.get_dimension()[2])
                            ib_neigh_z_axis.append(z_distance)
                        
                        distance_3D = [min(ib_neigh_x_axis), min(ib_neigh_y_axis), min(ib_neigh_z_axis)]
                        pivot_dict[tuple(pivot)] = distance_3D
                
                n += 1
        
        return pivot_dict
    
    def pivot_list(self, box, item):
        """Obtain all optional pivot points that one item could be placed into a certain box.
        Args:
            box: a box in box list that a certain item will be placed into.
            item: an unplaced item in item list.
        Returns:
            a pivot_list containing all optional pivot points that the item could be placed into a certain box.
        """
        
        pivot_list = [] 
        
        for axis in range(0, 3): 
            items_in_box = box.items 
            
            for ib in items_in_box: 
                pivot = [0, 0, 0] 
                if axis == Axis.LENGTH: # axis = 0/ x-axis
                    pivot = [ib.position[0] + ib.get_dimension()[0],
                            ib.position[1],
                            ib.position[2]]
                elif axis == Axis.WIDTH: # axis = 1/ y-axis
                    pivot = [ib.position[0],
                            ib.position[1] + ib.get_dimension()[1],
                            ib.position[2]]
                elif axis == Axis.HEIGHT: # axis = 2/ z-axis
                    pivot = [ib.position[0],
                            ib.position[1],
                            ib.position[2] + ib.get_dimension()[2]]
        
                pivot_list.append(pivot)
            
        return pivot_list 
    
    def choose_pivot_point(self, box, item):
        """Choose the optimal one from all optional pivot points of the item after comparison.
        Args:
            box: a box in box list that a certain item will be placed into.
            item: an unplaced item in item list.
        Returns:
            the optimal pivot point that a item could be placed into a box.
        """
        
        can_put = False
        pivot_available = []
        pivot_available_temp = []
        vertex_3d = []
        vertex_2d = []
        vertex_1d = []
        
        n = 0
        m = 0
        p = 0
        
        pivot_list = self.pivot_list(box, item)
        
        for pivot in pivot_list:
            try_put_item = box.can_hold_item_with_rotation(item, pivot)
            
            if try_put_item:
                can_put = True
                pivot_available.append(pivot)
                pivot_temp = sorted(pivot)
                pivot_available_temp.append(pivot_temp)
        
        if pivot_available:
            while p < len(pivot_available_temp):
                vertex_3d.append(pivot_available_temp[p][0])
                p += 1
            
            p = 0
            while p < len(pivot_available_temp): 
                if pivot_available_temp[p][0] == min(vertex_3d):
                    n += 1
                    vertex_2d.append(pivot_available_temp[p][1])
                
                p += 1
        
            if n == 1:
                p = 0
                while p < len(pivot_available_temp):
                    if pivot_available_temp[p][0] == min(pivot_available_temp[p]):
                        return pivot_available[p]
                
                    p += 1
        
            else:
                p = 0
                while p < len(pivot_available_temp):
                    if (
                        pivot_available_temp[p][0] == min(pivot_available_temp[p]) and 
                        pivot_available_temp[p][1] == min(vertex_2d)
                    ):
                        m += 1
                        vertex_1d.append(pivot_available_temp[p][2])
                
                    p += 1
        
            if m == 1:
                p = 0
                while p < len(pivot_available_temp):
                    if (
                        pivot_available_temp[p][0] == min(pivot_available_temp[p]) and 
                        pivot_available_temp[p][1] == min(vertex_2d)
                    ):
                        return pivot_available[p]
                
                    p += 1
        
            else:
                p = 0
                while p < len(pivot_available_temp):
                    if (
                        pivot_available_temp[p][0] == min(pivot_available_temp[p]) and
                        pivot_available_temp[p][1] == min(vertex_2d) and
                        pivot_available_temp[p][2] == min(vertex_1d)
                    ):
                        return pivot_available[p]
                
                    p += 1
        
        if not pivot_available:
            return can_put
        
    def pack_to_box(self, box, item): 
        """For each item and each box, perform whole pack process with optimal orientation and pivot point.
        Args:
            box: a box in box list that a certain item will be placed into.
            item: an unplaced item in item list.
        Returns: return value is void.
        """

        if float(set_to_decimal(box.remaining_volume, DEFAULT_NUMBER_OF_DECIMALS)) < float(item.get_volume()):
            box.unfitted_items.append(item)
            return
        
        if not box.items:
            response = box.put_item(item, START_POSITION, [box.inner_length, box.inner_width, box.inner_depth])
            
            if not response:
                box.unfitted_items.append(item)
            
            return 
        
        else:
            pivot_point = self.choose_pivot_point(box, item)
            pivot_dict = self.pivot_dict(box, item)
                
            if not pivot_point:
                box.unfitted_items.append(item)
                return 
                
            distance_3D = pivot_dict[tuple(pivot_point)]
            response = box.put_item(item, pivot_point, distance_3D)
            return  

    def pack_only_one_item(self, box, item):
        """ For each item which needs to be packed in one box, 
            check if a box is suitable for the item. 
            Args:
                box: the box in which the item needs to be placed
                item: the item that needs placing

            Returns: True, if box can place item
                     False if box cannot place item. 
        """
        return box.put_item(item, START_POSITION, [box.inner_length, box.inner_width, box.inner_depth])
            
    def pack(
        self, bigger_first=False, number_of_decimals=DEFAULT_NUMBER_OF_DECIMALS, criteria = Criteria.Items):
        """For a list of items and a list of boxes, perform the whole pack process.
        Args:
            box: a box in box list that a certain item will be placed into.
            item: an unplaced item in item list.
            criteria: Maximize items(arg = 1) or maximize volume (arg = 2).
        
        """
        
        for box in self.boxes:
            box.format_numbers(number_of_decimals)
            
        for unplaced_item in self.unplaced_items:
            unplaced_item.format_numbers(number_of_decimals)
        
        for item in self.packaged_in_own_box:
            item.format_numbers(number_of_decimals)

        it = copy.deepcopy(self.packaged_in_own_box)
        
        self.boxes.sort(
            key = lambda box: box.get_volume()) # default order of bins: from smallest to biggest
        self.unplaced_items.sort(
            key = lambda unplaced_item: unplaced_item.get_volume(), reverse=bigger_first) # default order of items: from biggest to smallest
        

        if len(self.packaged_in_own_box) > 0:
            for index, item in enumerate(self.packaged_in_own_box):
                for box in self.boxes:
                    ret = self.pack_only_one_item(box, item)
                    if ret:
                        self.selected_box = box
                        self.placed_items.append(item)
                        self.packaged_in_own_box.pop(index)
                        return
                self.unfit_items.append(item)
                self.packaged_in_own_box.pop(index)
                return

        self.boxes.sort(
            key = lambda box: box.get_volume(), reverse = True)
        
        filling_ratio_list = []
        item_list = []
        
        for box in self.boxes: 
            for unplaced_item in self.unplaced_items: 
                box.unplaced_items.append(unplaced_item) 
        
        for box in self.boxes:
            for unplaced_item in self.unplaced_items:
                self.pack_to_box(box, unplaced_item)
            
            filling_ratio_list.append(box.get_filling_ratio())
            item_list.append(len(box.items))
            
        max_filling_ratio = max(filling_ratio_list)
        max_item_list = max(item_list) 

        self.boxes.sort(key = lambda box: box.get_volume())
        
        for box in self.boxes:
            if criteria == Criteria.Volume:
                if box.get_filling_ratio() == max_filling_ratio: 
                    for item in box.items:
                        self.placed_items.append(item)
                        self.selected_box = box
                        return
            elif criteria == Criteria.Items:
                if len(box.items) == max_item_list: 
                    for item in box.items:
                        self.placed_items.append(item)
                        self.selected_box = box
                        return

    def pack_recursive(self, bigger_first = True, number_of_decimals = DEFAULT_NUMBER_OF_DECIMALS, criteria = Criteria.Items):
        """
        Perform the whole pack process continuosly, till only items that cannot fit remain. 
        Args:
            box: a box in box list that a certain item will be placed into.
            item: an unplaced item in item list.
            criteria: Maximize items(arg = 1) or maximize volume (arg = 2).        
        """
        for item in self.packaged_already:
            self.createBoxForAlreadyPackedItem(item, number_of_decimals)
        while(True):
            prev_own_box = len(self.packaged_in_own_box) # Previous own box packages
            self.pack(bigger_first= bigger_first, number_of_decimals=number_of_decimals, criteria=criteria)
            if not self.placed_items:
                if prev_own_box == len(self.packaged_in_own_box): #If previous own box packages are reduced
                    self.unfit_items.extend(self.unplaced_items)
                    break
            if self.selected_box:
                self.packing.append(PackedShipmentBox(copy.deepcopy(self.selected_box)))
            self.clearPackedItems()

    def clearPackedItems(self):
        """
        After every iteration of packing, remove the packed items and set the packer to its original state.

        """
        if self.selected_box:
            for item in self.selected_box.items:
                if item in self.unplaced_items:
                    self.unplaced_items.remove(item)
        for box in self.boxes:
            box.empty_box()
        self.placed_items = []
        self.selected_box = None

    def createBoxForAlreadyPackedItem(self, item, number_of_decimals = DEFAULT_NUMBER_OF_DECIMALS):
        """
        Creates a new box for already packed item. Adds it to the list of packed box
        """
        inner_depth, outer_depth = item.height, item.height
        inner_width, outer_width = item.width, item.width
        inner_length, outer_length = item.length, item.length   
        empty_weight = 0
        max_weight = 1000000000
        reference = 'PR:' + item.reference
        inner_volume = inner_depth*inner_width*inner_length

        context = {'inner_depth': inner_depth,
                    'outer_depth':outer_depth,
                    'inner_width': inner_width,
                    'outer_width': outer_width, 
                    'inner_length':inner_length, 
                    'outer_length': outer_length, 
                    'empty_weight':empty_weight, 
                    'max_weight': max_weight, 
                    'reference': reference, 
                    }
        box = Box(**context)
        item.format_numbers(number_of_decimals)
        box.format_numbers(number_of_decimals)
        box.items.append(item)
        self.packing.append(PackedShipmentBox(box))