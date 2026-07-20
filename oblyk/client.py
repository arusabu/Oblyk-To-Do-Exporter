from typing import Any

import requests


class OblykClient:
    BASE_URL = "https://api.oblyk.org/api/v1"

    HTTP_API_ACCESS_TOKEN = (
        "M4rvBxc4M7kqqdtXPDvFEYm9"
    )

    def __init__(self) -> None:
        self.session = requests.Session()

        self.session.headers.update(
            {
                "Accept": "application/json",
                "HttpApiAccessToken": (
                    self.HTTP_API_ACCESS_TOKEN
                ),
            }
        )


    def login(
        self,
        email: str,
        password: str,
    ) -> None:
        response = self.session.post(
            f"{self.BASE_URL}/sessions/sign_in",
            json={
                "email": email,
                "password": password,
                "oblyk_full_name": None,
            },
            timeout=30,
        )
        response.raise_for_status()

        payload = response.json()

        token = payload.get("token")

        if token is None:
            raise RuntimeError(
                "Login succeeded but no bearer token was returned."
            )

        self.session.headers["Authorization"] = (
            f"Bearer {token}"
        )


    def get_current_user(self) -> dict:
        response = self.session.get(
            f"{self.BASE_URL}/current_users.json"
        )
        response.raise_for_status()

        return response.json()


    def get_gym_spaces(
        self,
        gym_id: int,
    ) -> list[dict[str, Any]]:

        response = self.session.get(
            f"{self.BASE_URL}/gyms/{gym_id}/gym_spaces/groups.json",
            timeout=30,
        )
        response.raise_for_status()

        payload = response.json()

        for space in payload["ungrouped_spaces"]:
            space["name"] = (space.get("name") or "")

        return payload["ungrouped_spaces"]


    def get_current_gym_routes(
        self,
        gym_id: int,
    ) -> list[dict[str, Any]]:
        routes: list[dict[str, Any]] = []
        page = 1

        while True:

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

        response = self.session.get(
            (
                f"{self.BASE_URL}/current_users/"
                f"climbing_sessions/{session_date}.json"
            ),
            timeout=30,
        )
        response.raise_for_status()

        return response.json()


def build_space_order(
    spaces: list[dict[str, Any]],
) -> dict[str, int]:
    return {
        space["name"]: index
        for index, space in enumerate(spaces)
    }