import os

file_path = r"C:\Users\cweir\.gemini\antigravity\brain\845aff2f-58a7-40aa-bfd8-445469189850\task.md"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Normalize newlines
content = content.replace('\r\n', '\n')

# Fix 1: Stage 1
content = content.replace(
    "### 1.1 System Architecture & Documentation\n- [x] Define system architecture blueprint",
    "### 1.1 System Architecture & Documentation\n\n- [x] Define system architecture blueprint"
)

# Fix 2: Stage 4 (Roster Management to Performance Tests)
block_stage_4_old = """##### Roster Management Flow Tests
  - [ ] Test: Viewing team roster
    - [ ] Navigate to team page
    - [ ] Verify all players displayed
    - [ ] Verify position grouping works
  - [ ] Test: Editing depth chart
    - [ ] Open depth chart editor
    - [ ] Drag and drop player to new position
    - [ ] Save changes
    - [ ] Verify changes persisted
  - [ ] Test: Viewing player details
    - [ ] Click on player name
    - [ ] Verify player modal opens
    - [ ] Verify all attributes displayed
    - [ ] Verify career stats shown

##### Offseason Flow Tests
  - [ ] Test: Running the draft
    - [ ] Navigate to draft board
    - [ ] Verify draft order shown
    - [ ] Click "Simulate Draft"
    - [ ] Verify all picks made
    - [ ] Verify rookies added to rosters
  - [ ] Test: Free agency simulation
    - [ ] Enter offseason phase
    - [ ] Navigate to free agency
    - [ ] View available players
    - [ ] Simulate FA signing period
    - [ ] Verify players signed to teams
  - [ ] Test: Salary cap management
    - [ ] Navigate to salary cap page
    - [ ] Verify cap space calculated correctly
    - [ ] Verify player contracts displayed
    - [ ] Test contract restructuring (if applicable)

##### Data Persistence Tests
  - [ ] Test: Page refresh maintains state
    - [ ] Start a season
    - [ ] Refresh the page
    - [ ] Verify season data reloaded
  - [ ] Test: Navigation maintains context
    - [ ] Navigate between multiple pages
    - [ ] Verify correct data shown on each page
    - [ ] Return to previous page
    - [ ] Verify state preserved

##### Error Handling Tests
  - [ ] Test: API failure handling
    - [ ] Mock API failure
    - [ ] Trigger action that calls API
    - [ ] Verify error message displayed
    - [ ] Verify user can retry action
  - [ ] Test: Invalid data handling
    - [ ] Submit invalid form data
    - [ ] Verify validation errors shown
    - [ ] Verify form not submitted

##### Performance Tests
  - [ ] Test: Large dataset rendering
    - [ ] Load page with 500+ players
    - [ ] Verify page renders within 2 seconds
    - [ ] Verify scrolling is smooth
  - [ ] Test: Real-time updates
    - [ ] Start WebSocket connection
    - [ ] Trigger simulation event
    - [ ] Verify UI updates in real-time
    - [ ] Verify no lag or freezing"""

block_stage_4_new = """#### Roster Management Flow Tests

- [ ] Test: Viewing team roster
  - [ ] Navigate to team page
  - [ ] Verify all players displayed
  - [ ] Verify position grouping works
- [ ] Test: Editing depth chart
  - [ ] Open depth chart editor
  - [ ] Drag and drop player to new position
  - [ ] Save changes
  - [ ] Verify changes persisted
- [ ] Test: Viewing player details
  - [ ] Click on player name
  - [ ] Verify player modal opens
  - [ ] Verify all attributes displayed
  - [ ] Verify career stats shown

#### Offseason Flow Tests

- [ ] Test: Running the draft
  - [ ] Navigate to draft board
  - [ ] Verify draft order shown
  - [ ] Click "Simulate Draft"
  - [ ] Verify all picks made
  - [ ] Verify rookies added to rosters
- [ ] Test: Free agency simulation
  - [ ] Enter offseason phase
  - [ ] Navigate to free agency
  - [ ] View available players
  - [ ] Simulate FA signing period
  - [ ] Verify players signed to teams
- [ ] Test: Salary cap management
  - [ ] Navigate to salary cap page
  - [ ] Verify cap space calculated correctly
  - [ ] Verify player contracts displayed
  - [ ] Test contract restructuring (if applicable)

#### Data Persistence Tests

- [ ] Test: Page refresh maintains state
  - [ ] Start a season
  - [ ] Refresh the page
  - [ ] Verify season data reloaded
- [ ] Test: Navigation maintains context
  - [ ] Navigate between multiple pages
  - [ ] Verify correct data shown on each page
  - [ ] Return to previous page
  - [ ] Verify state preserved

#### Error Handling Tests

- [ ] Test: API failure handling
  - [ ] Mock API failure
  - [ ] Trigger action that calls API
  - [ ] Verify error message displayed
  - [ ] Verify user can retry action
- [ ] Test: Invalid data handling
  - [ ] Submit invalid form data
  - [ ] Verify validation errors shown
  - [ ] Verify form not submitted

#### Performance Tests

- [ ] Test: Large dataset rendering
  - [ ] Load page with 500+ players
  - [ ] Verify page renders within 2 seconds
  - [ ] Verify scrolling is smooth
- [ ] Test: Real-time updates
  - [ ] Start WebSocket connection
  - [ ] Trigger simulation event
  - [ ] Verify UI updates in real-time
  - [ ] Verify no lag or freezing"""

content = content.replace(block_stage_4_old, block_stage_4_new)

# Fix 3: Stage 5
block_stage_5_old = """### 5.1 UI/UX Improvements
- [ ] Implement dark mode toggle
- [ ] Add loading skeletons for better perceived performance
- [ ] Implement toast notifications for user actions
- [ ] Add animations and transitions
- [ ] Implement keyboard shortcuts for power users
- [ ] Add accessibility features (ARIA labels, screen reader support)
- [ ] Optimize mobile responsiveness

### 5.2 Advanced Features
##### Multi-season franchise mode
  - [ ] Implement season history tracking
  - [ ] Implement HOF (Hall of Fame) system
  - [ ] Implement franchise records
  - [ ] Implement legacy/dynasty metrics
  
##### Advanced analytics
  - [ ] Implement player comparison tool
  - [ ] Implement team strength rankings
  - [ ] Implement playoff probability calculator
  - [ ] Add statistical visualizations (charts, graphs)
  
##### Custom league settings
  - [ ] Allow custom team creation
  - [ ] Allow rule customization (salary cap, roster size)
  - [ ] Implement difficulty settings
  - [ ] Allow historical draft classes import

### 5.3 Performance Optimization
- [ ] Implement database query optimization
- [ ] Add Redis caching layer for frequently accessed data
- [ ] Optimize frontend bundle size
- [ ] Implement code splitting and lazy loading
- [ ] Add service worker for offline functionality
- [ ] Implement database connection pooling

### 5.4 Monitoring & Observability
- [ ] Set up application performance monitoring (APM)
- [ ] Implement centralized logging (e.g., ELK stack)
- [ ] Add error tracking (e.g., Sentry)
- [ ] Create admin dashboard for system health
- [ ] Implement user analytics"""

block_stage_5_new = """### 5.1 UI/UX Improvements

- [ ] Implement dark mode toggle
- [ ] Add loading skeletons for better perceived performance
- [ ] Implement toast notifications for user actions
- [ ] Add animations and transitions
- [ ] Implement keyboard shortcuts for power users
- [ ] Add accessibility features (ARIA labels, screen reader support)
- [ ] Optimize mobile responsiveness

### 5.2 Advanced Features

#### Multi-season franchise mode

- [ ] Implement season history tracking
- [ ] Implement HOF (Hall of Fame) system
- [ ] Implement franchise records
- [ ] Implement legacy/dynasty metrics
  
#### Advanced analytics

- [ ] Implement player comparison tool
- [ ] Implement team strength rankings
- [ ] Implement playoff probability calculator
- [ ] Add statistical visualizations (charts, graphs)
  
#### Custom league settings

- [ ] Allow custom team creation
- [ ] Allow rule customization (salary cap, roster size)
- [ ] Implement difficulty settings
- [ ] Allow historical draft classes import

### 5.3 Performance Optimization

- [ ] Implement database query optimization
- [ ] Add Redis caching layer for frequently accessed data
- [ ] Optimize frontend bundle size
- [ ] Implement code splitting and lazy loading
- [ ] Add service worker for offline functionality
- [ ] Implement database connection pooling

### 5.4 Monitoring & Observability

- [ ] Set up application performance monitoring (APM)
- [ ] Implement centralized logging (e.g., ELK stack)
- [ ] Add error tracking (e.g., Sentry)
- [ ] Create admin dashboard for system health
- [ ] Implement user analytics"""

content = content.replace(block_stage_5_old, block_stage_5_new)

# Fix 4: Stage 6
block_stage_6_old = """### 6.1 Security
- [ ] Implement user authentication (JWT)
- [ ] Implement user authorization (role-based access)
- [ ] Add rate limiting to API endpoints
- [ ] Implement CSRF protection
- [ ] Add input sanitization and validation
- [ ] Perform security audit
- [ ] Set up HTTPS/TLS certificates

### 6.2 CI/CD Pipeline
- [ ] Create GitHub Actions workflow for backend tests
- [ ] Create GitHub Actions workflow for frontend tests
- [ ] Set up automated linting checks
- [ ] Implement automated deployment pipeline
- [ ] Add staging environment
- [ ] Implement blue-green deployment strategy

### 6.3 Production Deployment
- [ ] Set up cloud infrastructure (AWS/GCP/Azure)
- [ ] Configure production database (PostgreSQL)
- [ ] Set up CDN for static assets
- [ ] Configure auto-scaling
- [ ] Set up backup and disaster recovery
- [ ] Create production deployment checklist
- [ ] Perform load testing"""

block_stage_6_new = """### 6.1 Security

- [ ] Implement user authentication (JWT)
- [ ] Implement user authorization (role-based access)
- [ ] Add rate limiting to API endpoints
- [ ] Implement CSRF protection
- [ ] Add input sanitization and validation
- [ ] Perform security audit
- [ ] Set up HTTPS/TLS certificates

### 6.2 CI/CD Pipeline

- [ ] Create GitHub Actions workflow for backend tests
- [ ] Create GitHub Actions workflow for frontend tests
- [ ] Set up automated linting checks
- [ ] Implement automated deployment pipeline
- [ ] Add staging environment
- [ ] Implement blue-green deployment strategy

### 6.3 Production Deployment

- [ ] Set up cloud infrastructure (AWS/GCP/Azure)
- [ ] Configure production database (PostgreSQL)
- [ ] Set up CDN for static assets
- [ ] Configure auto-scaling
- [ ] Set up backup and disaster recovery
- [ ] Create production deployment checklist
- [ ] Perform load testing"""

content = content.replace(block_stage_6_old, block_stage_6_new)

# Fix 5: Summary
block_summary_old = """**Total Tasks: 236**
- **Completed: 210** ✅
- **In Progress: 0** 🔄
- **Remaining: 26** 📋

**Overall Completion: 89%**

### Immediate Next Steps
1. Set up E2E testing framework (Playwright/Cypress)
2. Implement core user flow tests
3. Add comprehensive E2E test coverage
4. Consider UI/UX polish enhancements
5. Plan production deployment strategy"""

block_summary_new = """#### Total Tasks: 236

- **Completed: 210** ✅
- **In Progress: 0** 🔄
- **Remaining: 26** 📋

#### Overall Completion: 89%

### Immediate Next Steps

1. Set up E2E testing framework (Playwright/Cypress)
2. Implement core user flow tests
3. Add comprehensive E2E test coverage
4. Consider UI/UX polish enhancements
5. Plan production deployment strategy"""

content = content.replace(block_summary_old, block_summary_new)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully updated task.md")
