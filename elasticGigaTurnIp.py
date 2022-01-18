import json
from uuid import uuid4
import requests
from token import token

class GigaTurnIp():
	rest_api = "http://127.0.0.1:8000/api/v1/"

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

	def create_campaign(self, name="Campaign", desc="", managers=[]):
		data = {"name": name, "description": desc, "managers": managers}
		response = json.loads(self.post_request(url="campaigns/", data=data).content)
		return self.get_objects(f"campaigns/{response.get('id')}/")

	def create_chain(self, campaign_id):
		data = {"name": "Init chain", "description": "", "campaign": campaign_id}
		response = json.loads(self.post_request(url="chains/", data=data).content)
		return self.get_objects(f"chains/{response.get('id')}/")

	def create_stage(self, chain_id, endpoint="taskstages",name="Initian task stage", kwargs=None):
		data = {
			"name": name,
			"x_pos": 1,
			"y_pos": 1,
			"chain": chain_id
		}
		if kwargs:
			data.update(kwargs)
		response = json.loads(self.post_request(url=f"{endpoint}/", data=data).content)
		return self.get_objects(f"{endpoint}/{response.get('id')}/")

	def create_rank(self, stage_id):
		data = {"name": stage_id, "description": ""}
		response = json.loads(self.post_request(url="ranks/", data=data).content)
		return self.get_objects(f"ranks/{response.get('id')}/")

	def create_rank_limit(self, rank_id, stage_id):
		data = {
			"rank": rank_id,
			"stage": stage_id,
			"open_limit": 0,
			"total_limit": 0,
			"is_listing_allowed": True,
			"is_creation_open": False,
		}
		response = json.loads(self.post_request(url="ranklimits/", data=data).content)
		return self.get_objects(f"ranklimits/{response.get('id')}/")

	def create_rank_record(self, rank_id, user_id):
		data = { "rank":rank_id, "user":user_id}
		response = json.loads(self.post_request("rankrecords/", data=data))
		return self.get_objects(f"rankrecords/{response.get('id')}/")

	def create_task(self, stage_id):
		response = json.loads(self.get_request(f'taskstages/{stage_id}/create_task/'))
		return self.get_objects(f'tasks/{response.get("id")}/')

	def update_task_responses(self, task_id, responses):
		data = {"responses": responses}
		response = self.patch_request(f"tasks/{task_id}/", data)
		return self.get_objects(f"tasks/{response.get('id')}/")

	def complete_task(self, task_id, responses=None):
		data = responses
		if not data:
			data = {"complete": True}
		else:
			data = {"complete": True, "responses": responses}
		response = self.patch_request(f'tasks/{task_id}/', data)
		return self.get_objects(f'tasks/{response.get("id")}/')

	def request_assignment(self, task_id):
		url = f'tasks/{task_id}/request_assignment/'
		response = self.get_request(url)
		return self.get_objects(f'tasks/{response.get("id")}/')

	def add_stages(self, stage_id, name="task", stages=[]):
		if name == "task":
			data = {"in_stages": stages}
			url = "taskstages/"
		elif name == "cond":
			data = {"out_stages": stages}
			url = "conditionalstages/"
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
dd = giga.get_request("campaigns/")
print(dd)
