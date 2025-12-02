import { RouterProvider } from "react-router-dom";
import { router } from "./router";
import "./App.css";

/**
 * App Component
 *
 * Now using React Router v7's RouterProvider for data-driven routing.
 * All route definitions, loaders, and error boundaries are configured in router.tsx
 */
function App() {
  return <RouterProvider router={router} />;
}

export default App;
