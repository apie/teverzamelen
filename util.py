# By Apie 2020-10-02
# License: MIT
from typing import List


def make_dict(item: List[str], header: List[str], fields: tuple) -> dict:
    return {header[i]: field for i, field in enumerate(item) if header[i].strip() in fields}
