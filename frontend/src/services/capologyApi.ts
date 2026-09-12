/**
 * Capology API Client
 * ===================
 * Service connecting the React frontend to the backend Capology engine.
 * Supports real-time multi-year simulations and baseline 5-year team outlooks.
 */

import { api } from "./api";
import type {
  MultiYearContractProposal,
  MultiYearCapProjectionResponse,
  YearlyCapLiability,
} from "../types/capology";

export const capologyApi = {
  /**
   * Simulates multi-year cap liabilities, void years proration,
   * accelerated dead money, and compensatory pick cancellation warnings.
   */
  simulateProposal: async (
    proposal: MultiYearContractProposal
  ): Promise<MultiYearCapProjectionResponse> => {
    const res = await api.post<MultiYearCapProjectionResponse>(
      "/api/capology/simulate-proposal",
      proposal
    );
    return res.data;
  },

  /**
   * Fetches baseline 5-year outlook for a franchise without an active proposal.
   */
  getFiveYearOutlook: async (teamId: number): Promise<YearlyCapLiability[]> => {
    const res = await api.get<YearlyCapLiability[]>(
      `/api/capology/teams/${teamId}/five-year-outlook`
    );
    return res.data;
  },
};
