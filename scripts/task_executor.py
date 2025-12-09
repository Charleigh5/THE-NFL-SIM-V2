#!/usr/bin/env python3
"""
NFL Sim Engine - Task Executor
==============================

This module contains the actual implementation logic for each task.
It generates the code files based on task definitions.

Usage:
    Called by automate_build.py

Author: Automated by Gemini
Date: 2025-12-08
"""

import os
import logging
from pathlib import Path
from typing import Optional
from datetime import datetime

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
BACKEND_DIR = PROJECT_ROOT / "backend"
FRONTEND_DIR = PROJECT_ROOT / "frontend"


# ==============================================================================
# BATCH 1: FOUNDATION
# ==============================================================================

LOGGING_CONFIG_PY = '''"""
Structured Logging Configuration
================================

This module provides a centralized logging configuration using structlog
for JSON-formatted, structured logging with request tracing.

Best Practices:
- Use logger hierarchy per module (__name__)
- Include request_id for distributed tracing
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- File rotation: 10MB max, 5 backups

Reference: https://www.structlog.org/
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional
import structlog
from structlog.typing import EventDict

# Create logs directory
LOGS_DIR = Path(__file__).parent.parent.parent / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)


def add_request_id(
    logger: logging.Logger,
    method_name: str,
    event_dict: EventDict
) -> EventDict:
    """Add request_id to log events for tracing."""
    from contextvars import ContextVar
    request_id_var: ContextVar[Optional[str]] = ContextVar("request_id", default=None)
    request_id = request_id_var.get()
    if request_id:
        event_dict["request_id"] = request_id
    return event_dict


def configure_logging(
    log_level: str = "INFO",
    json_format: bool = True,
    log_file: Optional[str] = None
) -> None:
    """
    Configure structured logging for the application.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_format: If True, output JSON format; else human-readable
        log_file: Optional path to log file (uses rotation)
    """

    # Configure standard logging
    handlers = []

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level))
    handlers.append(console_handler)

    # File handler with rotation (10MB max, 5 backups)
    if log_file:
        log_path = LOGS_DIR / log_file
    else:
        log_path = LOGS_DIR / "application.log"

    file_handler = logging.handlers.RotatingFileHandler(
        log_path,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)  # Log everything to file
    handlers.append(file_handler)

    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level),
        handlers=handlers,
        format="%(message)s"
    )

    # Configure structlog
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        add_request_id,
        structlog.processors.StackInfoRenderer(),
    ]

    if json_format:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer(colors=True))

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, log_level)
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.BoundLogger:
    """
    Get a configured logger for a module.

    Args:
        name: Module name (typically __name__)

    Returns:
        Configured structlog logger
    """
    return structlog.get_logger(name)


# Error categories for consistent error logging
class ErrorCategory:
    CHEMISTRY_ERROR = "CHEMISTRY_ERROR"
    SACK_CALC_ERROR = "SACK_CALC_ERROR"
    TRAIT_ERROR = "TRAIT_ERROR"
    WEATHER_ERROR = "WEATHER_ERROR"
    API_ERROR = "API_ERROR"
    DATABASE_ERROR = "DATABASE_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"


def log_error(
    logger: structlog.BoundLogger,
    category: str,
    message: str,
    exc_info: bool = True,
    **context
) -> None:
    """
    Log an error with category and context.

    Args:
        logger: The structlog logger instance
        category: Error category from ErrorCategory
        message: Error message
        exc_info: Whether to include exception info
        **context: Additional context key-value pairs
    """
    logger.error(
        message,
        error_category=category,
        exc_info=exc_info,
        **context
    )


# Initialize logging on module import
configure_logging()
'''


ERROR_BOUNDARY_TSX = '''import React, { Component, ErrorInfo, ReactNode } from 'react';
import './ErrorBoundary.css';

/**
 * Error Boundary Component
 * ========================
 *
 * Catches JavaScript errors in child component tree and displays
 * a fallback UI instead of crashing the entire application.
 *
 * Best Practices:
 * - Use getDerivedStateFromError for rendering fallback
 * - Use componentDidCatch for logging
 * - Provide retry functionality
 *
 * Reference: https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary
 */

interface ErrorBoundaryProps {
  children: ReactNode;
  fallback?: ReactNode;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
    };
  }

  static getDerivedStateFromError(error: Error): Partial<ErrorBoundaryState> {
    // Update state so the next render will show the fallback UI
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    // Log error to console
    console.error('ErrorBoundary caught an error:', error, errorInfo);

    // Update state with error info
    this.setState({ errorInfo });

    // Call optional error handler
    if (this.props.onError) {
      this.props.onError(error, errorInfo);
    }

    // Log to backend error logging service
    this.logErrorToService(error, errorInfo);
  }

  private async logErrorToService(error: Error, errorInfo: ErrorInfo): Promise<void> {
    try {
      const errorPayload = {
        timestamp: new Date().toISOString(),
        message: error.message,
        stack: error.stack,
        componentStack: errorInfo.componentStack,
        url: window.location.href,
        userAgent: navigator.userAgent,
      };

      // Send to backend logging endpoint
      await fetch('/api/errors/log', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(errorPayload),
      });
    } catch (logError) {
      // Silently fail - don't want to cause more errors
      console.warn('Failed to log error to service:', logError);
    }
  }

  private handleRetry = (): void => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null,
    });
  };

  render(): ReactNode {
    if (this.state.hasError) {
      // Custom fallback UI if provided
      if (this.props.fallback) {
        return this.props.fallback;
      }

      // Default fallback UI
      return (
        <div className="error-boundary">
          <div className="error-boundary__content">
            <div className="error-boundary__icon">⚠️</div>
            <h2 className="error-boundary__title">Something went wrong</h2>
            <p className="error-boundary__message">
              We apologize for the inconvenience. An unexpected error has occurred.
            </p>
            {process.env.NODE_ENV === 'development' && this.state.error && (
              <details className="error-boundary__details">
                <summary>Error Details</summary>
                <pre>{this.state.error.message}</pre>
                <pre>{this.state.error.stack}</pre>
                {this.state.errorInfo && (
                  <pre>{this.state.errorInfo.componentStack}</pre>
                )}
              </details>
            )}
            <button
              className="error-boundary__retry-button"
              onClick={this.handleRetry}
            >
              Try Again
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
'''


ERROR_BOUNDARY_CSS = '''.error-boundary {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
  padding: 2rem;
  background-color: var(--bg-secondary, #1a1a2e);
  border-radius: 8px;
  margin: 1rem;
}

.error-boundary__content {
  text-align: center;
  max-width: 500px;
}

.error-boundary__icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.error-boundary__title {
  color: var(--color-error, #ff6b6b);
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.error-boundary__message {
  color: var(--text-secondary, #a0a0a0);
  margin-bottom: 1.5rem;
}

.error-boundary__details {
  text-align: left;
  background-color: var(--bg-tertiary, #0f0f1a);
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1.5rem;
  max-height: 200px;
  overflow: auto;
}

.error-boundary__details summary {
  cursor: pointer;
  color: var(--text-primary, #ffffff);
  margin-bottom: 0.5rem;
}

.error-boundary__details pre {
  font-size: 0.75rem;
  color: var(--text-secondary, #a0a0a0);
  white-space: pre-wrap;
  word-break: break-word;
}

.error-boundary__retry-button {
  background-color: var(--color-primary, #4a9eff);
  color: white;
  border: none;
  padding: 0.75rem 2rem;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.error-boundary__retry-button:hover {
  background-color: var(--color-primary-hover, #3a8eef);
}

.error-boundary__retry-button:focus {
  outline: 2px solid var(--color-primary, #4a9eff);
  outline-offset: 2px;
}
'''


ERROR_LOGGER_SERVICE_TS = '''/**
 * Error Logging Service
 * =====================
 *
 * Centralized service for logging errors to the backend.
 * Provides consistent error formatting and categorization.
 */

export interface ErrorLogPayload {
  timestamp: string;
  category: ErrorCategory;
  message: string;
  stack?: string;
  componentStack?: string;
  url: string;
  userAgent: string;
  context?: Record<string, unknown>;
}

export enum ErrorCategory {
  RENDER = 'RENDER',
  API = 'API',
  VALIDATION = 'VALIDATION',
  NAVIGATION = 'NAVIGATION',
  STATE = 'STATE',
  UNKNOWN = 'UNKNOWN',
}

class ErrorLoggerService {
  private static instance: ErrorLoggerService;
  private endpoint = '/api/errors/log';
  private queue: ErrorLogPayload[] = [];
  private isProcessing = false;

  private constructor() {
    // Process queue periodically
    setInterval(() => this.processQueue(), 5000);

    // Process queue before page unload
    window.addEventListener('beforeunload', () => {
      this.processQueueSync();
    });
  }

  public static getInstance(): ErrorLoggerService {
    if (!ErrorLoggerService.instance) {
      ErrorLoggerService.instance = new ErrorLoggerService();
    }
    return ErrorLoggerService.instance;
  }

  public logError(
    category: ErrorCategory,
    message: string,
    error?: Error,
    componentStack?: string,
    context?: Record<string, unknown>
  ): void {
    const payload: ErrorLogPayload = {
      timestamp: new Date().toISOString(),
      category,
      message,
      stack: error?.stack,
      componentStack,
      url: window.location.href,
      userAgent: navigator.userAgent,
      context,
    };

    // Log to console in development
    if (process.env.NODE_ENV === 'development') {
      console.error('[ErrorLogger]', payload);
    }

    // Add to queue for batch processing
    this.queue.push(payload);
  }

  private async processQueue(): Promise<void> {
    if (this.isProcessing || this.queue.length === 0) {
      return;
    }

    this.isProcessing = true;
    const batch = [...this.queue];
    this.queue = [];

    try {
      await fetch(this.endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ errors: batch }),
      });
    } catch (e) {
      // Re-queue failed items
      this.queue = [...batch, ...this.queue];
      console.warn('Failed to send error logs:', e);
    } finally {
      this.isProcessing = false;
    }
  }

  private processQueueSync(): void {
    if (this.queue.length === 0) return;

    // Use sendBeacon for reliable delivery on page unload
    const data = JSON.stringify({ errors: this.queue });
    navigator.sendBeacon(this.endpoint, data);
    this.queue = [];
  }
}

export const errorLogger = ErrorLoggerService.getInstance();

// Convenience functions
export const logRenderError = (message: string, error?: Error, componentStack?: string) =>
  errorLogger.logError(ErrorCategory.RENDER, message, error, componentStack);

export const logApiError = (message: string, error?: Error, context?: Record<string, unknown>) =>
  errorLogger.logError(ErrorCategory.API, message, error, undefined, context);

export const logValidationError = (message: string, context?: Record<string, unknown>) =>
  errorLogger.logError(ErrorCategory.VALIDATION, message, undefined, undefined, context);
'''


def create_batch1_files():
    """Create all files for Batch 1: Foundation & Logging."""

    # Backend: logging_config.py
    logging_path = BACKEND_DIR / "app" / "core" / "logging_config.py"
    logging_path.parent.mkdir(parents=True, exist_ok=True)
    logging_path.write_text(LOGGING_CONFIG_PY)
    logger.info(f"Created: {logging_path}")

    # Frontend: ErrorBoundary.tsx
    error_boundary_path = FRONTEND_DIR / "src" / "components" / "ErrorBoundary.tsx"
    error_boundary_path.parent.mkdir(parents=True, exist_ok=True)
    error_boundary_path.write_text(ERROR_BOUNDARY_TSX)
    logger.info(f"Created: {error_boundary_path}")

    # Frontend: ErrorBoundary.css
    error_boundary_css_path = FRONTEND_DIR / "src" / "components" / "ErrorBoundary.css"
    error_boundary_css_path.write_text(ERROR_BOUNDARY_CSS)
    logger.info(f"Created: {error_boundary_css_path}")

    # Frontend: errorLogger.ts service
    error_logger_path = FRONTEND_DIR / "src" / "services" / "errorLogger.ts"
    error_logger_path.parent.mkdir(parents=True, exist_ok=True)
    error_logger_path.write_text(ERROR_LOGGER_SERVICE_TS)
    logger.info(f"Created: {error_logger_path}")

    return True


# ==============================================================================
# MAIN EXECUTOR
# ==============================================================================

def execute_batch(batch_number: int) -> bool:
    """Execute all tasks for a specific batch."""

    executors = {
        1: create_batch1_files,
        # Add more batch executors as implemented
    }

    if batch_number in executors:
        return executors[batch_number]()
    else:
        logger.warning(f"Batch {batch_number} executor not yet implemented")
        return True  # Return True to continue automation


if __name__ == "__main__":
    import sys
    batch = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    success = execute_batch(batch)
    sys.exit(0 if success else 1)
