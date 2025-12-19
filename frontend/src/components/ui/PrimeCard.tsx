import { motion } from "framer-motion";
import { clsx } from "clsx";
import { type ReactNode } from "react";

interface PrimeCardProps {
  children: ReactNode;
  className?: string;
  title?: string;
  icon?: ReactNode;
  variant?: "default" | "danger" | "glass";
  delay?: number;
}

export const PrimeCard = ({
  children,
  className,
  title,
  icon,
  variant = "default",
  delay = 0,
}: PrimeCardProps) => {
  const variants = {
    default: "bg-gradient-to-br from-broadcast-metal to-black border border-white/10",
    danger: "bg-gradient-to-br from-red-950 to-black border border-red-500/30",
    glass: "bg-broadcast-glass backdrop-blur-md border border-white/10",
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20, skewX: -6 }}
      animate={{ opacity: 1, y: 0, skewX: -6 }}
      transition={{ duration: 0.4, delay: delay, ease: "easeOut" }}
      className={clsx(
        "relative group overflow-hidden shadow-2xl skew-x-[-6deg]",
        variants[variant],
        className
      )}
    >
      {/* Metallic Sheen Overlay */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent -translate-x-full group-hover:animate-sheen pointer-events-none z-20" />

      {/* Header Line */}
      <div className="absolute top-0 left-0 w-2 h-full bg-brand/50 group-hover:bg-brand transition-colors duration-300" />

      {/* Content Content - skewed back to normal for readability */}
      <div className="relative z-10 p-6 skew-x-[6deg]">
        {(title || icon) && (
          <div className="flex items-center gap-3 mb-4 border-b border-white/10 pb-2">
            {icon && <span className="text-brand text-xl">{icon}</span>}
            {title && (
              <h3 className="font-header text-2xl uppercase tracking-wide text-white drop-shadow-md">
                {title}
              </h3>
            )}
          </div>
        )}
        <div className="font-body text-gray-300">{children}</div>
      </div>
    </motion.div>
  );
};
