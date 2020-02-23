### Testing with Django REST Framework

#### Create a JSON POST request with factory
_factory_ contains `.get()`, `.post()`, `.put()`, `.patch()`, `.delete()`, `.head()` and `.options()` _methods_
```python
from rest_framework.test import APIClient, APIRequestFactory
factory = APIRequestFactory()
```
##### Format  Arg:
`post,put,patch` methods include a `format` arg: `multipart` is _default_, `json` is available
```python
request = factory.post('/notes/', {'title': 'new idea'}, format='json')
```

##### Explicitly encoding request body
use of `content_type` flag
```python
import json
request = factory.post('/notes/', json.dumps({'title': 'new idea'}), content_type='application/json')
```

##### Forcing authentication
When testing views directly using a request factory, it's oftern convenient to be able to directly authenticate the req-
uest, rather than having to construct the correct authentication credentials.
To forcibly authenticate a request, use the `force_authenticate()` method.
```python
from rest_framework.test import force_authenticate
factory = APIRequestFactory()
user = User.objects.get(username='testuser')
view = AccountDetail.as_view()

# Make an authenticated request to the view...
request = factory.get('/users/')
force_authenticate(request, user=user)
response = view(request)
```
The signature for the method is `force_authenticate(request, user=None, token=None`. When making the call , either or both
of the user and token may be set.

For example, when forcibly authenticating using a token, you might do something like the following:
```python
user = User.objects.get(username='testuser')
request = factory.get('/users/')
force_authenticate(request, user=user, token=user.auth_token)
```
**Note:** `force_authenticate` directly sets `request.user` to the in-memory `user` instance. If you are re-using the same
`user` instance across multiple tests that update the saved `user` state, you may need to call refresh_from_db() between tests.

##### Forcing CSRF validation
By default, requests created with `APIRequestFactory` will not have CSRF validation applied when passed to a REST framework
view. If you need to explicitly turn CSRF validation on, you can do so by setting the enforce_csrf_checks flag when instantiating
the factory.
```python
factory = APIReuestFactory(enforce_csrf_checks=True)
```
**Note:** It's worth noting that Django's standard RequestFactory doesn't need to include this option, because when using
regular Django the CSRF validation takes place in middleware, which is not run when testing views directly. When using REST
framework, CSRF validation takes place inside the view, so the request factory needs to disable view-level CSRF checks.

#### APIClient
Extends **Django's existing `Client` class**
##### Making Requests
The `APIClient` class supports the same request interface as Django's standart Client class. This means that the standard
.get(), .post(), .put(), .pathch(), .delete(), .head(), and .options() methods are available. For example:
```python
from rest_framework.test import APIClient
client = APIClient()
client.post('/notes/', {'title': 'new idea'}, format='json')
```

##### Authenticating
###### .login(**kwargs)
Then `login` method functions exactly as it does with Django's regular `Client` class. This allows you to authenticate requests
against any views which include `SessionAuthentication`
```python
client = APIClient()
client.login(username='testuser', 'password'='secret')
```
To logout, call the `logout` method as usual.
```python
client.logout()
```
The `login` method is appropriate for testing APIs that use session authentication, for example websites which include AJAX
interaction with the API.
###### .credentials(,,kwargs)
The `credentials` method can be used to set headers that will then be included on all subsequent requests by the test client.
```python
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

token = Token.objects.get(user__username='testuser')
client = APIClient()
client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
```
Note that calling `credentials` a second time overwrites any existing credentials. You can unset any exisiting credentials
by calling the method with no arguments.
```python
# stop including any credentials
client.credentials()
```
The `credentials` method is appropriate for testing APIs that require authentication headers, such as basic authentication,
OAuth2 and simple other token authentication schemes.
- force_authenticate(user=None, token=None)
Sometimes you may want to bypass authentication entirely and force all requests by the test client to be automatically treated
as authenticated.
This can be a useful shortcut if you're testing the API but don't want t have to construct valid authentication credentials in
order to make test requests.
```python
user = User.objects.get(username='testuser')
client = APIClient()
client.force_authenticate(user=user)
```
To unauthenticate subsequent requests, call `force_authenticate` setting the user and/or token to `None`.

```python
client.force_authenticate(user=None)
```
##### CSRF validation
By default CSRF validation is not applied when using APIClient. If you need to explicitly enable CSRF validation, you can
do so by setting the enforce_csrf_checks flag when instantiating the client.
```python
client = APIClient(enforce_csrf_checks=True)
```
As usual CSRF validation will only apply to any session authenticated views. This means CSRF validation will only occur if
the client has been logged in by calling `login()`.
#### Other REST Framework Test Clients
- RequestsClient uses `requests`
- CoreAPIClient uses `coreapi`

#### API Test cases
REST framework includes the following test case classes, that mirror the existing Django test case classes, but use 
`APIClient` instead of Django's default `Client`.
- `APISimpleTestCase`
- `APITransactionTestCase`
- `APITestCase`
- `APILiveServerTestCase`

##### Example
You can use any of Rest framework's test case classes as you would for the regular `Django` test case classes. The `self.client` attribute will be an `APIClient` instance.
```python
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class UserTests(APITestCase):
    def test_create_user(self):
        """
        Ensure we can create a new user object
        """
        url = reverse('user')
        data = {'username': 'testuser', 'password': 'secret'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
```
##### Testing responses
###### Checking the response data
When checking the validity of test responses it's often more convenient to inspect the data that the response was created
with, rather than inspecting the fully rendered response.

For example, it's easier to inspect response.data:
```python
response = self.client.get('/users/4/')
self.assertEqual(response.data, {'id': 4, 'username': 'testuser'})
```
Instead of inspecting the result of parsing response.content:
```python
response = self.client.get('/users/4/')
self.assertEqual(json.loads(response.content), {'id': 4, 'username': 'testuser'})
```
###### Rendering responses
If you're testing views directly using `APIRequestFactory`, the responses that are returned will not yet be rendered, as
rendering  of template responses is performed by Django's internal request-response cycle. In order to access `response.content`,
you'll first need to render the response.
```python
view = UserDetail.as_view()
request = factory.get('/users/4/')
response = view(request, pk=4)
response.render() # cannot access response.content without this
self.assertEqual(response.content, '{"username":"testuser", "id": 4}')
```

##### Configuration
###### Setting the default format
The default format used to make test requests may be set using the `TEST_REQUEST_DEFAULT_FORMAT` setting key. For example,
to always use JSON for test requests by default instead of standard multipart form requests, set the following in your settings.py
file:
```python
REST_FRAMEWORK = {
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}
```
###### Setting the available formats
If you need to test requests using something other than multipart or json requests, you can do so by setting the
`TEST_REQUEST_RENDERER_CLASSES` setting.
For example, to add support for using format='html' in test requests, you might have something like this in your settings.py file.
```python
REST_FRAMEWORK = {
    ...
    'TEST_REQUEST_DEFAULT_CLASSES': [
        'rest_framework.renderers.MultiPartRenderer',
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.TemplateHTMLRenderer'
    ]
}
```






