from .car import Car
from .bike import Bike

modules = {
    "car": Car,
    "bike": Bike
}

__all__ = ["modules"]