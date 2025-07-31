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

def pivot_table(input_dat:tableDAT, script_op:scriptDAT, key_source:Literal["row", "col"] = "col", id_source:str = "path", names_source:str = "name", value_source = "value"):
    """
        Thanks Mickey!
        Takes the input of our scriptDat and pivots it based on the source-arguments.
        The default arguments are set for multi-parameter tables.
    """
    
    script_op.clear()
    
    # Extract unique paths and parameter names

    item_ids = [cell.val for cell in getattr(input_dat, key_source)(id_source)[1:]]
    unique_paths = list(dict.fromkeys(item_ids))  # Preserves order, removes duplicates
    
    result_name = [cell.val for cell in getattr(input_dat, key_source)(names_source)[1:]]
    unique_params = list(dict.fromkeys(result_name))
    
    script_op.setSize(len(unique_paths), len(unique_params))
    
    # Add header row
    script_op.insertRow(unique_params, -1)
    script_op.insertCol([id_source], -1)
    
    for row_idx, path in enumerate(unique_paths, start=1):
        script_op[row_idx, id_source] = path # pyright: ignore[reportIndexIssue]
        
        # Find all rows in input that match this path
        matching_rows = input_dat.findCells(path, cols=[id_source])
        
        # Fill in parameter values for this path
        for match in matching_rows:
            # Derivative should add the correct __getitem__ method in the stups.

            param_name = input_dat[match.row, names_source]     # pyright: ignore[reportIndexIssue]
            param_value = input_dat[match.row, value_source]    # pyright: ignore[reportIndexIssue]
            script_op[row_idx, param_name] = param_value        # pyright: ignore[reportIndexIssue]