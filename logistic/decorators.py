def employee_required(user):
    return user.is_employee or user.is_staff

def shopowner_required(user):
    return user.is_shopowner or user.is_staff