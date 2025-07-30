from td import *  # pyright: ignore[reportMissingImports]
from typing import cast, TypeVar, Union, TypeGuard, Tuple, Type
T = TypeVar("T")

def is_tuple(value) -> TypeGuard[Tuple]:
	return isinstance( value, tuple )

def op_as(pattern:Union[str, int, Tuple[Union[str, int], ...]], asType:Type[T], includeUtility = False, assert_type = True):
	# T is in use. This is only a utility function!
	if is_tuple( pattern ): _pattern = pattern
	else: _pattern = (pattern,)
	result = op(*_pattern, includeUtility = includeUtility) # pyright: ignore[reportArgumentType]
	if assert_type: assert isinstance( result, asType )
	return cast( T, result) 

opAs = op_as

def op_as_ex(pattern:Union[str, int, Tuple[Union[str, int], ...]], asType:Type[T], includeUtility = False, assert_type = True): 
	if is_tuple( pattern ): _pattern = pattern
	else: _pattern = (pattern,)
	result = opex(*_pattern, includeUtility = includeUtility) # pyright: ignore[reportArgumentType]
	if assert_type: assert isinstance( result, asType )
	return cast( T, result) 

opAsEx = op_as_ex

