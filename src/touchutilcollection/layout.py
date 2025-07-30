from td import * # pyright: ignore[reportMissingImports]
from typing import List

def quantize_attribute(target:object, quantize_step:int, attribute_name:str):
    target_attribute = getattr( target, attribute_name)
    if not isinstance( target_attribute, (float, int)): 
        raise TypeError(f"Expected Int or Float argument, got {type(target_attribute)}")
    new_value = round(target_attribute/quantize_step)*quantize_step
    setattr( target, attribute_name, new_value )
    return new_value

def quantize_operator_position( target_op:OP, quantize_step:int):
    quantize_attribute( target_op, quantize_step, "nodeX")
    quantize_attribute( target_op, quantize_step, "nodeY")


def quantize_operator_size( target_op:OP, quantize_step:int):
    quantize_attribute( target_op, quantize_step, "nodeWidth")
    quantize_attribute( target_op, quantize_step, "nodeHeight")

def quantize_annoations_comps(target_comp:COMP, quantize_step:int):
    for child in target_comp.findChildren(type = annotateCOMP):
        quantize_operator_position( child, quantize_step)
        quantize_operator_size( child, quantize_step)


def align_vertical( target_ops:List[OP], distance = 120, start_x = None, start_y = None ):
    start_x = target_ops[0].nodeX if start_x is None else start_x
    start_y = target_ops[0].nodeY if start_y is None else start_y

    for index, operator in enumerate(sorted(target_ops, key = lambda operator: operator.nodeX)):
        operator.nodeX = start_x
        operator.nodeY = start_y + distance * index


def align_horizontal( target_ops:List[OP], distance = 120, start_x = None, start_y = None ):
    start_x = target_ops[0].nodeX if start_x is None else start_x
    start_y = target_ops[0].nodeY if start_y is None else start_y

    for index, operator in enumerate(sorted(target_ops, key = lambda operator: operator.nodeX)):
        operator.nodeX = start_x + distance * index
        operator.nodeY = start_y 