# Task 2.6: Visual Regression Testing - Detailed Plan

## Overview

Visual regression testing ensures that the migration from mock data to real API data hasn't broken the UI design, styling, or user experience.

---

## Subtask 2.6.1: Compare Current UI to Mock-Data Version

### Objective

Document and compare the FrontOffice page before and after API integration.

### Steps

#### A. Capture Baseline (Mock Data Version)

- [ ] Check git history for the last commit with mock data
- [ ] Run: `git log --oneline frontend/src/pages/FrontOffice.tsx`
- [ ] Find commit hash before API integration (look for "Update FrontOffice.tsx to fetch real roster data")
- [ ] Create a new branch from that commit:

  ```bash
  git checkout -b visual-test-baseline <commit-hash>
  ```

- [ ] Start frontend: `npm run dev`
- [ ] Navigate to Front Office page
- [ ] Take screenshots:
  - Full page view
  - Zoomed view of player cards (first 6 cards)
  - Roster header section
- [ ] Save screenshots to: `frontend/docs/screenshots/baseline/`
- [ ] Return to main branch: `git checkout main`

#### B. Capture Current (Real Data Version)

- [ ] Ensure backend is running with seeded data
- [ ] Ensure frontend is running
- [ ] Navigate to Front Office page
- [ ] Take identical screenshots:
  - Full page view (same zoom level)
  - Zoomed view of player cards
  - Roster header section
- [ ] Save screenshots to: `frontend/docs/screenshots/current/`

#### C. Visual Comparison Checklist

- [ ] **Header Section:**
  - Font size matches
  - Color scheme identical
  - Team name placement correct
  - Cap space display unchanged
- [ ] **Roster Grid:**
  - Grid layout matches (columns, gaps)
  - Card spacing identical
  - Scroll behavior works
- [ ] **Player Cards:**
  - Card dimensions same
  - Border styling unchanged
  - Shadow effects present
  - Hover states work
- [ ] **Typography:**
  - Font families match
  - Font weights consistent
  - Letter spacing identical
- [ ] **Colors:**
  - Background colors unchanged
  - Text colors match
  - Accent colors (cyan) identical
  - Glass panel effects consistent

#### D. Document Differences

- [ ] Create comparison report: `frontend/docs/visual-regression-report.md`
- [ ] List any visual differences found
- [ ] Categorize as:
  - ✅ Expected (e.g., different player names)
  - ⚠️ Acceptable (minor shifts due to content)
  - ❌ Bug (styling broken)

---

## Subtask 2.6.2: Verify Styling Remains Consistent

### 2.6.2 Objective

Ensure all CSS classes and styles are applied correctly with real data.

### 2.6.2 Steps

#### A. Inspect Element Styles

- [x] Open browser DevTools (F12)
- [x] Navigate to Elements/Inspector tab
- [x] Select header element (`<h1>`)
- [x] Verify applied classes:
  - `text-4xl`
  - `font-bold`
  - `text-white`
  - `tracking-tight`
- [x] Check computed styles match expectations

#### B. Glass Panel Effect Verification

- [x] Inspect roster container div
- [x] Verify classes present:
  - `glass-panel`
  - `p-6`
  - `rounded-xl`
  - `border`
  - `border-white/5`
- [x] Check CSS custom properties:
  - `backdrop-filter: blur(...)`
  - `background: rgba(...)`
- [x] Verify no inline styles overriding

#### C. Grid Layout Verification

- [x] Inspect player card container
- [x] Verify responsive grid classes:
  - `grid-cols-1` (mobile)
  - `md:grid-cols-2` (tablet)
  - `xl:grid-cols-3` (desktop)
- [x] Check gap spacing: `gap-4`
- [x] Verify overflow scroll: `max-h-[600px] overflow-y-auto`

#### D. DraggableCard Component Styles

- [x] Inspect individual card element
- [x] Check all style properties applied
- [x] Verify no missing classes
- [x] Check for CSS errors in console

#### E. Color Consistency

- [x] Create color palette checklist:
  - [x] Primary text: `#ffffff` (white)
  - [x] Accent text: `#22d3ee` or similar (cyan)
  - [x] Background transparency matches
  - [x] Border colors consistent
- [x] Use browser color picker to verify exact values
- [x] Compare to design system/style guide

---

## Subtask 2.6.3: Check DraggableCard Component Functions Correctly

### 2.6.3 Objective

Ensure the DraggableCard component renders and behaves properly with real data.

### 2.6.3 Steps

#### A. Component Rendering Test

- [ ] Verify all 52 cards render
- [ ] Check each card displays:
  - [ ] Player name in format "F. Lastname"
  - [ ] Position badge (QB, WR, RB, etc.)
  - [ ] Overall rating (number 60-99)
  - [ ] Team abbreviation "ARI"
- [ ] Scroll through entire roster
- [ ] Verify no cards are missing or duplicated
- [ ] Check for any rendering errors in console

#### B. Data Binding Verification

- [ ] Select random card and inspect props
- [ ] In React DevTools:
  - Open Components tab
  - Find DraggableCard instance
  - Check props values:

    ```typescript
    name: string (from API)
    position: string (from API)
    rating: number (from API)
    team: string (from API)
    ```

- [ ] Verify props match data from API
- [ ] Test with different players

#### C. Drag Functionality Test

- [ ] Attempt to drag a player card
- [ ] Verify drag cursor appears
- [ ] Check if drag handlers fire (if implemented)
- [ ] Test drop zones (if implemented)
- [ ] Note: May not be fully functional yet - document status

#### D. Interactive States

- [ ] **Hover State:**
  - [ ] Move mouse over card
  - [ ] Verify hover effect (scale, glow, shadow)
  - [ ] Check transition smoothness
- [ ] **Focus State:**
  - [ ] Tab to card (keyboard navigation)
  - [ ] Verify focus ring/outline visible
- [ ] **Active State:**
  - [ ] Click and hold card
  - [ ] Verify active state styling

#### E. Performance Test

- [ ] Open Performance tab in DevTools
- [ ] Record while scrolling roster
- [ ] Check frame rate stays above 30fps
- [ ] Identify any layout thrashing
- [ ] Check for memory leaks:
  - Record heap snapshot before scroll
  - Scroll extensively
  - Record heap snapshot after
  - Compare memory delta

---

## Subtask 2.6.4: Test Responsive Layout on Different Screen Sizes

### 2.6.4 Objective

Verify the FrontOffice page adapts correctly to all device sizes.

### 2.6.4 Steps

#### A. Desktop Testing (1920x1080)

- [ ] Set browser viewport to 1920x1080
- [ ] Verify layout:
  - [ ] 3-column grid for player cards
  - [ ] Full navigation visible
  - [ ] Transaction log panel visible
  - [ ] No horizontal scrolling
- [ ] Take screenshot: `screenshots/responsive/desktop-1920.png`

#### B. Laptop Testing (1366x768)

- [ ] Resize to 1366x768
- [ ] Verify:
  - [ ] Still 3-column grid or adapts to 2
  - [ ] No content cut off
  - [ ] Scrolling works smoothly
- [ ] Take screenshot: `screenshots/responsive/laptop-1366.png`

#### C. Tablet Testing (768x1024 Portrait)

- [ ] Resize to 768px width
- [ ] Verify responsive changes:
  - [ ] Grid switches to 2 columns (`md:grid-cols-2`)
  - [ ] Transaction log either stacks below or hides
  - [ ] Font sizes remain readable
  - [ ] Touch targets adequately sized (min 44x44px)
- [ ] Take screenshot: `screenshots/responsive/tablet-768.png`

#### D. Tablet Landscape (1024x768)

- [ ] Rotate to landscape
- [ ] Verify grid adapts
- [ ] Check horizontal spacing
- [ ] Take screenshot

#### E. Mobile Testing (375x667 - iPhone SE)

- [ ] Resize to 375px width
- [ ] Verify responsive changes:
  - [ ] Grid switches to single column (`grid-cols-1`)
  - [ ] Header text wraps properly
  - [ ] Cards stack vertically
  - [ ] Navigation may collapse to hamburger
  - [ ] No horizontal overflow
- [ ] Test scrolling performance
- [ ] Take screenshot: `screenshots/responsive/mobile-375.png`

#### F. Mobile Large (430x932 - iPhone 14 Pro Max)

- [ ] Resize to 430px width
- [ ] Verify similar to iPhone SE
- [ ] Check if grid shows 1 or 2 columns
- [ ] Take screenshot

#### G. Edge Cases

- [ ] **Ultra Wide (2560x1440):**
  - [ ] Content centered or expands?
  - [ ] Max-width constraints work?
- [ ] **Very Narrow (320px):**
  - [ ] Text doesn't overflow
  - [ ] Buttons remain clickable
  - [ ] No layout breaking

#### H. Dynamic Resize Test

- [ ] Start at desktop size
- [ ] Slowly drag browser edge to narrow
- [ ] Watch breakpoints transition:
  - 1280px (XL breakpoint)
  - 1024px (LG breakpoint)
  - 768px (MD breakpoint)
  - 640px (SM breakpoint)
- [ ] Verify smooth transitions
- [ ] No sudden jumps or broken layouts
- [ ] CSS grid recalculates correctly

#### I. Device Emulation (Chrome DevTools)

- [ ] Open DevTools (F12)
- [ ] Toggle device toolbar (Ctrl+Shift+M)
- [ ] Test preset devices:
  - [ ] iPhone 12/13/14 Pro
  - [ ] iPhone SE
  - [ ] iPad Air
  - [ ] iPad Mini
  - [ ] Samsung Galaxy S20
  - [ ] Pixel 5
- [ ] Test both portrait and landscape
- [ ] Verify touch interactions work

---

## Subtask 2.6.5: Cross-Browser Testing

### 2.6.5 Objective

Ensure consistent rendering across major browsers.

### 2.6.5 Steps

#### A. Chrome/Edge (Chromium)

- [ ] Already tested (development browser)
- [ ] Document version number
- [ ] Note any specific issues

#### B. Firefox

- [ ] Open <http://localhost:5173> in Firefox
- [ ] Run through visual checklist
- [ ] Check for:
  - [ ] Glass panel effects render
  - [ ] Grid layout identical
  - [ ] Fonts render correctly
  - [ ] Colors match
- [ ] Take comparison screenshot

#### C. Safari (macOS/iOS)

- [ ] Test on macOS Safari (if available)
- [ ] Check for:
  - [ ] Backdrop filter support
  - [ ] Grid layout differences
  - [ ] Font rendering variations
- [ ] Test iOS Safari via iPhone/iPad or simulator
- [ ] Note any webkit-specific issues

#### D. Mobile Browsers

- [ ] Test on actual mobile device:
  - [ ] Chrome Mobile (Android)
  - [ ] Safari Mobile (iOS)
- [ ] Verify touch interactions
- [ ] Check scroll performance
- [ ] Test pull-to-refresh doesn't interfere

---

## Success Criteria

### Must Pass

- ✅ All styling classes present and applied
- ✅ No regression in visual design
- ✅ Responsive breakpoints work correctly
- ✅ All 52 cards render with correct data
- ✅ No console errors
- ✅ Smooth scrolling and interactions

### Nice to Have

- ✅ Drag functionality works (if implemented)
- ✅ Performance above 30fps
- ✅ Identical rendering across browsers
- ✅ Accessibility features intact

## Deliverables

1. **Screenshots**
   - Baseline (mock data) vs Current (real data)
   - Responsive layouts for all major breakpoints
   - Cross-browser comparisons

2. **Visual Regression Report**
   - Document in `frontend/docs/visual-regression-report.md`
   - List all differences found
   - Categorize severity (bug, acceptable, expected)
   - Include screenshots with annotations

3. **Responsive Test Results**
   - Table of breakpoints tested
   - Pass/Fail status for each device
   - Notes on any issues

4. **Updated Task.md**
   - Mark subtasks as complete
   - Document any bugs found
   - Create follow-up tasks if needed

## Tools & Resources

### Browser DevTools

- Elements/Inspector: Check applied styles
- Responsive Design Mode: Test breakpoints
- Performance: Profile frame rates
- Network: Verify API calls

### External Tools (Optional)

- **Percy** (percy.io): Automated visual regression testing
- **Chromatic** (chromatic.com): Component screenshot diffing
- **BrowserStack**: Test on real devices
- **LambdaTest**: Cross-browser testing

### Screenshots Organization

```text
frontend/docs/screenshots/
├── baseline/
│   ├── desktop-full.png
│   ├── cards-closeup.png
│   └── header.png
├── current/
│   ├── desktop-full.png
│   ├── cards-closeup.png
│   └── header.png
└── responsive/
    ├── desktop-1920.png
    ├── tablet-768.png
    └── mobile-375.png
```

---

**Estimated Time:** 2-3 hours  
**Priority:** Medium (critical for user-facing features)  
**Dependencies:** Task 2.2-2.5 must pass first

**Next Steps After Completion:**

- Update verification_results.md with findings
- Create bug tickets for any regressions found
- Proceed to Task 3 (Simulation Persistence Testing)
