from unittest import TestCase

from Models import BaseModel, Campaign, Chain, TaskStage


class TestModels(TestCase):
	def setUp(self):
		self.campaign = Campaign(name="Testing campaign", managers=[6])
		self.campaign.create_instance()

	def test_set_data_function(self):
		data = {"name": "campaign", "description": "newdesc", "managers": [12, 123, 23]}
		campaign = Campaign(**data)
		data_post = campaign.set_data()
		self.assertEqual(data, data_post)

	def test_create(self):
		self.assertNotEqual(type(self.campaign.id), type(None))
		self.assertEqual(self.campaign.name, "Testing campaign")

	def test_update(self):
		self.campaign.name = "NEW NAME"
		self.campaign.update()
		self.assertEqual(self.campaign.name, "NEW NAME")

	def test_get(self):
		self.campaign.get()
		default_attributes = ["id", "data", "name", "description", "managers", "endpoint", "rest_api", "headers"]
		for i in self.campaign.__dict__:
			self.assertIn(i, default_attributes)

	def test_create_chain(self):
		chain = Chain(name="my chain", campaign=self.campaign)
		chain.create_instance()
		init_stage = chain.create_init_stage()
		second_stage = TaskStage(chain, name="Second stage")
		second_stage.create_instance()

		third_stage = TaskStage(chain, name="Third stage")
		third_stage.create_instance()

		closing_stage = TaskStage(chain, name="Closing stage")
		closing_stage.create_instance()

		init_stage.add_in_stage(second_stage) \
			.add_in_stage(third_stage) \
			.add_in_stage(closing_stage)

		self.assertEqual(init_stage.in_stages, [second_stage.id])
		self.assertEqual(second_stage.in_stages, [third_stage.id])
		self.assertEqual(third_stage.in_stages, [closing_stage.id])
		self.assertEqual(third_stage.in_stages, [])
