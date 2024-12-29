# from rest_framework.views import exception_handler
# from rest_framework.response import Response
# from rest_framework import status

# def custom_exception_handler(exc, context):
#     # Call DRF's default exception handler first
#     response = exception_handler(exc, context)

#     if response is not None:
#         if response.status_code == status.HTTP_401_UNAUTHORIZED:
#             response.data['detail'] = "Authentication credentials were not provided. Please include a valid 'Bearer <token>' in the Authorization header."
#         elif response.status_code == status.HTTP_403_FORBIDDEN:
#             response.data['detail'] = "You do not have permission to perform this action."
#         elif response.status_code == status.HTTP_400_BAD_REQUEST and 'token' in str(exc).lower():
#             response.data['detail'] = "The provided token is invalid or expired. Please log in again."

#     return response

from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None and response.status_code == 400:
        response.data['required_fields'] = ['email', 'first_name', 'last_name', 'password']

    return response
