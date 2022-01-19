from Requests import Requests
import json

class BaseModel():
	def __init__(self, name, description):
		self.name = name
		self.description = description


class Campaign(BaseModel, Requests):

	def __init__(self, name='', description='', managers=[]):
		self.managers = managers
		super().__init__(name, description)
		self.endpoint = 'campaigns/'

	def create_new_chain(self, chain):
		chain.campaign = self
		chain.create_instance()
		return chain


class Chain(BaseModel, Requests):
	def __init__(self, name='', description='', campaign=None):
		self.campaign = campaign
		self.endpoint = "chains/"
		super().__init__(name, description)

	def create_init_stage(self):
		stage = TaskStage(self.id, "Initial Task Stage")
		stage.create_instance()
		return stage


class Stage(Requests):

	def __init__(self, name, desc, chain, in_stages, x=1, y=1):
		self.chain = chain
		self.in_stages = in_stages
		self.name = name
		self.description = desc
		self.x_pos = x
		self.y_pos = y

	def add_stage(self, stage):
		self.get()
		if stage.id not in self.in_stages:
			self.in_stages += [stage.id]

		data = {
			"id": self.id,
			"in_stages": self.in_stages
		}
		response = self.patch_request(f"{self.endpoint}{self.id}/", data)
		if response.status_code != 200:
			self.get()
		return stage


class TaskStage(Stage, Requests):
	def __init__(self, chain=None, name="Task Stage", desc='', in_stages=[], rich_text=None,
				 copy_input=False,
				 allow_multiple_files=False,
				 is_creatable=False,
				 displayed_prev_stages=None,
				 assign_user_by="RA",
				 assign_user_from_stage=None,
				 allow_go_back=False,
				 allow_release=False,
				 is_public=False,
				 webhook_address=None,
				 webhook_payload_field=None,
				 webhook_params=None,
				 webhook_response_field=None):
		self.rich_text = rich_text
		self.copy_input = copy_input
		self.allow_multiple_files = allow_multiple_files
		self.is_creatable = is_creatable
		self.displayed_prev_stages = displayed_prev_stages
		self.assign_user_by = assign_user_by
		self.assign_user_from_stage = assign_user_from_stage
		self.allow_go_back = allow_go_back
		self.allow_release = allow_release
		self.is_public = is_public
		self.webhook_address = webhook_address
		self.webhook_payload_field = webhook_payload_field
		self.webhook_params = webhook_params
		self.webhook_response_field = webhook_response_field
		self.endpoint = "taskstages/"
		super().__init__(name, desc, chain, in_stages)


class ConditionalStage(Stage, Requests):
	def __init__(self, chain, name="Conditional Stage", desc='', in_stages=[], conditions=None, pingpong=False):
		self.conditions = conditions
		self.pingpong = pingpong
		self.endpoint = "conditionalstages/"
		super().__init__(name, desc, chain, in_stages)


class Rank(BaseModel):

	def __init__(self, stages, track=None):
		self.stages = stages
		self.track = track


class RankLimit():

	def __init__(self, rank=Rank, stage=Stage, open_limit=0,
				 total_limit=0,
				 is_listing_allowed=False,
				 is_submission_open=True,
				 is_selection_open=True,
				 is_creation_open=True):
		self.rank = rank
		self.stage = stage
		self.open_limit = open_limit
		self.total_limit = total_limit
		self.is_listing_allowed = is_listing_allowed
		self.is_submission_open = is_submission_open
		self.is_selection_open = is_selection_open
		self.is_creation_open = is_creation_open


class RankRecord():
	def __init__(self, user, rank=None):
		self.user = user
		self.rank = rank


class Task(Requests):

	def __init__(self, stage, assignee=None,
				 case=None,
				 responses=None,
				 in_tasks=None,
				 integrator_group=None,
				 complete=False,
				 force_complete=False,
				 reopened=False):
		self.stage = stage
		self.assignee = assignee
		self.case = case
		self.responses = responses
		self.in_tasks = in_tasks
		self.integrator_group = integrator_group
		self.complete = complete
		self.force_complete = force_complete
		self.reopened = reopened
		self.endpoint = "tasks/"

	def create_task(self, stage):
		response = json.loads(self.get_request(f'taskstages/{stage.id}/create_task/'))
		self.id = response.get('id')
		return self.get()

	def complete_task(self):
		if self.responses:
			args = {"complete": True, "responses": self.responses}
		else:
			args = {"complete": True}
		response = self.patch_request(f'tasks/{self.id}/', data=args)
		return self.get()

	def request_assignment(self):
		self.get_request(f'{self.endpoint}{self.id}/request_assignment/')
		return self.get()


class Track(BaseModel):

	def __init__(self, campaign=Campaign):
		self.campaign = campaign
		self.default_rank = Rank

