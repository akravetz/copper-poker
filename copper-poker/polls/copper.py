import os
from .parkwhiz import ParkwhizPoller


VENUE_ID = "448854"


class CopperPoller(ParkwhizPoller):
    def __init__(self, bearer_token: str =None):
        if not bearer_token:
            bearer_token = os.environ["COPPER_AUTH_TOKEN"]
        super().__init__("Copper", VENUE_ID, bearer_token)
