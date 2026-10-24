/**
 * Automated Verification Suite for Modal Stack Store & Interaction Hierarchy
 * Standards: Deterministic invariants, W3C WAI-APG stacking rules, LIFO ordering.
 */

import assert from "node:assert/strict";
import { useModalStackStore } from "../store/useModalStackStore.ts";

console.log("================================================================================");
console.log("MODAL STACK STORE & HIERARCHY VERIFICATION SUITE");
console.log("================================================================================\n");

// Helper to reset store before each test
function resetStore() {
  useModalStackStore.getState().clearStack();
}

// -----------------------------------------------------------------------------
// Test 1: Initial State Invariant
// -----------------------------------------------------------------------------
console.log("Test 1: Initial State Invariants...");
{
  resetStore();
  const state = useModalStackStore.getState();

  assert.deepEqual(state.stack, [], "Initial stack should be empty array");
  assert.equal(state.getTopModal(), null, "getTopModal should return null when stack is empty");
  assert.equal(
    state.isTopModal("any-modal"),
    false,
    "isTopModal should return false for any id when stack is empty"
  );
  console.log("  [PASS] Initial state has empty stack, null topModal, false isTopModal.");
}

// -----------------------------------------------------------------------------
// Test 2: LIFO Push & Depth Sequencing Invariant
// -----------------------------------------------------------------------------
console.log("\nTest 2: LIFO Push & Depth Sequencing Invariants...");
{
  resetStore();
  let dismissACalled = 0;
  let dismissBCalled = 0;
  let dismissCCalled = 0;

  const mockTriggerA = { id: "button-trigger-a" } as unknown as HTMLElement;
  const mockTriggerB = { id: "button-trigger-b" } as unknown as HTMLElement;

  // Push Modal A
  useModalStackStore.getState().pushModal(
    "modal-a",
    () => {
      dismissACalled++;
    },
    mockTriggerA
  );
  {
    const state = useModalStackStore.getState();
    assert.equal(state.stack.length, 1, "Stack length should be 1 after push A");
    assert.equal(state.stack[0].id, "modal-a");
    assert.equal(state.stack[0].depth, 0, "First modal depth should be 0");
    assert.equal(
      state.stack[0].triggerElement,
      mockTriggerA,
      "Trigger element should be preserved"
    );
    assert.equal(state.getTopModal()?.id, "modal-a");
    assert.equal(state.isTopModal("modal-a"), true, "modal-a should be top modal");
  }

  // Push Modal B
  useModalStackStore.getState().pushModal(
    "modal-b",
    () => {
      dismissBCalled++;
    },
    mockTriggerB
  );
  {
    const state = useModalStackStore.getState();
    assert.equal(state.stack.length, 2, "Stack length should be 2 after push B");
    assert.equal(state.stack[1].id, "modal-b");
    assert.equal(state.stack[1].depth, 1, "Second modal depth should be 1");
    assert.equal(state.stack[1].triggerElement, mockTriggerB);
    assert.equal(state.getTopModal()?.id, "modal-b");
    assert.equal(state.isTopModal("modal-b"), true, "modal-b should be top modal");
    assert.equal(state.isTopModal("modal-a"), false, "modal-a should no longer be top modal");
  }

  // Push Modal C
  useModalStackStore.getState().pushModal("modal-c", () => {
    dismissCCalled++;
  });
  {
    const state = useModalStackStore.getState();
    assert.equal(state.stack.length, 3, "Stack length should be 3 after push C");
    assert.equal(state.stack[2].id, "modal-c");
    assert.equal(state.stack[2].depth, 2, "Third modal depth should be 2");
    assert.equal(state.stack[2].triggerElement, null, "Default trigger element should be null");
    assert.equal(state.getTopModal()?.id, "modal-c");
    assert.equal(state.isTopModal("modal-c"), true, "modal-c should be top modal");
    assert.equal(state.isTopModal("modal-b"), false);
    assert.equal(state.isTopModal("modal-a"), false);
  }

  assert.equal(dismissACalled, 0, "No dismiss callbacks should have fired during push");
  assert.equal(dismissBCalled, 0);
  assert.equal(dismissCCalled, 0);
  console.log(
    "  [PASS] Sequential push correctly increments stack size, depths (0, 1, 2), and top assignment."
  );
}

// -----------------------------------------------------------------------------
// Test 3: Stack Deduplication Invariant
// -----------------------------------------------------------------------------
console.log("\nTest 3: Stack Deduplication Invariants...");
{
  resetStore();
  let dismissA1 = 0;
  let dismissA2 = 0;

  useModalStackStore.getState().pushModal("modal-a", () => {
    dismissA1++;
  });
  useModalStackStore.getState().pushModal("modal-b", () => {});
  useModalStackStore.getState().pushModal("modal-c", () => {});

  assert.equal(useModalStackStore.getState().stack.length, 3);
  assert.equal(useModalStackStore.getState().isTopModal("modal-a"), false);

  // Re-push modal-a (simulates bringing an existing modal to front or re-opening)
  useModalStackStore.getState().pushModal("modal-a", () => {
    dismissA2++;
  });

  const state = useModalStackStore.getState();
  assert.equal(state.stack.length, 3, "Stack length should remain 3 (deduplicated, not 4)");
  assert.deepEqual(
    state.stack.map((m) => m.id),
    ["modal-b", "modal-c", "modal-a"],
    "modal-a should have moved to top of stack"
  );
  assert.equal(state.isTopModal("modal-a"), true, "modal-a should now be top modal");
  assert.equal(state.getTopModal()?.id, "modal-a");
  assert.equal(
    state.stack[2].depth,
    2,
    "Re-pushed modal should have depth equal to filtered length"
  );
  assert.equal(dismissA1, 0, "Deduplication push should not fire dismiss callback");
  assert.equal(
    dismissA2,
    0,
    "Deduplication push should not fire dismiss callback for new instance"
  );

  console.log(
    "  [PASS] Deduplication removes previous instance and promotes modal to top without duplication."
  );
}

// -----------------------------------------------------------------------------
// Test 4: LIFO Pop & Dismiss Callback Execution Invariant
// -----------------------------------------------------------------------------
console.log("\nTest 4: LIFO Pop & Dismiss Callback Execution Invariants...");
{
  resetStore();
  let dismissA = 0;
  let dismissB = 0;
  let dismissC = 0;

  useModalStackStore.getState().pushModal("modal-a", () => {
    dismissA++;
  });
  useModalStackStore.getState().pushModal("modal-b", () => {
    dismissB++;
  });
  useModalStackStore.getState().pushModal("modal-c", () => {
    dismissC++;
  });

  // Pop #1 -> should pop modal-c
  useModalStackStore.getState().popModal();
  {
    const state = useModalStackStore.getState();
    assert.equal(dismissC, 1, "modal-c onDismiss should be called exactly once");
    assert.equal(dismissB, 0);
    assert.equal(dismissA, 0);
    assert.equal(state.stack.length, 2);
    assert.equal(state.getTopModal()?.id, "modal-b");
    assert.equal(state.isTopModal("modal-b"), true);
  }

  // Pop #2 -> should pop modal-b
  useModalStackStore.getState().popModal();
  {
    const state = useModalStackStore.getState();
    assert.equal(dismissC, 1);
    assert.equal(dismissB, 1, "modal-b onDismiss should be called exactly once");
    assert.equal(dismissA, 0);
    assert.equal(state.stack.length, 1);
    assert.equal(state.getTopModal()?.id, "modal-a");
    assert.equal(state.isTopModal("modal-a"), true);
  }

  // Pop #3 -> should pop modal-a
  useModalStackStore.getState().popModal();
  {
    const state = useModalStackStore.getState();
    assert.equal(dismissC, 1);
    assert.equal(dismissB, 1);
    assert.equal(dismissA, 1, "modal-a onDismiss should be called exactly once");
    assert.equal(state.stack.length, 0);
    assert.equal(state.getTopModal(), null);
  }

  // Pop #4 on empty stack -> safe no-op
  useModalStackStore.getState().popModal();
  {
    const state = useModalStackStore.getState();
    assert.equal(state.stack.length, 0);
    assert.equal(state.getTopModal(), null);
    assert.equal(dismissA, 1, "No further callbacks should fire on empty pop");
  }

  console.log(
    "  [PASS] LIFO popModal correctly unwinds stack and invokes onDismiss for each popped modal."
  );
}

// -----------------------------------------------------------------------------
// Test 5: Targeted Removal (Pop by ID from Arbitrary Stack Depth) Invariant
// -----------------------------------------------------------------------------
console.log("\nTest 5: Targeted Removal by ID Invariants...");
{
  resetStore();
  let dismissM1 = 0;
  let dismissM2 = 0;
  let dismissM3 = 0;
  let dismissM4 = 0;

  useModalStackStore.getState().pushModal("M1", () => {
    dismissM1++;
  });
  useModalStackStore.getState().pushModal("M2", () => {
    dismissM2++;
  });
  useModalStackStore.getState().pushModal("M3", () => {
    dismissM3++;
  });
  useModalStackStore.getState().pushModal("M4", () => {
    dismissM4++;
  });

  assert.equal(useModalStackStore.getState().stack.length, 4);

  // Pop middle modal M2 by ID
  useModalStackStore.getState().popModal("M2");
  {
    const state = useModalStackStore.getState();
    assert.equal(dismissM2, 1, "M2 onDismiss should be invoked");
    assert.equal(dismissM1, 0, "M1 onDismiss should NOT be invoked");
    assert.equal(dismissM3, 0, "M3 onDismiss should NOT be invoked");
    assert.equal(dismissM4, 0, "M4 onDismiss should NOT be invoked");
    assert.deepEqual(
      state.stack.map((m) => m.id),
      ["M1", "M3", "M4"],
      "M2 should be cleanly removed from middle"
    );
    assert.deepEqual(
      state.stack.map((m) => m.depth),
      [0, 1, 2],
      "Remaining modal depths should be re-indexed sequentially after removal"
    );
    assert.equal(state.getTopModal()?.id, "M4", "Top modal should remain M4");
    assert.equal(state.isTopModal("M4"), true);
    assert.equal(state.isTopModal("M2"), false);
  }

  // Pop bottom modal M1 by ID
  useModalStackStore.getState().popModal("M1");
  {
    const state = useModalStackStore.getState();
    assert.equal(dismissM1, 1, "M1 onDismiss should be invoked");
    assert.deepEqual(
      state.stack.map((m) => m.id),
      ["M3", "M4"]
    );
  }

  // Pop top modal M4 by ID
  useModalStackStore.getState().popModal("M4");
  {
    const state = useModalStackStore.getState();
    assert.equal(dismissM4, 1, "M4 onDismiss should be invoked");
    assert.deepEqual(
      state.stack.map((m) => m.id),
      ["M3"]
    );
    assert.equal(state.getTopModal()?.id, "M3");
    assert.equal(state.isTopModal("M3"), true);
  }

  // Non-existent ID pop -> safe no-op
  useModalStackStore.getState().popModal("non-existent-id");
  {
    const state = useModalStackStore.getState();
    assert.equal(state.stack.length, 1);
    assert.equal(dismissM3, 0, "M3 should not be dismissed");
  }

  console.log(
    "  [PASS] Targeted popModal(id) surgically removes target modal without disrupting sibling integrity."
  );
}

// -----------------------------------------------------------------------------
// Test 6: Clear Stack Invariant & Re-entrancy
// -----------------------------------------------------------------------------
console.log("\nTest 6: Clear Stack Invariant & Re-entrancy...");
{
  resetStore();
  let dismissX = 0;
  let dismissY = 0;

  useModalStackStore.getState().pushModal("X", () => {
    dismissX++;
  });
  useModalStackStore.getState().pushModal("Y", () => {
    dismissY++;
  });

  assert.equal(useModalStackStore.getState().stack.length, 2);

  useModalStackStore.getState().clearStack();
  {
    const state = useModalStackStore.getState();
    assert.deepEqual(state.stack, []);
    assert.equal(state.getTopModal(), null);
    assert.equal(state.isTopModal("X"), false);
    assert.equal(state.isTopModal("Y"), false);
    assert.equal(dismissX, 0, "clearStack resets state without calling onDismiss");
    assert.equal(dismissY, 0);
  }

  // Re-pushing works normally after clear
  useModalStackStore.getState().pushModal("Z", () => {});
  {
    const state = useModalStackStore.getState();
    assert.equal(state.stack.length, 1);
    assert.equal(state.getTopModal()?.id, "Z");
    assert.equal(state.stack[0].depth, 0);
  }

  console.log("  [PASS] clearStack purges all modal instances and preserves store re-usability.");
}

console.log("\n================================================================================");
console.log("ALL 6 MODAL STACK HIERARCHY TESTS PASSED WITH 100% SUCCESS!");
console.log("================================================================================\n");
