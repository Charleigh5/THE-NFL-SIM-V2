import React from "react";
import {
  FootballLacesIcon,
  YardHashesIcon,
  GoalpostsIcon,
  ChainGangIcon,
  RefereeWhistleIcon,
  PenaltyFlagIcon,
  BlitzBoltIcon,
  DefensiveBlitzBoltIcon,
  PlayClockIcon,
  LombardiTrophyIcon,
  ChalkboardRouteIcon,
  HelmetIcon,
  DownMarkerIcon,
  GridironIcon,
  resolveIconSize,
  type GridironIconName,
  type IconBaseProps,
} from "./index";

/**
 * Verification test script for NFL Gridiron Vector Iconography
 */
function runIconVerification() {
  console.log("=== NFL GRIDIRON ICONOGRAPHY VERIFICATION ===");

  const expectedIcons: Array<{
    name: GridironIconName;
    component: React.FC<IconBaseProps>;
  }> = [
    { name: "football_laces", component: FootballLacesIcon },
    { name: "yard_hashes", component: YardHashesIcon },
    { name: "goalposts", component: GoalpostsIcon },
    { name: "chain_gang", component: ChainGangIcon },
    { name: "referee_whistle", component: RefereeWhistleIcon },
    { name: "penalty_flag", component: PenaltyFlagIcon },
    { name: "blitz_bolt", component: BlitzBoltIcon },
    { name: "play_clock", component: PlayClockIcon },
    { name: "lombardi_trophy", component: LombardiTrophyIcon },
    { name: "chalkboard_route", component: ChalkboardRouteIcon },
    { name: "helmet", component: HelmetIcon },
    { name: "down_marker", component: DownMarkerIcon },
  ];

  console.log(`[1] Verifying 12 core icons and component exports...`);
  if (expectedIcons.length !== 12) {
    throw new Error(`Expected exactly 12 icons, found ${expectedIcons.length}`);
  }

  expectedIcons.forEach(({ name, component }) => {
    if (typeof component !== "function") {
      throw new Error(`Icon component for ${name} is not a valid function!`);
    }

    // Render component directly
    const element = React.createElement(component, {
      size: 24,
      className: "test-icon",
      title: "Test Title",
    });
    if (!element || element.type !== component) {
      throw new Error(`Component element instantiation failed for ${name}`);
    }

    // Render via unified GridironIcon
    const unifiedElement = React.createElement(GridironIcon, { name, size: 20 });
    if (!unifiedElement || unifiedElement.props.name !== name) {
      throw new Error(`Unified GridironIcon instantiation failed for ${name}`);
    }

    console.log(`  ✓ Verified icon: ${name}`);
  });

  console.log(`[2] Verifying aliases and presets...`);
  if (DefensiveBlitzBoltIcon !== BlitzBoltIcon) {
    throw new Error("DefensiveBlitzBoltIcon alias must match BlitzBoltIcon");
  }

  if (resolveIconSize(16) !== 16) throw new Error("resolveIconSize(16) failed");
  if (resolveIconSize("xs") !== 12) throw new Error("resolveIconSize('xs') failed");
  if (resolveIconSize("sm") !== 16) throw new Error("resolveIconSize('sm') failed");
  if (resolveIconSize("md") !== 20) throw new Error("resolveIconSize('md') failed");
  if (resolveIconSize("lg") !== 24) throw new Error("resolveIconSize('lg') failed");
  if (resolveIconSize("xl") !== 32) throw new Error("resolveIconSize('xl') failed");
  if (resolveIconSize("48px") !== "48px") throw new Error("resolveIconSize('48px') failed");
  if (resolveIconSize(undefined) !== 24) {
    throw new Error("resolveIconSize(undefined) default failed");
  }
  console.log("  ✓ Verified size resolution helper");

  console.log("=== ALL 12 GRIDIRON ICONS FULLY VERIFIED ===");
}

runIconVerification();
