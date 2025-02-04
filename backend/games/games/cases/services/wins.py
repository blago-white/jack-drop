import random


class WinDropsService:
    _drops_count: int = 0
    _next_is_win: bool = False
    _fail_serial: int = 0

    @classmethod
    def add_new_drop(cls) -> bool:
        cls._drops_count += 1

        if cls._next_is_win:
            cls._next_is_win = False
            return True

        if cls._drops_count-1 < 0:
            return False

        # if cls._drops_count > 5:
        #     cls._drops_count = 0
        #     print("|---RAISED TRUE")
        #     return True

        is_win = ((random.randint(0, 100) < 44) and (random.randint(0, 100) < 44)) or cls._fail_serial > 7

        if is_win:
            # cls._drops_count = cls._drops_count - 5
            cls._drops_count = 0
            cls._fail_serial = 0

    @classmethod
    def revert_drop(cls):
        cls._drops_count -= 1
