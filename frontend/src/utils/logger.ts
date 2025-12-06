/**
 * Logger Utility for Frontend
 *
 * Enforces the "Clean Console Log" policy.
 * Only logs when explicit flags are enabled or level is high enough.
 */

type LogLevel = 'debug' | 'info' | 'warn' | 'error';

const CURRENT_LOG_LEVEL: LogLevel = process.env.NODE_ENV === 'production' ? 'warn' : 'info';

const LEVELS: Record<LogLevel, number> = {
  debug: 0,
  info: 1,
  warn: 2,
  error: 3
};

class Logger {
  private shouldLog(level: LogLevel): boolean {
    return LEVELS[level] >= LEVELS[CURRENT_LOG_LEVEL];
  }

  debug(message: string, ...args: any[]) {
    if (this.shouldLog('debug')) {
      console.debug(`[DEBUG] ${message}`, ...args);
    }
  }

  info(message: string, ...args: any[]) {
    if (this.shouldLog('info')) {
      console.info(`[INFO] ${message}`, ...args);
    }
  }

  warn(message: string, ...args: any[]) {
    if (this.shouldLog('warn')) {
      console.warn(`[WARN] ${message}`, ...args);
    }
  }

  error(message: string, ...args: any[]) {
    if (this.shouldLog('error')) {
      console.error(`[ERROR] ${message}`, ...args);
    }
  }
}

export const logger = new Logger();
