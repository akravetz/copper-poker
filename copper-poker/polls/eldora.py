import os
from .parkwhiz import ParkwhizPoller

VENUE_ID = "478490"


class EldoraPoller(ParkwhizPoller):
    def __init__(self, auth_token):
        if auth_token is None:
            auth_token = os.environ["ELDORA_AUTH_TOKEN"]
        super().__init__("Eldora", VENUE_ID, auth_token)
