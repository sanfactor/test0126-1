import { Spinner } from './ui/spinner';

interface LoadingOverlayProps {
  message?: string;
}

export function LoadingOverlay({ message = 'Loading...' }: LoadingOverlayProps) {
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white dark:bg-zinc-800 p-6 rounded-lg shadow-lg flex flex-col items-center gap-4">
        <Spinner size="lg" />
        <p className="text-zinc-900 dark:text-zinc-50">{message}</p>
      </div>
    </div>
  );
}
