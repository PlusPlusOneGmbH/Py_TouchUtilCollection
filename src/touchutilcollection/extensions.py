from typing import Any, TypeVar, Type, overload, ClassVar, cast, List, Union
from abc import abstractmethod
from dataclasses import dataclass



from .par_def import partypes

## Utils Start
lookupdict = {}

def _pop_default_kwarsg( target_dict:dict ):
    return {
        key : value for key, value in target_dict.items() if key not in  ["page", "label"]
    }

@dataclass
class _ParProxy():
    data : dict
    par_type : Type[partypes._Par]

    def __call__(self, ownerComp) -> Any:
        target_par = ensure_parameter(
            ownerComp, 
            self.data["name"], 
            self.data["page"], 
            f"append{self.par_type.style}", 
            self.par_type.style
        )  

        #One can dram. Pleas derivative senpai.
        #_dependency_object = tdu.Dependency( target_par.eval() )
        #_dependency_object.bindMaster = target_par
        #_dependency_object.callbacks.append( self.data.get("callback", lambda *args: None) )

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



from typing import Unpack

T = TypeVar("T") 

### Overlods for typehinting.
@overload
def parfield(field_type:Type[partypes.ParStr], name:str, page:str = "Custom", label= "", **kwargs:Unpack[ partypes.ParStr._args]) -> partypes.ParStr: 
    pass

@overload
def parfield(field_type:Type[partypes.ParFloat], name:str, page:str = "Custom", label= "", **kwargs:Unpack[ partypes.ParFloat._args]) -> partypes.ParFloat: 
    pass

@overload
def parfield(field_type:Type[partypes.ParInt], name:str, page:str = "Custom", label= "",**kwargs:Unpack[ partypes.ParInt._args]) -> partypes.ParInt: 
    pass
@overload
def parfield(field_type:Type[partypes.ParToggle], name:str, page:str = "Custom", label= "", **kwargs:Unpack[ partypes.ParToggle._args]) -> partypes.ParToggle: 
    pass

@overload
def parfield(field_type:Type[partypes.ParMomentary], name:str, page:str = "Custom", label= "",**kwargs:Unpack[ partypes.ParMomentary._args ]) -> partypes.ParMomentary: 
    pass

@overload
def parfield(field_type:Type[partypes.ParPulse], name:str, page:str = "Custom", label= "",**kwargs:Unpack[ partypes.ParPulse._args ]) -> partypes.ParPulse: 
    pass

@overload
def parfield(field_type:Type[partypes.ParMenu], name:str, page:str = "Custom", label= "",**kwargs:Unpack[ partypes.ParMenu._args]) -> partypes.ParMenu: 
    pass

@overload
def parfield(field_type:Type[partypes.ParStrMenu], name:str, page:str = "Custom", label= "",**kwargs:Unpack[ partypes.ParStrMenu._args]) -> partypes.ParStrMenu: 
    pass

@overload
def parfield(field_type:Type[partypes.ParOP], name:str, page:str = "Custom", label= "",**kwargs:Unpack[ partypes.ParOP._args]) -> partypes.ParOP: 
    pass

## Actual Implementation.
def parfield(field_type:Type[T], name:str, page:str = "Custom", label= "",**kwargs) -> T: 
    pass_args = {
        "name" : name, 
        "label" : label or name,
        "page" : page,
        **_pop_default_kwarsg( kwargs )
    }
    return cast( T, _ParProxy(pass_args, field_type) )  # pyright: ignore[reportArgumentType]

class EnsureExtension():
    par:ClassVar
    def __init__(self, ownerComp) -> None:
        self.par = self.par() # pyright: ignore[reportAttributeAccessIssue]
        for attr_name in dir(self.par):
            attr_object = getattr( self.par, attr_name )
            if not isinstance( attr_object, _ParProxy): continue
            setattr( self.par, attr_name, attr_object(ownerComp) )


__all__ = [ "EnsureExtension", "parfield", "partypes" ]

demo = None
if demo:

    class extExample( EnsureExtension ):
        class par:
            Foo = parfield(partypes.ParFloat, "Foo")
            Bar = parfield(partypes.ParFloat, "MyFloat", page ="Different", min = 0, max = 10)
            Baba = parfield( partypes.ParMenu, "MyMenu", menuLabels=["Eins", "Zwei", "Drei" ],bindExpr="Hello World")

        def __init__(self, ownerComp) -> None:
            super().__init__(ownerComp)
            self.par.Foo.val = 23

    something = extExample(None)
    something.par.Baba.default = 123 # pyright: ignore[reportAttributeAccessIssue] # Errors
    something.par.Baba.default = "123" # Works!
