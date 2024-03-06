from .utils import session_not_started
from .types import *

class DummyClientSession:
    def __init__(self, *args: Unused, **kwargs: Unused) -> None:
        self.request = session_not_started
        self.get = session_not_started
        self.post = session_not_started
        self.put = session_not_started
        self.patch = session_not_started
        self.delete = session_not_started
        self.head = session_not_started
        self.options = session_not_started