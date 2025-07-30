from td import *  # pyright: ignore[reportMissingImports]
from typing import Dict, List, Literal

def table_to_dicts( table_op:tableDAT, key_source:Literal["row", "col"] = "row" ) -> List[Dict[str, str]]:
    keys = tuple( cell.val for cell in getattr(table_op, key_source)(0) )
    collection_source = getattr(table_op, f"{key_source}s")
    return [ {
        keys[ index ] :  cell.val for index ,cell in enumerate(collection)  
    } for collection in collection_source()[1:] ]

def append_dict_to_table( table_op:tableDAT, source_dict:dict, key_source:Literal["row", "col"] = "row", default_value:str = "" ):
    keys = tuple( cell.val for cell in getattr(table_op, key_source)(0) )
    getattr( table_op, f"append{key_source.capitalize()}")([
        source_dict.get( key, default_value) for key in keys
    ])