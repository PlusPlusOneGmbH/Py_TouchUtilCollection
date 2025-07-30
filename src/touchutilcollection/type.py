from td import *  # pyright: ignore[reportMissingImports]
from typing import cast, TypeVar, Union, TypeGuard, Tuple, Type
T = TypeVar("T")

def is_tuple(value) -> TypeGuard[Tuple]:
	return isinstance( value, tuple )

def op_as(pattern:Union[str, int, Tuple[Union[str, int], ...]], asType:Type[T], includeUtility = False):
	# T is in use. This is only a utility function!
	if is_tuple( pattern ): _pattern = pattern
	else: _pattern = (pattern,)

	return cast( Union[T, None], op(*_pattern, includeUtility = includeUtility)) # pyright: ignore[reportArgumentType]

opAs = op_as

def op_as_ex(pattern:Union[str, int, Tuple[Union[str, int], ...]], asType:Type[T], includeUtility = False): 
	if is_tuple( pattern ): _pattern = pattern
	else: _pattern = (pattern,)
	return cast( T, opex(*_pattern, includeUtility = includeUtility)) # pyright: ignore[reportArgumentType]

opAsEx = op_as_ex
