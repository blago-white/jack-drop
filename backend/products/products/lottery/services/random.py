import random


class LotteryRandomService:
    @classmethod
    def get_winner(cls, participants: list[int]) -> int:
        return random.choice(participants)
