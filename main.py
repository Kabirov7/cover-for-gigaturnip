from Models import BaseModel
from Models import Campaign
from Models import Chain
from Models import ConditionalStage
from Models import Rank
from Models import RankLimit
from Models import RankRecord
from Models import Stage
from Models import Task
from Models import TaskStage
from Models import Track

campaign = Campaign(name="Khakim campaign")
campaign.create_instance()
campaign.name="Khakim new"
campaign.update()

chain = campaign.create_new_chain(Chain("Khakim new chain"))
init_stage = chain.create_init_stage()

middle_stage = TaskStage(chain, name="cook Plov")
middle_stage.create_instance()

init_stage.add_in_stage(middle_stage)

rank = Rank()