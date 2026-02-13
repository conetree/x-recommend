from fastapi import FastAPI
from confluent_kafka import Producer
import json

from .config import settings
from .schemas import EventIn, FeedResponse
from .clients import GorseClient, FaissClient
from .recommender import FeedMixer

app = FastAPI(title="video-feed-api", version="0.1.0")

producer = Producer({"bootstrap.servers": settings.kafka_bootstrap_servers})
gorse = GorseClient(settings.gorse_server_url, settings.gorse_api_key)
faiss = FaissClient(settings.faiss_recall_url)
mixer = FeedMixer()


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/events")
def ingest_event(event: EventIn):
    payload = event.model_dump_json().encode("utf-8")
    producer.produce(settings.kafka_topic_events, payload)
    producer.poll(0)
    return {"accepted": True}


@app.get("/feed/{user_id}", response_model=FeedResponse)
async def get_feed(user_id: str, scene: str = "feed", size: int = 20, debug: bool = False):
    gorse_items = await gorse.get_user_recommend(user_id, n=max(size * 3, 60))
    faiss_items = await faiss.get_user_recall(user_id, n=max(size * 4, 80))

    merged = mixer.merge_and_rerank(gorse_items, faiss_items, size=size)

    return {
        "user_id": user_id,
        "scene": scene,
        "size": size,
        "items": merged,
        "debug": {
            "gorse_candidates": len(gorse_items),
            "faiss_candidates": len(faiss_items),
        } if debug else None,
    }
