from .models import Linguist


FICTIONAL_LINGUISTS = (
    Linguist("Anna Kovacs", ("en>hu", "de>hu"), ("marketing", "general"), 7000, 4.9),
    Linguist("Markus Weber", ("en>de", "hu>de"), ("technical", "legal"), 9000, 4.8),
    Linguist("Sofia Rossi", ("en>it", "de>it"), ("marketing", "technical"), 6000, 4.7),
    Linguist("Elena Petrova", ("en>de", "en>hu"), ("medical", "technical"), 3500, 4.9),
)
