from dataclasses import dataclass
from typing import Optional

@dataclass
class Estate:
    boliga_id: str


@dataclass
class ListItem:
    id: int = None
    list_type: str = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    propertyType: Optional[str] = None
    energyClass: Optional[str] = None
    openHouse: Optional[str] = None
    price: Optional[int] = None
    selfsale: Optional[bool] = None
    rooms: Optional[int] = None
    size: Optional[int] = None
    lotSize: Optional[int] = None
    floor: Optional[int] = None
    buildYear: Optional[int] = None
    city: Optional[str] = None
    isForeclosure: Optional[bool] = None
    isActive: Optional[bool] = None
    zipCode: Optional[int] = None
    street: Optional[str] = None
    squaremeterPrice: Optional[float] = None
    daysForSale: Optional[int] = None
    createdDate: Optional[str] = None
    net: Optional[int] = None
    exp: Optional[int] = None
    basementSize: Optional[int] = None

    @property
    def raw_fields(self):
        return set(self.__dict__.keys()) - self.custom_fields
    
    @property
    def custom_fields(self):
        return set([self.list_type])
    
