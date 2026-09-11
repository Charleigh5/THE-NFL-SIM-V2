/**
 * Capology Double-Entry Ledger TypeScript Contracts
 * ==================================================
 * Strict 1:1 type parity with backend Pydantic models. Zero `any` types.
 */

export type CapAccountType =
  | "CAP_ROOM"
  | "ACTIVE_SALARY_LIABILITY"
  | "UNAMORTIZED_BONUS_POOL"
  | "DEAD_MONEY_LIABILITY"
  | "ESCROW_GUARANTEE_POOL";

export type CapTransactionType =
  | "INITIAL_ALLOCATION"
  | "CONTRACT_SIGNING"
  | "CONTRACT_RESTRUCTURE"
  | "RELEASE_PRE_JUNE_1"
  | "RELEASE_POST_JUNE_1"
  | "TRADE_ACQUISITION"
  | "TRADE_OUTGOING"
  | "VOID_YEAR_ACCELERATION"
  | "CAP_ROLLOVER";

export interface CapLedgerEntryDTO {
  id?: number;
  accountId: number;
  accountType: CapAccountType;
  amount: number;
}

export interface CapLedgerTransactionDTO {
  id: string;
  teamId: number;
  playerId?: number;
  playerName?: string;
  transactionType: CapTransactionType;
  leagueYear: number;
  timestamp: string;
  description: string;
  isCommitted: boolean;
  entries: CapLedgerEntryDTO[];
  netCapDelta: number;
}

export interface TeamLedgerStatementDTO {
  teamId: number;
  teamName: string;
  leagueYear: number;
  totalSalaryCap: number;
  availableCapRoom: number;
  activeSalaryLiability: number;
  deadMoneyLiability: number;
  unamortizedBonusPool: number;
  isBalanced: boolean;
  proofOfBalanceDelta: number;
  transactions: CapLedgerTransactionDTO[];
}

export interface MultiYearLedgerStatementResponse {
  teamId: number;
  teamName: string;
  baseLeagueYear: number;
  yearlyStatements: TeamLedgerStatementDTO[];
  isFullyCompliant: boolean;
}

export interface LedgerSimulateRequest {
  teamId: number;
  playerId?: number;
  transactionType: CapTransactionType;
  annualBaseSalary: number;
  signingBonusTotal: number;
  realYears: number;
  voidYears: number;
  postJune1Designation: boolean;
  description?: string;
}

export interface LedgerSimulateResponse {
  teamId: number;
  isCompliant: boolean;
  currentCapRoom: number;
  projectedCapRoom: number;
  netCapDelta: number;
  isBalanced: boolean;
  proofOfBalanceDelta: number;
  stagedEntries: CapLedgerEntryDTO[];
  complianceMessage: string;
}
