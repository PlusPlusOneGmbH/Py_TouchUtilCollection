from td import * # pyright: ignore[reportMissingImports]
from typing import cast
from pathlib import Path

def better_import():
    """
        Opiniated utility to import external data. It will create the correct operator for the filetype, set the refference to the file
        and lets you place it in the according location.
        If the path is relative, relative pathing will be used.
        If it is a tox, a hard refference to the tox will be created.
    """
    current_pane:Pane = ui.panes.current

    if not isinstance( current_pane, NetworkEditor ):
        ui.messageBox("Invalid Pane", "Requires NetworkEditor to be selected as current pane.")
        return
    
    current_editor:NetworkEditor = current_pane
    owner = current_pane.owner    
    _filepath = ui.chooseFile()
    if _filepath is None: return
    try:
        filepath = Path( _filepath ).absolute().relative_to( Path(".").absolute() )
    except ValueError:
        filepath = Path( _filepath )

    file_item = tdu.FileInfo( _filepath )
    if file_item.fileType in ("movie", "image"):
        new_op = owner.create( moviefileinTOP, "moviefilein1" )
        new_op.par.file.val = filepath
    elif file_item.fileType in ("audio",):
        new_op = owner.create( audiofileinCHOP, "audiofilein1" )
        new_op.par.file.val = filepath

    elif file_item.fileType in ("pointdata",):
        new_op = owner.create( pointfileinTOP, "pointdatain1" )
        new_op.par.file.val = filepath

    elif file_item.fileType in ("text",):
        new_op = owner.create( textDAT, "text1" )
        new_op.par.file.val = filepath
        new_op.par.language.menuIndex = 1
        new_op.par.extension.val = Path( filepath ).suffix.strip(".")
        new_op.par.loadonstartpulse.pulse()

    elif file_item.fileType in ("component",):
        new_op = cast(COMP, owner.loadTox( filepath ) )
        new_op.par.externaltox.val = filepath
        new_op.par.enableexternaltox.val = True
    else:
        return

    current_editor.placeOPs([new_op])
    