/**
 * CSS Selector Generation Utility
 * ================================
 * Generates unique CSS selectors for DOM elements.
 *
 * Context7 Best Practices:
 * - Pure function (no side effects)
 * - Type safety with TypeScript
 * - Comprehensive fallback strategy
 */

/**
 * Generate a unique CSS selector for a given DOM element.
 * Priority: ID > data-testid > unique class combo > nth-child path
 */
export function generateCssSelector(element: HTMLElement): string {
  // 1. Try ID (most unique)
  if (element.id) {
    return `#${CSS.escape(element.id)}`;
  }

  // 2. Try data-testid (common in React testing)
  const testId = element.getAttribute("data-testid");
  if (testId) {
    return `[data-testid="${CSS.escape(testId)}"]`;
  }

  // 3. Try unique class combination
  if (element.classList.length > 0) {
    const classes = Array.from(element.classList);
    const classSelector = `.${classes.map((c) => CSS.escape(c)).join(".")}`;

    // Verify uniqueness
    if (document.querySelectorAll(classSelector).length === 1) {
      return classSelector;
    }
  }

  // 4. Build nth-child path from element to body
  return buildNthChildPath(element);
}

/**
 * Build a path using nth-of-type selectors.
 */
function buildNthChildPath(element: HTMLElement): string {
  const path: string[] = [];
  let current: HTMLElement | null = element;

  while (current && current !== document.body && current.parentElement) {
    const tag = current.tagName.toLowerCase();
    const parent: HTMLElement = current.parentElement;

    // Find index among siblings of same tag type
    const siblings = Array.from(parent.children).filter(
      (child: Element) => child.tagName === current!.tagName
    );
    const index = siblings.indexOf(current) + 1;

    // Use nth-of-type if multiple siblings, else just tag
    path.unshift(siblings.length > 1 ? `${tag}:nth-of-type(${index})` : tag);

    current = parent;
  }

  return path.join(" > ");
}

/**
 * Get a human-readable description of an element.
 */
export function getElementDescription(element: HTMLElement): string {
  // Try text content first
  const text = element.textContent?.trim().substring(0, 50);
  if (text) {
    return text.length === 50 ? `${text}...` : text;
  }

  // Try aria-label
  const ariaLabel = element.getAttribute("aria-label");
  if (ariaLabel) {
    return ariaLabel;
  }

  // Try placeholder (for inputs)
  const placeholder = element.getAttribute("placeholder");
  if (placeholder) {
    return placeholder;
  }

  // Fall back to tag name and classes
  return `<${element.tagName.toLowerCase()}${
    element.className ? ` class="${element.className}"` : ""
  }>`;
}

/**
 * Verify that a selector correctly identifies the target element.
 */
export function verifySelectorUniqueness(selector: string): boolean {
  try {
    const matches = document.querySelectorAll(selector);
    return matches.length === 1;
  } catch {
    return false;
  }
}
