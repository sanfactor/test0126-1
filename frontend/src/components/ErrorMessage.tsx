import { AlertCircle } from 'lucide-react';

interface ErrorMessageProps {
  message: string;
}

export function ErrorMessage({ message }: ErrorMessageProps) {
  return (
    <div className="flex items-center gap-2 p-2 text-sm text-red-500 bg-red-50 dark:bg-red-950 rounded-md">
      <AlertCircle className="h-4 w-4" />
      <span>{message}</span>
    </div>
  );
}
