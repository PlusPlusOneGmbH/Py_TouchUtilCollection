from typing import Any, TypeVar, Type, overload, ClassVar, cast
from abc import abstractmethod
from dataclasses import dataclass

if __package__:
    from .par_def import partypes
else:
    # For testing in TD Itself.
    import partypes # pyright: ignore[reportMissingImports]


## Utils Start
T = TypeVar("T")

lookupdict = {}

def pop_default_kwarsg( target_dict:dict ):
    return {
        key : value for key, value in target_dict.items() if key not in  ["page", "label"]
    }

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
## Utils End



## Par Int
@dataclass(kw_only=True)
class _ParInt(_BasePar):
    min:float = 0
    max:float = 1
    default:int = 0
    def __call__(self, ownerComp) -> Any:
        target_par = ensure_parameter(
            ownerComp, self.name, self.page, "appendInt", "Int"
        )      
        target_par.min = self.min
        target_par.max = self.max
        return target_par
    
lookupdict[partypes.ParInt] = _ParInt

@overload
def parfield(field_type:Type[partypes.ParInt], 
             name:str, 
             label = "",
             page:str = "Custom", 
             default = 0,
             min = 0, 
             max = 1) -> partypes.ParInt:
    pass


## Par Float
@dataclass(kw_only=True)
class _ParFloat(_BasePar):
    min:float = 0
    max:float = 1
    default:float = 0
    def __call__(self, ownerComp) -> Any:
        target_par = ensure_parameter(
            ownerComp, self.name, self.page, "appendFloat", "Float"
        )      
        target_par.min = self.min
        target_par.max = self.max
        return target_par

lookupdict[partypes.ParFloat] = _ParFloat

@overload
def parfield(field_type:Type[partypes.ParFloat], 
             name:str, 
             label = "",
             page:str = "Custom", 
             default = 0,
             min = 0, 
             max = 1, ) -> partypes.ParFloat:
    pass


## Par Menu
from typing import List
@dataclass(kw_only=True)
class _ParMenu(_BasePar):
    menuNames:List[str]
    menuLabels:List[str]
    def __call__(self, ownerComp) -> Any:
        target_par = ensure_parameter(
            ownerComp, self.name, self.page, "appendMenu", "Menu"
        )      
        target_par.menuNames, target_par.menuLabels = self.menuNames, self.menuLabels or self.menuNames
        return target_par
    
lookupdict[partypes.ParMenu] = _ParMenu

@overload
def parfield(field_type:Type[partypes.ParMenu], 
             name:str, 
             label = "",
             page:str = "Custom", 
             default = "", 
             menuLabels:List[str] = [], 
             menuNames:List[str] = []) -> partypes.ParMenu:
    pass

## Str Menu

class _ParStrMenu(_BasePar):
    menuNames:List[str]
    menuLabels:List[str]
    def __call__(self, ownerComp) -> Any:
        target_par = ensure_parameter(
            ownerComp, self.name, self.page, "appendStrMenu", "StrMenu"
        )      
        target_par.menuNames, target_par.menuLabels = self.menuNames, self.menuLabels or self.menuNames
        return target_par
    
lookupdict[partypes.ParStrMenu] = _ParStrMenu

@overload
def parfield(field_type:Type[partypes.ParStrMenu], 
             name:str, 
             label = "",
             page:str = "Custom", 
             default = "", 
             menuLabels:List[str] = [], 
             menuNames:List[str] = []) -> partypes.ParStrMenu:
    pass

## Implementation

def parfield(field_type:Type[T], name:str, *args, page:str = "Custom", label= "",**kwargs): 
    pass_args = {
        "name" : name, 
        "label" : label,
        "page" : page,
        **pop_default_kwarsg( kwargs )
    }
    return cast( T, lookupdict[field_type](**pass_args) )

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


__all__ = [ "EnsureExtension", "EnsureParCollection", "parfield" ]

demo = None

if demo:

    class extExample( EnsureExtension ):
        class par( EnsureParCollection ):
            Foo = parfield(partypes.ParInt, "Foo")
            Bar = parfield(partypes.ParFloat, "MyFloat", page ="Different", min = 0, max = 10)
            Baba = parfield( partypes.ParMenu, "MyMenu", menuLabels=["Eins", "Zwei", "Drei" ] )

        def __init__(self, ownerComp) -> None:
            super().__init__(ownerComp)


    something = extExample(None)
    something.par.Bar
