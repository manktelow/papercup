import datetime


class Sentence:
    def __init__(self, text: str, start_time: datetime.timedelta, end_time: datetime.timedelta, length: int):
        self.text = text
        self.start_time = start_time
        self.end_time = end_time
        self.duration = end_time - start_time
        self.length = length

    def to_json(self):
        json_self = {
            'text': self.text,
            'start_time': self.start_time.total_seconds(),
            'end_time': self.end_time.total_seconds(),
            'duration': self.duration.total_seconds()
        }
        return dict(json_self)
