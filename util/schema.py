from arcgis.features import FeatureLayerCollection
def unlock_schema(flc: FeatureLayerCollection ) -> dict:
    '''
    ##Inputs
     - source: should be a feature layer collection created using the
     arcgis.feature.FeatureLayerCollection() class.
    ##Return
     - A dictionary containing a status key and a props key. 
     Update status can be verified with the status key and further validation can
     be provided using the props key to review the targeted attributes.
    '''
    
    from arcgis.features import FeatureLayerCollection
    
    #convert item to flc to access and manipulate properties
    
    updates = {'sourceSchemaChangesAllowed' : True,
               'hasStaticData' : False,
               'lastEditDate' : ''}
    
    status = flc.manager.update_definition(updates)
    
    output = {'status' : status,
              'props' : flc.properties}
    
    return output

def lock_schema(flc: FeatureLayerCollection ) -> dict:
    '''
    ##Inputs
     - source: should be a feature layer collection created using the
     arcgis.feature.FeatureLayerCollection() class.
    ##Return
     - A dictionary containing a status key and a props key. 
     Update status can be verified with the status key and further validation can
     be provided using the props key to review the targeted attributes.
    '''
    
    from arcgis.features import FeatureLayerCollection
    
    #convert item to flc to access and manipulate properties
    
    updates = {'sourceSchemaChangesAllowed' : False,
               'hasStaticData' : True,
               'lastEditDate' : ''}
    
    status = flc.manager.update_definition(updates)
    
    output = {'status' : status,
              'props' : flc.properties}
    
    return output