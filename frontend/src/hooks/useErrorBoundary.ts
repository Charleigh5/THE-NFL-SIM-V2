import { createContext, useContext } from "react";

/**
 * Context value for error boundary state
 */
export interface ErrorBoundaryContextValue {
  error: Error | null;
  resetError: () => void;
}

/**
 * Error boundary context - exported for use by ErrorBoundary component
 */
export const ErrorBoundaryContext = createContext<ErrorBoundaryContextValue>({
  error: null,
  resetError: () => {},
});

/**
 * Hook to access error boundary state from child components.
 *
 * @example
 * ```tsx
 * function ChildComponent() {
 *   const { error, resetError } = useErrorBoundary();
 *   if (error) {
 *     return <button onClick={resetError}>Try Again</button>;
 *   }
 *   return <div>Normal content</div>;
 * }
 * ```
 */
export function useErrorBoundary(): ErrorBoundaryContextValue {
  return useContext(ErrorBoundaryContext);
}
