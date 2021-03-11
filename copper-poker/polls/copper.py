import os
from .parkwhiz import ParkwhizPoller




VENUE_ID = "448854"
def get_auth_token():
    return os.environ["COPPER_AUTH_TOKEN"]


class CopperPoller(ParkwhizPoller):
    def __init__(self, auth_token=None):
        if not auth_token:
            auth_token = get_auth_token()
        super().__init__("Copper", VENUE_ID, auth_token)
