/**
 * Capology & Multi-Year Contract Types
 * ====================================
 * Frontend TypeScript contracts matching backend Pydantic V2 schemas.
 * Strictly zero `any` types.
 */

export interface ContractYearStructure {
  yearIndex: number;
  calendarYear: number;
  baseSalary: number;
  proratedBonus: number;
  rosterBonus: number;
  workoutBonus: number;
  isVoidYear: boolean;
  capHit: number;
}

export interface MultiYearContractProposal {
  player_id: number;
  team_id: number;
  real_years: number;
  void_years: number;
  annual_base_salary: number;
  signing_bonus_total: number;
  guaranteed_total: number;
  post_june_1_designation: boolean;
}

export interface YearlyCapLiability {
  year: number;
  projected_cap: number;
  committed_salaries: number;
  prorated_bonus: number;
  proposed_contract_cap_hit: number;
  dead_money: number;
  net_cap_space: number;
  is_cap_compliant: boolean;
}

export interface CompPickImpact {
  qualifies_as_cfa: boolean;
  cfa_tier: number | null;
  cancelled_pick_round: number | null;
  projected_comp_picks_lost: string[];
  impact_summary: string;
}

export interface MultiYearCapProjectionResponse {
  player_id: number;
  team_id: number;
  total_contract_value: number;
  annual_average_value: number;
  proration_years_used: number;
  yearly_schedule: YearlyCapLiability[];
  accelerated_dead_money_void_year: number;
  comp_pick_impact: CompPickImpact;
  is_fully_compliant: boolean;
}
