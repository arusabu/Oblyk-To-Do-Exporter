from typing import Any

import requests


class OblykClient:
    BASE_URL = "https://api.oblyk.org/api/v1"

    def __init__(
        self,
        api_access_token: str,
        bearer_token: str,
    ) -> None:
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "HttpApiAccessToken": api_access_token,
                "Authorization": f"Bearer {bearer_token}",
            }
        )

    def get_current_gym_routes(
        self,
        gym_id: int,
    ) -> list[dict[str, Any]]:
        routes: list[dict[str, Any]] = []
        page = 1

        while True:
            print(f"[INFO] Fetching gym routes page {page}...")

            response = self.session.get(
                f"{self.BASE_URL}/gyms/{gym_id}/gym_routes/paginated.json",
                params={
                    "order_by": "grade",
                    "direction": "desc",
                    "page": page,
                    "dismounted": "false",
                },
                timeout=30,
            )
            response.raise_for_status()

            page_routes: list[dict[str, Any]] = response.json()

            if not page_routes:
                break

            routes.extend(page_routes)
            page += 1

        return routes
    
    def get_climbing_sessions(
        self,
    ) -> list[dict[str, Any]]:
        sessions: list[dict[str, Any]] = []
        page = 1

        while True:
            print(f"[INFO] Fetching climbing sessions page {page}...")

            response = self.session.get(
                f"{self.BASE_URL}/current_users/climbing_sessions.json",
                params={
                    "page": page,
                    "only_crag": "false",
                    "only_gym": "false",
                },
                timeout=30,
            )
            response.raise_for_status()

            payload: dict[str, Any] = response.json()
            page_sessions = payload.get("sessions") or []

            if not page_sessions:
                break

            sessions.extend(page_sessions)
            page += 1

        return sessions

    def get_climbing_session(
        self,
        session_date: str,
    ) -> dict[str, Any]:
        print(f"[INFO] Fetching climbing session {session_date}...")

        response = self.session.get(
            (
                f"{self.BASE_URL}/current_users/"
                f"climbing_sessions/{session_date}.json"
            ),
            timeout=30,
        )
        response.raise_for_status()

        return response.json()