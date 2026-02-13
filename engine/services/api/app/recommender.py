from collections import defaultdict
from typing import List, Dict


class FeedMixer:
    """融合 gorse + faiss 的简易重排器（MVP）"""

    def merge_and_rerank(
        self,
        gorse_items: List[str],
        faiss_items: List[Dict],
        size: int,
    ):
        pool = defaultdict(lambda: {"score": 0.0, "sources": set()})

        # 1) gorse 候选打分（位置衰减）
        for idx, item_id in enumerate(gorse_items):
            pool[item_id]["score"] += 1.0 / (1 + idx)
            pool[item_id]["sources"].add("gorse")

        # 2) faiss 候选打分（按相似度）
        for idx, it in enumerate(faiss_items):
            item_id = str(it.get("item_id"))
            sim = float(it.get("score", 0.0))
            pool[item_id]["score"] += 0.8 * sim + 0.1 / (1 + idx)
            pool[item_id]["sources"].add("faiss")

        # 3) 简易多样性：避免同源连续过多（这里只做来源平衡占位）
        ranked = sorted(pool.items(), key=lambda x: x[1]["score"], reverse=True)

        result = []
        for item_id, info in ranked[: size * 2]:
            result.append(
                {
                    "item_id": item_id,
                    "score": round(info["score"], 6),
                    "sources": sorted(list(info["sources"])),
                }
            )
            if len(result) >= size:
                break
        return result
