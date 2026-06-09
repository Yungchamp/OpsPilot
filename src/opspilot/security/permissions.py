def requires_role(user_role: str, allowed: list[str]) -> bool:
    return user_role in allowed
