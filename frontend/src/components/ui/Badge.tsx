import React from "react";
import clsx from "clsx";
import "./Badge.css";

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  children: React.ReactNode;
  variant?: "default" | "success" | "warning" | "danger" | "neutral";
  className?: string;
}

export const Badge = ({ children, variant = "default", className, ...props }: BadgeProps) => {
  return (
    <span className={clsx("ui-badge", `ui-badge--${variant}`, className)} {...props}>
      <span className="ui-badge-dot" />
      {children}
    </span>
  );
};
