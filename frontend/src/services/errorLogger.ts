/**
 * Error Logging Service
 * =====================
 *
 * Centralized service for logging errors to the backend with 2025 best practices:
 *
 * - Singleton pattern with lazy initialization
 * - Batch processing to reduce network requests
 * - Reliable delivery with sendBeacon on page unload
 * - TypeScript discriminated unions for error categories
 * - Context enrichment with request/session info
 * - Rate limiting to prevent log flooding
 * - Offline queue with localStorage fallback
 *
 * @version 2.0.0
 */

// ==============================================================================
// TYPES
// ==============================================================================

/**
 * Error categories for classification and filtering
 */
export const ErrorCategory = {
  /** React rendering errors caught by ErrorBoundary */
  RENDER: "RENDER",
  /** API/network request failures */
  API: "API",
  /** Form validation errors */
  VALIDATION: "VALIDATION",
  /** Router/navigation errors */
  NAVIGATION: "NAVIGATION",
  /** State management errors (Redux, Zustand, etc.) */
  STATE: "STATE",
  /** WebSocket connection errors */
  WEBSOCKET: "WEBSOCKET",
  /** Authentication/authorization errors */
  AUTH: "AUTH",
  /** Performance-related issues */
  PERFORMANCE: "PERFORMANCE",
  /** Uncategorized errors */
  UNKNOWN: "UNKNOWN",
} as const;

export type ErrorCategory = (typeof ErrorCategory)[keyof typeof ErrorCategory];

/**
 * Severity levels for prioritizing errors
 */
export const ErrorSeverity = {
  /** Minor issues that don't affect user experience */
  LOW: "LOW",
  /** Issues that degrade user experience */
  MEDIUM: "MEDIUM",
  /** Critical issues that block user actions */
  HIGH: "HIGH",
  /** Fatal errors that crash the application */
  CRITICAL: "CRITICAL",
} as const;

export type ErrorSeverity = (typeof ErrorSeverity)[keyof typeof ErrorSeverity];

/**
 * Error log payload sent to the backend
 */
export interface ErrorLogPayload {
  /** ISO timestamp of when the error occurred */
  timestamp: string;
  /** Unique identifier for this error instance */
  id: string;
  /** Error category for classification */
  category: ErrorCategory;
  /** Error severity level */
  severity: ErrorSeverity;
  /** Human-readable error message */
  message: string;
  /** Error stack trace if available */
  stack?: string;
  /** React component stack for render errors */
  componentStack?: string;
  /** URL where the error occurred */
  url: string;
  /** User agent string */
  userAgent: string;
  /** Additional context data */
  context?: Record<string, unknown>;
  /** Client-side session ID */
  sessionId?: string;
  /** Request correlation ID */
  requestId?: string;
  /** User ID if authenticated */
  userId?: string;
}

/**
 * Configuration options for the error logger
 */
export interface ErrorLoggerConfig {
  /** API endpoint for logging errors */
  endpoint: string;
  /** Maximum errors to queue before sending */
  batchSize: number;
  /** Interval in ms to flush the queue */
  flushInterval: number;
  /** Maximum errors per minute (rate limiting) */
  maxErrorsPerMinute: number;
  /** Whether to log to console in development */
  logToConsole: boolean;
  /** Whether to persist queue to localStorage */
  persistQueue: boolean;
}

// ==============================================================================
// CONSTANTS
// ==============================================================================

const DEFAULT_CONFIG: ErrorLoggerConfig = {
  endpoint: "/api/errors/log",
  batchSize: 10,
  flushInterval: 5000,
  maxErrorsPerMinute: 30,
  logToConsole: import.meta.env.DEV,
  persistQueue: true,
};

const STORAGE_KEY = "nfl_sim_error_queue";
const SESSION_ID_KEY = "nfl_sim_session_id";

// ==============================================================================
// UTILITY FUNCTIONS
// ==============================================================================

/**
 * Generate a unique ID for error tracking
 */
function generateId(): string {
  return `${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
}

/**
 * Get or create a session ID for the current browser session
 */
function getSessionId(): string {
  let sessionId = sessionStorage.getItem(SESSION_ID_KEY);
  if (!sessionId) {
    sessionId = generateId();
    sessionStorage.setItem(SESSION_ID_KEY, sessionId);
  }
  return sessionId;
}

/**
 * Safely serialize error objects
 */
function serializeError(error: unknown): { message: string; stack?: string } {
  if (error instanceof Error) {
    return {
      message: error.message,
      stack: error.stack,
    };
  }
  if (typeof error === "string") {
    return { message: error };
  }
  try {
    return { message: JSON.stringify(error) };
  } catch {
    return { message: String(error) };
  }
}

// ==============================================================================
// ERROR LOGGER SERVICE
// ==============================================================================

class ErrorLoggerService {
  private static instance: ErrorLoggerService | null = null;
  private config: ErrorLoggerConfig;
  private queue: ErrorLogPayload[] = [];
  private isProcessing = false;
  private flushIntervalId: ReturnType<typeof setInterval> | null = null;
  private errorCount = 0;
  private errorCountResetTime = 0;
  private sessionId: string;

  /**
   * Private constructor - use getInstance() instead
   */
  private constructor(config: Partial<ErrorLoggerConfig> = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config };
    this.sessionId = getSessionId();

    // Restore queue from localStorage if enabled
    if (this.config.persistQueue) {
      this.restoreQueue();
    }

    // Start periodic flush
    this.startFlushInterval();

    // Flush queue before page unload
    if (typeof window !== "undefined") {
      window.addEventListener("beforeunload", () => this.flushSync());
      window.addEventListener("visibilitychange", () => {
        if (document.visibilityState === "hidden") {
          this.flushSync();
        }
      });

      // Capture unhandled errors
      window.addEventListener("error", (event) => {
        this.logError(
          ErrorCategory.UNKNOWN,
          event.message || "Unhandled error",
          event.error,
          undefined,
          { filename: event.filename, lineno: event.lineno, colno: event.colno }
        );
      });

      // Capture unhandled promise rejections
      window.addEventListener("unhandledrejection", (event) => {
        this.logError(
          ErrorCategory.UNKNOWN,
          "Unhandled promise rejection",
          event.reason,
          undefined,
          { type: "unhandledrejection" }
        );
      });
    }
  }

  /**
   * Get the singleton instance
   */
  public static getInstance(config?: Partial<ErrorLoggerConfig>): ErrorLoggerService {
    if (!ErrorLoggerService.instance) {
      ErrorLoggerService.instance = new ErrorLoggerService(config);
    }
    return ErrorLoggerService.instance;
  }

  /**
   * Reset the singleton instance (useful for testing)
   */
  public static resetInstance(): void {
    if (ErrorLoggerService.instance) {
      ErrorLoggerService.instance.destroy();
      ErrorLoggerService.instance = null;
    }
  }

  /**
   * Log an error with full context
   */
  public logError(
    category: ErrorCategory,
    message: string,
    error?: Error | unknown,
    componentStack?: string,
    context?: Record<string, unknown>,
    severity: ErrorSeverity = ErrorSeverity.MEDIUM
  ): void {
    // Rate limiting check
    if (!this.checkRateLimit()) {
      if (this.config.logToConsole) {
        console.warn("[ErrorLogger] Rate limit exceeded, dropping error");
      }
      return;
    }

    const serializedError = error ? serializeError(error) : { message };

    const payload: ErrorLogPayload = {
      timestamp: new Date().toISOString(),
      id: generateId(),
      category,
      severity,
      message: serializedError.message,
      stack: serializedError.stack,
      componentStack,
      url: typeof window !== "undefined" ? window.location.href : "",
      userAgent: typeof navigator !== "undefined" ? navigator.userAgent : "",
      context,
      sessionId: this.sessionId,
    };

    // Log to console in development
    if (this.config.logToConsole) {
      console.group(`🔴 [ErrorLogger] ${category}`);
      console.error("Message:", message);
      if (error) console.error("Error:", error);
      if (context) console.log("Context:", context);
      console.groupEnd();
    }

    // Add to queue
    this.queue.push(payload);

    // Persist to localStorage
    if (this.config.persistQueue) {
      this.persistQueue();
    }

    // Flush if batch size reached
    if (this.queue.length >= this.config.batchSize) {
      void this.flush();
    }
  }

  /**
   * Check and update rate limiting
   */
  private checkRateLimit(): boolean {
    const now = Date.now();

    // Reset counter every minute
    if (now - this.errorCountResetTime > 60000) {
      this.errorCount = 0;
      this.errorCountResetTime = now;
    }

    if (this.errorCount >= this.config.maxErrorsPerMinute) {
      return false;
    }

    this.errorCount++;
    return true;
  }

  /**
   * Start the periodic flush interval
   */
  private startFlushInterval(): void {
    if (this.flushIntervalId) {
      clearInterval(this.flushIntervalId);
    }
    this.flushIntervalId = setInterval(() => void this.flush(), this.config.flushInterval);
  }

  /**
   * Async flush - sends queued errors to the backend
   */
  private async flush(): Promise<void> {
    if (this.isProcessing || this.queue.length === 0) {
      return;
    }

    this.isProcessing = true;
    const batch = [...this.queue];
    this.queue = [];

    try {
      const response = await fetch(this.config.endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Error-Batch": "true",
          "X-Session-ID": this.sessionId,
        },
        body: JSON.stringify({ errors: batch }),
        keepalive: true,
      });

      if (!response.ok) {
        // Re-queue on failure
        this.queue = [...batch, ...this.queue];
        console.warn("[ErrorLogger] Failed to send errors:", response.status);
      } else {
        // Clear persisted queue on success
        if (this.config.persistQueue) {
          this.clearPersistedQueue();
        }
      }
    } catch (e) {
      // Re-queue on network failure
      this.queue = [...batch, ...this.queue];
      console.warn("[ErrorLogger] Network error:", e);
    } finally {
      this.isProcessing = false;
    }
  }

  /**
   * Synchronous flush using sendBeacon (for page unload)
   */
  private flushSync(): void {
    if (this.queue.length === 0) return;

    const data = JSON.stringify({ errors: this.queue });

    try {
      const success = navigator.sendBeacon(this.config.endpoint, data);
      if (success) {
        this.queue = [];
        this.clearPersistedQueue();
      }
    } catch {
      // Beacon not supported or failed, queue will be restored on next page load
      console.warn("[ErrorLogger] sendBeacon failed");
    }
  }

  /**
   * Persist queue to localStorage
   */
  private persistQueue(): void {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(this.queue));
    } catch {
      // localStorage not available or quota exceeded
    }
  }

  /**
   * Restore queue from localStorage
   */
  private restoreQueue(): void {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        const restored = JSON.parse(stored) as ErrorLogPayload[];
        this.queue = [...restored, ...this.queue];
      }
    } catch {
      // Invalid or corrupted data
    }
  }

  /**
   * Clear persisted queue from localStorage
   */
  private clearPersistedQueue(): void {
    try {
      localStorage.removeItem(STORAGE_KEY);
    } catch {
      // Ignore
    }
  }

  /**
   * Clean up resources
   */
  private destroy(): void {
    if (this.flushIntervalId) {
      clearInterval(this.flushIntervalId);
      this.flushIntervalId = null;
    }
    this.flushSync();
  }
}

// ==============================================================================
// SINGLETON EXPORTS
// ==============================================================================

/** Singleton error logger instance */
export const errorLogger = ErrorLoggerService.getInstance();

// ==============================================================================
// CONVENIENCE FUNCTIONS
// ==============================================================================

/**
 * Log a React render error (used by ErrorBoundary)
 */
export const logRenderError = (
  message: string,
  error?: Error,
  componentStack?: string,
  context?: Record<string, unknown>
): void => {
  errorLogger.logError(
    ErrorCategory.RENDER,
    message,
    error,
    componentStack,
    context,
    ErrorSeverity.HIGH
  );
};

/**
 * Log an API error
 */
export const logApiError = (
  message: string,
  error?: Error,
  context?: Record<string, unknown>
): void => {
  errorLogger.logError(ErrorCategory.API, message, error, undefined, context, ErrorSeverity.MEDIUM);
};

/**
 * Log a validation error
 */
export const logValidationError = (message: string, context?: Record<string, unknown>): void => {
  errorLogger.logError(
    ErrorCategory.VALIDATION,
    message,
    undefined,
    undefined,
    context,
    ErrorSeverity.LOW
  );
};

/**
 * Log a navigation error
 */
export const logNavigationError = (
  message: string,
  error?: Error,
  context?: Record<string, unknown>
): void => {
  errorLogger.logError(
    ErrorCategory.NAVIGATION,
    message,
    error,
    undefined,
    context,
    ErrorSeverity.MEDIUM
  );
};

/**
 * Log an authentication error
 */
export const logAuthError = (
  message: string,
  error?: Error,
  context?: Record<string, unknown>
): void => {
  errorLogger.logError(ErrorCategory.AUTH, message, error, undefined, context, ErrorSeverity.HIGH);
};

/**
 * Log a WebSocket error
 */
export const logWebSocketError = (
  message: string,
  error?: Error,
  context?: Record<string, unknown>
): void => {
  errorLogger.logError(
    ErrorCategory.WEBSOCKET,
    message,
    error,
    undefined,
    context,
    ErrorSeverity.MEDIUM
  );
};
