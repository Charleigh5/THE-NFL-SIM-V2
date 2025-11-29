import React from "react";
import "./LoadingSpinner.css";

interface LoadingSpinnerProps {
  size?: "small" | "medium" | "large";
  color?: string;
  text?: string;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = "medium",
  color = "#3b82f6",
  text,
}) => {
  return (
    <div className={`loading-spinner-container ${size}`}>
      <div
        className="loading-spinner"
        style={{ borderColor: `${color} transparent transparent transparent` }}
      ></div>
      {text && <div className="loading-text">{text}</div>}
    </div>
  );
};
