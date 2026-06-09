from .tokens import sign_token, verify_token

# Simplified auth helpers

def create_user_token(user_id: str):
    return sign_token(user_id)


def validate_token(token: str):
    return verify_token(token)
