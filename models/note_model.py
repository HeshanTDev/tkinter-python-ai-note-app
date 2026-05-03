from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Tag:
    name: str
    id: Optional[int] = None

@dataclass
class Note:
    title: str
    content: str
    created_at: str
    updated_at: str
    id: Optional[int] = None
    tags: List[Tag] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []
