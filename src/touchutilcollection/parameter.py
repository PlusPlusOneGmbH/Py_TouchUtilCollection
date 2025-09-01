from td import * # pyright: ignore[reportMissingImports]

from functools import lru_cache
from typing import Union

@lru_cache( maxsize = None )
def get_parameter_page(operator:OP, pagename:str, builtin:bool = True, custom:bool = True) -> Union[Page, None]:
	for page in operator.pages * builtin + operator.customPages * custom:
		if page.name == pagename: return page

from typing import List, Dict, Any

class MenuSource:
	def __init__(self, names:List[str], labels:List[str] = []) -> None:
		if labels and len(labels) != len(names):
			raise TypeError("Names and labels need same length.")
		self.names = names
		self.labels = labels or names
	
	@property
	def menuLabels(self):
		return self.labels
	
	@property
	def menuNames(self):
		return self.names
	
def dictkeys_to_source(source_dict:Dict[str, Any], capitalize_labels=False):
    return MenuSource(
		[ key for key in source_dict.keys() ],
		[ key.capitalize() for key in source_dict.keys() ] if capitalize_labels else []
	)