class BaseModel():
	def __init__(self, name, description):
		self.name = name
		self.description = description


class Campaign(BaseModel, Requests):

	def __init__(self, name='', description='', managers=[]):
		self.managers = managers
		super().__init__(name, description)
		self.endpoint = 'campaigns/'


class Chain(BaseModel, Requests):
	def __init__(self, name='', description='', campaign=None):
		self.campaign = campaign
		self.endpoint = "chains/"
		super().__init__(name, description)


class Stage(Requests):

	def __init__(self, chain, in_stages, x=1, y=1):
		self.chain = chain
		self.in_stages = in_stages
		self.x_pos = x
		self.y_pos = y


class TaskStage(Stage, Requests):
	def __init__(self, chain, in_stages, rich_text=None,
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
		super().__init__(chain, in_stages)


class ConditionalStage(Stage, Requests):
	def __init__(self, chain, in_stages, conditions=None, pingpong=False):
		self.conditions = conditions
		self.pingpong = pingpong
		super().__init__(chain, in_stages)


class Rank(BaseModel):
	# track = Track()

	def __init__(self, stages, track=Track):
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
	def __init__(self, user, rank=Rank()):
		self.user = user
		self.rank = rank


class Task():

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


class Track(BaseModel):

	def __init__(self, campaign=Campaign):
		self.campaign = campaign
		self.default_rank = Rank
