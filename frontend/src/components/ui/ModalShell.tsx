import React, { useEffect, useRef, useCallback, type ReactNode } from "react";
import { createPortal } from "react-dom";
import { useModalStackStore } from "../../store/useModalStackStore";

export interface ModalShellProps {
  id: string;
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  ariaLabel?: string;
  children: ReactNode;
  className?: string;
  overlayClassName?: string;
  testId?: string;
  closeOnBackdropClick?: boolean;
  returnFocusRef?: HTMLElement | null;
}

const FOCUSABLE_SELECTOR =
  'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"]):not([disabled])';

function getFocusableElements(container: HTMLElement | null): HTMLElement[] {
  if (!container) return [];
  const elements = Array.from(container.querySelectorAll<HTMLElement>(FOCUSABLE_SELECTOR));
  return elements.filter(
    (el) => el.offsetParent !== null || el.getClientRects().length > 0 || el.tabIndex >= 0
  );
}

export const ModalShell: React.FC<ModalShellProps> = ({
  id,
  isOpen,
  onClose,
  title,
  ariaLabel,
  children,
  className = "",
  overlayClassName = "",
  testId,
  closeOnBackdropClick = true,
  returnFocusRef = null,
}) => {
  const dialogRef = useRef<HTMLDivElement>(null);
  const triggerElementRef = useRef<HTMLElement | null>(null);
  const isClosingRef = useRef(false);
  const mouseDownTargetRef = useRef<EventTarget | null>(null);
  const onCloseRef = useRef(onClose);

  useEffect(() => {
    onCloseRef.current = onClose;
  }, [onClose]);

  const isTop = useModalStackStore((state) => state.isTopModal(id));
  const stackLength = useModalStackStore((state) => state.stack.length);
  const depth = useModalStackStore((state) => {
    const idx = state.stack.findIndex((m) => m.id === id);
    return idx >= 0 ? idx : 0;
  });

  // Background page scroll lock when any modal is open
  useEffect(() => {
    if (typeof document === "undefined") return;
    if (stackLength > 0) {
      const originalOverflow = document.body.style.overflow;
      document.body.style.overflow = "hidden";
      return () => {
        if (useModalStackStore.getState().stack.length === 0) {
          document.body.style.overflow = originalOverflow;
        }
      };
    }
  }, [stackLength]);

  // Modal lifecycle & stack registration
  useEffect(() => {
    if (isOpen) {
      isClosingRef.current = false;
      const trigger =
        returnFocusRef ||
        (typeof document !== "undefined" && document.activeElement instanceof HTMLElement
          ? document.activeElement
          : null);
      triggerElementRef.current = trigger;

      useModalStackStore.getState().pushModal(
        id,
        () => {
          if (!isClosingRef.current) {
            isClosingRef.current = true;
            onCloseRef.current();
          }
        },
        trigger
      );

      return () => {
        isClosingRef.current = true;
        const stack = useModalStackStore.getState().stack;
        if (stack.some((m) => m.id === id)) {
          useModalStackStore.getState().popModal(id);
        }
        if (triggerElementRef.current && typeof triggerElementRef.current.focus === "function") {
          triggerElementRef.current.focus();
        }
      };
    }
  }, [isOpen, id, returnFocusRef]);

  // Initial focus management when opening or becoming top modal
  useEffect(() => {
    if (isOpen && isTop) {
      const timer = requestAnimationFrame(() => {
        if (!dialogRef.current) return;
        // Only shift focus if focus is not already inside this dialog
        if (document.activeElement && dialogRef.current.contains(document.activeElement)) {
          return;
        }
        const focusables = getFocusableElements(dialogRef.current);
        if (focusables.length > 0) {
          focusables[0].focus();
        } else {
          dialogRef.current.focus();
        }
      });
      return () => cancelAnimationFrame(timer);
    }
  }, [isOpen, isTop]);

  // Keyboard navigation: Escape key & Focus Trapping within dialog
  useEffect(() => {
    if (!isOpen || !isTop) return;

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        e.stopPropagation();
        e.preventDefault();
        onCloseRef.current();
        return;
      }

      if (e.key === "Tab") {
        if (!dialogRef.current) return;
        const focusables = getFocusableElements(dialogRef.current);

        if (focusables.length === 0) {
          e.preventDefault();
          dialogRef.current.focus();
          return;
        }

        const firstElement = focusables[0];
        const lastElement = focusables[focusables.length - 1];

        if (e.shiftKey) {
          if (
            document.activeElement === firstElement ||
            !dialogRef.current.contains(document.activeElement)
          ) {
            e.preventDefault();
            lastElement.focus();
          }
        } else {
          if (
            document.activeElement === lastElement ||
            !dialogRef.current.contains(document.activeElement)
          ) {
            e.preventDefault();
            firstElement.focus();
          }
        }
      }
    };

    window.addEventListener("keydown", handleKeyDown, true);
    return () => {
      window.removeEventListener("keydown", handleKeyDown, true);
    };
  }, [isOpen, isTop]);

  const handleBackdropClick = useCallback(
    (e: React.MouseEvent<HTMLDivElement>) => {
      if (
        e.target === e.currentTarget &&
        mouseDownTargetRef.current === e.currentTarget &&
        closeOnBackdropClick &&
        isTop
      ) {
        e.stopPropagation();
        onCloseRef.current();
      }
    },
    [closeOnBackdropClick, isTop]
  );

  if (!isOpen || typeof document === "undefined") {
    return null;
  }

  const zIndex = 100 + depth * 10;

  return createPortal(
    <div
      className={`fixed inset-0 flex items-center justify-center p-4 transition-all ${overlayClassName} ${
        !isTop ? "pointer-events-none" : ""
      }`}
      style={{ zIndex }}
      aria-hidden={!isTop ? "true" : undefined}
      data-testid={testId ? `${testId}-overlay` : undefined}
      onMouseDown={(e) => {
        mouseDownTargetRef.current = e.target;
      }}
      onClick={handleBackdropClick}
    >
      {/* Backdrop visual container */}
      <div
        className={`fixed inset-0 bg-black/70 backdrop-blur-sm transition-opacity pointer-events-none ${
          !isTop ? "opacity-40" : "opacity-100"
        }`}
        aria-hidden="true"
      />

      {/* Dialog container */}
      <div
        ref={dialogRef}
        role="dialog"
        aria-modal="true"
        aria-label={ariaLabel || title || "Dialog"}
        tabIndex={-1}
        className={`relative max-w-full max-h-[90vh] overflow-y-auto outline-none transition-all ${className} ${
          !isTop
            ? "pointer-events-none opacity-80 scale-[0.98]"
            : "pointer-events-auto opacity-100 scale-100"
        }`}
        data-testid={testId}
        onClick={(e) => e.stopPropagation()}
      >
        {children}
      </div>
    </div>,
    document.body
  );
};

export default ModalShell;
