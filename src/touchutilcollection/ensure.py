from td import root, COMP, baseCOMP, op  # pyright: ignore[reportMissingImports]
from os import environ
from pathlib import Path

def ensure_global_tox(
		filepath, 
		op_shortcut, 
		root_comp = root, 
		default_path = "utils", 
		reloadcustom = False, 
		reloadbuiltin = False):

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
	
from typing import TypeVar, Type, cast
T = TypeVar("T")
def ensure_global_tdp( tdp_module, default_path = "utils", root_comp = "root", cast_as:Type[T] = COMP ):
	return  cast(T,
		ensure_global_tox(
				 tdp_module.ToxFile,
				 getattr( tdp_module, "DefaultGlobalOpShortcut", tdp_module.__name__.capitalize() ),
				 root_comp      = root_comp,
				 default_path   =   default_path
             )
    )


