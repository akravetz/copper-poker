import os
from .parkwhiz import ParkwhizPoller
from typing import List

VENUE_ID = "478490"


class EldoraPoller(ParkwhizPoller):
    def __init__(self, bearer_token: str = None):
        if bearer_token is None:
            bearer_token = os.environ["ELDORA_AUTH_TOKEN"]
        super().__init__("Eldora", VENUE_ID, bearer_token)

    def resort_names(self) -> List[str]:
        return ["Eldora"]
