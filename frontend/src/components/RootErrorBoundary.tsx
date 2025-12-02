/**
 * RootErrorBoundary Component
 * Top-level error boundary for catching errors at the router level
 */
const RootErrorBoundary = () => (
  <div className="page-placeholder">
    <h1>Oops! Something went wrong</h1>
    <p>We encountered an unexpected error. Please try refreshing the page.</p>
  </div>
);

export default RootErrorBoundary;
