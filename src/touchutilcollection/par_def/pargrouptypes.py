from .partypes import ParMode


import typing as _T
ParValueT 	= _T.TypeVar('ParValueT')
ParTypeT 	= _T.TypeVar("ParTypeT")

from typing import NotRequired, TypedDict, Tuple, Any, Literal, List

from abc import abstractmethod, abstractproperty
###
class _ParGroupArgs( TypedDict, _T.Generic[ParValueT] ):
		#size        : Literal[2,3,4]
		label 		: NotRequired[str]
		mode 		: NotRequired[Tuple[ParMode,...]]
		defaultMode : NotRequired[Tuple[ParMode,...]]
		default     : NotRequired[Tuple[ParValueT,...]]
		defaultExpr : NotRequired[Tuple[str, ...]]
		defaultBindExpr : NotRequired[Tuple[str,...]]		
		expr        : NotRequired[Tuple[str,...]]
		bindExpr    : NotRequired[Tuple[str,...]]
		
		readOnly    : NotRequired[bool]
		help        : NotRequired[str]
		enable      : NotRequired[bool]
		enableExpr  : NotRequired[str]

		startSection: NotRequired[bool]
		order		: NotRequired[float]

class _ParGroup(_T.Generic[ParValueT, ParTypeT]):
	class _args(_ParGroupArgs[ParValueT]): # pyright: ignore[reportGeneralTypeIssues]
		pass

	@abstractmethod
	def __getitem__(self, index:Literal[2,3,4]) -> ParTypeT:
		pass

	defaultMode : Tuple[ParMode,...]
	mode		: Tuple[ParMode,...]
	
	_creationMethodName : str
	style:str

	val:Tuple[ParValueT,...]
	
	@abstractmethod
	def eval(self) -> Tuple[ParValueT,...]:
		pass
	
	default : Tuple[ParValueT,...]
	defaultExpr : Tuple[str,...]
	defaultBindExpr : Tuple[str,...]
	
	readOnly : bool
	enable : bool

	owner : Any

	expr : Tuple[str,...]
	enableExpr : Tuple[str,...]
	bindExpr :Tuple[str,...]
	
	name : str
	label : str
	help : str

	startSection: bool
	order		: float
	
	@abstractmethod
	def destroy(self):
		pass
	@abstractmethod
	def reset() -> bool:
		pass
	@abstractmethod
	def isPar( par:Any ) -> bool:
		pass

class _NumericParGroupArgs( TypedDict, _T.Generic[ParValueT] ):	
		min : NotRequired[Tuple[ParValueT,...]]
		max : NotRequired[Tuple[ParValueT,...]]
		normMin : NotRequired[Tuple[ParValueT,...]]
		normMax : NotRequired[Tuple[ParValueT,...]]
		clampMin : NotRequired[Tuple[ParValueT,...]]
		clampMax : NotRequired[Tuple[ParValueT,...]]
		


class _NumericParGroup(_ParGroup[ParValueT, ParTypeT]):
	class _args(_NumericParGroupArgs[ParValueT], _ParGroupArgs[ParValueT]): # pyright: ignore[reportGeneralTypeIssues]
		pass
	min : Tuple[ParValueT,...]
	max : Tuple[ParValueT,...]
	normMin : Tuple[ParValueT,...]
	normMax : Tuple[ParValueT,...]
	clampMin : Tuple[ParValueT,...]
	clampMax : Tuple[ParValueT,...]
	@abstractmethod
	def evalNorm(self) -> Tuple[ParValueT,...]:
		pass


class _MenuParGroupArgs( TypedDict, _T.Generic[ParValueT] ):	
		menuNames : NotRequired[Tuple[List[ParValueT],...]]
		menuLabels : NotRequired[Tuple[List[ParValueT],...]]
		menuSource : NotRequired[Tuple[str,...]]		

class _MenuParGroup(_ParGroup[ParValueT, ParTypeT]):
	class _args(_MenuParGroupArgs[ParValueT], _ParGroupArgs[ParValueT]): # pyright: ignore[reportGeneralTypeIssues]
		pass
	menuNames : Tuple[ParValueT,...]
	menuLabels : Tuple[ParValueT,...]
	menuSource : Tuple[str,...]



from .partypes import ParFloat, ParInt

class ParGroupFloat(_NumericParGroup["float", ParFloat]):
	class _args(_NumericParGroupArgs[float], _ParGroupArgs[float]):
		size : Literal[2,3,4]
	"TD Float Parameter"
	style:str = "Float"

class ParGroupMenu(_MenuParGroup["str", ParFloat]):
	class _args(_MenuParGroupArgs[str], _ParGroupArgs[str]):
		size : Literal[2,3,4]
	"TD Menu Parameter"
	style:str = "Menu"

class ParGroupStrMenu(_MenuParGroup["str", ParFloat]):
	class _args(_MenuParGroupArgs[str], _ParGroupArgs[str]):
		size : Literal[2,3,4]
	"TD Menu Parameter"
	style:str = "Menu"

class ParGroupInt(_NumericParGroup["int", ParInt]):
	class _args(_NumericParGroupArgs[int], _ParGroupArgs[int]):
		size : Literal[2,3,4]

	"TD Int Parameter"
	style:str = "Int"
	
class ParGroupRGBA(_NumericParGroup["float", ParFloat]):
	class _args(_NumericParGroupArgs[float], _ParGroupArgs[float]):
		size : Literal[2,3,4]

	"TD RGBA Parameter"
	style:str = "RGBA"
	
class ParGroupXYZW(_NumericParGroup["float", ParFloat]):
	class _args(_NumericParGroupArgs[float], _ParGroupArgs[float]):
		size : Literal[2,3,4]

	"TD XYZW Parameter"
	style:str = "XYZW"
	
class ParGroupUVW(_NumericParGroup["float", ParFloat]):
	class _args(_NumericParGroupArgs[float], _ParGroupArgs[float]):
		size : Literal[2,3]

	"TD XYZW Parameter"
	style:str = "UVW"
	
class ParGroupWH(_NumericParGroup["float", ParFloat]):
	class _args(_NumericParGroupArgs[float], _ParGroupArgs[float]):
		size : Literal[2]
	"TD XYZW Parameter"
	style:str = "WH"

__all__ = ["ParGroupFloat", "ParGroupMenu", "ParGroupStrMenu", "ParGroupInt", "ParGroupRGBA", "ParGroupXYZW", "ParGroupUVW", "ParGroupWH"]