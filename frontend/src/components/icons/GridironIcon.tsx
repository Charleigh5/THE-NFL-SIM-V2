import React from "react";
import { type GridironIconProps, type GridironIconName, type IconBaseProps } from "./types";
import { FootballLacesIcon } from "./FootballLacesIcon";
import { YardHashesIcon } from "./YardHashesIcon";
import { GoalpostsIcon } from "./GoalpostsIcon";
import { ChainGangIcon } from "./ChainGangIcon";
import { RefereeWhistleIcon } from "./RefereeWhistleIcon";
import { PenaltyFlagIcon } from "./PenaltyFlagIcon";
import { BlitzBoltIcon } from "./BlitzBoltIcon";
import { PlayClockIcon } from "./PlayClockIcon";
import { LombardiTrophyIcon } from "./LombardiTrophyIcon";
import { ChalkboardRouteIcon } from "./ChalkboardRouteIcon";
import { HelmetIcon } from "./HelmetIcon";
import { DownMarkerIcon } from "./DownMarkerIcon";

const ICON_MAP: Record<GridironIconName, React.FC<IconBaseProps>> = {
  football_laces: FootballLacesIcon,
  yard_hashes: YardHashesIcon,
  goalposts: GoalpostsIcon,
  chain_gang: ChainGangIcon,
  referee_whistle: RefereeWhistleIcon,
  penalty_flag: PenaltyFlagIcon,
  blitz_bolt: BlitzBoltIcon,
  play_clock: PlayClockIcon,
  lombardi_trophy: LombardiTrophyIcon,
  chalkboard_route: ChalkboardRouteIcon,
  helmet: HelmetIcon,
  down_marker: DownMarkerIcon,
};

/**
 * GridironIcon
 * Unified NFL domain iconography renderer.
 * Dynamically resolves and renders any of the 12 authentic gridiron icons.
 */
export const GridironIcon: React.FC<GridironIconProps> = ({ name, ...props }) => {
  const IconComponent = ICON_MAP[name];

  if (!IconComponent) {
    console.warn(`[GridironIcon] Unknown icon name: "${name}"`);
    return null;
  }

  return <IconComponent {...props} />;
};

export default GridironIcon;
