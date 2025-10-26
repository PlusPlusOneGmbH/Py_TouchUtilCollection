from typing import Any, TypeVar, Type, overload, ClassVar, cast, List, Union
from abc import abstractmethod
from dataclasses import dataclass

from .par_def import partypes



## Utils Start
lookupdict = {}

def pop_default_kwarsg( target_dict:dict ):
    return {
        key : value for key, value in target_dict.items() if key not in  ["page", "label"]
    }

@dataclass
class _Par():
    data : dict
    par_type : partypes.Par

    def __call__(self, ownerComp) -> Any:
        target_par = ensure_parameter(
            ownerComp, 
            self.data["name"], 
            self.data["page"], 
            f"append{self.par_type.style}", 
            self.par_type.style
        )  
        return target_par
    

def ensure_page(ownerComp, pagename):
    for page in ownerComp.pages:
        if page.name == pagename: return page
    return ownerComp.appendCustomPage( pagename )

def ensure_parameter(ownerComp, par_name:str, pagename:str, adder_method_name:str, par_style:str):
    page = ensure_page( ownerComp, pagename )
    if (par := ownerComp.par[par_name]) is not None:
        # lets validate the partype itself.
        if par.style != par_style: par.destroy()

    if ownerComp.par[par_name] is None:
        # now lets check if the par already exists, if not    
        getattr(page, adder_method_name)( par_name )
    return ownerComp.par[par_name] # This noteably only works with single value parameters!
## Utils End

@overload
def parfield(field_type:Type[partypes.ParInt], 
             name:str, 
             label = "",
             page:str = "Custom", 
             default = 0,
             min = 0, 
             max = 1) -> partypes.ParInt:
    pass

@overload
def parfield(field_type:Type[partypes.ParFloat], 
             name:str, 
             label = "",
             page:str = "Custom", 
             default = 0.0,
             min = 0.0, 
             max = 1.0, ) -> partypes.ParFloat:
    pass


@overload
def parfield(field_type:Type[Union[partypes.ParMenu, partypes.ParStrMenu]], 
             name:str, 
             label = "",
             page:str = "Custom", 
             default = "", 
             menuLabels:List[str] = [], 
             menuNames:List[str] = []) -> Union[partypes.ParMenu, partypes.ParStrMenu]:
    pass

@overload
def parfield(field_type:Type[partypes.ParPulse], 
             name:str, 
             label = "",
             page:str = "Custom"
            ) -> partypes.ParPulse:
    pass

@overload
def parfield(field_type:Type[partypes.ParMomentary], 
             name:str, 
             label = "",
             page:str = "Custom", 
            ) -> partypes.ParMomentary:
    pass



T = TypeVar("T")


def parfield(field_type:Type[T], name:str, *args, page:str = "Custom", label= "",**kwargs): 
    pass_args = {
        "name" : name, 
        "label" : label or name,
        "page" : page,
        **pop_default_kwarsg( kwargs )
    }
    return cast( T, _Par(pass_args, field_type) ) # pyright: ignore[reportArgumentType] # Yeah yeah, I know :)

#class EnsureParCollection( ):
#    pass

class EnsureExtension ():
    par:ClassVar
    def __init__(self, ownerComp) -> None:
        self.par = self.par() # pyright: ignore[reportAttributeAccessIssue]
        for attr_name in dir(self.par):
            attr_object = getattr( self.par, attr_name )
            if not isinstance( attr_object, _Par): continue
            setattr( self.par, attr_name, attr_object(ownerComp) )


__all__ = [ "EnsureExtension", "parfield" ]

demo = None
if demo:

    class extExample( EnsureExtension ):
        class par:
            Foo = parfield(partypes.ParInt, "Foo")
            Bar = parfield(partypes.ParFloat, "MyFloat", page ="Different", min = 0, max = 10)
            Baba = parfield( partypes.ParMenu, "MyMenu", menuLabels=["Eins", "Zwei", "Drei" ] )

        def __init__(self, ownerComp) -> None:
            super().__init__(ownerComp)


    something = extExample(None)
    something.par.Baba.default = 123 # Errors
    something.par.Baba.default = "123" # Works!
