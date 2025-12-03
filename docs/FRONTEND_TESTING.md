# Frontend Testing Setup Guide

## Current Testing Setup

The frontend currently has **Playwright** configured for end-to-end testing.

### Running E2E Tests

```bash
# Run all E2E tests
npm run test:e2e

# Run with UI
npm run test:e2e:ui

# Run in headed mode (see browser)
npm run test:e2e:headed

# Debug mode
npm run test:e2e:debug

# View test report
npm run test:e2e:report
```

## Recommended: Add Vitest for Component Testing

For comprehensive frontend testing, we recommend adding **Vitest** with **React Testing Library** for component unit tests.

### Installation

```bash
cd frontend
npm install -D vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom @vitest/ui
```

### Configuration File: `vitest.config.ts`

Create this file in the `frontend/` directory:

```typescript
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: "./src/test/setup.ts",
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html"],
      exclude: [
        "node_modules/",
        "src/test/",
        "**/*.d.ts",
        "**/*.config.*",
        "**/mockData",
        "**/*.spec.tsx",
        "**/*.test.tsx",
      ],
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
```

### Test Setup File: `src/test/setup.ts`

```typescript
import { expect, afterEach } from "vitest";
import { cleanup } from "@testing-library/react";
import * as matchers from "@testing-library/jest-dom/matchers";

// Extend Vitest's expect with jest-dom matchers
expect.extend(matchers);

// Cleanup after each test
afterEach(() => {
  cleanup();
});
```

### Add Scripts to `package.json`

Add these scripts to your `package.json`:

```json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage"
  }
}
```

## Example Component Tests

### Example 1: Simple Component Test

Create `src/components/__tests__/TeamCard.test.tsx`:

```typescript
import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { TeamCard } from "../TeamCard";

describe("TeamCard", () => {
  it("renders team name correctly", () => {
    const team = {
      id: 1,
      name: "New England Patriots",
      city: "New England",
      abbreviation: "NE",
    };

    render(<TeamCard team={team} />);

    expect(screen.getByText("New England Patriots")).toBeInTheDocument();
  });

  it("displays team abbreviation", () => {
    const team = {
      id: 1,
      name: "New England Patriots",
      city: "New England",
      abbreviation: "NE",
    };

    render(<TeamCard team={team} />);

    expect(screen.getByText("NE")).toBeInTheDocument();
  });
});
```

### Example 2: Component with User Interaction

Create `src/pages/__tests__/RosterPage.test.tsx`:

```typescript
import { describe, it, expect, vi } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { RosterPage } from "../RosterPage";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  });

  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
};

describe("RosterPage", () => {
  it("allows filtering players by position", async () => {
    const user = userEvent.setup();

    render(<RosterPage />, { wrapper: createWrapper() });

    // Find and click the QB filter
    const qbFilter = screen.getByRole("button", { name: /quarterback/i });
    await user.click(qbFilter);

    // Wait for filtered results
    await waitFor(() => {
      expect(screen.getByText(/quarterbacks/i)).toBeInTheDocument();
    });
  });
});
```

### Example 3: Testing with API Mocks

Create `src/services/__tests__/api.test.ts`:

```typescript
import { describe, it, expect, vi, beforeEach } from "vitest";
import axios from "axios";
import { fetchTeams, fetchTeamRoster } from "../api";

vi.mock("axios");

describe("API Service", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("fetches teams successfully", async () => {
    const mockTeams = [
      { id: 1, name: "Patriots", city: "New England" },
      { id: 2, name: "Cowboys", city: "Dallas" },
    ];

    vi.mocked(axios.get).mockResolvedValueOnce({ data: mockTeams });

    const teams = await fetchTeams();

    expect(teams).toEqual(mockTeams);
    expect(axios.get).toHaveBeenCalledWith("/api/teams");
  });

  it("handles API errors gracefully", async () => {
    vi.mocked(axios.get).mockRejectedValueOnce(new Error("Network error"));

    await expect(fetchTeams()).rejects.toThrow("Network error");
  });
});
```

## Running Tests

After setup:

```bash
# Run all unit tests
npm test

# Run in watch mode (default)
npm test

# Run with coverage
npm run test:coverage

# Run with UI
npm run test:ui

# Run E2E tests (existing)
npm run test:e2e
```

## Best Practices

1. **Test user behavior, not implementation details**
2. **Use data-testid sparingly** - prefer queries like `getByRole`, `getByText`
3. **Mock external dependencies** (API calls, third-party libraries)
4. **Keep tests focused** - one concept per test
5. **Use descriptive test names** - describe what the test validates
6. **Test accessibility** - use roles and semantic queries

## Coverage Goals

- **Components**: 80%+ coverage
- **Services/Utils**: 90%+ coverage
- **Pages**: 70%+ coverage (some integration overlap with E2E)

## CI/CD Integration

Add to your GitHub Actions workflow:

```yaml
- name: Run Unit Tests
  run: |
    cd frontend
    npm run test:coverage

- name: Upload Coverage
  uses: codecov/codecov-action@v3
  with:
    directory: ./frontend/coverage
```
