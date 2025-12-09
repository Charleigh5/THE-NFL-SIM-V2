import { Component } from "react";
import type { ErrorInfo, ReactNode } from "react";
import "./ErrorBoundary.css";
import { ErrorBoundaryContext } from "../hooks/useErrorBoundary";
import type { ErrorBoundaryContextValue } from "../hooks/useErrorBoundary";

/**
 * Error Boundary Component for NFL Sim Engine
 * ============================================
 *
 * Enterprise-grade error boundary following 2025 React best practices:
 *
 * - TypeScript with strict typing
 * - getDerivedStateFromError for synchronous state updates
 * - componentDidCatch for side effects (logging)
 * - Retry functionality with exponential backoff
 * - Error logging to backend service
 * - Context API for accessing error state in children
 * - Suspense integration patterns
 *
 * References:
 * - https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary
 * - https://react.dev/reference/react/Suspense
 *
 * @version 2.0.0
 */

// ==============================================================================
// TYPES
// ==============================================================================

export interface ErrorBoundaryProps {
  /** Child components to wrap */
  children: ReactNode;
  /** Custom fallback UI to render on error */
  fallback?: ReactNode | ((props: FallbackProps) => ReactNode);
  /** Callback when an error is caught */
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
  /** Callback when user clicks retry */
  onRetry?: () => void;
  /** Maximum number of retry attempts before giving up */
  maxRetries?: number;
  /** Whether to show error details in non-production */
  showDetails?: boolean;
  /** Custom error boundary name for logging context */
  name?: string;
}

export interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
  retryCount: number;
  isRetrying: boolean;
}

export interface FallbackProps {
  error: Error | null;
  errorInfo: ErrorInfo | null;
  resetError: () => void;
  retryCount: number;
  isRetrying: boolean;
}

// ==============================================================================
// ERROR BOUNDARY CLASS
// ==============================================================================

class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  private retryTimeoutId: ReturnType<typeof setTimeout> | null = null;

  static defaultProps: Partial<ErrorBoundaryProps> = {
    maxRetries: 3,
    showDetails: import.meta.env.DEV,
    name: "ErrorBoundary",
  };

  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
      retryCount: 0,
      isRetrying: false,
    };
  }

  /**
   * Static lifecycle method called when a child throws an error.
   * Updates state to trigger fallback UI rendering.
   * Must be pure - no side effects allowed here.
   */
  static getDerivedStateFromError(error: Error): Partial<ErrorBoundaryState> {
    return {
      hasError: true,
      error,
    };
  }

  /**
   * Lifecycle method called after an error is caught.
   * Use for side effects like logging.
   */
  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    // Store error info in state
    this.setState({ errorInfo });

    // Log to console in development
    if (import.meta.env.DEV) {
      console.group(`🚨 ${this.props.name} caught an error`);
      console.error("Error:", error);
      console.error("Component Stack:", errorInfo.componentStack);
      console.groupEnd();
    }

    // Call optional error handler
    if (this.props.onError) {
      this.props.onError(error, errorInfo);
    }

    // Log to backend service
    this.logErrorToService(error, errorInfo);
  }

  componentWillUnmount(): void {
    // Clean up any pending retry timeouts
    if (this.retryTimeoutId) {
      clearTimeout(this.retryTimeoutId);
    }
  }

  /**
   * Send error details to backend logging service.
   * Uses navigator.sendBeacon for reliability on page unload.
   */
  private async logErrorToService(error: Error, errorInfo: ErrorInfo): Promise<void> {
    try {
      const errorPayload = {
        timestamp: new Date().toISOString(),
        type: "render_error",
        boundary: this.props.name,
        error: {
          name: error.name,
          message: error.message,
          stack: error.stack,
        },
        componentStack: errorInfo.componentStack,
        context: {
          url: window.location.href,
          userAgent: navigator.userAgent,
          viewport: {
            width: window.innerWidth,
            height: window.innerHeight,
          },
          retryCount: this.state.retryCount,
        },
      };

      // Try fetch first, fall back to sendBeacon
      const response = await fetch("/api/errors/log", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Error-Type": "react-error-boundary",
        },
        body: JSON.stringify(errorPayload),
        keepalive: true, // Ensure delivery even if page is closing
      });

      if (!response.ok) {
        console.warn("Failed to log error to service:", response.status);
      }
    } catch {
      // Use sendBeacon as fallback
      try {
        navigator.sendBeacon(
          "/api/errors/log",
          JSON.stringify({
            timestamp: new Date().toISOString(),
            type: "render_error",
            error: { message: error.message },
          })
        );
      } catch {
        // Silently fail - don't want to cause more errors
        console.warn("Failed to log error via sendBeacon");
      }
    }
  }

  /**
   * Reset error state and attempt to re-render children.
   * Implements exponential backoff for retry attempts.
   */
  private handleRetry = (): void => {
    const { maxRetries = 3, onRetry } = this.props;
    const { retryCount } = this.state;

    if (retryCount >= maxRetries) {
      console.warn(`${this.props.name}: Max retry attempts (${maxRetries}) reached`);
      return;
    }

    this.setState({ isRetrying: true });

    // Exponential backoff: 100ms, 200ms, 400ms, etc.
    const delay = Math.min(100 * Math.pow(2, retryCount), 3000);

    this.retryTimeoutId = setTimeout(() => {
      this.setState({
        hasError: false,
        error: null,
        errorInfo: null,
        retryCount: retryCount + 1,
        isRetrying: false,
      });

      if (onRetry) {
        onRetry();
      }
    }, delay);
  };

  /**
   * Reset error state immediately (used by context consumers).
   */
  private resetError = (): void => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null,
      retryCount: 0,
      isRetrying: false,
    });
  };

  render(): ReactNode {
    const { children, fallback, showDetails, maxRetries = 3 } = this.props;
    const { hasError, error, errorInfo, retryCount, isRetrying } = this.state;

    // Create context value for child components
    const contextValue: ErrorBoundaryContextValue = {
      error,
      resetError: this.resetError,
    };

    if (hasError) {
      const fallbackProps: FallbackProps = {
        error,
        errorInfo,
        resetError: this.handleRetry,
        retryCount,
        isRetrying,
      };

      // Render custom fallback if provided
      if (fallback) {
        if (typeof fallback === "function") {
          return (
            <ErrorBoundaryContext.Provider value={contextValue}>
              {fallback(fallbackProps)}
            </ErrorBoundaryContext.Provider>
          );
        }
        return (
          <ErrorBoundaryContext.Provider value={contextValue}>
            {fallback}
          </ErrorBoundaryContext.Provider>
        );
      }

      // Default fallback UI
      return (
        <ErrorBoundaryContext.Provider value={contextValue}>
          <div className="error-boundary" role="alert" aria-live="assertive">
            <div className="error-boundary__content">
              <div className="error-boundary__icon" aria-hidden="true">
                ⚠️
              </div>
              <h2 className="error-boundary__title">Something went wrong</h2>
              <p className="error-boundary__message">
                We apologize for the inconvenience. An unexpected error has occurred.
              </p>

              {showDetails && error && (
                <details className="error-boundary__details">
                  <summary>Error Details (Development Only)</summary>
                  <div className="error-boundary__error-info">
                    <p>
                      <strong>Error:</strong> {error.name}
                    </p>
                    <p>
                      <strong>Message:</strong> {error.message}
                    </p>
                    {error.stack && <pre className="error-boundary__stack">{error.stack}</pre>}
                    {errorInfo?.componentStack && (
                      <>
                        <p>
                          <strong>Component Stack:</strong>
                        </p>
                        <pre className="error-boundary__stack">{errorInfo.componentStack}</pre>
                      </>
                    )}
                  </div>
                </details>
              )}

              <div className="error-boundary__actions">
                {retryCount < maxRetries && (
                  <button
                    className="error-boundary__retry-button"
                    onClick={this.handleRetry}
                    disabled={isRetrying}
                    {...(isRetrying && { "aria-busy": "true" })}
                  >
                    {isRetrying ? (
                      <>
                        <span className="error-boundary__spinner" aria-hidden="true" />
                        Retrying...
                      </>
                    ) : (
                      `Try Again ${retryCount > 0 ? `(${retryCount}/${maxRetries})` : ""}`
                    )}
                  </button>
                )}

                <button
                  className="error-boundary__reload-button"
                  onClick={() => window.location.reload()}
                >
                  Reload Page
                </button>
              </div>

              {retryCount >= maxRetries && (
                <p className="error-boundary__max-retries">
                  Maximum retry attempts reached. Please reload the page or contact support.
                </p>
              )}
            </div>
          </div>
        </ErrorBoundaryContext.Provider>
      );
    }

    return (
      <ErrorBoundaryContext.Provider value={contextValue}>{children}</ErrorBoundaryContext.Provider>
    );
  }
}

export default ErrorBoundary;
