/**
 * Represents a humanized analytical narrative tag with its associated explanatory tooltip.
 */
export interface HumanizedNarrativeNote {
  /** Clean, natural language label suitable for coaches and general managers. */
  label: string;
  /** Detailed plain-language tooltip articulating how the metric influences GM evaluation. */
  tooltip: string;
}

/**
 * Transforms raw backend trade evaluation narrative strings into human-readable labels
 * and contextual tooltips.
 * - TNI -> Team Need Fit
 * - EV Decay -> Draft Value Drift
 * - Cap Surcharge -> Salary Cap Impact
 * - TVP -> Pts
 *
 * @param note Raw narrative note string from the GM trade evaluation response.
 * @returns An object containing the formatted label and rich explanatory tooltip.
 */
export function humanizeNarrativeNote(note: string): HumanizedNarrativeNote {
  const label = note
    .replace(/\bTNI\b/g, "Team Need Fit")
    .replace(/\bEV Decay\b/gi, "Draft Value Drift")
    .replace(/\bEV\b/g, "Draft Value")
    .replace(/\bCap Surcharge\b/gi, "Salary Cap Impact")
    .replace(/\bSurcharge\b/gi, "Cap Impact")
    .replace(/\bTVP\b/g, "Pts");

  let tooltip = "Analytical factor evaluated by the GM trade engine.";

  if (/team need|need fit/i.test(label) || /\btni\b/i.test(note)) {
    tooltip =
      "Team Need Fit (formerly TNI): Weights player acquisition value based on positional roster depth and championship window urgency.";
  } else if (/draft value drift|ev decay/i.test(label) || /ev decay/i.test(note)) {
    tooltip =
      "Draft Value Drift (EV Decay): Future draft picks carry discount risk due to slot uncertainty and time-value discounting.";
  } else if (/salary cap impact|cap impact|surcharge/i.test(label) || /surcharge/i.test(note)) {
    tooltip =
      "Salary Cap Impact: Financial adjustments accounting for absorbed salary cap hits, dead money, or luxury thresholds.";
  } else if (/medical|injury/i.test(label) || /medical/i.test(note)) {
    tooltip =
      "Medical Risk Flag: Durability and health discount applied based on current injury designation.";
  } else if (/holdout|morale/i.test(label)) {
    tooltip =
      "Locker Room Leverage: Discount applied due to low player morale, holdout threats, or contractual tension.";
  } else if (/compensatory/i.test(label)) {
    tooltip =
      "Compensatory Pick Floor: Asset retention floor based on projected NFL compensatory draft pick compensation.";
  } else if (/rivalry|division/i.test(label)) {
    tooltip =
      "Intradivision Tax: Strategic penalty applied when trading key talent to a direct divisional rival.";
  } else if (/urgency|hot-seat|deadline/i.test(label)) {
    tooltip =
      "Window Urgency: Strategic pressure from trade deadlines or GM job security influencing negotiation posture.";
  }

  return { label, tooltip };
}
