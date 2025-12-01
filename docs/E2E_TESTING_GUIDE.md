# E2E Testing Guide

This project uses [Playwright](https://playwright.dev/) for End-to-End (E2E) testing. The tests are located in the `frontend/e2e` directory and are configured to test the frontend application flows, mocking backend API responses where necessary.

## 1. Running Tests Locally

We have several npm scripts defined in `frontend/package.json` to help you run tests in different modes.

### Run all tests (Headless)
This is the standard way to run tests. It runs all tests in headless mode (no browser window visible).
```bash
cd frontend
npm run test:e2e
```

### Run with UI Mode
Opens the Playwright UI, which allows you to run individual tests, see traces, and debug visually.
```bash
cd frontend
npm run test:e2e:ui
```

### Run in Headed Mode
Runs tests with the browser window visible. Useful for visually verifying what the test is doing.
```bash
cd frontend
npm run test:e2e:headed
```

### Debug Mode
Runs tests with the Playwright Inspector, allowing you to step through test execution.
```bash
cd frontend
npm run test:e2e:debug
```

### View Test Report
After a test run, you can view the HTML report to see results, traces, and screenshots.
```bash
cd frontend
npm run test:e2e:report
```

## 2. Writing New Tests

### File Location
Create new test files in `frontend/e2e/` with the `.spec.ts` extension.
Example: `frontend/e2e/new-feature.spec.ts`

### Basic Structure
```typescript
import { test, expect } from '@playwright/test';

test.describe('Feature Name', () => {
  
  test('should perform specific action', async ({ page }) => {
    // 1. Setup / Navigation
    await page.goto('/feature-page');
    
    // 2. Interaction
    await page.locator('button.submit').click();
    
    // 3. Assertion
    await expect(page.locator('.success-message')).toBeVisible();
  });

});
```

### Best Practices
- **Selectors**: Use user-facing locators like `getByRole`, `getByText`, or `getByTestId` (configured as `data-testid` attributes).
- **Isolation**: Each test should be independent. Use `test.beforeEach` for common setup.
- **Mocking**: Prefer mocking API responses to ensure tests are deterministic and fast.

## 3. Test Data Management

### Static Fixtures
Common mock data is stored in `frontend/e2e/fixtures/test-data.ts`. You can import these constants to use in your tests.

```typescript
import { mockTeam, mockPlayers } from './fixtures/test-data';
```

### Mocking API Responses
Use `page.route` to intercept network requests and return mock data. This prevents the tests from hitting the real backend.

```typescript
test('should display team data', async ({ page }) => {
  // Mock the team API endpoint
  await page.route('**/api/teams/1', async route => {
    await route.fulfill({ json: mockTeam });
  });

  await page.goto('/front-office');
});
```

## 4. Debugging Techniques

### Playwright UI
The best tool for debugging is the UI mode (`npm run test:e2e:ui`). It lets you:
- Run specific tests.
- "Time travel" through the test execution.
- Inspect the DOM and network calls at each step.
- See console logs and errors.

### Visual Debugging
You can pause execution at any point in your test code:
```typescript
await page.pause();
```
This will open the Inspector and wait for you to resume.

### Trace Viewer
If a test fails in CI or locally, the report (`npm run test:e2e:report`) often contains a "Trace". The trace is a full recording of the test execution, including snapshots, network requests, and console logs.

## 5. CI/CD Integration

E2E tests are automatically run via GitHub Actions.
**Workflow File**: `.github/workflows/e2e-tests.yml`

### Triggers
- Pushes to `main` or `master` branches.
- Pull Requests.

### Artifacts
If tests fail in CI, the workflow uploads the Playwright report as an artifact. You can download this artifact from the GitHub Actions run summary to inspect traces and screenshots of failures.
