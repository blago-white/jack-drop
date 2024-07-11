

class WinDropsService:
    _drops_count: int = 0

    @classmethod
    def add_new_drop(cls) -> bool:
        cls._drops_count += 1

        return not bool(cls._drops_count % 3)  # TODO: Make services for
        # chance of
        # win
