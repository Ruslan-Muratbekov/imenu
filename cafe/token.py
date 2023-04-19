from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_cafe(user):
	refresh = RefreshToken.for_user(user)

	return str(refresh.access_token)
