from flask_jwt_extended import create_access_token, create_refresh_token


class TokenService:

    @staticmethod
    def generate_tokens(payload):
        access_token = create_access_token(identity=payload)
        refresh_token = create_refresh_token(identity=payload)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
