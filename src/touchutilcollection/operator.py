from td import *  # pyright: ignore[reportMissingImports]

from pathlib import Path
from typing import cast, TypeVar
from os import environ

T = TypeVar("T")


def refresh_tox(target_operator:COMP):
    target_operator.par.enableexternaltoxpulse.pulse(True)



def ensure_tox(filepath, op_shortcut, root_comp = root, default_path = "utils", reloadcustom = False, reloadbuiltin = False):
	if (_potentialy:= getattr(op, op_shortcut, None)) is not None:
		return _potentialy

	current_comp = root_comp
	for path_element in environ.get("ENSURE_UTILITY_PATH", default_path ).strip("/ ").split("/"):
		current_comp = current_comp.op( path_element ) or current_comp.create( baseCOMP, path_element)

	newly_loaded 							= current_comp.loadTox(filepath)
	newly_loaded.name 						= op_shortcut
	newly_loaded.par.opshortcut.val 		= op_shortcut
	newly_loaded.par.externaltox.val 		= Path(filepath).relative_to( Path(".").absolute() )
	newly_loaded.par.enableexternaltox.val 	= True
	newly_loaded.par.savebackup.val 		= False
	newly_loaded.par.reloadcustom.val 		= reloadcustom
	newly_loaded.par.reloadbuiltin.val 		= reloadbuiltin
	newly_loaded.par.enableexternaltoxpulse.pulse()
	
	return newly_loaded

def iter_parents( target_op:OP ):
    next_parent = target_op
    while next_parent:
        next_parent = target_op.parent()
        if next_parent is None: break
        target_op = next_parent
        yield target_op
    return target_op
