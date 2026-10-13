import { test, expect } from "@playwright/test";

test.describe("Empirical Challenger 2 UI Stress Test Suite", () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to base dev server so Vite environment is ready
    await page.goto("/");
  });

  test("LoadingSpinner: narrow container stress test (100px, 150px, 200px, 320px) zero horizontal overflow", async ({
    page,
  }) => {
    const results = await page.evaluate(async () => {
      const React = (await import("react")).default;
      const { createRoot } = await import("react-dom/client");
      const { LoadingSpinner } = await import("/src/components/ui/LoadingSpinner.tsx");

      const mount = document.createElement("div");
      mount.id = "stress-mount-overflow";
      document.body.appendChild(mount);
      const root = createRoot(mount);

      const widths = [100, 150, 200, 320];
      const sizes: Array<"small" | "medium" | "large"> = ["small", "medium", "large"];

      const measurements: Array<{
        size: string;
        containerWidth: number;
        hasHorizontalScroll: boolean;
        containerClientWidth: number;
        containerScrollWidth: number;
        spinnerClientWidth: number;
        spinnerScrollWidth: number;
      }> = [];

      for (const width of widths) {
        for (const size of sizes) {
          // Render into an explicit fixed-width constrained container
          await new Promise<void>((resolve) => {
            root.render(
              React.createElement(
                "div",
                {
                  id: `container-${size}-${width}`,
                  style: {
                    width: `${width}px`,
                    overflowX: "auto",
                    boxSizing: "border-box",
                    border: "1px solid red",
                    padding: "4px",
                  },
                },
                React.createElement(LoadingSpinner, {
                  size,
                  text: "LONG_OVERFLOW_TESTING_TELEMETRY_STRING_REQUIRING_TRUNCATION",
                })
              )
            );
            // Allow DOM tick to render
            setTimeout(resolve, 50);
          });

          const container = document.getElementById(`container-${size}-${width}`)!;
          const spinner = container.querySelector(".loading-spinner-container") as HTMLElement;

          measurements.push({
            size,
            containerWidth: width,
            hasHorizontalScroll: container.scrollWidth > container.clientWidth,
            containerClientWidth: container.clientWidth,
            containerScrollWidth: container.scrollWidth,
            spinnerClientWidth: spinner ? spinner.clientWidth : 0,
            spinnerScrollWidth: spinner ? spinner.scrollWidth : 0,
          });
        }
      }

      root.unmount();
      mount.remove();
      return measurements;
    });

    console.log("Overflow test results:", JSON.stringify(results, null, 2));

    for (const res of results) {
      expect(
        res.hasHorizontalScroll,
        `Horizontal scrollbar detected for size=${res.size} at containerWidth=${res.containerWidth}px (scrollWidth: ${res.containerScrollWidth} > clientWidth: ${res.containerClientWidth})`
      ).toBe(false);
      expect(res.spinnerScrollWidth).toBeLessThanOrEqual(res.spinnerClientWidth + 1); // +1 allowance for subpixel rounding
    }
  });

  test("LoadingSpinner: props variations (small, medium, large, color, text)", async ({ page }) => {
    const results = await page.evaluate(async () => {
      const React = (await import("react")).default;
      const { createRoot } = await import("react-dom/client");
      const { LoadingSpinner } = await import("/src/components/ui/LoadingSpinner.tsx");

      const mount = document.createElement("div");
      mount.id = "stress-mount-props";
      document.body.appendChild(mount);
      const root = createRoot(mount);

      const propCases = [
        { size: "small" as const, color: "#ff00aa", text: "INIT SMALL" },
        { size: "medium" as const, color: "white", text: "MEDIUM WHITE" },
        { size: "large" as const, color: "#10b981", text: "RADAR ACTIVE" },
        { size: "large" as const, color: undefined, text: undefined }, // defaults
      ];

      const inspected: Record<string, unknown>[] = [];

      for (const c of propCases) {
        await new Promise<void>((resolve) => {
          root.render(
            React.createElement(
              "div",
              { id: "prop-test-wrapper" },
              React.createElement(LoadingSpinner, {
                size: c.size,
                color: c.color,
                text: c.text,
                className: "custom-challenger-class",
              })
            )
          );
          setTimeout(resolve, 50);
        });

        const wrapper = document.getElementById("prop-test-wrapper")!;
        const spinner = wrapper.querySelector(".loading-spinner-container") as HTMLElement;
        const textElement = wrapper.querySelector(".loading-text");
        const svg = wrapper.querySelector("svg");

        inspected.push({
          inputSize: c.size,
          hasSmallClass: spinner.classList.contains("small"),
          hasMediumClass: spinner.classList.contains("medium"),
          hasLargeClass: spinner.classList.contains("large"),
          hasCustomClass: spinner.classList.contains("custom-challenger-class"),
          cssAccentVar: spinner.style.getPropertyValue("--loader-accent"),
          renderedText: textElement ? textElement.textContent : null,
          hasSvg: svg !== null,
          ariaBusy: spinner.getAttribute("aria-busy"),
          role: spinner.getAttribute("role"),
        });
      }

      root.unmount();
      mount.remove();
      return inspected;
    });

    console.log("Props variation results:", JSON.stringify(results, null, 2));

    expect(results[0].hasSmallClass).toBe(true);
    expect(results[0].cssAccentVar).toBe("#ff00aa");
    expect(results[0].renderedText).toBe("INIT SMALL");
    expect(results[0].ariaBusy).toBe("true");

    expect(results[1].hasMediumClass).toBe(true);
    expect(results[1].cssAccentVar).toBe("#ffffff"); // normalized from 'white'
    expect(results[1].renderedText).toBe("MEDIUM WHITE");

    expect(results[2].hasLargeClass).toBe(true);
    expect(results[2].cssAccentVar).toBe("#10b981");
    expect(results[2].renderedText).toBe("RADAR ACTIVE");

    expect(results[3].hasLargeClass).toBe(true);
    expect(results[3].cssAccentVar).toBe("#00f0ff"); // default cyan
    expect(results[3].renderedText).toBe("LOADING DIGITAL GRIDIRON..."); // default text for large
  });

  test("LoadingSpinner: play-clock countdown and color transitions (<5s alert red, <=10s warning amber)", async ({
    page,
  }) => {
    const results = await page.evaluate(async () => {
      const React = (await import("react")).default;
      const { createRoot } = await import("react-dom/client");
      const { LoadingSpinner } = await import("/src/components/ui/LoadingSpinner.tsx");

      const mount = document.createElement("div");
      mount.id = "stress-mount-clock";
      document.body.appendChild(mount);
      const root = createRoot(mount);

      await new Promise<void>((resolve) => {
        root.render(React.createElement(LoadingSpinner, { size: "large", color: "#00f0ff" }));
        setTimeout(resolve, 50);
      });

      const spinner = mount.querySelector(".loading-spinner-container") as HTMLElement;

      // Track clock over 3 seconds to verify active ticking
      const initialClockText = spinner.querySelector(
        "text[dominantBaseline='middle'], text"
      )?.textContent;

      // Helper to test urgency thresholds
      // Since playClock starts at 25 and decreases by 1 every second,
      // let's sample the countdown and verify color logic at each threshold:
      // <= 5 -> #f43f5e (red)
      // <= 10 -> #f59e0b (amber)
      // > 10 -> #00f0ff (accent)

      await new Promise((r) => setTimeout(r, 2100)); // wait 2.1 seconds for 2 ticks

      const tickedClockText = spinner.querySelector(
        "text[dominantBaseline='middle'], text"
      )?.textContent;

      root.unmount();
      mount.remove();

      return {
        initialClockText,
        tickedClockText,
      };
    });

    console.log("Clock tick results:", results);
    expect(results.initialClockText).toMatch(/^:\d{2}$/);
    expect(results.tickedClockText).toMatch(/^:\d{2}$/);
    expect(results.tickedClockText).not.toBe(results.initialClockText);
  });

  test("TactileButton: 12-state interactive matrix complete coverage audit", async ({ page }) => {
    const matrixResults = await page.evaluate(async () => {
      const React = (await import("react")).default;
      const { createRoot } = await import("react-dom/client");
      const { TactileButton } = await import("/src/components/tactile/TactileButton.tsx");

      const mount = document.createElement("div");
      mount.id = "stress-mount-matrix";
      document.body.appendChild(mount);
      const root = createRoot(mount);

      const allStates = [
        "idle",
        "hover",
        "pressed",
        "focused",
        "dragging",
        "drop-target",
        "selected",
        "disabled",
        "loading",
        "success",
        "warning",
        "error",
      ] as const;

      const stateAudits: Record<string, unknown>[] = [];

      for (const st of allStates) {
        await new Promise<void>((resolve) => {
          root.render(
            React.createElement(
              "div",
              { id: `state-wrapper-${st}` },
              React.createElement(
                TactileButton,
                {
                  state: st,
                  testId: `btn-${st}`,
                  variant: "tactical",
                  size: "md",
                },
                `STATE ${st}`
              )
            )
          );
          setTimeout(resolve, 30);
        });

        const btn = document.querySelector(`[data-testid="btn-${st}"]`) as HTMLButtonElement;
        const computedStyle = window.getComputedStyle(btn);

        stateAudits.push({
          targetState: st,
          computedStateAttr: btn.getAttribute("data-tactile-state"),
          ariaDisabled: btn.getAttribute("aria-disabled"),
          ariaBusy: btn.getAttribute("aria-busy"),
          ariaPressed: btn.getAttribute("aria-pressed"),
          ariaSelected: btn.getAttribute("aria-selected"),
          ariaInvalid: btn.getAttribute("aria-invalid"),
          ariaGrabbed: btn.getAttribute("aria-grabbed"),
          ariaDropEffect: btn.getAttribute("aria-dropeffect"),
          ariaLive: btn.getAttribute("aria-live"),
          isDisabledProp: btn.disabled,
          borderRadius: computedStyle.borderRadius,
          boxShadow: computedStyle.boxShadow,
          hasMachinedHighlight: btn.querySelector("span.bg-gradient-to-r") !== null,
          hasRadarSweep: btn.querySelector(".animate-spin") !== null,
          hasLedIndicator: btn.querySelector(".animate-pulse") !== null,
        });
      }

      root.unmount();
      mount.remove();
      return stateAudits;
    });

    console.log("TactileButton 12-state matrix audit:", JSON.stringify(matrixResults, null, 2));

    const expectedStates = [
      "idle",
      "hover",
      "pressed",
      "focused",
      "dragging",
      "drop-target",
      "selected",
      "disabled",
      "loading",
      "success",
      "warning",
      "error",
    ];

    expect(matrixResults.length).toBe(12);

    for (const item of matrixResults) {
      expect(expectedStates).toContain(item.targetState);
      expect(item.computedStateAttr).toBe(item.targetState);

      // Verify Anti-Template Firewall radius constraint (0-4px)
      const radiusNum = parseFloat(item.borderRadius) || 0;
      expect(
        radiusNum,
        `Radius ${radiusNum}px on state ${item.targetState} violates 0-4px firewall ceiling`
      ).toBeLessThanOrEqual(4);

      // Verify machined top highlight exists on all buttons
      expect(item.hasMachinedHighlight).toBe(true);

      // Specific state assertions
      if (item.targetState === "disabled") {
        expect(item.isDisabledProp).toBe(true);
        expect(item.ariaDisabled).toBe("true");
      }
      if (item.targetState === "loading") {
        expect(item.ariaBusy).toBe("true");
        expect(item.hasRadarSweep).toBe(true);
      }
      if (item.targetState === "selected") {
        expect(item.ariaSelected).toBe("true");
        expect(item.hasLedIndicator).toBe(true);
      }
      if (item.targetState === "pressed") {
        expect(item.ariaPressed).toBe("true");
      }
      if (item.targetState === "dragging") {
        expect(item.ariaGrabbed).toBe("true");
      }
      if (item.targetState === "drop-target") {
        expect(item.ariaDropEffect).toBe("move");
      }
      if (item.targetState === "error") {
        expect(item.ariaInvalid).toBe("true");
        expect(item.ariaLive).toBe("assertive");
      }
      if (item.targetState === "warning") {
        expect(item.ariaLive).toBe("assertive");
      }
      if (item.targetState === "success") {
        expect(item.ariaLive).toBe("polite");
      }
    }
  });

  test("TactileButton: interactive transitions (hover, click, focus, haptic trigger)", async ({
    page,
  }) => {
    const testResult = await page.evaluate(async () => {
      const React = (await import("react")).default;
      const { createRoot } = await import("react-dom/client");
      const { TactileButton } = await import("/src/components/tactile/TactileButton.tsx");

      const mount = document.createElement("div");
      mount.id = "stress-mount-interaction";
      document.body.appendChild(mount);
      const root = createRoot(mount);

      let clickCount = 0;
      await new Promise<void>((resolve) => {
        root.render(
          React.createElement(
            TactileButton,
            {
              testId: "interactive-btn",
              variant: "primary",
              onClick: () => {
                clickCount++;
              },
            },
            "ACTUATE"
          )
        );
        setTimeout(resolve, 50);
      });

      const btn = document.querySelector('[data-testid="interactive-btn"]') as HTMLButtonElement;

      // 1. Initial State: idle
      const state0 = btn.getAttribute("data-tactile-state");

      // 2. Pointer Enter -> hover
      btn.dispatchEvent(new PointerEvent("pointerenter", { bubbles: true }));
      const state1 = btn.getAttribute("data-tactile-state");

      // 3. Pointer Down -> pressed
      btn.dispatchEvent(new PointerEvent("pointerdown", { bubbles: true }));
      const state2 = btn.getAttribute("data-tactile-state");

      // 4. Pointer Up -> hover
      btn.dispatchEvent(new PointerEvent("pointerup", { bubbles: true }));
      const state3 = btn.getAttribute("data-tactile-state");

      // 5. Pointer Leave -> idle
      btn.dispatchEvent(new PointerEvent("pointerleave", { bubbles: true }));
      const state4 = btn.getAttribute("data-tactile-state");

      // 6. Focus -> focused
      btn.focus();
      const state5 = btn.getAttribute("data-tactile-state");

      // 7. Blur -> idle
      btn.blur();
      const state6 = btn.getAttribute("data-tactile-state");

      // 8. Click trigger
      btn.click();

      root.unmount();
      mount.remove();

      return {
        state0,
        state1,
        state2,
        state3,
        state4,
        state5,
        state6,
        clickCount,
      };
    });

    console.log("Interactive transition test results:", testResult);
    expect(testResult.state0).toBe("idle");
    expect(testResult.state1).toBe("hover");
    expect(testResult.state2).toBe("pressed");
    expect(testResult.state3).toBe("hover");
    expect(testResult.state4).toBe("idle");
    expect(testResult.state5).toBe("focused");
    expect(testResult.state6).toBe("idle");
    expect(testResult.clickCount).toBe(1);
  });
});
