import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from appdirs import user_data_dir

DATA_FILE = Path(user_data_dir("philipstv-gui", "cyran.dev")) / "data.json"


@dataclass(frozen=True)
class HostData:
    host: str
    id: str
    key: str

    @classmethod
    def from_dict(cls, raw_dict: Dict[str, Any]) -> "HostData":
        return cls(host=raw_dict["host"], id=raw_dict["id"], key=raw_dict["key"])


@dataclass
class AppData:
    last_host: Optional[HostData]

    @classmethod
    def load(cls) -> "AppData":
        raw_data = {}
        if DATA_FILE.exists():
            raw_data = json.loads(DATA_FILE.read_text())
        last_host = HostData.from_dict(raw_data["last_host"]) if raw_data.get("last_host") else None
        return cls(last_host=last_host)

    def save(self) -> None:
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        DATA_FILE.touch(exist_ok=True)
        DATA_FILE.write_text(json.dumps(asdict(self)))
