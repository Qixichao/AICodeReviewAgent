from utils import postgre


def search_components_from_db(component) -> list:
    related_components = []
    dboperation = postgre.DBOperation()
    related_components = dboperation.get_component_list(component)
    return related_components
