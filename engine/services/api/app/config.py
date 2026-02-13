from pydantic import BaseModel
import os


class Settings(BaseModel):
    gorse_server_url: str = os.getenv("GORSE_SERVER_URL", "http://localhost:8087")
    gorse_api_key: str = os.getenv("GORSE_API_KEY", "")
    faiss_recall_url: str = os.getenv("FAISS_RECALL_URL", "http://localhost:8091")

    kafka_bootstrap_servers: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    kafka_topic_events: str = os.getenv("KAFKA_TOPIC_EVENTS", "video_events")

    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")


settings = Settings()
