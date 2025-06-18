
from ..bd.repositories.TopicRepository import TopicRepository
from ..bd.repositories.CategoryRepository import CategoryRepository
from sqlalchemy.orm import Session
from app.services.topic_services.CreateTopics import CreateTopic
from app.services.topic_services.GetTopics import GetTopics
from app.services.topic_services.DeleteTopic import DeleteTopic
from app.services.topic_services.GetTopicsCategory import GetTopicsCategory
from app.bd.schemas import schema_topic

class TopicController:

    def __init__(self, db:Session):
        self.db = db
        self.topicR = TopicRepository(db)
        self.categoryR = CategoryRepository(db)


    def createTopic(self, topicS: schema_topic.TopicCreate):
        return CreateTopic.run(
            db= self.db,
            topicS= topicS,
            categoryR = self.categoryR,
            topicR = self.topicR
        )

    def getTopics(self):
        return GetTopics.run(
            db= self.db,
            topicR = self.topicR
        )
    
    def deleteTopic(self, topic_name: str):
        return DeleteTopic.run(
            db= self.db,
            topic_name= topic_name,
            topicR= self.topicR
        )

    def getTopicsCategory(self, category_name):
        return GetTopicsCategory.run(
            db = self.db,
            category_name = category_name,
            topicR = self.topicR
        )