import os
from .parkwhiz import ParkwhizPoller

VENUE_ID = "478490"


class EldoraPoller(ParkwhizPoller):
    def __init__(self, bearer_token: str = None):
        if bearer_token is None:
            bearer_token = os.environ["ELDORA_AUTH_TOKEN"]
        super().__init__("Eldora", VENUE_ID, bearer_token)
