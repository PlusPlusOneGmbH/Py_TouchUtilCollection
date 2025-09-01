from typing import Any, TypeVar, Type, overload, ClassVar
from abc import abstractmethod
from dataclasses import dataclass
from . import partypes

T = TypeVar("T")

@dataclass
class _BasePar():
    name:str
    page:str
    label:str = ""

    @abstractmethod
    def __call__(self, ownerComp) -> Any:
        raise NotImplemented
    pass

def ensure_page(ownerComp, pagename):
    for page in ownerComp.pages:
        if page.name == pagename: return page
    return ownerComp.appendCustomPage( pagename )

def ensure_parameter(ownerComp, par_name:str, pagename:str, adder_method_name:str, par_style:str):
    page = ensure_page( ownerComp, pagename)
    if (par := ownerComp.par[par_name]) is not None:
        # lets validate the partype itself.
        if par.style != par_style: par.destroy()

    if ownerComp.par[par_name] is None:
        # now lets check if the par already exists, if not    
        getattr(page, adder_method_name)( par_name )
    return ownerComp.par[par_name]
    

@dataclass(kw_only=True)
class _ParInt(_BasePar):
    min:float
    max:float
    def __call__(self, ownerComp) -> Any:
        target_par = ensure_parameter(
            ownerComp, self.name, self.page, "appendInt", "Int"
        )      
        target_par.min = self.min
        target_par.max = self.max
        return target_par


@dataclass(kw_only=True)
class _ParFloat(_BasePar):
    min:float
    max:float
    def __call__(self, ownerComp) -> Any:
        target_par = ensure_parameter(
            ownerComp, self.name, self.page, "appendFloat", "Float"
        )      
        target_par.min = self.min
        target_par.max = self.max
        return target_par
from typing import cast

@overload
def parfield(fieldType:Type[partypes.ParInt], name:str, page:str = "Custom", label = "",min = 0, max = 1) -> partypes.ParInt:
    pass
@overload
def parfield(fieldType:Type[partypes.ParFloat], name:str, page:str = "Custom", label = "",min = 0, max = 1) -> partypes.ParFloat:
    pass
   
def parfield(fieldType:Type[T], name:str, *args, page:str = "Custom", label= "", **kwargs): 
    if fieldType == partypes.ParInt: 
        return cast( T, _ParInt(name = name, label = label, page= page, min = kwargs["min"], max = kwargs["max"]) )
    if fieldType == partypes.ParFloat:
        return cast( T,  _ParFloat(name = name, label = label, page= page, min = kwargs["min"], max = kwargs["max"]))
    return cast(T, None)

class EnsureParCollection( ):
    pass

class EnsureExtension ():
    par:ClassVar
    def __init__(self, ownerComp) -> None:
        self.par = self.par() # pyright: ignore[reportAttributeAccessIssue]
        for attr_name in dir(self.par):
            attr_object = getattr( self.par, attr_name )
            if not isinstance( attr_object, _BasePar): continue
            setattr( self.par, attr_name, attr_object(ownerComp) )





class extExample( EnsureExtension ):
    class par( EnsureParCollection ):
        Foo = parfield(partypes.ParInt, "Foo")
        Bar = parfield(partypes.ParFloat, "MyFloat", page ="Different", min = 0, max = 10)

    def __init__(self, ownerComp) -> None:
        super().__init__(ownerComp)
        self.par.Bar
