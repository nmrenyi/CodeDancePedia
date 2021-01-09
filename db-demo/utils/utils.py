"""
Some utilized function of django backend
"""
from manage_user.models import User


def check_user_id(user_id):
    """
    Check type of user_id valid
    """
    if isinstance(user_id, int):
        return True
    if isinstance(user_id, str):
        if not user_id:
            return False
        if not user_id.isdigit():
            return False
        return True
    return False


def get_user(user_id):
    """
    Get user by user_id
    """
    if check_user_id(user_id):
        user = User.objects.filter(pk=user_id).first()
        return user
    return None
