users_error_messages = dict(
    user_with_email_already_exists=(
        "User with email <<{email}>> already exists"
    ),
    user_not_exists="User wit id <<{user_id}>> not exists",
    error_to_remove_user="User with id <<{user_id}>> can not removed",
    created_user_open_not_allowed=(
        "Open user registration is forbidden on this server"
    ),
)

user_roles_error_messages = dict(
    user_roles_already_exists_for_user=(
        "User with id <<{user_id}>> already has been assigned a role"
    ),
    invalid_assigned_user_role=(
        "There is no role assigned to this user with id <<{user_id}>>"
    ),
)
