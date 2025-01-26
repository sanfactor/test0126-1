import { cn } from "@/lib/utils";

interface SpinnerProps extends React.HTMLAttributes<HTMLDivElement> {
  size?: "sm" | "md" | "lg";
}

const sizeClasses = {
  sm: "h-4 w-4",
  md: "h-8 w-8",
  lg: "h-12 w-12",
};

export function Spinner({ className, size = "md", ...props }: SpinnerProps) {
  return (
    <div
      className={cn("animate-spin", sizeClasses[size], className)}
      {...props}
    >
      <div className="h-full w-full rounded-full border-2 border-zinc-200 border-t-zinc-800 dark:border-zinc-800 dark:border-t-zinc-200" />
    </div>
  );
}
