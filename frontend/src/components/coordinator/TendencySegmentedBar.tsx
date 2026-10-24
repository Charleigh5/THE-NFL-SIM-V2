import React from "react";

interface TendencySegmentedBarProps {
  label: string;
  leftLabel: string;
  leftPercent: number;
  rightLabel: string;
  rightPercent: number;
  leftColor?: string;
  rightColor?: string;
}

export const TendencySegmentedBar: React.FC<TendencySegmentedBarProps> = ({
  label,
  leftLabel,
  leftPercent,
  rightLabel,
  rightPercent,
  leftColor = "#38bdf8",
  rightColor = "#f59e0b",
}) => {
  return (
    <div className="tendency-bar-root">
      <div className="tendency-bar-meta">
        <span className="tendency-bar-title">{label}</span>
        <div className="tendency-bar-tags">
          <span className="tag-left" style={{ color: leftColor }}>
            {leftLabel} {leftPercent}%
          </span>
          <span className="tag-divider">/</span>
          <span className="tag-right" style={{ color: rightColor }}>
            {rightLabel} {rightPercent}%
          </span>
        </div>
      </div>

      <div
        className="tendency-bar-track"
        role="progressbar"
        aria-valuenow={leftPercent}
        aria-valuemin={0}
        aria-valuemax={100}
      >
        <div
          className="tendency-bar-segment segment-left"
          style={{ width: `${leftPercent}%`, backgroundColor: leftColor }}
        />
        <div
          className="tendency-bar-segment segment-right"
          style={{ width: `${rightPercent}%`, backgroundColor: rightColor }}
        />
        <div className="tendency-bar-hairline-50" />
      </div>
    </div>
  );
};
