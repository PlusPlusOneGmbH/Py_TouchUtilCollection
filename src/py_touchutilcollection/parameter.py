from td import * # pyright: ignore[reportMissingImports]

from functools import lru_cache
from typing import Union

@lru_cache( maxsize = None )
def get_parameter_page(operator:OP, pagename:str, builtin:bool = True, custom:bool = True) -> Union[Page, None]:
	for page in operator.pages * builtin + operator.customPages * custom:
		if page.name == pagename: return page
	