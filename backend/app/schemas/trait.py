from datetime import date

from pydantic import BaseModel, ConfigDict

from app.models.trait import TraitEffectType, TraitSource


class TraitBase(BaseModel):
    name: str
    description: str | None = None
    effect_type: TraitEffectType
    effect_value: float
    position_groups: dict | None = None

class TraitCreate(TraitBase):
    pass

class Trait(TraitBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class PlayerTraitBase(BaseModel):
    trait_id: int
    player_id: int # Often contextually known, but good to have
    acquired_date: date
    source: TraitSource

class PlayerTrait(PlayerTraitBase):
    trait: "Trait" # Nested full trait info
    model_config = ConfigDict(from_attributes=True)

class TraitAssignment(BaseModel):
    trait_id: int
    source: TraitSource = TraitSource.DEVELOPMENT

class TraitUnlockRequest(BaseModel):
    trait_name: str

