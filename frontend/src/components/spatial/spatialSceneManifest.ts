export type SpatialAssetStatus = "AVAILABLE" | "MISSING" | "GENERATED_APPROXIMATION";
export type SpatialRenderMode = "PROCEDURAL_2_5D" | "DEPTH_PLATE" | "TRUE_3D";

export interface SpatialRoutePolicy {
  globalStadiumBackdrop: boolean;
  weatherFx: boolean;
  weatherHud: boolean;
}

export interface SpatialSceneManifest {
  id: string;
  name: string;
  route: string;
  renderMode: SpatialRenderMode;
  storyboardAsset: string;
  assetStatus: SpatialAssetStatus;
  productionAssetPath?: string;
  fallback: "PROCEDURAL_WAR_ROOM";
  motion: {
    pointerParallaxPx: number;
    reducedMotionParallaxPx: number;
  };
  routePolicy: SpatialRoutePolicy;
}

/**
 * Scene 05 from NFL-SIM-STORYBOARD-001.
 *
 * The storyboard names depth_chart_warboard_1789227219044.jpg, but that binary
 * is not present in the repository as of the proof-slice baseline. We therefore
 * render a code-native procedural war room rather than silently substituting a
 * different image or claiming the production plate exists.
 */
export const DEPTH_CHART_SCENE: SpatialSceneManifest = {
  id: "SCN-005",
  name: "Depth Chart Strategy War Room",
  route: "/depth-chart",
  renderMode: "PROCEDURAL_2_5D",
  storyboardAsset: "depth_chart_warboard_1789227219044.jpg",
  assetStatus: "MISSING",
  fallback: "PROCEDURAL_WAR_ROOM",
  motion: {
    pointerParallaxPx: 8,
    reducedMotionParallaxPx: 0,
  },
  routePolicy: {
    globalStadiumBackdrop: false,
    weatherFx: false,
    weatherHud: false,
  },
};

const DEFAULT_ROUTE_POLICY: SpatialRoutePolicy = {
  globalStadiumBackdrop: true,
  weatherFx: true,
  weatherHud: true,
};

export function getSpatialRoutePolicy(pathname: string): SpatialRoutePolicy {
  if (pathname === "/depth-chart" || pathname === "/empire/depth-chart") {
    return DEPTH_CHART_SCENE.routePolicy;
  }

  return DEFAULT_ROUTE_POLICY;
}
