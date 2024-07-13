API_VERSION = 'API_v1.0' # This is Mandatory!
MOD_NAME = 'TestMod' # Your Mod Name


class TestMod(object):
  def __init__(self):
    events.onBattleStart(self.onBattleStart)
    events.onBattleQuit(self.onBattleQuit)
    events.onKeyEvent(self.onKeyEvent)
    self._uiId = None

  def onBattleStart(self, *args):
    # Creates an entity in DataHub and retrieves its id
    self._uiId = uiId = ui.createUiElement()

    # Add `mods_DataComponent` to the created entity
    #
    # Important Note:
    # The second argument is the key - 
    # that helps you to find this entity from Unbound DataHub.
    # It MUST be a UNIQUE STRING across All the Modifications.
    ui.addDataComponentWithId(uiId, 'superUniqueTestModEntityKey', {})

  def onBattleQuit(self, *args):
    # Remove entity from DataHub
    # Components in the entity will automatically be cleared
    ui.deleteUiElement(self._uiId)
    self._uiId = None

  def onKeyEvent(self, keyEvent):
    data = dict(
    keyName     = keyEvent.key,
    isShiftDown = keyEvent.isShiftDown(),
    )
    #
    # Update `mods_DataComponent` data
    #
    # DataHub accepts the following types:
    # - int, float, str, bool, list, tuple, dict
    # - Other types (custom classes) will cause errors.
    # 
    #
    # Another important thing is how data is synchronized
    # between Unbound Datahub and C++/Python Datahub.
    #
    # - Changes to Python Datahub will not be reflected to Unbound Datahub
    # when the memory address remains the same.
    #
    # e.g.
    #
    # initdict = {'key1': 'value1'}
    # id(initdict) #>> object is at 0L on memory
    # ui.addDataComponent(entityId, initdict)
    # ### This will be reflected to Ub DataHub
    # ### So you can retrieve 'key1' and 'value1' from Unbound
    #
    # somedict = {'key1': 'value2'}
    # id(somedict) #>> 1L
    # ui.updateUiElementData(entityId, somedict)
    # ### This update proeprly triggers mods_DataComponent.evDataChanged event.
    # ### Because target object's memory address is differnt. (0L != 1L)
    # 
    # somedict['key1'] = 'value3'
    # id(somedict) #>> still 1L
    # ui.updateUiElementData(entityId, somedict)
    # ### However, this does not trigger evDataChanged
    # ### because the address on memory of somedict is the same as before.
    # ### So the value of 'key1' also remains unchanged ('value2') in Unbound.
    #
    # ### Thus, you must create a new instance of the object in order to trigger the update event.
    # ### This behavior applies recursively.
    # ### So objects within another object (lists in dict, etc) also need to be on new memory address.
    #
    # ui.updateUiElementData(entityId, dict(somedict))
    # ### This will trigger evDataChanged event.
    #
    ui.updateUiElementData(self._uiId, data)

testMod = TestMod()