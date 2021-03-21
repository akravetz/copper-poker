from abc import ABC, abstractmethod
from dataclasses import dataclass
import datetime as dt
import requests

from typing import List


@dataclass
class Resort:
    name: str
    available_dates: List[dt.date]


class WebsitePoller(ABC):
    @abstractmethod
    def resort_names(self) -> List[str]:
        pass

    @abstractmethod
    def poll(self, session: requests.Session = None) -> List[Resort]:
        pass
