from dataclasses import dataclass, field
from typing import List
import pandas as pd

@dataclass
class Housing:
    boliga_id: int = None
    property_type: str = None
    address: str = None
    list_price: int = None
    living_area: int = None
    lot_area: int = None
    rooms: int = None
    floors: int = None
    construction_year : int = None
    energy_rating: str = None
    taxes_pr_month: int = None
    bsmnt_area: int = None
    created_date: str = None
    url: str = None
    for_sale: bool = None
    final_price: int = None
    latlng: str = None
    gmaps: str = None
    station_dist_km: float = None
    market_days: int = None

    def column_list(self) -> list:
        return list(self.__dict__.keys())

    def generator(self):
        return ((col, self.__getattribute__(col)) for col in self.column_list())

    def as_dict(self):
        return {k: v for k, v in self.generator()}


@dataclass
class HousingList:
    
    list: List[Housing] = field(default_factory=list)

    def append(self, housing):
        self.list.append(housing)
    
    def to_pandas(self) -> pd.DataFrame:
        return pd.DataFrame([x.as_dict() for x in self.list])
