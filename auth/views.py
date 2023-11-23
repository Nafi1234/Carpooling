import requests
from django.http import JsonResponse

def get_access_token(request):
    client_id = '33OkryzDZsJlL2wXmJNfiUi7Bc9uJhiB8VmqMDQeHMXANwWcIxZlVf-ODzZAqF7Zpfkq8WrKn4jr_3AMsCCaCQ=='
    client_secret = 'lrFxI-iSEg8g0nroFDIZ6x-MdUwfX_xboh3uEkf6EzAk9fXIe5p0lAtCosLltWuFdj5sNnIEWGgiN7l-c6BMmDi8DsB6k48L'
    token_generation_url = 'https://outpost.mappls.com/api/security/oauth/token'

    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    }

    try:
        response = requests.post(token_generation_url, data=data)
    
        if response.status_code == 200:
            response_data = response.json()
            access_token = response_data.get('access_token')
            token_type = response_data.get('token_type')
            return JsonResponse({'access_token': access_token, 'token_type': token_type})
        else:
            print("yes")
            return JsonResponse({'error': 'Failed to obtain the access token'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
