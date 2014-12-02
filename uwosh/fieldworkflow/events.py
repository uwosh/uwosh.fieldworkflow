from interfaces import IFieldWorkflowEnabled
from zope.interface import classImplements
from Products.CMFCore.utils import getToolByName

#do not allow all attributes to be dynamic...  
#these are things that usually are not needed to be dynamic anyways
#changing some of these things dynamically would otherwise cause problems
forbidden_attributes = ['widget', 'generateMode', 'searchable', 'isMetadata', 'old_field_name', 'mutator',
                        'force', 'accessor', 'edit_accessor', 'edit_accessor', 'index', 'default_content_type',
                        'default', 'storage', 'vocabulary_factory', 'languageIndependent', 'multiValued', 
                        'default_method', 'index_method', 'type']

def set_field_settings_for_state(field, state):
    """
    sets the fields settings for the specified state
    """
    defaults = field.workflow_settings['__defaults__']
    state_settings = field.workflow_settings[state]
    
    for key in [key for key in field._properties.keys() if key not in forbidden_attributes]:
        if state_settings.has_key(key):
            setattr(field, key, state_settings[key])
        else:
            setattr(field, key, defaults[key])
            
    field._validationLayer() #sets up validation for field

def set_default_field_settings(field):
    """
    If state does not have anything custom defined for it, revert to its default settings
    """
    defaults = field.workflow_settings['__defaults__']
    
    for key in [key for key in field._properties.keys() if key not in forbidden_attributes]:
        setattr(field, key, defaults[key])
    
    field._validationLayer() #sets up validation for field

def copy_default_settings(field):
    """
    copies all the default settings to the __defaults__ key in the dict
    """
    field.workflow_settings['__defaults__'] = field._properties.copy()

def validate_fields(obj):
    """
    iterates through each field and validates it
    calling the custom error hanlder if needed
    """
    
    fields = obj.Schema().fields()
    
    for field in fields:
        error = field.validate(field.get(obj), obj)
        if error:
            #traverse to validator page
            #don't know how to get the actual request object since this does not seem to be working
            
            if hasattr(obj, 'validation_error_handler'):
                obj.validation_error_handler(error)
            else:
                #need to find a way to traverse to validated page
                raise Exception(error)
            
            return False
            
    return True

def should_validate(obj, event):
    """
    Checks if the validation is required
    """
    if hasattr(obj, 'validate_on_transition') and obj.validate_on_transition and event.transition:
        if hasattr(obj, 'transitions_to_validate_on') and event.transition in obj.transitions_to_validate_on:
           return True
        else:
            return False
     
def after_transition_event(obj, event):
    """
    What gets called after each transition for an object
    """
    
    #check if obj implements field workflows, just return if it doesn't
    if not IFieldWorkflowEnabled.implementedBy(obj.__class__): return
    
    #check if you should validate, if so validate
    if should_validate(obj, event) and not validate_fields(obj): return
    
    state = event.new_state.id
    fields = obj.Schema().fields()
    
    for field in fields:
        if hasattr(field, 'workflow_settings'):
            #if the defaults were not copied yet
            #might need a better way to hook into
            if not field.workflow_settings.has_key('__defaults__'): 
                copy_default_settings(field)
            elif field.workflow_settings.has_key(state):
                set_field_settings_for_state(field, state)
            else:
                set_default_field_settings(field)
        
        
    
    
    
    