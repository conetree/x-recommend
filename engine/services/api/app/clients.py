from __future__ import annotations

from typing import List, Dict, Any
import httpx


class GorseClient:
    def __init__(self, base_url: str, api_key: str = ""):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    @property
    def _headers(self):
        if not self.api_key:
            return {}
        return {"X-API-Key": self.api_key}

    async def get_user_recommend(self, user_id: str, n: int = 50) -> List[str]:
        # 说明：不同 gorse 版本接口可能有细节差异，这里用最常见 REST 形态做基础适配。
        url = f"{self.base_url}/api/recommend/{user_id}"
        params = {"n": n}
        async with httpx.AsyncClient(timeout=3.0) as client:
            try:
                r = await client.get(url, params=params, headers=self._headers)
                r.raise_for_status()
                data = r.json()
                if isinstance(data, list):
                    return [str(x) for x in data]
                if isinstance(data, dict) and "data" in data:
                    return [str(x) for x in data["data"]]
            except Exception:
                return []
        return []


class FaissClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    async def get_user_recall(self, user_id: str, n: int = 100) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/recall/user/{user_id}"
        async with httpx.AsyncClient(timeout=3.0) as client:
            try:
                r = await client.get(url, params={"n": n})
                r.raise_for_status()
                data = r.json()
                return data.get("items", [])
            except Exception:
                return []
