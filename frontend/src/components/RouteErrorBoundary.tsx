import { useRouteError, isRouteErrorResponse } from "react-router-dom";

/**
 * RouteErrorBoundary Component
 *
 * Enhanced error boundary for individual routes
 * Displays user-friendly error messages based on error type
 */
const RouteErrorBoundary = () => {
  const error = useRouteError();

  // Handle HTTP response errors (thrown Response objects)
  if (isRouteErrorResponse(error)) {
    return (
      <div className="page-placeholder">
        <h1>{error.status} Error</h1>
        <p>{error.statusText || "An error occurred"}</p>
        {error.data && <p className="error-detail">{error.data}</p>}
      </div>
    );
  }

  // Handle JavaScript errors
  if (error instanceof Error) {
    return (
      <div className="page-placeholder">
        <h1>Unexpected Error</h1>
        <p>{error.message}</p>
        <details>
          <summary>Stack Trace</summary>
          <pre>{error.stack}</pre>
        </details>
      </div>
    );
  }

  // Fallback for unknown error types
  return (
    <div className="page-placeholder">
      <h1>Something went wrong</h1>
      <p>An unexpected error occurred. Please try again.</p>
    </div>
  );
};

export default RouteErrorBoundary;
