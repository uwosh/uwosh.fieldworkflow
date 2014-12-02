from zope.interface import Interface, Attribute

class IFieldWorkflowEnabled(Interface):
    """
    marker interface to specify if the class wants to use
    workflows for fields
    """
    
    validate_on_transition = Attribute("""Specify is you want to validate on transitions or not""")