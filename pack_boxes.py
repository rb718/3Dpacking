from .packer import Packer
from .box import Box
from .item import Item
from .constants import Criteria

def pack_boxes(request, account_key = None, criteria = Criteria.Items, **kwargs):
    """
    Use this function for getting the optimal packing solution. 

    Args: request: http request
          account_key : account key, unused for now
    """
    shipmentBoxes = []
    shipmentBoxItems = []
    for box in request.get('boxes', []):
        shipmentBoxes.append(Box(**box))

    for product in request.get('products', []):
        shipmentBoxItems.append(Item(**product))

    packer = Packer()
    for box in shipmentBoxes:
        packer.add_box(box)
    
    for item in shipmentBoxItems:
        packer.add_item(item)

    packer.pack_recursive(criteria=criteria)

    packed_shipment_boxes = [box.to_dict() for box in packer.packing]
    unpacked_products = [item.context for item in packer.unfit_items]

    return {
        'success': not bool(unpacked_products),
        'message': "No packing configuration is possible" if unpacked_products else "ok",
        'packed_shipment_boxes': packed_shipment_boxes,
        'unpacked_products': unpacked_products
    }

def pack_boxes_json(request, account_key = None, criteria = Criteria.Items, **kwargs):
    """
    Use this function for optimal  if you're using a json file instead of a GET request. 
    Args :
        request: dictionary containing the details of items and boxes
        account_key: unused for now

    """
    shipmentBoxes = []
    shipmentBoxItems = []
    for box in request['boxes']:
        shipmentBoxes.append(Box(**box))

    for product in request['products']:
        shipmentBoxItems.append(Item(**product))

    packer = Packer()
    for box in shipmentBoxes:
        packer.add_box(box)
    
    for item in shipmentBoxItems:
        packer.add_item(item)

    packer.pack_recursive(criteria=criteria)

    packed_shipment_boxes = [box.to_dict() for box in packer.packing]
    unpacked_products = [item.context for item in packer.unfit_items]

    return {
        'success': not bool(unpacked_products),
        'message': "No packing configuration is possible" if unpacked_products else "ok",
        'packed_shipment_boxes': packed_shipment_boxes,
        'unpacked_products': unpacked_products
    }