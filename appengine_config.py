from google.appengine.api import namespace_manager

def namespace_manager_default_namespace_for_request():
    #namespace_manager.set_name
    return "pocket_juke"
