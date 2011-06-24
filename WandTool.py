from __main__ import vtk, qt, ctk, slicer
import EditorLib
from EditorLib.EditOptions import HelpButton

#
# The Editor Extenion itself.
# 
# This needs to define the hooks to be come an editor effect.
#

class WandToolDisplayableManager:
  """ WandTool-specific displayable manager
  """

  def __init__(self, parent):
    # parent is a vtkScriptedDisplayableManager
    self.Parent = parent
    
    slicer.sliceWidgetRed_interactorStyle.AddObserver('MouseMoveEvent', self.OnMouseMove());

  def Create(self):
    pass

  def ProcessMRMLEvents(self, scene, eventId, node):
    pass
  
  def OnMouseMove(self, caller, event):
    
    print "Hello"
    

class WandToolOptions(EditorLib.LabelerOptions):
  """ WandTool-specfic gui
  """

  def __init__(self, parent=0):
    super(WandToolOptions,self).__init__(parent)
    # self.attributes should be tuple of options:
    # 'MouseTool' - grabs the cursor
    # 'Nonmodal' - can be applied while another is active
    # 'Disabled' - not available
    self.attributes = ('MouseTool', 'Nonmodal')
    self.displayName = 'Editor Extension Template'

  def __del__(self):
    super(WandToolOptions,self).__del__()

  def create(self):
    super(WandToolOptions,self).create()
    self.apply = qt.QPushButton("Apply", self.frame)
    self.apply.setToolTip("Apply the extension operation")
    self.frame.layout().addWidget(self.apply)
    self.widgets.append(self.apply)

    HelpButton(self.frame, "This is a sample with no real functionality.")

    self.apply.connect('clicked()', self.onApply)

    # Add vertical spacer
    self.frame.layout().addStretch(1)

    # create a displayable manager for the effect
    # slicer.app.scriptedDisplayableManager.register(WandToolDisplayableManager)
    self.displayableManager = WandToolDisplayableManager(self)

  def destroy(self):
    super(WandToolOptions,self).destroy()
    # slicer.app.scriptedDisplayableManager.unregister(WandToolDisplayableManager)    

  # note: this method needs to be implemented exactly as-is
  # in each leaf subclass so that "self" in the observer
  # is of the correct type 
  def updateParameterNode(self, caller, event):
    nodeID = tcl('[EditorGetParameterNode] GetID')
    node = slicer.mrmlScene.GetNodeByID(nodeID)
    if node != self.parameterNode:
      if self.parameterNode:
        node.RemoveObserver(self.parameterNodeTag)
      self.parameterNode = node
      self.parameterNodeTag = node.AddObserver("ModifiedEvent", self.updateGUIFromMRML)

  def setMRMLDefaults(self):
    super(WandToolOptions,self).setMRMLDefaults()

  def updateGUIFromMRML(self,caller,event):
    self.updatingGUI = True
    super(WandToolOptions,self).updateGUIFromMRML(caller,event)
    self.updatingGUI = False

  def onApply(self):
    print('This is just an example - nothing here yet')

  def updateMRMLFromGUI(self):
    if self.updatingGUI:
      return
    disableState = self.parameterNode.GetDisableModifiedEvent()
    self.parameterNode.SetDisableModifiedEvent(1)
    super(WandToolOptions,self).updateMRMLFromGUI()
    self.parameterNode.SetDisableModifiedEvent(disableState)
    if not disableState:
      self.parameterNode.InvokePendingModifiedEvent()

#
# WandTool
#

class WandTool:
  """
  This class is the 'hook' for slicer to detect and recognize the extension
  as a loadable scripted module
  """
  def __init__(self, parent):
    parent.title = "Wand Tool"
    parent.category = "Editor Extensions"
    parent.contributor = "Steve Pieper"
    parent.helpText = """
    Example of an editor extension.  No module interface here, only in the Editor module
    """
    parent.acknowledgementText = """
    This editor extension was developed by 
    <Author>, <Institution>
    based on work by:
    Steve Pieper, Isomics, Inc.
    based on work by:
    Jean-Christophe Fillion-Robin, Kitware Inc.
    and was partially funded by NIH grant 3P41RR013218.
    """

    # TODO:
    # don't show this module - it only appears in the Editor module
    #parent.hidden = True

    try: 
      slicer.modules.editorExtensions['WandToolOptions'] = WandToolOptions
    except AttributeError:
      slicer.modules.editorExtensions = {}
      slicer.modules.editorExtensions['WandToolOptions'] = WandToolOptions
      
#
# WandTool
#

class WandToolWidget:
  def __init__(self, parent = None):
    self.parent = parent
    
  def setup(self):
    # don't display anything for this widget - it will be hidden anyway
    pass

  def enter(self):
    pass
    
  def exit(self):
    pass


