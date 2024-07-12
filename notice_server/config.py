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
        self.DB_PORT: int = db_port or 27017
        self.DB_NAME: str = db_name or "notice-db"
        self.QUEUE_NAME: str = queue_name or "fetched_notices"
        self.BROKER_HOST: str = broker_host or "localhost"
        self.BROKER_PORT: int = broker_port or 5672