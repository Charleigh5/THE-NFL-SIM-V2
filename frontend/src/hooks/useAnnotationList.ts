/**
 * useAnnotationList Hook
 * ======================
 * Custom React hook for managing annotation list with localStorage persistence.
 *
 * Context7 Best Practices:
 * - useEffect for external system sync (localStorage)
 * - useCallback for memoized function references
 * - Clear type definitions
 */

import { useState, useEffect, useCallback } from "react";

// ============================================================================
// TYPES
// ============================================================================

export interface AIResearch {
  summary: string;
  codeExamples: string[];
  complexity: "Low" | "Medium" | "High";
  sources: string[];
}

export interface ElementMetadata {
  selector: string;
  tagName: string;
  textContent?: string;
  description?: string;
  className?: string;
  boundingRect?: {
    top: number;
    left: number;
    width: number;
    height: number;
  };
}

export interface Annotation {
  id: string;
  timestamp: string;
  note: string;
  element: ElementMetadata;
  screenshot?: string; // Base64 data URL
  aiResearch?: AIResearch;
}

// ============================================================================
// CONSTANTS
// ============================================================================

const STORAGE_KEY = "nfl-sim-annotations";

// ============================================================================
// HOOK
// ============================================================================

export function useAnnotationList() {
  const [annotations, setAnnotations] = useState<Annotation[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Load from localStorage on mount
  useEffect(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        const parsed = JSON.parse(stored);
        setAnnotations(Array.isArray(parsed) ? parsed : []);
      }
    } catch (error) {
      console.error("Failed to load annotations from localStorage:", error);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Sync to localStorage when annotations change
  useEffect(() => {
    if (!isLoading) {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(annotations));
      } catch (error) {
        console.error("Failed to save annotations to localStorage:", error);
      }
    }
  }, [annotations, isLoading]);

  // Cross-tab sync via storage event
  useEffect(() => {
    function handleStorageChange(event: StorageEvent) {
      if (event.key === STORAGE_KEY && event.newValue) {
        try {
          const parsed = JSON.parse(event.newValue);
          setAnnotations(Array.isArray(parsed) ? parsed : []);
        } catch (error) {
          console.error("Failed to parse storage event:", error);
        }
      }
    }

    window.addEventListener("storage", handleStorageChange);
    return () => window.removeEventListener("storage", handleStorageChange);
  }, []);

  // Add annotation - memoized per Context7 best practices
  const addAnnotation = useCallback(
    (note: string, element: ElementMetadata, screenshot?: string, aiResearch?: AIResearch) => {
      const newAnnotation: Annotation = {
        id: Date.now().toString(36) + Math.random().toString(36).substring(2),
        timestamp: new Date().toISOString(),
        note,
        element,
        screenshot,
        aiResearch,
      };

      setAnnotations((prev) => [...prev, newAnnotation]);
      return newAnnotation.id;
    },
    []
  );

  // Update annotation
  const updateAnnotation = useCallback((id: string, updates: Partial<Annotation>) => {
    setAnnotations((prev) => prev.map((ann) => (ann.id === id ? { ...ann, ...updates } : ann)));
  }, []);

  // Remove annotation
  const removeAnnotation = useCallback((id: string) => {
    setAnnotations((prev) => prev.filter((ann) => ann.id !== id));
  }, []);

  // Clear all annotations
  const clearAll = useCallback(() => {
    setAnnotations([]);
  }, []);

  // Get count
  const count = annotations.length;

  return {
    annotations,
    count,
    isLoading,
    addAnnotation,
    updateAnnotation,
    removeAnnotation,
    clearAll,
  };
}

export default useAnnotationList;
