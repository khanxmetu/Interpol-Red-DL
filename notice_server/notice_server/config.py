import os

class Config:
    def __init__(
        self,
        db_host=None,
        db_port=None,
        db_name=None,
        queue_name=None,
        broker_host=None,
        broker_port=None
    ):
        self.DB_HOST: str = db_host or "localhost"
        self.DB_PORT: int = int(db_port or 27017)
        self.DB_NAME: str = db_name or "notice-db"
        self.QUEUE_NAME: str = queue_name or "fetched_notices"
        self.BROKER_HOST: str = broker_host or "localhost"
        self.BROKER_PORT: int = int(broker_port or 5672)
    
    @classmethod
    def load_from_env(cls):
        return cls(
            db_host = os.getenv("DB_HOST"),
            db_port = os.getenv("DB_PORT"),
            db_name = os.getenv("DB_NAME"),
            queue_name=os.getenv("QUEUE_NAME"),
            broker_host = os.getenv("RABBITMQ_HOST"),
            broker_port = os.getenv("RABBITMQ_PORT")
        )
