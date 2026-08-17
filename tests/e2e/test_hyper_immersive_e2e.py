import re
import pytest
from playwright.sync_api import Page, expect

@pytest.mark.e2e
def test_draft_room_immersive_features(page: Page):
    """Test Draft Room immersive features: Ticker, Phone."""
    page.goto("http://localhost:5173/offseason/draft")

    # 1. Verify War Room Ticker is visible
    ticker = page.locator(".war-room-ticker")
    expect(ticker).to_be_visible()
    expect(page.locator(".ticker-label")).to_have_text("WAR ROOM LIVE")

    # 2. Verify Trade Phone is visible
    phone = page.locator(".trade-phone-container")
    expect(phone).to_be_visible()

    # 3. Verify Draft Board container is present (even if empty)
    expect(page.locator("[data-testid='draft-board']")).to_be_visible()


@pytest.mark.e2e
def test_medical_center_interactive(page: Page):
    """Test Medical Center interactions: Body Map and Treatments."""
    page.goto("http://localhost:5173/medical-center")

    # 1. Verify Medical Center page loaded
    expect(page.get_by_text("Medical Center")).to_be_visible()

    # 2. Verify Body Map container exists
    body_map = page.locator(".body-map-container")
    expect(body_map).to_be_visible()

    # 3. Verify Injury Report section exists
    expect(page.get_by_text("Injury Report")).to_be_visible()


@pytest.mark.e2e
def test_playbook_coaching_features(page: Page):
    """Test Playbook Coaching Tree and Gameplan tabs."""
    page.goto("http://localhost:5173/playbook")

    # 1. Verify Default Gameplan Tab
    expect(page.get_by_text("Offensive Install")).to_be_visible()
    expect(page.get_by_text("Week 10 Opponent Intel")).to_be_visible()

    # 2. Switch to Coaching Staff Tab
    page.get_by_text("Coaching Staff").click()

    # 3. Verify Coaching Tree
    expect(page.get_by_text("Coaching Dynasty Tree")).to_be_visible()
    expect(page.get_by_text("Zac Taylor")).to_be_visible()
    expect(page.get_by_text("Offensive Guru")).to_be_visible()


@pytest.mark.e2e
def test_gridiron_heatmap_telemetry(page: Page):
    """Test LiveSim Turf Heatmap and S2 Cognition Telemetry Visualizer."""
    page.goto("http://localhost:5173/live")

    # 1. Switch to Turf & Cognition tab
    turf_tab = page.get_by_role("button", name="Turf & Cognition")
    if turf_tab.is_visible():
        turf_tab.click()

    # 2. Verify Gridiron Visualizer container and canvas exist
    visualizer = page.locator("[data-testid='gridiron-visualizer']")
    expect(visualizer).to_be_visible()

    # 3. Verify layer toggle buttons
    expect(page.get_by_role("button", name=re.compile(r"Turf Heatmap"))).to_be_visible()
    expect(page.get_by_role("button", name=re.compile(r"Vision Cones"))).to_be_visible()
    expect(page.get_by_role("button", name=re.compile(r"S2 Telemetry"))).to_be_visible()
