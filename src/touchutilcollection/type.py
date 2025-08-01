from td import *  # pyright: ignore[reportMissingImports]

from typing import cast, TypeVar, Union, TypeGuard, Tuple, Type
T = TypeVar("T")
NoneType = type(None)

# Utils
class WrongOpType(TypeError):
	pass

def is_tuple(value) -> TypeGuard[Tuple]:
	return isinstance( value, tuple )

# Method Definitions.

def op_as(pattern:Union[str, int, Tuple[Union[str, int], ...]], asType:Type[T], includeUtility = False):
	"""
		Returns the operator as the defined asType to make use of strict typehinting.
		Idealy use the assert methods to make sure that this is actually true!
	"""
	if is_tuple( pattern ): _pattern = pattern
	else: _pattern = (pattern,)
	result = op(*_pattern, includeUtility = includeUtility) # pyright: ignore[reportArgumentType]
	return cast( T, result) 



def op_ex_as(pattern:Union[str, int, Tuple[Union[str, int], ...]], asType:Type[T], includeUtility = False): 
	"""
		Returns the operator as the defined asType to make use of strict typehinting.
		Raises an Exception when no operator is found.
		Idealy use the assert methods to make sure that this is actually true!
	"""
	if is_tuple( pattern ): _pattern = pattern
	else: _pattern = (pattern,)
	result = opex(*_pattern, includeUtility = includeUtility) # pyright: ignore[reportArgumentType]
	
	return cast( T, result) 

def op_assert(pattern:Union[str, int, Tuple[Union[str, int], ...]], asType:Type[T], includeUtility = False):
	"""
		Checks if the result is actually of the given type and raises WronfOpType if this is not the case. May return None.
	"""
	target_operator = op_as( pattern, asType, includeUtility=includeUtility)
	if not isinstance( target_operator, (asType, NoneType)):
		raise WrongOpType(f"Wrong operator type. Expected {asType}, got {type(target_operator)}")
	return target_operator

def op_ex_assert(pattern:Union[str, int, Tuple[Union[str, int], ...]], asType:Type[T], includeUtility = False):
	"""
		Uses the opEx method instead of op, so if the target op is None an exceptions raised from the call itself.
	"""
	target_operator = op_as( pattern, asType, includeUtility=includeUtility)
	if not isinstance( target_operator, asType):
		raise WrongOpType(f"Wrong operator type. Expected {asType}, got {type(target_operator)}")
	return target_operator


# This can stay for a moment.

opAs = op_as
opAsEx = op_ex_as
