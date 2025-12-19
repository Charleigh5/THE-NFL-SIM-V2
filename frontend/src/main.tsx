import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import "./index.css";
import { AudioProvider } from "./context/AudioContext.tsx";
import { ThemeProvider } from "./context/ThemeContext.tsx";
import App from "./App.tsx";

const queryClient = new QueryClient();

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <AudioProvider>
        <ThemeProvider>
          <App />
        </ThemeProvider>
      </AudioProvider>
    </QueryClientProvider>
  </StrictMode>
);
