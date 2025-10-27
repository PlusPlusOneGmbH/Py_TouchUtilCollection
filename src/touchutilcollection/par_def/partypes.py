"""
partypes.py

This file contains special classes for TouchDesigner parameters.
These objects don't exist in TD but are necessary for tdi to 
provide proper return types from parameters.
"""

from typing import Any, List
from abc import abstractmethod
from enum import Enum

class ParMode(Enum):
	BIND = "BIND"
	CONSTANT = "CONSTANT"
	EXPORT = "EXPORT"
	EXPRESSION = "EXPRESSION"


import typing as _T
ParValueT = _T.TypeVar('ParValueT')

from typing import NotRequired, TypedDict
###
class _ParArgs( TypedDict, _T.Generic[ParValueT] ):
		defaultMode : NotRequired[ParMode]
		default : NotRequired[ParValueT]
		defaultExpr : NotRequired[str]
		defaultBindExpr : NotRequired[str]
		readOnly : NotRequired[bool]
		enable : NotRequired[bool]
		expr : NotRequired[str]
		enableExpr : NotRequired[str]
		bindExpr : NotRequired[str]
		help : NotRequired[str]

class _Par(_T.Generic[ParValueT]):
	class _args(_ParArgs[ParValueT]): # pyright: ignore[reportGeneralTypeIssues]
		pass

	defaultMode : ParMode
	
	_creationMethodName : str
	style:str

	val:ParValueT
	@abstractmethod
	def eval(self) -> ParValueT:
		pass
	
	default : ParValueT
	defaultExpr : str
	defaultBindExpr : str
	
	readOnly : bool
	enable : bool

	owner : Any

	expr : str
	enableExpr : str
	bindExpr :str
	
	name : str
	label : str
	help : str
	
	@abstractmethod
	def destroy(self):
		pass
	@abstractmethod
	def reset() -> bool:
		pass
	@abstractmethod
	def isPar( par:Any ) -> bool:
		pass

class _NumericParArgs( TypedDict, _T.Generic[ParValueT] ):	
		min : NotRequired[ParValueT]
		max : NotRequired[ParValueT]
		normMin : NotRequired[ParValueT]
		normMax : NotRequired[ParValueT]
		clampMin : NotRequired[ParValueT]
		clampMax : NotRequired[ParValueT]
		


class _NumericPar(_Par[ParValueT]):
	class _args(_NumericParArgs[ParValueT], _ParArgs[ParValueT]): # pyright: ignore[reportGeneralTypeIssues]
		pass
	min : ParValueT
	max : ParValueT
	normMin : ParValueT
	normMax : ParValueT
	clampMin : ParValueT
	clampMax : ParValueT
	@abstractmethod
	def evalNorm(self) -> ParValueT:
		pass


class _MenuParArgs( TypedDict ):
		menuLabels : NotRequired[List[str]]
		menuSource : NotRequired[str]
		

class _MenuPar( _Par["str"]):
	class _args(_MenuParArgs, _ParArgs["str"]): # pyright: ignore[reportGeneralTypeIssues]
		pass
	menuNames : List[str]
	menuLabels : List[str]
	menuSource : str
	"""
	Get or set an expression that returns an object with .menuItems .menuNames members. This can be used to create a custom menu whose entries dynamically follow that of another menu for example. Simple menu sources include another parameter with a menu c, an object created by tdu.TableMenu, or an object created by TDFunctions.parMenu.
	```
	p.menuSource = "op('audiodevin1').par.device"
	```
	Note the outside quotes, as menuSource is an expression, not an object.
	"""




class ParStr(_Par["str"]):
	"TD Str Parameter"
	style:str = "Str"

class ParFloat(_NumericPar["float"]):
	"TD Float Parameter"
	style:str = "Float"

class ParInt(_NumericPar["int"]):
	"TD Int Parameter"
	style:str = "Int"

class ParToggle(_Par["bool"]):
	"TD Toggle Parameter"
	style:str = "Toggle"

class ParMomentary(_Par["bool"]):
	"TD Momentary Parameter"
	style:str = "Momentary"

class ParPulse(_Par["bool"]):
	"TD Pulse Parameter"
	style:str = "Pulse"

class ParMenu(_MenuPar):
	"TD Menu Parameter"
	style:str = "Menu"

class ParStrMenu(_MenuPar):
	"TD StrMenu Parameter"
	style:str = "StrMenu"

class ParCOMP(_Par["None | COMP"]):
	"TD COMP Parameter"
	style:str = "COMP"


class ParOP(_Par["None | OP"]):
	"TD OP Parameter"
	style:str = "OP"


# Not yet implemented.
"""
class ParPython(_Par["Any"]):
	"TD Python Parameter"

class ParRGB(_NumericPar["float"]):
	"TD RGB Parameter"

class ParRGBA(_NumericPar["float"]):
	"TD RGBA Parameter"

class ParUV(_NumericPar["float"]):
	"TD UV Parameter"

class ParUVW(_NumericPar["float"]):
	"TD UVW Parameter"

class ParWH(_NumericPar["float"]):
	"TD WH Parameter"

class ParXY(_NumericPar["float"]):
	"TD XY Parameter"

class ParXYZ(_NumericPar["float"]):
	"TD XYZ Parameter"

class ParXYZW(_NumericPar["float"]):
	"TD XYZW Parameter"

class ParObject(_Par["None | ObjectCOMP"]):
	"TD Object Parameter"

class ParSOP(_Par["None | SOP"]):
	"TD SOP Parameter"

class ParPOP(_Par["None | POP"]):
	"TD POP Parameter"

class ParMAT(_Par["None | MAT"]):
	"TD MAT Parameter"

class ParCHOP(_Par["None | CHOP"]):
	"TD CHOP Parameter"

class ParTOP(_Par["None | TOP"]):
	"TD TOP Parameter"

class ParDAT(_Par["None | DAT"]):
	"TD DAT Parameter"

class ParPanelCOMP(_Par["None | PanelCOMP"]):
	"TD PanelCOMP Parameter"

class ParCOMP(_Par["None | COMP"]):
	"TD COMP Parameter"

class ParOP(_Par["None | OP"]):
	"TD OP Parameter"

class ParFile(_Par["str"]):
	"TD File Parameter"

class ParFileSave(_Par["str"]):
	"TD FileSave Parameter"

class ParFolder(_Par["str"]):
	"TD Folder Parameter"

class ParHeader(_Par["str"]):
	"TD Header Parameter"

class ParSequence(_NumericPar["int"]):
	"TD Sequence Parameter"

class ParDATAdder(_Par["None"]):
	"TD DATAdder Parameter"
"""