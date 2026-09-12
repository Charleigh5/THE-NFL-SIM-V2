import React, { useRef, useState, useMemo, useCallback } from "react";
import { useVirtualizer } from "@tanstack/react-virtual";
import { ArrowUpDown, ArrowUp, ArrowDown } from "lucide-react";

export type SortDirection = "asc" | "desc" | null;

export interface VirtualizedTableColumn<T> {
  id: string;
  header: string | React.ReactNode;
  accessor?: (item: T) => React.ReactNode;
  cell?: (item: T, index: number) => React.ReactNode;
  width?: string | number;
  minWidth?: string | number;
  maxWidth?: string | number;
  align?: "left" | "center" | "right";
  sortable?: boolean;
  sortKey?: (item: T) => string | number | null | undefined;
  className?: string;
  headerClassName?: string;
}

export interface VirtualizedTableProps<T> {
  data: T[];
  columns: VirtualizedTableColumn<T>[];
  height?: number | string;
  estimateRowHeight?: number;
  overscan?: number;
  onRowClick?: (item: T, index: number) => void;
  getRowId?: (item: T, index: number) => string | number;
  selectedRowId?: string | number;
  emptyMessage?: string;
  isLoading?: boolean;
  className?: string;
  tableClassName?: string;
  headerClassName?: string;
  rowClassName?: (item: T, index: number) => string;
  searchQuery?: string;
  searchFilter?: (item: T, query: string) => boolean;
  defaultSortColumnId?: string;
  defaultSortDirection?: "asc" | "desc";
  testId?: string;
}

interface MemoizedVirtualRowProps<T> {
  virtualRow: {
    key: React.Key;
    index: number;
    start: number;
  };
  measureElement?: (el: HTMLElement | null) => void;
  item: T;
  columns: VirtualizedTableColumn<T>[];
  isSelected: boolean;
  onRowClick?: (item: T, index: number) => void;
  customClass?: string;
}

function VirtualRowInner<T>({
  virtualRow,
  measureElement,
  item,
  columns,
  isSelected,
  onRowClick,
  customClass = "",
}: MemoizedVirtualRowProps<T>): React.ReactElement {
  return (
    <div
      key={virtualRow.key}
      data-index={virtualRow.index}
      ref={measureElement}
      onClick={() => onRowClick && onRowClick(item, virtualRow.index)}
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        width: "100%",
        transform: `translateY(${virtualRow.start}px)`,
      }}
      className={`flex items-center px-3 border-b border-white/5 transition-colors text-xs font-mono select-none ${
        onRowClick ? "cursor-pointer hover:bg-white/10" : ""
      } ${
        isSelected
          ? "bg-yellow-500/20 text-yellow-300 border-l-2 border-l-yellow-400 font-bold"
          : virtualRow.index % 2 === 0
            ? "bg-transparent"
            : "bg-white/[0.02]"
      } ${customClass}`}
    >
      {columns.map((col) => {
        const alignClass =
          col.align === "center"
            ? "justify-center text-center"
            : col.align === "right"
              ? "justify-end text-right"
              : "justify-start text-left";

        return (
          <div
            key={col.id}
            style={{
              width: col.width,
              minWidth: col.minWidth,
              maxWidth: col.maxWidth,
              flex: col.width ? undefined : 1,
            }}
            className={`flex items-center px-2 py-2 truncate ${alignClass} ${col.className || ""}`}
          >
            {col.cell ? col.cell(item, virtualRow.index) : col.accessor ? col.accessor(item) : null}
          </div>
        );
      })}
    </div>
  );
}

const MemoizedVirtualRow = React.memo(
  VirtualRowInner,
  (prev, next) =>
    prev.virtualRow.key === next.virtualRow.key &&
    prev.virtualRow.index === next.virtualRow.index &&
    prev.virtualRow.start === next.virtualRow.start &&
    prev.isSelected === next.isSelected &&
    prev.item === next.item &&
    prev.columns === next.columns &&
    prev.customClass === next.customClass &&
    prev.onRowClick === next.onRowClick
) as typeof VirtualRowInner;

export function VirtualizedTable<T>({
  data,
  columns,
  height = 540,
  estimateRowHeight = 48,
  overscan = 12,
  onRowClick,
  getRowId,
  selectedRowId,
  emptyMessage = "No records found.",
  isLoading = false,
  className = "",
  tableClassName = "",
  headerClassName = "",
  rowClassName,
  searchQuery = "",
  searchFilter,
  defaultSortColumnId,
  defaultSortDirection = "asc",
  testId = "virtualized-table",
}: VirtualizedTableProps<T>): React.ReactElement {
  const parentRef = useRef<HTMLDivElement>(null);

  // Sorting state
  const [sortColumnId, setSortColumnId] = useState<string | null>(defaultSortColumnId || null);
  const [sortDirection, setSortDirection] = useState<SortDirection>(
    defaultSortColumnId ? defaultSortDirection : null
  );

  const handleHeaderClick = useCallback(
    (col: VirtualizedTableColumn<T>) => {
      if (!col.sortable) return;

      if (sortColumnId !== col.id) {
        setSortColumnId(col.id);
        setSortDirection("asc");
      } else if (sortDirection === "asc") {
        setSortDirection("desc");
      } else if (sortDirection === "desc") {
        setSortColumnId(null);
        setSortDirection(null);
      } else {
        setSortDirection("asc");
      }
    },
    [sortColumnId, sortDirection]
  );

  // Filtered and Sorted Data
  const processedData = useMemo(() => {
    let result = [...data];

    // Filter
    if (searchQuery.trim() && searchFilter) {
      const query = searchQuery.trim().toLowerCase();
      result = result.filter((item) => searchFilter(item, query));
    }

    // Sort
    if (sortColumnId && sortDirection) {
      const targetCol = columns.find((c) => c.id === sortColumnId);
      if (targetCol && targetCol.sortKey) {
        const keyFn = targetCol.sortKey;
        result.sort((a, b) => {
          const valA = keyFn(a);
          const valB = keyFn(b);

          if (valA == null && valB == null) return 0;
          if (valA == null) return sortDirection === "asc" ? 1 : -1;
          if (valB == null) return sortDirection === "asc" ? -1 : 1;

          if (typeof valA === "number" && typeof valB === "number") {
            return sortDirection === "asc" ? valA - valB : valB - valA;
          }

          const strA = String(valA).toLowerCase();
          const strB = String(valB).toLowerCase();
          return sortDirection === "asc" ? strA.localeCompare(strB) : strB.localeCompare(strA);
        });
      }
    }

    return result;
  }, [data, searchQuery, searchFilter, sortColumnId, sortDirection, columns]);

  // Virtualizer
  const rowVirtualizer = useVirtualizer({
    count: processedData.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => estimateRowHeight,
    overscan,
  });

  const virtualRows = rowVirtualizer.getVirtualItems();
  const totalSize = rowVirtualizer.getTotalSize();

  const containerHeight = typeof height === "number" ? `${height}px` : height;

  return (
    <div
      className={`relative flex flex-col rounded-xl border border-white/10 bg-slate-950/70 backdrop-blur-md overflow-hidden shadow-xl ${className}`}
      data-testid={testId}
    >
      {/* Sticky Table Header */}
      <div
        className={`flex items-center sticky top-0 z-20 bg-slate-900/95 border-b border-white/15 px-3 py-2.5 text-xs font-header uppercase tracking-wider text-gray-300 select-none shadow-sm ${headerClassName}`}
      >
        {columns.map((col) => {
          const isSorted = sortColumnId === col.id;
          const alignClass =
            col.align === "center"
              ? "justify-center text-center"
              : col.align === "right"
                ? "justify-end text-right"
                : "justify-start text-left";

          return (
            <div
              key={col.id}
              onClick={() => handleHeaderClick(col)}
              style={{
                width: col.width,
                minWidth: col.minWidth,
                maxWidth: col.maxWidth,
                flex: col.width ? undefined : 1,
              }}
              className={`flex items-center gap-1.5 px-2 font-semibold transition-colors ${alignClass} ${
                col.sortable ? "cursor-pointer hover:text-white" : ""
              } ${col.headerClassName || ""}`}
            >
              <span>{col.header}</span>
              {col.sortable && (
                <span className="shrink-0 text-gray-400">
                  {isSorted && sortDirection === "asc" ? (
                    <ArrowUp size={12} className="text-yellow-400" />
                  ) : isSorted && sortDirection === "desc" ? (
                    <ArrowDown size={12} className="text-yellow-400" />
                  ) : (
                    <ArrowUpDown size={11} className="opacity-40 hover:opacity-100" />
                  )}
                </span>
              )}
            </div>
          );
        })}
      </div>

      {/* Virtualized Scroll Viewport */}
      <div
        ref={parentRef}
        style={{ height: containerHeight }}
        className={`w-full overflow-y-auto overflow-x-hidden custom-scrollbar ${tableClassName}`}
        tabIndex={0}
      >
        {isLoading ? (
          <div className="flex items-center justify-center h-full text-gray-400 font-mono text-sm">
            <span className="animate-pulse">Loading telemetry records...</span>
          </div>
        ) : processedData.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-gray-400 font-mono text-xs p-8 text-center">
            <p>{emptyMessage}</p>
          </div>
        ) : (
          <div
            style={{
              height: `${totalSize}px`,
              width: "100%",
              position: "relative",
            }}
          >
            {virtualRows.map((virtualRow) => {
              const item = processedData[virtualRow.index];
              const rowId = getRowId ? getRowId(item, virtualRow.index) : virtualRow.index;
              const isSelected = selectedRowId !== undefined && selectedRowId === rowId;
              const customClass = rowClassName ? rowClassName(item, virtualRow.index) : "";

              return (
                <MemoizedVirtualRow
                  key={virtualRow.key}
                  virtualRow={virtualRow}
                  measureElement={rowVirtualizer.measureElement}
                  item={item}
                  columns={columns}
                  isSelected={isSelected}
                  onRowClick={onRowClick}
                  customClass={customClass}
                />
              );
            })}
          </div>
        )}
      </div>

      {/* Footer Info Bar */}
      <div className="flex items-center justify-between px-3 py-1.5 bg-slate-950/90 border-t border-white/10 text-[11px] font-mono text-gray-400">
        <span>
          Showing <strong className="text-white">{processedData.length}</strong> entries
          {processedData.length !== data.length && <span> (filtered from {data.length})</span>}
        </span>
        <span className="text-[10px] text-gray-400 uppercase tracking-wider">
          Virtualized 60 FPS Engine
        </span>
      </div>
    </div>
  );
}

export default VirtualizedTable;
