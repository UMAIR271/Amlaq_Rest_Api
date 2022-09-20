def modify_input_for_multiple_files(id, image):
    dict = {}
    dict['listing'] = id
    dict['images_Url'] = image
    return dict

def multiple_Amenaties(id,Amenities_name):
    dict = {}
    dict['listing'] = id
    dict['Amenities_Name'] = Amenities_name
    return dict

def multiple_property(id,property):
    dict = {}
    dict['listing'] = id
    dict['property_type'] = property
    return dict

def floorPlans_multiple_files(id, floorImage):
    dict = {}
    dict['listing'] = id
    dict['floorPlaneImage'] = floorImage
    return dict

def verify_multiple_files(id, verify_image):
    dict = {}
    dict['listing'] = id
    dict['propertyVerificationImage'] = verify_image
    return dict