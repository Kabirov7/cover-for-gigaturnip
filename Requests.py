import requests
import json
from token111 import token


class Requests():
	rest_api = "http://127.0.0.1:8000/api/v1/"
	headers = {
		"Authorization": f"JWT {token}"}
	id = None
	endpoint = None
	data = None

	def post_request(self, url, data):
		response = requests.post(self.rest_api + url, data=data, headers=self.headers)
		print(response.status_code)
		return response

	def get_request(self, url, data=None):
		if not data:
			data = ''
		response = requests.get(self.rest_api + url, data=data, headers=self.headers)
		print(response.status_code)
		return response

	def patch_request(self, url, data):
		response = requests.patch(self.rest_api + url, data=data, headers=self.headers)
		print(response.status_code)
		return response

	def delete_request(self, url):
		response = requests.delete(url)
		print(response.status_code)
		return response

	def create_instance(self):
		self.set_data()
		response = json.loads(self.post_request(self.endpoint, data=self.data).content)
		self.id = response.get('id')
		self.get()

	def update(self):
		self.set_data()
		response = json.loads(self.patch_request(f"{self.endpoint}{self.id}/", data=self.data).content)
		self.id = response.get('id')
		self.get()

	def get(self):
		response = self.get_request(f"{self.endpoint}{self.id}")
		for key in json.loads(response.content):
			setattr(self, key, json.loads(response.content)[key])
		return self

	def get_all(self, params=''):
		response = self.get_request(self.endpoint, data=params)
		return json.loads(response.content)['results']

	def get_by_id(self, id):
		self.id = id
		self.get()

	def set_data(self):
		data = {}
		for i in list(self.__dict__.items()):
			if i[0] not in ["rest_api", "headers", "endpoint", "data"]:
				i = list(i)
				if i[1].__class__.__module__ != 'builtins':
					i[1] = i[1].id
				data[i[0]] = i[1]
		self.data = data
		return data
