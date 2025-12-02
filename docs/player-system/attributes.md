# Global Attributes

These attributes apply to every player regardless of position.

## Physical & Mental

- **`speed`** (0-100)

  - **Description**: Top speed potential.
  - **System Usage**: Movement engine, pursuit angles.

- **`acceleration`** (0-100)

  - **Description**: Rate of reaching top speed.
  - **System Usage**: Burst off line, closing speed.

- **`strength`** (0-100)

  - **Description**: Physical power.
  - **System Usage**: Blocking, tackling force, shed block.

- **`agility`** (0-100)

  - **Description**: Ability to change direction.
  - **System Usage**: Juking, route cutting, coverage reaction.

- **`awareness`** (0-100)

  - **Description**: AI decision making.
  - **System Usage**: Reaction time to plays, reading defenses.

- **`stamina`** (0-100)

  - **Description**: Energy pool.
  - **System Usage**: Fatigue accumulation, sub logic.

- **`injury_resistance`** (0-100)

  - **Description**: Durability.
  - **System Usage**: Injury probability roll after contact.

- **`morale`** (0-100)
  - **Description**: Player happiness.
  - **System Usage**: **Critical**: Affects team chemistry. Low morale triggers "Mutiny Cascades" in `SocialGraph`.

## Contract & Status

- **`contract_salary`**

  - **Description**: Annual cost in dollars.

- **`contract_years`**

  - **Description**: Remaining seasons.

- **`development_trait`**
  - **Description**: Growth potential (`NORMAL`, `STAR`, `SUPERSTAR`, `XFACTOR`). Affects XP multipliers in `OffseasonService`.
