import React, { useState, useEffect, useMemo, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Search, Filter, X, Dumbbell, Zap, Brain, Heart, Wind, Coffee, Star } from "lucide-react";
import type { Drill, DrillCategory } from "../../types/training";
import { DrillCategory as DrillCategoryEnum } from "../../types/training";
import { trainingApi } from "../../services/trainingApi";
import { DrillCard3D } from "./DrillCard3D";
import "./DrillSelector.css";

interface DrillSelectorProps {
  position?: string;
  seasonPhase?: string;
  onDrillSelect: (drill: Drill) => void;
  selectedDrill?: Drill | null;
  playerWeaknesses?: string[]; // New prop for recommendations
}

const CATEGORY_CONFIG: Record<string, { label: string; icon: React.ReactNode; color: string }> = {
  [DrillCategoryEnum.STRENGTH]: {
    label: "Strength",
    icon: <Dumbbell className="w-4 h-4" />,
    color: "from-red-500 to-red-700",
  },
  [DrillCategoryEnum.SPEED]: {
    label: "Speed",
    icon: <Zap className="w-4 h-4" />,
    color: "from-yellow-500 to-orange-600",
  },
  [DrillCategoryEnum.TECHNIQUE]: {
    label: "Technique",
    icon: <Wind className="w-4 h-4" />,
    color: "from-purple-500 to-purple-700",
  },
  [DrillCategoryEnum.MENTAL]: {
    label: "Mental",
    icon: <Brain className="w-4 h-4" />,
    color: "from-blue-500 to-blue-700",
  },
  [DrillCategoryEnum.ENDURANCE]: {
    label: "Endurance",
    icon: <Heart className="w-4 h-4" />,
    color: "from-green-500 to-green-700",
  },
  [DrillCategoryEnum.RECOVERY]: {
    label: "Recovery",
    icon: <Coffee className="w-4 h-4" />,
    color: "from-teal-500 to-teal-700",
  },
};

export const DrillSelector: React.FC<DrillSelectorProps> = ({
  position,
  // seasonPhase - reserved for future season-phase filtering
  onDrillSelect,
  selectedDrill,
  playerWeaknesses = [],
}) => {
  const [drills, setDrills] = useState<Drill[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [activeCategory, setActiveCategory] = useState<DrillCategory | null>(null);
  const [showFilters, setShowFilters] = useState(false);
  const [showRecommendedOnly, setShowRecommendedOnly] = useState(false);

  // Fetch drills on mount or when filters change
  useEffect(() => {
    const fetchDrills = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await trainingApi.getDrills({
          position,
          category: activeCategory ?? undefined,
        });
        setDrills(response.drills);
      } catch (err) {
        setError("Failed to load drills. Please try again.");
        console.error("DrillSelector fetch error:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchDrills();
  }, [position, activeCategory]);

  // Determine if a drill is recommended based on player weaknesses
  const isDrillRecommended = useCallback(
    (drill: Drill) => {
      return playerWeaknesses.some(
        (weakness) =>
          drill.target_stat.toLowerCase() === weakness.toLowerCase() ||
          drill.secondary_stats?.some((stat) => stat.toLowerCase() === weakness.toLowerCase())
      );
    },
    [playerWeaknesses]
  );

  // Filter drills by search query and recommendation
  const filteredDrills = useMemo(() => {
    let result = drills;

    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      result = result.filter(
        (drill) =>
          drill.name.toLowerCase().includes(query) ||
          drill.target_stat.toLowerCase().includes(query) ||
          drill.description?.toLowerCase().includes(query)
      );
    }

    if (showRecommendedOnly) {
      result = result.filter((drill) => isDrillRecommended(drill));
    }

    // Sort recommended drills to the top if not filtering strictly by recommended
    if (!showRecommendedOnly) {
      result.sort((a, b) => {
        const aRec = isDrillRecommended(a);
        const bRec = isDrillRecommended(b);
        if (aRec && !bRec) return -1;
        if (!aRec && bRec) return 1;
        return 0;
      });
    }

    return result;
  }, [drills, searchQuery, showRecommendedOnly, isDrillRecommended]);

  // Handle category toggle
  const handleCategoryClick = useCallback((category: DrillCategory) => {
    setActiveCategory((prev) => (prev === category ? null : category));
  }, []);

  // Clear all filters
  const clearFilters = useCallback(() => {
    setSearchQuery("");
    setActiveCategory(null);
    setShowRecommendedOnly(false);
  }, []);

  const hasActiveFilters = searchQuery.length > 0 || activeCategory !== null || showRecommendedOnly;

  return (
    <div className="drill-selector" data-testid="drill-selector">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-white flex items-center gap-3">
          Select Drill
          {playerWeaknesses.length > 0 && (
            <span className="text-xs font-normal px-2 py-0.5 rounded bg-blue-900/50 text-blue-300 border border-blue-500/30">
              Training Focus: {playerWeaknesses.slice(0, 2).join(", ")}
            </span>
          )}
        </h2>
        <div className="flex items-center gap-3">
          {hasActiveFilters && (
            <motion.button
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              onClick={clearFilters}
              className="flex items-center gap-1 px-3 py-1.5 text-sm text-gray-300 hover:text-white bg-gray-800/50 rounded-lg transition-colors"
            >
              <X className="w-4 h-4" />
              Clear
            </motion.button>
          )}

          <button
            onClick={() => setShowRecommendedOnly(!showRecommendedOnly)}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm transition-all ${
              showRecommendedOnly
                ? "bg-yellow-500/20 text-yellow-300 border border-yellow-500/50"
                : "bg-gray-800/50 text-gray-400 hover:text-white border border-transparent"
            }`}
            data-testid="recommended-filter-button"
          >
            <Star className={`w-4 h-4 ${showRecommendedOnly ? "fill-yellow-300" : ""}`} />
            Recommended
          </button>

          <button
            onClick={() => setShowFilters(!showFilters)}
            aria-label="Toggle filters"
            title="Toggle filters"
            className={`p-2 rounded-lg transition-colors ${
              showFilters
                ? "bg-blue-600 text-white"
                : "bg-gray-800/50 text-gray-300 hover:text-white"
            }`}
            data-testid="filter-toggle-button"
          >
            <Filter className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Search & Filters */}
      <AnimatePresence>
        {showFilters && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="overflow-hidden mb-6"
          >
            {/* Search Input */}
            <div className="relative mb-4">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search drills by name or stat..."
                className="w-full pl-10 pr-4 py-3 bg-gray-800/60 border border-gray-700/50 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all"
                data-testid="drill-search-input"
              />
            </div>

            {/* Category Pills */}
            <div className="flex flex-wrap gap-2">
              {Object.entries(CATEGORY_CONFIG).map(([key, config]) => {
                const isActive = activeCategory === key;
                return (
                  <motion.button
                    key={key}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => handleCategoryClick(key as DrillCategory)}
                    className={`flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium transition-all ${
                      isActive
                        ? `bg-gradient-to-r ${config.color} text-white shadow-lg`
                        : "bg-gray-800/60 text-gray-300 hover:bg-gray-700/60"
                    }`}
                    data-testid={`drill-category-${key.toLowerCase()}`}
                  >
                    {config.icon}
                    {config.label}
                  </motion.button>
                );
              })}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Results Count */}
      <div className="text-sm text-gray-400 mb-4 flex justify-between items-center">
        <span>
          {loading
            ? "Loading..."
            : `${filteredDrills.length} drill${filteredDrills.length !== 1 ? "s" : ""} available`}
        </span>
      </div>

      {/* Error State */}
      {error && (
        <div className="p-4 mb-4 bg-red-900/30 border border-red-500/30 rounded-xl text-red-300 text-center">
          {error}
        </div>
      )}

      {/* Drill Grid */}
      <motion.div
        layout
        className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
      >
        <AnimatePresence mode="popLayout">
          {!loading &&
            filteredDrills.map((drill, index) => (
              <motion.div
                key={drill.name}
                layout
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.8 }}
                transition={{ delay: index * 0.05 }}
                data-testid={`drill-card-${drill.name}`}
              >
                <DrillCard3D
                  drill={drill}
                  isSelected={selectedDrill?.name === drill.name}
                  isRecommended={isDrillRecommended(drill)}
                  onSelect={onDrillSelect}
                />
              </motion.div>
            ))}
        </AnimatePresence>
      </motion.div>

      {/* Empty State */}
      {!loading && filteredDrills.length === 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="flex flex-col items-center justify-center py-16 text-gray-400"
        >
          <Dumbbell className="w-16 h-16 mb-4 opacity-30" />
          <p className="text-lg">No drills found</p>
          <p className="text-sm mt-1">Try adjusting your filters</p>
        </motion.div>
      )}

      {/* Loading Skeleton */}
      {loading && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div key={i} className="w-64 h-80 rounded-xl bg-gray-800/40 animate-pulse" />
          ))}
        </div>
      )}
    </div>
  );
};

export default DrillSelector;
