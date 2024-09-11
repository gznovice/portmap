from typing import Tuple

class base_host_selector:
    def get_host(self) -> Tuple[str, int]:
        raise NotImplementedError("must implement this")