from fastapi import FastAPI
import numpy as np
import faiss

app = FastAPI(title="faiss-recall", version="0.1.0")

DIM = 64
N_ITEMS = 5000
RNG = np.random.default_rng(42)

# mock item embedding
item_ids = np.array([f"v_{100000+i}" for i in range(N_ITEMS)])
item_vecs = RNG.normal(size=(N_ITEMS, DIM)).astype("float32")
faiss.normalize_L2(item_vecs)

index = faiss.IndexFlatIP(DIM)
index.add(item_vecs)


def fake_user_vec(user_id: str) -> np.ndarray:
    # 仅用于基础演示：按 user_id 生成稳定向量
    seed = abs(hash(user_id)) % (2**32)
    rng = np.random.default_rng(seed)
    v = rng.normal(size=(DIM,)).astype("float32")
    v = v.reshape(1, -1)
    faiss.normalize_L2(v)
    return v


@app.get("/health")
def health():
    return {"ok": True, "items": N_ITEMS, "dim": DIM}


@app.get("/recall/user/{user_id}")
def recall_for_user(user_id: str, n: int = 100):
    q = fake_user_vec(user_id)
    scores, idxs = index.search(q, n)

    result = []
    for score, idx in zip(scores[0], idxs[0]):
        result.append({"item_id": str(item_ids[idx]), "score": float(score)})

    return {"user_id": user_id, "items": result}
