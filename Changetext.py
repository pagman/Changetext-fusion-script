import adsk.core, adsk.fusion, adsk.cam, traceback
import os.path, sys, time
from pathlib import Path

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface        
        design = app.activeProduct
        rootComp = design.rootComponent

        
        
        # Get the sketch named "ChangeText"
        sk = rootComp.sketches.itemByName('ChangeText')
        
        # Get the first sketch text.
        skText = sk.sketchTexts.item(0)

        #Prompts the user for the new Text   
        (returnValue, cancelled) = ui.inputBox('What text?', 'New text:', )
        (digits, cancelled) = ui.inputBox('digits', 'New text:', )
        for x in range(0,10):

            #move to previous step
            tl = design.timeline
            tl.moveToPreviousStep()

            value = int(returnValue[int(digits):])
            value = value+x

        
            # Grab the sketch and first text entity 
            sk = rootComp.sketches.itemByName('ChangeText') 
            skText = sk.sketchTexts.item(0)

            # Change the text.
            skText.text = returnValue[0:int(digits)] + str(value)

            #move to next step
            tl.movetoNextStep()
            basePath = 'C:\stl\Y'
            addedPath = returnValue[0:int(digits)]
            # Write in the path to the folder where you want to save STL‘s
            folder = basePath[:-1] + addedPath
        
            # Construct the output filename. Name will be the same as you‘ve changed    the text into.
            filename = folder + skText.text[int(digits):] + '.stl'

            # Save the file as STL.
            exportMgr = adsk.fusion.ExportManager.cast(design.exportManager)
            stlOptions = exportMgr.createSTLExportOptions(rootComp)
            stlOptions.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementMedium
            stlOptions.filename = filename
            exportMgr.execute(stlOptions)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))