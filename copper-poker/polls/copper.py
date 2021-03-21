import os
from .parkwhiz import ParkwhizPoller
from typing import List


VENUE_ID = "448854"


class CopperPoller(ParkwhizPoller):
    def __init__(self, bearer_token: str = None):
        if not bearer_token:
            bearer_token = os.environ["COPPER_AUTH_TOKEN"]
        super().__init__("Copper", VENUE_ID, bearer_token)

    def resort_names(self) -> List[str]:
        return ["Copper"]
