from app.utils.errors import handle_errors, MissingData, ValidationError, NotFound
from app.bd.schemas import schema_topic
from sqlalchemy.orm import Session
from app.models import Topic, Category
from app.bd.repositories.Repository import Repository
from fastapi.responses import JSONResponse
from fastapi import status

class CreateTopic:
    @handle_errors
    def run(
        db: Session,
        topicS: schema_topic.TopicCreate,
        categoryR : Repository[Category],
        topicR: Repository[Topic]
    ):  
        if topicS.topic_name == '' or topicS.category_name == '':
            raise ValueError('Insert void value')
        
        topicS.topic_name = topicS.topic_name.upper()
        topicS.category_name = topicS.category_name.upper()
        category = categoryR.get_by({'category_name': topicS.category_name})

        if len(category) == 0 :
            categoryR.create({'category_name':topicS.category_name})

        topicR.create({'topic_name':topicS.topic_name,
                       'category_name':topicS.category_name})

        db.commit()

        return JSONResponse(status_code= status.HTTP_201_CREATED, content='Topic Created')

