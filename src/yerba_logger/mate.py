from dataclasses import dataclass
from typing import Optional
import pandas as pd
import numpy as np

@dataclass
class Mate:
    name: str
    location: str
    smell_rank: Optional[int] = None
    smell_notes: Optional[str] = None
    taste_rank: Optional[int] = None
    taste_notes: Optional[str] = None
    cycle: Optional[str] = None
    gourd_count: Optional[int] = None
    energy_descrip: Optional[str] = None
    energy_rank: Optional[int] = None
    energy_notes: Optional[str] = None
    

    def process(self):
        # Calculate overall score as a weighted sum of ranks
        self.overall_score = (self.smell_rank * 0.2 + self.taste_rank * 0.3 + self.energy_rank * 0.5)

        # create a dictionary of the attributes to be used for DataFrame creation
        data = {
            'name': self.name,
            'location': self.location,
            'smell_rank': self.smell_rank,
            'smell_notes': self.smell_notes,
            'taste_rank': self.taste_rank,
            'taste_notes': self.taste_notes,
            'cycle': self.cycle,
            'gourd_count': self.gourd_count,
            'energy_descrip': self.energy_descrip,
            'energy_rank': self.energy_rank,
            'energy_notes': self.energy_notes,
            'overall_score': self.overall_score
        }
        df = pd.DataFrame([data])
        # Replace NaN values with 0
        df.fillna(0, inplace=True)

        return df



        

