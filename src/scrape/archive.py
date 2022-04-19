from re import L
from typing import Protocol, List, Set
from schema import ListItem, Estate


class Archive(Protocol):

    def save_list_result(data: List[ListItem], save_path: str) -> None:
        raise NotImplementedError

    def read_list_result(read_path: str) -> List[ListItem]:
        raise NotImplementedError

    def save_estate_collection(data: List[Estate], save_path: str) -> None:
        raise NotImplementedError

    def read_estate_collection(read_path: str) -> List[Estate]:
        raise NotImplementedError

    def identify_missing_and_removed_ids(
        sold_list: List[ListItem],
        forsale_list: List[ListItem],
        estates: List[Estate]
        ) -> Set:
        raise NotImplementedError
