from td import *  # pyright: ignore[reportMissingImports]

from .type import op_as_ex

from pathlib import Path
from typing import cast, TypeVar, Union, Type
T = TypeVar("T")



def ensure_path(path:str, root_comp = op_as_ex("/", COMP), comp_type:Type[T] = baseCOMP, strict_type_assert:bool= False) -> T:
    """Ensures the existence of a COMP at the given path.

    Parameters:
    path (str): The path from the devfined root comp on. Leading / will be discarded.
    root_comp (COMP): The comp from which we start searching.
    comp_type: The type of COMP that should be created when missing. Also is used to check with strict_type_assert
    strict_type_asser: If enabled will check all elements in the path to be of the defined type.

    Returns:
    T: The operator of the defined type.
    """
    current_level = root_comp
    for level in path.strip("/").split("/"):
        next_level = current_level.op( level )

        if not (isinstance( next_level, COMP ) or ( strict_type_assert and isinstance( next_level, comp_type ) )):

            raise ValueError(f"Found non-COMP operator with the name {level} at {current_level.path}")
        
        assert isinstance(current_level, COMP)
        if next_level is None: 
            next_level = current_level.create( comp_type, level )
        current_level = next_level

    return cast(T, current_level)


def ensure_tox(op_path:str, file_path:Union[str, Path], root_comp = op_as_ex("/", COMP)):
    target_comp = op( op_path ) or ensure_path( str(op_path) , root_comp=root_comp)

    if Path(target_comp.par.externaltox.eval()).absolute != Path( file_path ).absolute():
        target_comp.par.externaltox.val = str(file_path)
        target_comp.par.enableexternaltoxpulse.pulse(True) # actually no required to pass value.
    return target_comp


