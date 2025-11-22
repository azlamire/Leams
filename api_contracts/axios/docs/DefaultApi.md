# DefaultApi

All URIs are relative to *http://localhost:3000*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**authGithubPost**](#authgithubpost) | **POST** /auth/github | |
|[**mainVideosCategoriesGet**](#mainvideoscategoriesget) | **GET** /main/videos/categories | |
|[**registerPost**](#registerpost) | **POST** /register | |

# **authGithubPost**
> AuthGithubPost200Response authGithubPost()

API for generating and sending GitHub token to sign via this one

### Example

```typescript
import {
    DefaultApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new DefaultApi(configuration);

let clientId: string; //Client Id of github (default to undefined)
let redierectUri: string; //Where user will redierected (default to undefined)
let responseType: Code; //What type of response will be got (default to undefined)
let scope: Array<string>; //Which permissions will be granted to user (default to undefined)

const { status, data } = await apiInstance.authGithubPost(
    clientId,
    redierectUri,
    responseType,
    scope
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **clientId** | [**string**] | Client Id of github | defaults to undefined|
| **redierectUri** | [**string**] | Where user will redierected | defaults to undefined|
| **responseType** | **Code** | What type of response will be got | defaults to undefined|
| **scope** | **Array&lt;string&gt;** | Which permissions will be granted to user | defaults to undefined|


### Return type

**AuthGithubPost200Response**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **mainVideosCategoriesGet**
> mainVideosCategoriesGet()

Getting from backend(S3) videos via recommendations

### Example

```typescript
import {
    DefaultApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new DefaultApi(configuration);

let authorization: string; //value must be `Bearer <token>` where `<token>` is api key prefixed with cal_ (default to undefined)

const { status, data } = await apiInstance.mainVideosCategoriesGet(
    authorization
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **authorization** | [**string**] | value must be &#x60;Bearer &lt;token&gt;&#x60; where &#x60;&lt;token&gt;&#x60; is api key prefixed with cal_ | defaults to undefined|


### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **registerPost**
> RegisterPost200Response registerPost()

API for creating new user and after logging it after this

### Example

```typescript
import {
    DefaultApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new DefaultApi(configuration);

const { status, data } = await apiInstance.registerPost();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**RegisterPost200Response**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

