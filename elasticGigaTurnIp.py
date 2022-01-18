import json
from uuid import uuid4
import requests
from token import token

class GigaTurnIp():
	rest_api = "http://127.0.0.1:8000/"

	def __init__(self, headers):
		self.headers = headers

	def post_request(self, url, data):
		return requests.post(self.rest_api + url, data=data, headers=self.headers)

	def get_request(self, url, data=None):
		if not data:
			data = ''
		return requests.get(self.rest_api + url, data=data, headers=self.headers)

	def patch_request(self, url, data):
		return requests.patch(self.rest_api + url, data=data, headers=self.headers)

	def delete_request(self, url):
		return requests.delete(url)

	def get_objects(self, url, params=None):
		data = params
		if not data:
			data = ''
		return json.loads(self.get_request(url, data=data).content)

	def create_campaign(self):
		data = {"name": "Initial campaign", "description": "", "managers": []}
		response = json.loads(self.post_request(url="api/v1/campaigns/", data=data).content)
		return self.get_objects(f"api/v1/campaigns/{response.get('id')}/")

	def create_chain(self, campaign_id):
		data = {"name": "Init chain", "description": "", "campaign": campaign_id}
		response = json.loads(self.post_request(url="api/v1/chains/", data=data).content)
		return self.get_objects(f"api/v1/chains/{response.get('id')}/")

	def create_task_stage(self, chain_id):
		data = {
			"name": "Initial",
			"x_pos": 1,
			"y_pos": 1,
			"chain": chain_id
		}
		response = json.loads(self.post_request(url="api/v1/taskstages/", data=data).content)
		return self.get_objects(f"api/v1/taskstages/{response.get('id')}/")

	def create_rank(self, stage_id):
		data = {"name": stage_id, "description": ""}
		response = json.loads(self.post_request(url="api/v1/ranks/", data=data).content)
		return self.get_objects(f"api/v1/ranks/{response.get('id')}/")

	def create_rank_limit(self, rank_id, stage_id):
		data = {
			"rank": rank_id,
			"stage": stage_id,
			"open_limit": 0,
			"total_limit": 0,
			"is_listing_allowed": True,
			"is_creation_open": False,
		}
		response = json.loads(self.post_request(url="api/v1/ranklimits/", data=data).content)
		return self.get_objects(f"api/v1/ranklimits/{response.get('id')}/")

	def create_task(self, stage_id):
		response = json.loads(self.get_request(f'api/v1/taskstages/{stage_id}/create_task/'))
		return self.get_objects(f'api/v1/tasks/{response.get("id")}/')

	def update_task_responses(self, task_id, responses):
		data = {"responses": responses}
		response = self.patch_request(f"api/v1/tasks/{task_id}/", data)
		return self.get_objects(f"api/v1/tasks/{response.get('id')}/")

	def complete_task(self, task_id, responses=None):
		data = responses
		if not data:
			data = {"complete": True}
		else:
			data = {"complete": True, "responses": responses}
		response = self.patch_request(f'api/v1/tasks/{task_id}/', data)
		return self.get_objects(f'api/v1/tasks/{response.get("id")}/')

	def request_assignment(self, task_id):
		url = f'api/v1/tasks/{task_id}/request_assignment/'
		response = self.get_request(url)
		return self.get_objects(f'api/v1/tasks/{response.get("id")}/')

	def add_stages(self, stage_id, name="task", stages=[]):
		if name == "task":
			data = {"in_stages": stages}
			url = "api/v1/taskstages/"
		elif name == "cond":
			data = {"out_stages": stages}
			url = "api/v1/conditionalstages/"
		response = self.patch_request(f"{url}{stage_id}/", data)
		return self.get_objects(f"{url}{response.get('id')}/")


# def create_rank_record(self):


headers = {
	"Authorization": f"JWT {token}"}

giga = GigaTurnIp(headers)
# data = {
# 	"name": "Initial campaign",
# 	"description": "desc",
# }
# dd = giga.post_request("api/v1/campaigns/", data)
dd = giga.get_request("api/v1/campaigns/")
print(dd)
