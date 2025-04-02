from auth import Auth
import requests

class Services:
    def __init__(self, auth_instance=None):
        self.auth = auth_instance if auth_instance else Auth()

    def _get_headers(self):
        token = self.auth.token
        if not token:
            print("You are not logged in! Please log in first.")
            return None
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def _handle_response(self, response):
        if 200 <= response.status_code < 300:
            try:
                return response.json()
            except ValueError:
                return response.text
        else:
            print(f"Request failed with status code: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error details: {error_data}")
            except ValueError:
                print(f"Error details: {response.text}")
            return response.status_code

    def request(self, method, url, data=None, headers=None):
        base_headers = self._get_headers()
        if base_headers is None:
            return None
        final_headers = base_headers.copy()
        if headers:
            final_headers.update(headers)
        try:
            response = requests.request(method, url, json=data, headers=final_headers)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None

    def get(self, url, headers=None):
        return self.request("get", url, headers=headers)

    def post(self, url, data=None, headers=None):
        return self.request("post", url, data=data, headers=headers)

    def put(self, url, data=None, headers=None):
        return self.request("put", url, data=data, headers=headers)

    def delete(self, url, headers=None):
        return self.request("delete", url, headers=headers)