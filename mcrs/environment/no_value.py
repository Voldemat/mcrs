from __future__ import annotations


class NoValue:
    instance: NoValue | None = None

    @classmethod
    def build(cls) -> NoValue:
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance
