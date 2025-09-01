"""
partypes.py

This file contains special classes for TouchDesigner parameters.
These objects don't exist in TD but are necessary for tdi to 
provide proper return types from parameters.
"""

from typing import Any
from abc import abstractmethod

import typing as _T
ParValueT = _T.TypeVar('ParValueT')
###

class Par(_T.Generic[ParValueT]):
    """
    This is only a bandaid and nor for actual production use.
    """
    val:ParValueT

    @abstractmethod
    def eval(self) -> ParValueT:
        pass
	

class ParStr(Par["str"]):
	"TD Str Parameter"

class ParPython(Par["Any"]):
	"TD Python Parameter"

class ParFloat(Par["float"]):
	"TD Float Parameter"

class ParInt(Par["int"]):
	"TD Int Parameter"

class ParToggle(Par["bool"]):
	"TD Toggle Parameter"

class ParMomentary(Par["bool"]):
	"TD Momentary Parameter"

class ParPulse(Par["bool"]):
	"TD Pulse Parameter"

class ParMenu(Par["str"]):
	"TD Menu Parameter"

class ParStrMenu(Par["str"]):
	"TD StrMenu Parameter"

class ParRGB(Par["float"]):
	"TD RGB Parameter"

class ParRGBA(Par["float"]):
	"TD RGBA Parameter"

class ParUV(Par["float"]):
	"TD UV Parameter"

class ParUVW(Par["float"]):
	"TD UVW Parameter"

class ParWH(Par["float"]):
	"TD WH Parameter"

class ParXY(Par["float"]):
	"TD XY Parameter"

class ParXYZ(Par["float"]):
	"TD XYZ Parameter"

class ParXYZW(Par["float"]):
	"TD XYZW Parameter"

class ParObject(Par["None | ObjectCOMP"]):
	"TD Object Parameter"

class ParSOP(Par["None | SOP"]):
	"TD SOP Parameter"

class ParPOP(Par["None | POP"]):
	"TD POP Parameter"

class ParMAT(Par["None | MAT"]):
	"TD MAT Parameter"

class ParCHOP(Par["None | CHOP"]):
	"TD CHOP Parameter"

class ParTOP(Par["None | TOP"]):
	"TD TOP Parameter"

class ParDAT(Par["None | DAT"]):
	"TD DAT Parameter"

class ParPanelCOMP(Par["None | PanelCOMP"]):
	"TD PanelCOMP Parameter"

class ParCOMP(Par["None | COMP"]):
	"TD COMP Parameter"

class ParOP(Par["None | OP"]):
	"TD OP Parameter"

class ParFile(Par["str"]):
	"TD File Parameter"

class ParFileSave(Par["str"]):
	"TD FileSave Parameter"

class ParFolder(Par["str"]):
	"TD Folder Parameter"

class ParHeader(Par["str"]):
	"TD Header Parameter"

class ParSequence(Par["int"]):
	"TD Sequence Parameter"

class ParDATAdder(Par["None"]):
	"TD DATAdder Parameter"
