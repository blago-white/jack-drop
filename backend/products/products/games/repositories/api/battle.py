from django.db.models import QuerySet
from rest_framework.exceptions import ValidationError, APIException
from rest_framework.serializers import Serializer

from cases.serializers.case import CaseSerializer
from cases.services.cases import CaseService
from cases.services.items import CaseItemsService
from cases.serializers.case import CaseSerializer
from cases.serializers.items import ItemSerializer
from games.api.services.battle import BattleRequestApiService, BattleApiService
from games.api.services.site import SiteFundsApiService
from games.api.services.users import UsersApiService
from games.models import Games
from games.serializers.battle import BattleRequestServiceEndpointSerializer
from games.serializers.drop import DropItemSerializer
from games.services.result import GameResultService
from games.services.transfer import GameResultData
from items.services.items import ItemService
from inventory.services.inventory import InventoryService
from .base import BaseApiRepository


class _BaseBattleApiRepository(BaseApiRepository):
    def _validate_funds(self, battle_case_id: int, user_data: dict) -> None:
        case_price = self._cases_service.get_price(case_id=battle_case_id)

        if user_data.get("displayed_balance") < case_price:
            raise ValidationError(
                "There are not enough balance funds for action"
            )


class BattleRequestApiRepository(_BaseBattleApiRepository):
    default_api_service = BattleRequestApiService()
    default_cases_service = CaseService()

    _api_service: BattleRequestApiService

    def __init__(
            self, *args,
            cases_service: CaseService = None,
            **kwargs):
        self._cases_service = cases_service or self.default_cases_service

        super().__init__(*args, **kwargs)

    def create(
            self, battle_case_id: int,
            user_data: dict) -> dict:
        serialized: BattleRequestServiceEndpointSerializer = (
            self.default_api_service.default_endpoint_serializer_class(
                data={
                    "battle_case_id": battle_case_id,
                    "initiator_id": user_data.get("id")
                }
            )
        )

        serialized.is_valid(raise_exception=True)

        self._validate_funds(battle_case_id=battle_case_id,
                             user_data=user_data)

        ok = self._api_service.create(serialized=serialized)

        return {"success": ok}

    def cancel(self, initiator_id: int) -> dict:
        ok = self._api_service.cancel(initiator_id=initiator_id)

        return {"success": ok}


class BattleApiRepository(_BaseBattleApiRepository):
    default_cases_service = CaseService()
    default_api_service = BattleApiService()
    default_case_items_service = CaseItemsService()
    default_inventory_service = InventoryService()
    default_users_service = UsersApiService()
    default_site_funds_service = SiteFundsApiService()
    default_game_result_service = GameResultService()
    default_items_service = ItemService()

    default_case_serializer = CaseSerializer

    _api_service: BattleApiService

    def __init__(
            self, *args,
            cases_service: CaseService = None,
            case_items_service: CaseItemsService = None,
            inventory_service: InventoryService = None,
            users_service: UsersApiService = None,
            site_funds_service: SiteFundsApiService = None,
            game_result_service: GameResultService = None,
            case_serializer: CaseSerializer = None,
            item_service: ItemService = None,
            **kwargs):
        self._cases_service = cases_service or self.default_cases_service
        self._case_items_service = (case_items_service or
                                    self.default_case_items_service)
        self._inventory_service = inventory_service or self.default_inventory_service
        self._users_service = users_service or self.default_users_service
        self._site_funds_service = site_funds_service or self.default_site_funds_service
        self._game_result_service = game_result_service or self.default_game_result_service
        self._case_serializer = case_serializer or self.default_case_serializer
        self._item_service = item_service or self.default_items_service

        super().__init__(*args, **kwargs)

    def make(
            self, battle_case_id: int,
            initiator_id: int,
            participant_data: dict) -> dict:
        self._validate_funds_participant(
            battle_case_id=battle_case_id,
            participant_data=participant_data
        )

        case_data = self._cases_service.get(
            case_id=battle_case_id
        )

        serialized = self._api_service.default_endpoint_serializer_class(
            data={
                "initiator_id": initiator_id,
                "participant_id": participant_data.get("id"),
                "site_funds": {
                    "site_active_funds": self._site_funds_service.get(),
                },
                "battle_case_id": case_data.pk,
                "battle_case_price": case_data.price,
                "battle_case_items": DropItemSerializer(
                    instance=self._case_items_service.get_drop_case_items_for_case(
                        case_pk=case_data.pk
                    ),
                    many=True
                ).data
            }
        )

        serialized.is_valid(raise_exception=True)

        battle_result = self._api_service.make(
            serialized=serialized
        )

        if not battle_result:
            raise APIException("Error with battle making")

        self._commit_result(battle_result=battle_result,
                            case_price=case_data.price)

        dropped_items = [
            self._case_items_service.get(
                item_id=battle_result.get("dropped_item_winner_id")
            ),
            self._case_items_service.get(
                item_id=battle_result.get("dropped_item_loser_id")
            )
        ]

        return {
            "winner_id": battle_result.get("winner_id"),
            "loser_id": battle_result.get("loser_id"),
            "dropped_item_winner_id": {
                "case_item_id": dropped_items[0].id,
                "title": dropped_items[0].item.title,
                "image_path": dropped_items[0].item.image_path,
                "price": dropped_items[0].item.price
            },
            "dropped_item_loser_id": {
                "case_item_id": dropped_items[-1].id,
                "title": dropped_items[-1].item.title,
                "image_path": dropped_items[-1].item.image_path,
                "price": dropped_items[-1].item.price
            },
            "battle_case": self._case_serializer(
                instance=case_data
            ).data
        }

    def get_stats(self, user_id: int) -> dict:
        return self._api_service.get_stats(user_id=user_id)

    def get_all(self, user_id: int) -> dict:
        response = self._api_service.get_all(user_id=user_id)
        result = []

        cases = self._qs_as_dict(
            self._cases_service.bulk_get([int(i["battle_case_id"])
                                          for i in response
                                          ]),
            serializer=CaseSerializer
        )

        items = self._values_as_dict(self._case_items_service.bulk_get_items(
            item_ids={i["dropped_item_loser_id"] for i in response} | {
                i["dropped_item_winner_id"] for i in response
            }
        ))

        for battle in response:
            result.append({
                "battle_case": cases.get(battle["battle_case_id"]),
                "dropped_item_winner": items.get(
                    battle["dropped_item_winner_id"]
                ),
                "dropped_item_loser": items.get(
                    battle["dropped_item_loser_id"]
                ),
            })

        return result

    def _commit_result(self, battle_result: dict, case_price: float | int):
        loser_case_item = self._case_items_service.get(battle_result.get(
            "dropped_item_loser_id")
        )

        winner_case_item = self._case_items_service.get(battle_result.get(
            "dropped_item_winner_id")
        )

        # self._users_service.update_user_balance_by_id(
        #     delta_amount=-case_price,
        #     user_id=battle_result.get("winner_id")
        # )
        #
        # self._users_service.update_user_balance_by_id(
        #     delta_amount=-case_price,
        #     user_id=battle_result.get("loser_id")
        # )
        #
        # _, loser_to_blogger_funds = self._users_service.update_user_advantage(
        #     delta_advantage=-case_price,
        #     user_id=battle_result.get("loser_id")
        # )
        #
        # _, winner_to_blogger_funds = self._users_service.update_user_advantage(
        #     delta_advantage=(winner_case_item - case_price) + loser_case_item.item.price,
        #     user_id=battle_result.get("winner_id")
        # )

        self._inventory_service.add_item(
            owner_id=battle_result.get("winner_id"),
            item_id=winner_case_item.item.pk
        )

        self._inventory_service.add_item(
            owner_id=battle_result.get("winner_id"),
            item_id=loser_case_item.item.pk
        )
        # TODO: Uncomment
        # self._site_funds_service.update(
        #     amount=battle_result.get("site_funds_diff") - (loser_to_blogger_funds + winner_to_blogger_funds)
        # )

        self._game_result_service.save(data=GameResultData(
            user_id=battle_result.get("winner_id"),
            game=Games.BATTLE,
            is_win=True,
            first_item_id=winner_case_item.item.id,
            case_id=battle_result.get("battle_case_id"),
            second_item_id=loser_case_item.item.id
        ))

        self._game_result_service.save(data=GameResultData(
            user_id=battle_result.get("loser_id"),
            game=Games.BATTLE,
            is_win=False,
            first_item_id=battle_result.get(
                "dropped_item_loser_id"
            ),
            case_id=battle_result.get("battle_case_id"),
            second_item_id=battle_result.get(
                "dropped_item_winner_id"
            ),
        ))

    def _validate_funds_participant(
            self, battle_case_id: int, participant_data: dict
    ) -> bool:
        case_price = self._cases_service.get_price(case_id=battle_case_id)

        return participant_data.get("displayed_balance") >= case_price

    @staticmethod
    def _qs_as_dict(qs: QuerySet, serializer: Serializer) -> dict:
        return {item.pk: serializer(instance=item).data for item in qs}

    @staticmethod
    def _values_as_dict(qs_values: list[dict]) -> dict:
        return {item.get("pk"): item for item in qs_values}
