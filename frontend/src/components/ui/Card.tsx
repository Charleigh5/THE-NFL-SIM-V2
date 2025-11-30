import React from "react";
import clsx from "clsx";
import "./Card.css";

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  className?: string;
  variant?: "default" | "glass" | "interactive";
}

export const Card = ({
  children,
  className,
  variant = "default",
  ...props
}: CardProps) => {
  return (
    <div
      className={clsx(
        "ui-card",
        `ui-card--${variant}`,
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};

export const CardHeader = ({
  children,
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={clsx("ui-card-header", className)} {...props}>
    {children}
  </div>
);

export const CardTitle = ({
  children,
  className,
  ...props
}: React.HTMLAttributes<HTMLHeadingElement>) => (
  <h3 className={clsx("ui-card-title", className)} {...props}>
    {children}
  </h3>
);

export const CardContent = ({
  children,
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={clsx("ui-card-content", className)} {...props}>
    {children}
  </div>
);

export const CardFooter = ({
  children,
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={clsx("ui-card-footer", className)} {...props}>
    {children}
  </div>
);
