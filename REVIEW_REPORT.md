# Code Review Report

**To:** cweir45@gmail.com

## Findings

### backend/app/core/redis_cache.py
- **Line:** 56
- **Error:** Security Risk: return hashlib.md5(lineup_str.encode()).hexdigest()[:12]
- **Proposed Solve:**
  ```
  Replace weak hashing algorithm (md5) with a stronger one like sha256.
  ```

### backend/app/services/database/optimizer.py
- **Line:** 56
- **Error:** Security Risk: return hashlib.md5(key_str.encode()).hexdigest()
- **Proposed Solve:**
  ```
  Replace weak hashing algorithm (md5) with a stronger one like sha256.
  ```

### backend/app/services/enhanced_chemistry_service.py
- **Line:** 49
- **Error:** Security Risk: return hashlib.md5(lineup_string.encode()).hexdigest()[:12]
- **Proposed Solve:**
  ```
  Replace weak hashing algorithm (md5) with a stronger one like sha256.
  ```

### frontend/src/components/3d/FieldVisualizer.tsx
- **Line:** 9
- **Error:** Missing JSDoc for exported const 'FieldVisualizer'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/3d/PlayAnimator.tsx
- **Line:** 28
- **Error:** Production Console Log: console.log("Animating pass from", qbPosition, "to", receiverEnd);
- **Proposed Solve:**
  ```
  Remove `console.log()` call used for debugging.
  ```

### frontend/src/components/3d/PlayAnimator.tsx
- **Line:** 39
- **Error:** Production Console Log: console.log("Animating run from", rbStart, "to", rbEnd);
- **Proposed Solve:**
  ```
  Remove `console.log()` call used for debugging.
  ```

### frontend/src/components/3d/PlayAnimator.tsx
- **Line:** 45
- **Error:** Production Console Log: console.log("Animating kickoff return for", returnYards, "yards");
- **Proposed Solve:**
  ```
  Remove `console.log()` call used for debugging.
  ```

### frontend/src/components/3d/PlayerCharacter.tsx
- **Line:** 13
- **Error:** Missing JSDoc for exported const 'PlayerCharacter'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/3d/SceneContainer.tsx
- **Line:** 7
- **Error:** Missing JSDoc for exported const 'SceneContainer'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/ErrorBoundary.tsx
- **Line:** 32
- **Error:** Missing JSDoc for exported interface 'ErrorBoundaryProps'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/ErrorBoundary.tsx
- **Line:** 57
- **Error:** Missing JSDoc for exported interface 'FallbackProps'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/FieldView.tsx
- **Line:** 6
- **Error:** Missing JSDoc for exported const 'FieldView'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/GameClock.tsx
- **Line:** 4
- **Error:** Missing JSDoc for exported const 'GameClock'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/PlayByPlayFeed.tsx
- **Line:** 5
- **Error:** Missing JSDoc for exported const 'PlayByPlayFeed'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/ScoreBoard.tsx
- **Line:** 4
- **Error:** Missing JSDoc for exported const 'ScoreBoard'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/coaching/CoachSettings.tsx
- **Line:** 63
- **Error:** Production Alert: alert("Settings saved!");
- **Proposed Solve:**
  ```
  Remove `alert()` call used for debugging.
  ```

### frontend/src/components/coaching/CoachSettings.tsx
- **Line:** 67
- **Error:** Production Alert: alert("Failed to save.");
- **Proposed Solve:**
  ```
  Remove `alert()` call used for debugging.
  ```

### frontend/src/components/coaching/CoachingTree.tsx
- **Line:** 28
- **Error:** Missing JSDoc for exported const 'CoachingTree'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/coaching/GameplanDashboard.tsx
- **Line:** 6
- **Error:** Missing JSDoc for exported const 'GameplanDashboard'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/common/FeedbackWidget.tsx
- **Line:** 95
- **Error:** Production Console Log: console.log("Research complete:", res.data);
- **Proposed Solve:**
  ```
  Remove `console.log()` call used for debugging.
  ```

### frontend/src/components/common/FeedbackWidget.tsx
- **Line:** 135
- **Error:** Production Alert: alert("❌ Failed to export tasks. Check console for details.");
- **Proposed Solve:**
  ```
  Remove `alert()` call used for debugging.
  ```

### frontend/src/components/common/FeedbackWidget.tsx
- **Line:** 161
- **Error:** Production Alert: alert(
- **Proposed Solve:**
  ```
  Remove `alert()` call used for debugging.
  ```

### frontend/src/components/common/FeedbackWidget.tsx
- **Line:** 168
- **Error:** Production Alert: alert("❌ Failed to generate plan. Check console for details.");
- **Proposed Solve:**
  ```
  Remove `alert()` call used for debugging.
  ```

### frontend/src/components/debug/PhysicsDebugOverlay.tsx
- **Line:** 17
- **Error:** Missing JSDoc for exported const 'PhysicsDebugOverlay'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/dev/TraitManager.tsx
- **Line:** 12
- **Error:** Missing JSDoc for exported const 'TraitManager'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/draft/DraftAssistant.tsx
- **Line:** 47
- **Error:** Missing JSDoc for exported const 'DraftAssistant'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/draft/FeedbackCollector.tsx
- **Line:** 10
- **Error:** Missing JSDoc for exported interface 'FeedbackData'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/draft/FeedbackCollector.tsx
- **Line:** 17
- **Error:** Missing JSDoc for exported const 'FeedbackCollector'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/draft/GenesisReveal.tsx
- **Line:** 13
- **Error:** Missing JSDoc for exported const 'GenesisReveal'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/draft/GpsSpeedViz.tsx
- **Line:** 9
- **Error:** Missing JSDoc for exported const 'GpsSpeedViz'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/draft/TradePhone.tsx
- **Line:** 11
- **Error:** Missing JSDoc for exported const 'TradePhone'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/draft/WarRoomTicker.tsx
- **Line:** 12
- **Error:** Missing JSDoc for exported const 'WarRoomTicker'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/game/CoachingWidget.tsx
- **Line:** 15
- **Error:** Missing JSDoc for exported const 'CoachingWidget'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/game/CrowdNoiseMeter.tsx
- **Line:** 10
- **Error:** Missing JSDoc for exported type 'CrowdNoiseLevel'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/game/CrowdNoiseMeter.tsx
- **Line:** 18
- **Error:** Missing JSDoc for exported const 'CrowdNoiseMeter'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/game/FieldCanvas.tsx
- **Line:** 16
- **Error:** Missing JSDoc for exported interface 'FieldCanvasRef'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/game/FieldCanvas.tsx
- **Line:** 30
- **Error:** Missing JSDoc for exported const 'FieldCanvas'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/game/GameCanvas.tsx
- **Line:** 68
- **Error:** Missing JSDoc for exported const 'GameCanvas'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/game/GameStats.tsx
- **Line:** 17
- **Error:** Missing JSDoc for exported const 'GameStats'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/game/MomentumIndicator.tsx
- **Line:** 11
- **Error:** Missing JSDoc for exported const 'MomentumIndicator'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/game/ReplayScrubber.tsx
- **Line:** 10
- **Error:** Missing JSDoc for exported const 'ReplayScrubber'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/game/WeatherWidget.tsx
- **Line:** 10
- **Error:** Missing JSDoc for exported const 'WeatherWidget'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/history/LogoTimeline.tsx
- **Line:** 19
- **Error:** Missing JSDoc for exported const 'LogoTimeline'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/immersive/BroadcastPanel.tsx
- **Line:** 14
- **Error:** Missing JSDoc for exported function 'BroadcastPanel'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/immersive/SpotlightButton.tsx
- **Line:** 7
- **Error:** Missing JSDoc for exported type 'SpotlightButtonProps'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/immersive/SpotlightButton.tsx
- **Line:** 11
- **Error:** Missing JSDoc for exported function 'SpotlightButton'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/immersive/TiltCard.tsx
- **Line:** 15
- **Error:** Missing JSDoc for exported function 'TiltCard'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/medical/BodyMap.tsx
- **Line:** 53
- **Error:** Missing JSDoc for exported const 'BodyMap'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/medical/TreatmentModal.tsx
- **Line:** 13
- **Error:** Missing JSDoc for exported const 'TreatmentModal'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/news/NewsFeedWidget.tsx
- **Line:** 36
- **Error:** Missing JSDoc for exported function 'NewsFeedWidget'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/news/StorylineTracker.tsx
- **Line:** 68
- **Error:** Missing JSDoc for exported function 'StorylineTracker'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/news/WeeklyRecapModal.tsx
- **Line:** 69
- **Error:** Missing JSDoc for exported function 'WeeklyRecapModal'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/offseason/DraftBoard.tsx
- **Line:** 19
- **Error:** Missing JSDoc for exported const 'DraftBoard'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/offseason/DraftTicker.tsx
- **Line:** 9
- **Error:** Missing JSDoc for exported const 'DraftTicker'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/offseason/OffseasonTimeline.tsx
- **Line:** 18
- **Error:** Missing JSDoc for exported const 'OffseasonTimeline'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/offseason/PlayerProgression.tsx
- **Line:** 14
- **Error:** Missing JSDoc for exported const 'PlayerProgression'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/offseason/SalaryCapWidget.tsx
- **Line:** 9
- **Error:** Missing JSDoc for exported const 'SalaryCapWidget'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/offseason/TeamNeeds.tsx
- **Line:** 9
- **Error:** Missing JSDoc for exported const 'TeamNeeds'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/offseason/TradeModal.tsx
- **Line:** 14
- **Error:** Missing JSDoc for exported const 'TradeModal'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/playbook/FamiliarityBar.tsx
- **Line:** 10
- **Error:** Missing JSDoc for exported const 'FamiliarityBar'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/player/ArchetypeBadge.tsx
- **Line:** 11
- **Error:** Missing JSDoc for exported const 'ArchetypeBadge'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/player/PlayerBackstoryModal.tsx
- **Line:** 13
- **Error:** Missing JSDoc for exported const 'PlayerBackstoryModal'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/scouting/ScoutingReportModal.tsx
- **Line:** 14
- **Error:** Missing JSDoc for exported const 'ScoutingReportModal'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/season/LeagueLeaders.tsx
- **Line:** 14
- **Error:** Missing JSDoc for exported const 'LeagueLeaders'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/season/NewsFeed.tsx
- **Line:** 26
- **Error:** Missing JSDoc for exported interface 'NewsItem'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/season/NewsFeed.tsx
- **Line:** 36
- **Error:** Missing JSDoc for exported interface 'NewsResponse'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/season/NewsFeed.tsx
- **Line:** 88
- **Error:** Missing JSDoc for exported const 'NewsFeed'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/season/QuickActions.tsx
- **Line:** 17
- **Error:** Missing JSDoc for exported const 'QuickActions'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/season/SeasonSummaryCard.tsx
- **Line:** 22
- **Error:** Missing JSDoc for exported const 'SeasonSummaryCard'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/shared/TraitBadge.tsx
- **Line:** 11
- **Error:** Missing JSDoc for exported const 'TraitBadge'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/skills/ConnectionLine.tsx
- **Line:** 13
- **Error:** Missing JSDoc for exported const 'ConnectionLine'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/skills/SkillNode3D.tsx
- **Line:** 47
- **Error:** Missing JSDoc for exported const 'SkillNode3D'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/skills/SkillTreeCanvas.tsx
- **Line:** 17
- **Error:** Missing JSDoc for exported const 'SkillTreeCanvas'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/skills/SkillsOverlay.tsx
- **Line:** 13
- **Error:** Missing JSDoc for exported const 'SkillsOverlay'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/skills/StarfieldBackground.tsx
- **Line:** 6
- **Error:** Missing JSDoc for exported const 'StarfieldBackground'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/trades/DraggableAsset.tsx
- **Line:** 175
- **Error:** Missing JSDoc for exported const 'DraggableAsset'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/trades/DroppableZone.tsx
- **Line:** 19
- **Error:** Missing JSDoc for exported const 'DroppableZone'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/trades/PendingOffers.tsx
- **Line:** 11
- **Error:** Missing JSDoc for exported const 'PendingOffers'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/trades/PendingOffers.tsx
- **Line:** 40
- **Error:** Production Alert: alert("Failed to process offer");
- **Proposed Solve:**
  ```
  Remove `alert()` call used for debugging.
  ```

### frontend/src/components/trades/TradeAnalyzer.tsx
- **Line:** 19
- **Error:** Missing JSDoc for exported const 'TradeAnalyzer'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/trades/TradeBlock.tsx
- **Line:** 16
- **Error:** Missing JSDoc for exported const 'TradeBlock'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/trades/TradeCenter.tsx
- **Line:** 20
- **Error:** Missing JSDoc for exported const 'TradeCenter'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/trades/TradeNegotiator.tsx
- **Line:** 32
- **Error:** Missing JSDoc for exported const 'TradeNegotiator'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/trades/TradeNegotiator.tsx
- **Line:** 460
- **Error:** Production Alert: alert(result.message); // Replace with nice toast later
- **Proposed Solve:**
  ```
  Remove `alert()` call used for debugging.
  ```

### frontend/src/components/trades/TradeNegotiator.tsx
- **Line:** 463
- **Error:** Production Alert: alert("Failed to submit offer"); // Replace with nice toast later
- **Proposed Solve:**
  ```
  Remove `alert()` call used for debugging.
  ```

### frontend/src/components/training/CoachingStyleDial.tsx
- **Line:** 11
- **Error:** Missing JSDoc for exported const 'CoachingStyleDial'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/training/CoachingStylePicker.tsx
- **Line:** 40
- **Error:** Missing JSDoc for exported const 'CoachingStylePicker'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/training/DrillCard.tsx
- **Line:** 10
- **Error:** Missing JSDoc for exported const 'DrillCard'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/training/DrillCard3D.tsx
- **Line:** 14
- **Error:** Missing JSDoc for exported const 'DrillCard3D'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/training/DrillSelector.tsx
- **Line:** 51
- **Error:** Missing JSDoc for exported const 'DrillSelector'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/training/PlayerProgressChart.tsx
- **Line:** 52
- **Error:** Missing JSDoc for exported const 'PlayerProgressChart'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/training/TrainingSessionResult.tsx
- **Line:** 11
- **Error:** Missing JSDoc for exported const 'TrainingSessionResult'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/training/WeeklyScheduleTimeline.tsx
- **Line:** 11
- **Error:** Missing JSDoc for exported const 'WeeklyScheduleTimeline'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/transitions/transitionVariants.ts
- **Line:** 19
- **Error:** Missing JSDoc for exported const 'pageVariants'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/transitions/transitionVariants.ts
- **Line:** 48
- **Error:** Missing JSDoc for exported const 'slideVariants'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/transitions/transitionVariants.ts
- **Line:** 72
- **Error:** Missing JSDoc for exported const 'fadeBlurVariants'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/transitions/transitionVariants.ts
- **Line:** 96
- **Error:** Missing JSDoc for exported const 'transitionVariants'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/trophy/TrophyAssets.tsx
- **Line:** 29
- **Error:** Missing JSDoc for exported const 'LombardiTrophy'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/trophy/TrophyAssets.tsx
- **Line:** 68
- **Error:** Missing JSDoc for exported const 'MvpTrophy'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/trophy/TrophyAssets.tsx
- **Line:** 92
- **Error:** Missing JSDoc for exported const 'DivisionTitleTrophy'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/trophy/TrophyCaseScene.tsx
- **Line:** 7
- **Error:** Missing JSDoc for exported const 'TrophyCaseScene'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/ui/Badge.tsx
- **Line:** 11
- **Error:** Missing JSDoc for exported const 'Badge'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/ui/Card.tsx
- **Line:** 11
- **Error:** Missing JSDoc for exported const 'Card'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/ui/Card.tsx
- **Line:** 19
- **Error:** Missing JSDoc for exported const 'CardHeader'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/ui/Card.tsx
- **Line:** 29
- **Error:** Missing JSDoc for exported const 'CardTitle'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/ui/Card.tsx
- **Line:** 39
- **Error:** Missing JSDoc for exported const 'CardContent'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/ui/Card.tsx
- **Line:** 49
- **Error:** Missing JSDoc for exported const 'CardFooter'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/ui/ChemistryBadge.tsx
- **Line:** 15
- **Error:** Missing JSDoc for exported const 'ChemistryBadge'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/ui/DraggableCard.tsx
- **Line:** 22
- **Error:** Missing JSDoc for exported const 'DraggableCard'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/ui/EnhancedPlayerProfile.tsx
- **Line:** 152
- **Error:** Missing JSDoc for exported const 'EnhancedPlayerProfile'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/ui/LoadingSpinner.tsx
- **Line:** 10
- **Error:** Missing JSDoc for exported const 'LoadingSpinner'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/ui/PlayerCard.tsx
- **Line:** 19
- **Error:** Missing JSDoc for exported const 'PlayerCard'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/ui/PlayerModal.tsx
- **Line:** 10
- **Error:** Missing JSDoc for exported const 'PlayerModal'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/ui/PrimeCard.tsx
- **Line:** 14
- **Error:** Missing JSDoc for exported const 'PrimeCard'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/ui/Sidebar.tsx
- **Line:** 13
- **Error:** Missing JSDoc for exported const 'Sidebar'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/components/ui/TraitNotification.tsx
- **Line:** 4
- **Error:** Missing JSDoc for exported interface 'TraitNotificationProps'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/config/SkillTreeConfig.ts
- **Line:** 1
- **Error:** Missing JSDoc for exported interface 'SkillTreeNodeConfig'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/config/SkillTreeConfig.ts
- **Line:** 9
- **Error:** Missing JSDoc for exported type 'SkillTreeLayout'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/config/SkillTreeConfig.ts
- **Line:** 14
- **Error:** Missing JSDoc for exported const 'QB_SKILL_TREE'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/config/SkillTreeConfig.ts
- **Line:** 85
- **Error:** Missing JSDoc for exported const 'SKILL_TREE_LAYOUTS'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/config/SkillTreeConfig.ts
- **Line:** 93
- **Error:** Missing JSDoc for exported const 'ICON_KEYS'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/constants/index.ts
- **Line:** 9
- **Error:** Missing JSDoc for exported const 'DEFAULT_PAGE_SIZE'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/constants/index.ts
- **Line:** 10
- **Error:** Missing JSDoc for exported const 'MAX_PAGE_SIZE'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/constants/index.ts
- **Line:** 13
- **Error:** Missing JSDoc for exported const 'REGULAR_SEASON_WEEKS'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/constants/index.ts
- **Line:** 14
- **Error:** Missing JSDoc for exported const 'PLAYOFF_WEEKS'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/constants/index.ts
- **Line:** 17
- **Error:** Missing JSDoc for exported const 'STANDINGS_REFRESH_INTERVAL'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/constants/index.ts
- **Line:** 18
- **Error:** Missing JSDoc for exported const 'GAME_REFRESH_INTERVAL'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/constants/index.ts
- **Line:** 21
- **Error:** Missing JSDoc for exported const 'DEFAULT_LEADERS_COUNT'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/constants/index.ts
- **Line:** 24
- **Error:** Missing JSDoc for exported const 'QUERY_KEYS'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/context/AudioContext.tsx
- **Line:** 27
- **Error:** Missing JSDoc for exported const 'AudioProvider'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/context/AudioTypes.ts
- **Line:** 3
- **Error:** Missing JSDoc for exported const 'STORAGE_KEY'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/context/AudioTypes.ts
- **Line:** 5
- **Error:** Missing JSDoc for exported interface 'AudioPreferences'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/context/AudioTypes.ts
- **Line:** 10
- **Error:** Missing JSDoc for exported interface 'AudioContextType'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/context/AudioTypes.ts
- **Line:** 21
- **Error:** Missing JSDoc for exported const 'AudioContext'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/context/ThemeContext.ts
- **Line:** 3
- **Error:** Missing JSDoc for exported interface 'TeamTheme'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/context/ThemeContext.ts
- **Line:** 9
- **Error:** Missing JSDoc for exported interface 'BasicTeamInfo'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/context/ThemeContext.ts
- **Line:** 15
- **Error:** Missing JSDoc for exported interface 'ThemeContextType'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/context/ThemeContext.ts
- **Line:** 21
- **Error:** Missing JSDoc for exported const 'ThemeContext'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/context/ThemeContext.tsx
- **Line:** 3
- **Error:** Missing JSDoc for exported interface 'TeamTheme'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/context/ThemeContext.tsx
- **Line:** 9
- **Error:** Missing JSDoc for exported interface 'BasicTeamInfo'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/context/ThemeContext.tsx
- **Line:** 15
- **Error:** Missing JSDoc for exported interface 'ThemeContextType'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/context/ThemeContext.tsx
- **Line:** 21
- **Error:** Missing JSDoc for exported const 'ThemeContext'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/context/ThemeProvider.tsx
- **Line:** 8
- **Error:** Missing JSDoc for exported const 'ThemeProvider'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/context/useAudio.ts
- **Line:** 5
- **Error:** Missing JSDoc for exported const 'useAudio'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/context/useTheme.ts
- **Line:** 4
- **Error:** Missing JSDoc for exported const 'useTheme'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/hooks/useAnnotationList.ts
- **Line:** 18
- **Error:** Missing JSDoc for exported interface 'AIResearch'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/hooks/useAnnotationList.ts
- **Line:** 25
- **Error:** Missing JSDoc for exported interface 'ElementMetadata'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/hooks/useAnnotationList.ts
- **Line:** 39
- **Error:** Missing JSDoc for exported interface 'Annotation'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/hooks/useAnnotationList.ts
- **Line:** 58
- **Error:** Missing JSDoc for exported function 'useAnnotationList'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/hooks/useLivingWorld.ts
- **Line:** 14
- **Error:** Missing JSDoc for exported interface 'LivingNewsItem'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/hooks/useLivingWorld.ts
- **Line:** 28
- **Error:** Missing JSDoc for exported interface 'LivingNewsFeedResponse'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/hooks/useLivingWorld.ts
- **Line:** 36
- **Error:** Missing JSDoc for exported interface 'WeeklyRecap'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/hooks/useLivingWorld.ts
- **Line:** 48
- **Error:** Missing JSDoc for exported interface 'Storyline'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/hooks/useLivingWorld.ts
- **Line:** 58
- **Error:** Missing JSDoc for exported function 'useLivingNews'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/hooks/useLivingWorld.ts
- **Line:** 101
- **Error:** Missing JSDoc for exported function 'useWeeklyRecap'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/hooks/useLivingWorld.ts
- **Line:** 163
- **Error:** Missing JSDoc for exported function 'useStorylines'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/hooks/useLoaderData.ts
- **Line:** 25
- **Error:** Missing JSDoc for exported function 'useSeasonDashboardData'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/hooks/useLoaderData.ts
- **Line:** 30
- **Error:** Missing JSDoc for exported interface 'OffseasonDashboardLoaderData'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/hooks/useLoaderData.ts
- **Line:** 36
- **Error:** Missing JSDoc for exported function 'useOffseasonDashboardData'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/hooks/useLoaderData.ts
- **Line:** 41
- **Error:** Missing JSDoc for exported interface 'DraftRoomLoaderData'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/hooks/useLoaderData.ts
- **Line:** 47
- **Error:** Missing JSDoc for exported function 'useDraftRoomData'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/hooks/useLoaderData.ts
- **Line:** 52
- **Error:** Missing JSDoc for exported interface 'FrontOfficeLoaderData'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/hooks/useLoaderData.ts
- **Line:** 60
- **Error:** Missing JSDoc for exported function 'useFrontOfficeData'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/hooks/useLoaderData.ts
- **Line:** 65
- **Error:** Missing JSDoc for exported interface 'DepthChartLoaderData'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/hooks/useLoaderData.ts
- **Line:** 71
- **Error:** Missing JSDoc for exported function 'useDepthChartData'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/hooks/useLoaderData.ts
- **Line:** 76
- **Error:** Missing JSDoc for exported interface 'TeamSelectionLoaderData'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/hooks/useLoaderData.ts
- **Line:** 80
- **Error:** Missing JSDoc for exported function 'useTeamSelectionData'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/hooks/useWebSocket.ts
- **Line:** 37
- **Error:** Production Console Log: console.log("Game state synchronized");
- **Proposed Solve:**
  ```
  Remove `console.log()` call used for debugging.
  ```

### frontend/src/hooks/useWebSocket.ts
- **Line:** 55
- **Error:** Production Console Log: console.log("WebSocket connected");
- **Proposed Solve:**
  ```
  Remove `console.log()` call used for debugging.
  ```

### frontend/src/hooks/useWebSocket.ts
- **Line:** 155
- **Error:** Production Console Log: console.log(`WebSocket disconnected. Reconnecting in ${delay}ms...`);
- **Proposed Solve:**
  ```
  Remove `console.log()` call used for debugging.
  ```

### frontend/src/pages/Dashboard.tsx
- **Line:** 30
- **Error:** Production Console Log: console.log("No active season found");
- **Proposed Solve:**
  ```
  Remove `console.log()` call used for debugging.
  ```

### frontend/src/pages/DepthChart.tsx
- **Line:** 7
- **Error:** Missing JSDoc for exported const 'DepthChart'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/pages/DepthChart.tsx
- **Line:** 91
- **Error:** Production Alert: alert("Depth chart saved successfully!");
- **Proposed Solve:**
  ```
  Remove `alert()` call used for debugging.
  ```

### frontend/src/pages/DepthChart.tsx
- **Line:** 94
- **Error:** Production Alert: alert("Failed to save depth chart.");
- **Proposed Solve:**
  ```
  Remove `alert()` call used for debugging.
  ```

### frontend/src/pages/DraftRoom.tsx
- **Line:** 28
- **Error:** Missing JSDoc for exported const 'DraftRoom'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/pages/FrontOffice.tsx
- **Line:** 7
- **Error:** Missing JSDoc for exported const 'FrontOffice'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/pages/FrontOffice_Baseline.tsx
- **Line:** 4
- **Error:** Missing JSDoc for exported const 'FrontOffice_Baseline'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/pages/LiveSim.tsx
- **Line:** 20
- **Error:** Missing JSDoc for exported const 'LiveSim'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/pages/LiveSim.tsx
- **Line:** 46
- **Error:** Production Console Log: console.log("Live simulation started - receiving WebSocket updates");
- **Proposed Solve:**
  ```
  Remove `console.log()` call used for debugging.
  ```

### frontend/src/pages/LiveSim.tsx
- **Line:** 58
- **Error:** Production Console Log: console.log("Simulation stopped");
- **Proposed Solve:**
  ```
  Remove `console.log()` call used for debugging.
  ```

### frontend/src/pages/LiveSim.tsx
- **Line:** 185
- **Error:** Production Console Log: onPlayComplete={() => console.log("Play complete")}
- **Proposed Solve:**
  ```
  Remove `console.log()` call used for debugging.
  ```

### frontend/src/pages/MedicalCenter.tsx
- **Line:** 6
- **Error:** Missing JSDoc for exported const 'MedicalCenter'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/pages/MedicalCenter.tsx
- **Line:** 26
- **Error:** Production Console Log: console.log(`Applied ${treatment} to ${selectedPart}`);
- **Proposed Solve:**
  ```
  Remove `console.log()` call used for debugging.
  ```

### frontend/src/pages/Playbook.tsx
- **Line:** 6
- **Error:** Missing JSDoc for exported const 'Playbook'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/pages/SeasonDashboard.tsx
- **Line:** 73
- **Error:** Production Console Log: console.log("No active season found");
- **Proposed Solve:**
  ```
  Remove `console.log()` call used for debugging.
  ```

### frontend/src/pages/SkillsPage.tsx
- **Line:** 15
- **Error:** Missing JSDoc for exported const 'SkillsPage'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/pages/SkillsPage.tsx
- **Line:** 71
- **Error:** Production Console Log: console.log("Toggle equip not fully supported yet");
- **Proposed Solve:**
  ```
  Remove `console.log()` call used for debugging.
  ```

### frontend/src/pages/TrainingCenter.tsx
- **Line:** 25
- **Error:** Missing JSDoc for exported const 'TrainingCenter'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/pages/TrainingCenter.tsx
- **Line:** 91
- **Error:** Production Alert: alert("Training session failed. Please try again.");
- **Proposed Solve:**
  ```
  Remove `alert()` call used for debugging.
  ```

### frontend/src/services/ImageGenService.ts
- **Line:** 14
- **Error:** Missing JSDoc for exported interface 'GeneratedImage'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/services/ImageGenService.ts
- **Line:** 69
- **Error:** Production Console Log: console.log("[ImageGenService] Generating image with prompt:", prompt);
- **Proposed Solve:**
  ```
  Remove `console.log()` call used for debugging.
  ```

### frontend/src/services/ImageGenService.ts
- **Line:** 74
- **Error:** Missing JSDoc for exported const 'ImageGenService'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/services/api.ts
- **Line:** 13
- **Error:** Missing JSDoc for exported interface 'Team'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/services/api.ts
- **Line:** 28
- **Error:** Missing JSDoc for exported interface 'Player'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/services/api.ts
- **Line:** 48
- **Error:** Missing JSDoc for exported interface 'PlayerStats'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/services/api.ts
- **Line:** 58
- **Error:** Missing JSDoc for exported interface 'ChemistryMetadata'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/services/api.ts
- **Line:** 75
- **Error:** Missing JSDoc for exported interface 'PaginatedResponse'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/services/api.ts
- **Line:** 83
- **Error:** Missing JSDoc for exported const 'api'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/services/api.ts
- **Line:** 174
- **Error:** Missing JSDoc for exported interface 'TraitInfo'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/services/api.ts
- **Line:** 180
- **Error:** Missing JSDoc for exported interface 'PersonalityInfo'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/services/api.ts
- **Line:** 187
- **Error:** Missing JSDoc for exported interface 'EnhancedPlayerProfile'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/services/api.ts
- **Line:** 220
- **Error:** Missing JSDoc for exported interface 'NewsItem'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/services/api.ts
- **Line:** 230
- **Error:** Missing JSDoc for exported interface 'NewsResponse'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/services/api.ts
- **Line:** 236
- **Error:** Missing JSDoc for exported interface 'InjuryReport'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/services/api.ts
- **Line:** 243
- **Error:** Missing JSDoc for exported interface 'InjuryReportResponse'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/services/draft.ts
- **Line:** 4
- **Error:** Missing JSDoc for exported interface 'HistoricalComparison'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/services/draft.ts
- **Line:** 11
- **Error:** Missing JSDoc for exported interface 'RosterGapAnalysis'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/services/draft.ts
- **Line:** 19
- **Error:** Missing JSDoc for exported interface 'AlternativePick'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/services/draft.ts
- **Line:** 29
- **Error:** Missing JSDoc for exported interface 'DraftSuggestionResponse'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/services/draft.ts
- **Line:** 44
- **Error:** Missing JSDoc for exported interface 'DraftSuggestionRequest'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/services/draft.ts
- **Line:** 51
- **Error:** Missing JSDoc for exported const 'draftService'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/services/errorLogger.ts
- **Line:** 295
- **Error:** Production Console Log: if (context) console.log("Context:", context);
- **Proposed Solve:**
  ```
  Remove `console.log()` call used for debugging.
  ```

### frontend/src/services/physicsService.ts
- **Line:** 15
- **Error:** Missing JSDoc for exported interface 'PlayerPosition'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/services/physicsService.ts
- **Line:** 26
- **Error:** Missing JSDoc for exported interface 'BallPosition'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/services/physicsService.ts
- **Line:** 34
- **Error:** Missing JSDoc for exported interface 'PhysicsFrame'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/services/physicsService.ts
- **Line:** 42
- **Error:** Missing JSDoc for exported interface 'SimulatePlayRequest'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/services/physicsService.ts
- **Line:** 48
- **Error:** Missing JSDoc for exported interface 'SimulatePlayResponse'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/services/physicsService.ts
- **Line:** 57
- **Error:** Missing JSDoc for exported interface 'PhysicsConstants'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/services/physicsService.ts
- **Line:** 66
- **Error:** Missing JSDoc for exported interface 'StreamFrame'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/services/physicsService.ts
- **Line:** 116
- **Error:** Missing JSDoc for exported type 'FrameCallback'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/services/physicsService.ts
- **Line:** 117
- **Error:** Missing JSDoc for exported type 'CompleteCallback'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/services/physicsService.ts
- **Line:** 215
- **Error:** Missing JSDoc for exported const 'physicsStream'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/services/scouting.ts
- **Line:** 35
- **Error:** Missing JSDoc for exported const 'scoutingService'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/services/season.ts
- **Line:** 22
- **Error:** Missing JSDoc for exported const 'seasonApi'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/services/simulation.ts
- **Line:** 4
- **Error:** Missing JSDoc for exported interface 'SimulationStatus'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/services/simulation.ts
- **Line:** 16
- **Error:** Missing JSDoc for exported const 'simulationService'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/services/tradeApi.ts
- **Line:** 37
- **Error:** Missing JSDoc for exported const 'tradeApi'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/services/tradeApi.ts
- **Line:** 137
- **Error:** Production Console Log: console.log("Executing trade proposal:", proposal);
- **Proposed Solve:**
  ```
  Remove `console.log()` call used for debugging.
  ```

### frontend/src/services/tradeApi.ts
- **Line:** 159
- **Error:** Production Console Log: console.log("Getting trade block for:", teamId);
- **Proposed Solve:**
  ```
  Remove `console.log()` call used for debugging.
  ```

### frontend/src/services/tradeApi.ts
- **Line:** 188
- **Error:** Production Console Log: console.log("Removing player from trade block:", playerId);
- **Proposed Solve:**
  ```
  Remove `console.log()` call used for debugging.
  ```

### frontend/src/services/tradeApi.ts
- **Line:** 247
- **Error:** Production Console Log: console.log(`Responded to offer ${offerId} with ${response}`);
- **Proposed Solve:**
  ```
  Remove `console.log()` call used for debugging.
  ```

### frontend/src/services/tradeApi.ts
- **Line:** 260
- **Error:** Production Console Log: console.log("Getting trade history:", seasonId, limit);
- **Proposed Solve:**
  ```
  Remove `console.log()` call used for debugging.
  ```

### frontend/src/services/trainingApi.ts
- **Line:** 73
- **Error:** Missing JSDoc for exported const 'trainingApi'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/services/traitService.ts
- **Line:** 41
- **Error:** Missing JSDoc for exported const 'traitService'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/services/traits.ts
- **Line:** 4
- **Error:** Missing JSDoc for exported const 'traitsApi'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/store/useDebugStore.ts
- **Line:** 42
- **Error:** Missing JSDoc for exported const 'useDebugStore'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/store/useGameStore.ts
- **Line:** 8
- **Error:** Missing JSDoc for exported const 'useGameStore'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/store/usePlayLogStore.ts
- **Line:** 22
- **Error:** Missing JSDoc for exported const 'usePlayLogStore'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/store/useScoreboardStore.ts
- **Line:** 68
- **Error:** Missing JSDoc for exported const 'useScoreboardStore'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/store/useSettingsStore.ts
- **Line:** 13
- **Error:** Missing JSDoc for exported const 'useSettingsStore'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/store/useSimulationStore.ts
- **Line:** 47
- **Error:** Missing JSDoc for exported const 'useSimulationStore'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/styles/motion.ts
- **Line:** 18
- **Error:** Missing JSDoc for exported const 't'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/styles/motion.ts
- **Line:** 31
- **Error:** Missing JSDoc for exported const 'routeVariants'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/styles/motion.ts
- **Line:** 38
- **Error:** Missing JSDoc for exported const 'fadeUp'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/styles/motion.ts
- **Line:** 44
- **Error:** Missing JSDoc for exported const 'slideFromRight'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/styles/motion.ts
- **Line:** 51
- **Error:** Missing JSDoc for exported const 'slideFromLeft'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/styles/motion.ts
- **Line:** 58
- **Error:** Missing JSDoc for exported const 'scaleTransition'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/styles/motion.ts
- **Line:** 65
- **Error:** Missing JSDoc for exported const 'staggerContainer'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/styles/motion.ts
- **Line:** 79
- **Error:** Missing JSDoc for exported const 'staggerItem'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/styles/motion.ts
- **Line:** 89
- **Error:** Missing JSDoc for exported const 'cardHover'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/styles/motion.ts
- **Line:** 96
- **Error:** Missing JSDoc for exported const 'listItem'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/api/scouting.ts
- **Line:** 1
- **Error:** Missing JSDoc for exported interface 'ScoutingReport'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/api/scouting.ts
- **Line:** 12
- **Error:** Missing JSDoc for exported interface 'PlayerBackstory'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/api/scouting.ts
- **Line:** 21
- **Error:** Missing JSDoc for exported interface 'ScoutingReportRequest'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/api/scouting.ts
- **Line:** 26
- **Error:** Missing JSDoc for exported interface 'BackstoryRequest'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/archetypes.ts
- **Line:** 1
- **Error:** Missing JSDoc for exported const 'PlayerArchetype'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/archetypes.ts
- **Line:** 11
- **Error:** Missing JSDoc for exported type 'PlayerArchetype'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/archetypes.ts
- **Line:** 13
- **Error:** Missing JSDoc for exported interface 'ArchetypeDefinition'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/archetypes.ts
- **Line:** 22
- **Error:** Missing JSDoc for exported const 'ARCHETYPE_CONFIG'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/combine.ts
- **Line:** 1
- **Error:** Missing JSDoc for exported interface 'CombineResult'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/combine.ts
- **Line:** 23
- **Error:** Missing JSDoc for exported interface 'ProspectWithCombine'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/engine-state.ts
- **Line:** 13
- **Error:** Missing JSDoc for exported interface 'GenesisPlayerState'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/engine-state.ts
- **Line:** 21
- **Error:** Missing JSDoc for exported interface 'GenesisState'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/engine-state.ts
- **Line:** 36
- **Error:** Missing JSDoc for exported interface 'EmpirePlayerXP'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/engine-state.ts
- **Line:** 48
- **Error:** Missing JSDoc for exported interface 'EmpireState'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/engine-state.ts
- **Line:** 58
- **Error:** Missing JSDoc for exported interface 'HiveUnitChemistry'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/engine-state.ts
- **Line:** 69
- **Error:** Missing JSDoc for exported interface 'HiveState'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/engine-state.ts
- **Line:** 80
- **Error:** Missing JSDoc for exported interface 'SocietyMomentumEvent'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/engine-state.ts
- **Line:** 88
- **Error:** Missing JSDoc for exported interface 'SocietyState'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/engine-state.ts
- **Line:** 100
- **Error:** Missing JSDoc for exported interface 'RPGActiveAbility'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/engine-state.ts
- **Line:** 107
- **Error:** Missing JSDoc for exported interface 'RPGTraitActivation'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/engine-state.ts
- **Line:** 114
- **Error:** Missing JSDoc for exported interface 'RPGState'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/engine-state.ts
- **Line:** 125
- **Error:** Missing JSDoc for exported interface 'TypedEngineData'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/engine-state.ts
- **Line:** 134
- **Error:** Missing JSDoc for exported const 'DEFAULT_GENESIS_STATE'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/engine-state.ts
- **Line:** 145
- **Error:** Missing JSDoc for exported const 'DEFAULT_EMPIRE_STATE'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/engine-state.ts
- **Line:** 151
- **Error:** Missing JSDoc for exported const 'DEFAULT_HIVE_STATE'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/engine-state.ts
- **Line:** 158
- **Error:** Missing JSDoc for exported const 'DEFAULT_SOCIETY_STATE'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/engine-state.ts
- **Line:** 166
- **Error:** Missing JSDoc for exported const 'DEFAULT_RPG_STATE'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/engine-state.ts
- **Line:** 173
- **Error:** Missing JSDoc for exported const 'DEFAULT_ENGINE_DATA'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/interaction.ts
- **Line:** 1
- **Error:** Missing JSDoc for exported const 'InteractionOutcome'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/interaction.ts
- **Line:** 11
- **Error:** Missing JSDoc for exported type 'InteractionOutcome'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/interaction.ts
- **Line:** 13
- **Error:** Missing JSDoc for exported interface 'InteractionResult'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/momentum.ts
- **Line:** 1
- **Error:** Missing JSDoc for exported const 'MomentumState'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/momentum.ts
- **Line:** 9
- **Error:** Missing JSDoc for exported type 'MomentumState'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/momentum.ts
- **Line:** 11
- **Error:** Missing JSDoc for exported interface 'TeamMomentum'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/offseason.ts
- **Line:** 3
- **Error:** Missing JSDoc for exported interface 'TeamNeed'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/offseason.ts
- **Line:** 17
- **Error:** Missing JSDoc for exported interface 'Prospect'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/offseason.ts
- **Line:** 38
- **Error:** Missing JSDoc for exported interface 'ScoutingReport'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/offseason.ts
- **Line:** 54
- **Error:** Missing JSDoc for exported interface 'DraftPickSummary'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/offseason.ts
- **Line:** 63
- **Error:** Missing JSDoc for exported interface 'DraftPickDetail'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/offseason.ts
- **Line:** 73
- **Error:** Missing JSDoc for exported interface 'PlayerProgressionResult'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/offseason.ts
- **Line:** 82
- **Error:** Missing JSDoc for exported interface 'SalaryCapData'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/physics.ts
- **Line:** 1
- **Error:** Missing JSDoc for exported interface 'Vector2'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/physics.ts
- **Line:** 6
- **Error:** Missing JSDoc for exported interface 'PlayerFrame'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/physics.ts
- **Line:** 14
- **Error:** Missing JSDoc for exported interface 'BallFrame'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/physics.ts
- **Line:** 20
- **Error:** Missing JSDoc for exported interface 'PhysicsFrame'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/physics.ts
- **Line:** 28
- **Error:** Missing JSDoc for exported interface 'PlayTrajectory'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/playbook.ts
- **Line:** 1
- **Error:** Missing JSDoc for exported const 'FamiliarityLevel'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/playbook.ts
- **Line:** 6
- **Error:** Missing JSDoc for exported type 'FamiliarityLevel'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/playbook.ts
- **Line:** 8
- **Error:** Missing JSDoc for exported interface 'PlaybookFamiliarity'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/playbook.ts
- **Line:** 15
- **Error:** Missing JSDoc for exported interface 'StrategyFamiliarity'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/playbook.ts
- **Line:** 22
- **Error:** Missing JSDoc for exported const 'getFamiliarityLevel'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/playoff.ts
- **Line:** 3
- **Error:** Missing JSDoc for exported const 'PlayoffRound'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/playoff.ts
- **Line:** 10
- **Error:** Missing JSDoc for exported type 'PlayoffRound'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/playoff.ts
- **Line:** 12
- **Error:** Missing JSDoc for exported const 'PlayoffConference'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/playoff.ts
- **Line:** 18
- **Error:** Missing JSDoc for exported type 'PlayoffConference'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/playoff.ts
- **Line:** 20
- **Error:** Missing JSDoc for exported interface 'PlayoffMatchup'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/season.ts
- **Line:** 1
- **Error:** Missing JSDoc for exported const 'SeasonStatus'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/season.ts
- **Line:** 8
- **Error:** Missing JSDoc for exported type 'SeasonStatus'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/season.ts
- **Line:** 10
- **Error:** Missing JSDoc for exported interface 'Season'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/season.ts
- **Line:** 22
- **Error:** Missing JSDoc for exported interface 'GameWeather'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/season.ts
- **Line:** 31
- **Error:** Missing JSDoc for exported const 'GameType'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/season.ts
- **Line:** 39
- **Error:** Missing JSDoc for exported type 'GameType'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/season.ts
- **Line:** 41
- **Error:** Missing JSDoc for exported interface 'Game'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/season.ts
- **Line:** 67
- **Error:** Missing JSDoc for exported interface 'TeamStanding'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/season.ts
- **Line:** 91
- **Error:** Missing JSDoc for exported interface 'WeekSimulationResult'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/season.ts
- **Line:** 97
- **Error:** Missing JSDoc for exported interface 'GameResult'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/season.ts
- **Line:** 106
- **Error:** Missing JSDoc for exported interface 'SingleGameResult'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/season.ts
- **Line:** 115
- **Error:** Missing JSDoc for exported interface 'SeasonSummary'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/season.ts
- **Line:** 123
- **Error:** Missing JSDoc for exported interface 'AwardCandidate'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/season.ts
- **Line:** 132
- **Error:** Missing JSDoc for exported interface 'SeasonAwards'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/simulation.ts
- **Line:** 3
- **Error:** Missing JSDoc for exported interface 'PlayResult'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/stats.ts
- **Line:** 1
- **Error:** Missing JSDoc for exported interface 'PlayerLeader'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/stats.ts
- **Line:** 10
- **Error:** Missing JSDoc for exported interface 'LeagueLeaders'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/trade.ts
- **Line:** 17
- **Error:** Missing JSDoc for exported interface 'TradePlayer'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/trade.ts
- **Line:** 31
- **Error:** Missing JSDoc for exported interface 'TradePick'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/trade.ts
- **Line:** 41
- **Error:** Missing JSDoc for exported interface 'TradeProposal'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/trade.ts
- **Line:** 53
- **Error:** Missing JSDoc for exported interface 'TradeEvaluation'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/trade.ts
- **Line:** 66
- **Error:** Missing JSDoc for exported interface 'IncomingTradeOffer'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/trade.ts
- **Line:** 79
- **Error:** Missing JSDoc for exported interface 'TradeBlockPlayer'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/trade.ts
- **Line:** 90
- **Error:** Missing JSDoc for exported interface 'TradeHistoryItem'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/trade.ts
- **Line:** 104
- **Error:** Missing JSDoc for exported type 'TradeEvaluationResult'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/trade.ts
- **Line:** 105
- **Error:** Missing JSDoc for exported type 'TradeDecision'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/trade.ts
- **Line:** 106
- **Error:** Missing JSDoc for exported type 'TradeOfferStatus'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/trade.ts
- **Line:** 108
- **Error:** Missing JSDoc for exported interface 'TradeOffer'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/trade.ts
- **Line:** 121
- **Error:** Missing JSDoc for exported interface 'TradeOfferDetails'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/training.ts
- **Line:** 1
- **Error:** Missing JSDoc for exported const 'SeasonPhase'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/training.ts
- **Line:** 7
- **Error:** Missing JSDoc for exported type 'SeasonPhase'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/training.ts
- **Line:** 9
- **Error:** Missing JSDoc for exported const 'CoachingStyleType'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/training.ts
- **Line:** 15
- **Error:** Missing JSDoc for exported type 'CoachingStyleType'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/training.ts
- **Line:** 17
- **Error:** Missing JSDoc for exported const 'DrillCategory'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/training.ts
- **Line:** 25
- **Error:** Missing JSDoc for exported type 'DrillCategory'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/training.ts
- **Line:** 27
- **Error:** Missing JSDoc for exported interface 'Drill'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/training.ts
- **Line:** 39
- **Error:** Missing JSDoc for exported interface 'CoachingStyle'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/training.ts
- **Line:** 49
- **Error:** Missing JSDoc for exported interface 'TrainingResult'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/training.ts
- **Line:** 62
- **Error:** Missing JSDoc for exported interface 'ScheduleRecommendation'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/training.ts
- **Line:** 69
- **Error:** Missing JSDoc for exported interface 'WeeklySchedule'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/training.ts
- **Line:** 77
- **Error:** Missing JSDoc for exported interface 'DrillListResponse'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/trait.ts
- **Line:** 1
- **Error:** Missing JSDoc for exported const 'TraitSource'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/trait.ts
- **Line:** 8
- **Error:** Missing JSDoc for exported type 'TraitSource'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/trait.ts
- **Line:** 10
- **Error:** Missing JSDoc for exported const 'TraitEffectType'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/trait.ts
- **Line:** 17
- **Error:** Missing JSDoc for exported type 'TraitEffectType'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/trait.ts
- **Line:** 19
- **Error:** Missing JSDoc for exported interface 'Trait'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/trait.ts
- **Line:** 29
- **Error:** Missing JSDoc for exported interface 'PlayerTrait'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/trait.ts
- **Line:** 37
- **Error:** Missing JSDoc for exported interface 'TraitAssignment'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```

### frontend/src/types/trait.ts
- **Line:** 42
- **Error:** Missing JSDoc for exported interface 'TraitUnlockRequest'
- **Proposed Solve:**
  ```
  Add JSDoc comment block describing the function parameters and return type.
  ```
