from typing import Dict, List


def check_if_element_exists_in_list(*, _list: List, _conditions: Dict) -> bool:
    def check_conditions(element) -> bool:
        for field, expected_value in _conditions.items():
            if element[field] != expected_value:
                return False
        return True

    element_exists_in_list = False
    try:
        element_exists_in_list = next(
            element for element in _list if check_conditions(element)
        )
    except StopIteration:
        return True
    except Exception:
        return False
    finally:
        return element_exists_in_list
