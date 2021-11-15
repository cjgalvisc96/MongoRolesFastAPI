users_error_messages = dict(
    user_with_email_already_exists=(
        "User with email <<{email}>> already exists"
    ),
    user_not_exists="User with id <<{user_id}>> not exists",
    error_to_remove_user="User with id <<{user_id}>> can not removed",
    created_user_open_not_allowed=(
        "Open user registration is forbidden on this server"
    ),
    inactive_user="Inactive user",
    invalid_format_user_id="user_id <<{user_id}>> invalid format",
)

user_roles_error_messages = dict(
    user_roles_already_exists_for_user=(
        "User with id <<{user_id}>> already has been assigned a role"
    ),
    invalid_assigned_user_role=(
        "There is no role assigned to this user with id <<{user_id}>>"
    ),
)

account_error_messages = dict(
    account_with_name_already_exists=(
        "An account with name <<{name}>> already exists"
    ),
    account_not_exists="Account with id <<{account_id}>> not exists",
)

authentication_error_messages = dict(
    error_to_validate_credentials="Could not validate credentials",
    not_enough_permissions="Not enough permissions",
    incorrect_credentials="Incorrect email or password",
)
