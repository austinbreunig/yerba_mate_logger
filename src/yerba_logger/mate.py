from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
import pandas as pd
import numpy as np
from yerba_logger.registry import WeightRegistry

@dataclass
class Mate:
    date: str = field(default=None)
    name: str = field(default=None)
    location: str = field(default=None)
    gourd_count: Optional[int] = field(default=None)
    body_rank: Optional[int] = field(default=None)
    body_profile: Optional[list] = field(default=None)
    flavor_rank: Optional[int] = field(default=None)
    flavor_profile: Optional[list] = field(default=None)
    cycle_rank: Optional[str] = field(default=None)
    cycle_profile: Optional[list] = field(default=None)
    effects_rank: Optional[str] = field(default=None)
    effects_profile: Optional[list] = field(default=None)
    strength_rank: Optional[str] = field(default=None)
    overall_score: Optional[float] = field(init=False)
    body_weight: Optional[float] = field(init=False)
    flavor_weight: Optional[float] = field(init=False)
    cycle_weight: Optional[float] = field(init=False)
    effects_weight: Optional[float] = field(init=False)

    def __post_init__(self):
        post_attribs = ['overall_score', 'body_weight', 'flavor_weight', 'cycle_weight', 'effects_weight']
        # iterate through all attributes and raise error if any of them is None
        for attr, value in self.__dict__.items():
            if value is None and attr not in post_attribs:
                raise ValueError(f"Missing required attribute: {attr}")
            
        
        weights = WeightRegistry()
        self.body_weight = weights.get_weight("body")
        self.flavor_weight = weights.get_weight("flavor")
        self.cycle_weight = weights.get_weight("cycle")
        self.effects_weight = weights.get_weight("effects")


    def process(self):
        # Calculate overall score as a weighted sum of ranks
        overall_body_rank = (self.body_rank * self.body_weight)
        overall_flavor_rank = (self.flavor_rank * self.flavor_weight)
        overall_cycle_rank = (self.cycle_rank * self.cycle_weight)
        overall_effects_rank = (((self.effects_rank + self.strength_rank) / 2) * self.effects_weight)
        self.overall_score = (overall_body_rank + overall_flavor_rank + overall_cycle_rank + overall_effects_rank)

        # create a dictionary of the attributes to be used for DataFrame creation
        data = {
            'date': self.date,
            'name': self.name,
            'location': self.location,
            'gourd_count': self.gourd_count,
            'body_rank': self.body_rank,
            'body_profile': self.body_profile,
            'flavor_rank': self.flavor_rank,
            'flavor_profile': self.flavor_profile,
            'cycle_rank': self.cycle_rank,
            'cycle_profile': self.cycle_profile,
            'effects_rank': self.effects_rank,
            'effects_profile': self.effects_profile,
            'overall_score': self.overall_score,
        }
        df = pd.DataFrame([data])
        # Replace NaN values with 0
        df.fillna(0, inplace=True)

        return df



        

