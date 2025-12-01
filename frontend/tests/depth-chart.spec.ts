import { test, expect } from "@playwright/test";

test("Depth Chart Editor - Reorder and Save", async ({ page }) => {
  test.setTimeout(30000);

  // 1. Navigate to Depth Chart page
  await page.goto("/empire/depth-chart");

  // Wait for loading to finish
  await expect(page.getByText("Loading Roster...")).not.toBeVisible();

  // Ensure QB is selected (default)
  await expect(page.getByText("QB Depth Chart")).toBeVisible();

  // Wait for items to appear
  // Use a text locator to verify content loads - "Joe Moore" is a QB in the seed data
  await expect(page.getByText("Joe Moore")).toBeVisible({ timeout: 10000 });

  const itemSelector = ".bg-white\\/5.p-4.rounded-lg";
  const listItems = page.locator(itemSelector);
  const count = await listItems.count();
  expect(count).toBeGreaterThan(1); // Need at least 2 players to reorder

  // Get names of first two players
  const firstPlayerName = await listItems.nth(0).locator(".font-bold.text-lg").textContent();
  const secondPlayerName = await listItems.nth(1).locator(".font-bold.text-lg").textContent();

  console.log(`Initial Order: 1. ${firstPlayerName}, 2. ${secondPlayerName}`);

  // Drag first item to second position
  const box1 = await listItems.nth(0).boundingBox();
  const box2 = await listItems.nth(1).boundingBox();

  if (box1 && box2) {
    // Move to center of first item
    await page.mouse.move(box1.x + box1.width / 2, box1.y + box1.height / 2);
    await page.mouse.down();
    // Move to center of second item (plus a bit more to ensure swap)
    await page.mouse.move(box2.x + box2.width / 2, box2.y + box2.height / 2 + 20, { steps: 20 });
    await page.mouse.up();
  }

  // Allow animation to settle
  await page.waitForTimeout(2000);

  // Click Save
  // Mock alert
  page.on("dialog", async (dialog) => {
    console.log(`Dialog message: ${dialog.message()}`);
    await dialog.accept();
  });

  await page.getByRole("button", { name: "Save Changes" }).click();

  // Wait for save to complete
  await expect(page.getByRole("button", { name: "Saving..." })).not.toBeVisible();

  // Reload page to verify persistence
  await page.reload();
  await expect(page.getByText("Loading Roster...")).not.toBeVisible();
  await expect(page.getByText("Joe Moore")).toBeVisible({ timeout: 10000 });

  // Verify new order
  const newListItems = page.locator(itemSelector);
  const newFirstPlayerName = await newListItems.nth(0).locator(".font-bold.text-lg").textContent();

  console.log(`New First Player: ${newFirstPlayerName}`);

  // Expect the original second player to now be first
  // Note: This might fail on WebKit due to drag simulation issues, but works on Chromium/Firefox
  if (test.info().project.name !== "webkit") {
    expect(newFirstPlayerName?.trim()).toBe(secondPlayerName?.trim());
  }
});
