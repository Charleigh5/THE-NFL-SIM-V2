import { test, expect } from '@playwright/test';
import { WebSocketServer } from 'ws';

// Mock game state updates for WebSocket
const mockGameUpdates = [
  { event: 'game_update', payload: { score: { home: 3, away: 0 }, quarter: 1, time_remaining: '10:00', play_by_play: 'Kickoff, touchback.' } },
  { event: 'game_update', payload: { score: { home: 7, away: 0 }, quarter: 1, time_remaining: '05:30', play_by_play: 'TOUCHDOWN! Home team scores.' } },
  { event: 'game_update', payload: { score: { home: 7, away: 3 }, quarter: 2, time_remaining: '12:00', play_by_play: 'Field Goal good for away team.' } },
];

test.describe('Live Simulation Flow', () => {
  let wss: WebSocketServer;

  test.beforeEach(async ({ page }) => {
    // Mock start and stop simulation API calls
    await page.route('**/api/simulation/live/start', async route => {
      await route.fulfill({ status: 200, json: { message: 'Simulation started' } });
    });
    await page.route('**/api/simulation/live/stop', async route => {
      await route.fulfill({ status: 200, json: { message: 'Simulation stopped' } });
    });

    // Start a mock WebSocket server for each test
    wss = new WebSocketServer({ port: 8001 }); // Use a different port for the mock WS
    wss.on('connection', ws => {
      console.log('Mock WebSocket client connected');
      // Send mock updates after a short delay to simulate real-time
      let i = 0;
      const interval = setInterval(() => {
        if (i < mockGameUpdates.length) {
          ws.send(JSON.stringify(mockGameUpdates[i]));
          i++;
        } else {
          clearInterval(interval);
          // ws.close(); // Optionally close after sending all messages
        }
      }, 500);

      ws.on('close', () => console.log('Mock WebSocket client disconnected'));
      ws.on('error', error => console.error('Mock WebSocket error:', error));
    });
    console.log('Mock WebSocket server started on port 8001');

    // Override the useWebSocket hook to connect to the mock server
    await page.addInitScript(() => {
      window.originalWebSocket = window.WebSocket;
      window.WebSocket = class MockWebSocket extends window.originalWebSocket {
        constructor(url: string, protocols?: string | string[]) {
          // Replace the original WebSocket URL with the mock server's URL
          const mockUrl = url.replace('ws://localhost:8000', 'ws://localhost:8001');
          super(mockUrl, protocols);
          console.log(`Intercepted WebSocket connection to: ${mockUrl}`);
        }
      };
    });
  });

  test.afterEach(async () => {
    // Close the mock WebSocket server after each test
    if (wss) {
      await new Promise<void>((resolve) => wss.close(() => {
        console.log('Mock WebSocket server closed');
        resolve();
      }));
    }
  });

  test('should load live sim and start simulation, receiving updates', async ({ page }) => {
    await page.goto('/live-sim');
    
    // Verify initial state: KICKOFF button is visible
    await expect(page.locator('button', { hasText: 'KICKOFF' })).toBeVisible();

    // Click KICKOFF button
    await page.locator('button', { hasText: 'KICKOFF' }).click();

    // Verify loading state, then Pause/FastForward buttons
    await expect(page.locator('button', { hasText: 'Starting...' })).toBeVisible();
    await expect(page.locator('button', { hasText: 'Pause' })).toBeVisible({ timeout: 5000 });
    await expect(page.locator('button', { hasText: 'FastForward' })).toBeVisible();

    // Verify UI updates based on mock WebSocket messages
    // First update: Score 3-0, Q1, 10:00
    await expect(page.locator('[data-testid="scoreboard-home-score"]')).toContainText('3', { timeout: 3000 });
    await expect(page.locator('[data-testid="scoreboard-away-score"]')).toContainText('0');
    await expect(page.locator('[data-testid="game-clock-quarter"]')).toContainText('Q1');
    await expect(page.locator('[data-testid="game-clock-time"]')).toContainText('10:00');
    await expect(page.locator('[data-testid="play-by-play-feed"]')).toContainText('Kickoff, touchback.');

    // Second update: Score 7-0, Q1, 05:30
    await expect(page.locator('[data-testid="scoreboard-home-score"]')).toContainText('7', { timeout: 3000 });
    await expect(page.locator('[data-testid="scoreboard-away-score"]')).toContainText('0');
    await expect(page.locator('[data-testid="game-clock-quarter"]')).toContainText('Q1');
    await expect(page.locator('[data-testid="game-clock-time"]')).toContainText('05:30');
    await expect(page.locator('[data-testid="play-by-play-feed"]')).toContainText('TOUCHDOWN! Home team scores.');

    // Third update: Score 7-3, Q2, 12:00
    await expect(page.locator('[data-testid="scoreboard-home-score"]')).toContainText('7', { timeout: 3000 });
    await expect(page.locator('[data-testid="scoreboard-away-score"]')).toContainText('3');
    await expect(page.locator('[data-testid="game-clock-quarter"]')).toContainText('Q2');
    await expect(page.locator('[data-testid="game-clock-time"]')).toContainText('12:00');
    await expect(page.locator('[data-testid="play-by-play-feed"]')).toContainText('Field Goal good for away team.');

    // Click Pause button
    await page.locator('button', { hasText: 'Pause' }).click();
    await expect(page.locator('button', { hasText: 'KICKOFF' })).toBeVisible();
  });
});
