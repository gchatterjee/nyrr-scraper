import json


class Race:
    def __init__(
        self,
        title: str = None,
        date: str = None,
        time: str = None,
        location: str = None,
        status: str = None,
        url: str = None,
    ) -> None:
        self.title = title
        self.date = date
        self.time = time
        self.location = location
        self.status = status
        self.url = url

    def __eq__(self, other) -> bool:
        if not hasattr(other, "title") or self.title != other.title:
            return False
        if not hasattr(other, "date") or self.date != other.date:
            return False
        if not hasattr(other, "time") or self.time != other.time:
            return False
        if not hasattr(other, "location") or self.location != other.location:
            return False
        if not hasattr(other, "status") or self.status != other.status:
            return False
        if not hasattr(other, "url") or self.url != other.url:
            return False
        return True

    def __repr__(self) -> str:
        return json.dumps(
            {
                "title": self.title,
                "date": self.date,
                "time": self.time,
                "location": self.location,
                "status": self.status,
                "url": self.url,
            }
        )
