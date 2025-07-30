from td import *  # pyright: ignore[reportMissingImports]
from typing import Dict, List, Literal

def table_to_dicts( table_op:tableDAT, key_source:Literal["row", "col"] = "row" ) -> List[Dict[str, str]]:
    keys = tuple( cell.val for cell in getattr(table_op, key_source)(0) )
    collection_source = getattr(table_op, f"{key_source}s")
    return [ {
        keys[ index ] :  cell.val for index ,cell in enumerate(collection)  
    } for collection in collection_source()[1:] ]

