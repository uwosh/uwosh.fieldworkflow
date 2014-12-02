Introduction
============
This product is designed to make your life easier when making
workflow applications.

We've come across situations where we need more complex control
over specific fields during each workflow state.

supported field attributes
-required
-validators
-write_permission
-read_permission

How to do it
================
All you need to do is have your content type implement IFieldWorkflowEnabled
and provide the desired workflow settings under each field.

Example
========================


from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces
from example.config import *
from uwosh.fieldworkflow.interfaces import IFieldWorkflowEnabled

schema = Schema((

    IntegerField(
        name='numberOfWheels',
        widget=StringField._properties['widget'](
            label="Number of wheels",
        ),
        searchable=True,
				#this is how you would set workflow changes to fields
				workflow_settings={
					"published" :{
						"required": True,
						"validators": ("isNumeric",)
					}
				}
    ),
),
)


CarSchema = BaseSchema.copy() + schema.copy()


class Car(BaseContent, BrowserDefaultMixin):

		#required to make this work!
    implements(interfaces.ICar, IFieldWorkflowEnabled)
		
		#set if you would like to validate on transitions...  Required attribute
		validate_on_transition = True
		
		#set to fine tune what transitions you would like to validate on
		transitions_to_validate_on = ["submit", "publish"]

		#used to handle your errors the way you want.
		def validation_error_handler(self, error):
				pass

    meta_type = portal_type = 'Car'
    schema = ExpertSchema
    
    
registerType(Car, PRODUCT_NAME)