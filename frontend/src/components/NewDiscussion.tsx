import { useState } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from './ui/card';
import { Spinner } from './ui/spinner';
import { ErrorMessage } from './ErrorMessage';
import { createDiscussion } from '../api/discussions';
import { Discussion } from '../types/discussion';

interface NewDiscussionProps {
  onDiscussionCreated: (discussion: Discussion) => void;
  onStartLoading: () => void;
}

export function NewDiscussion({ onDiscussionCreated, onStartLoading }: NewDiscussionProps) {
  const [topic, setTopic] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    onStartLoading();

    try {
      const result = await createDiscussion({ topic });
      onDiscussionCreated(result);
      setTopic('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Start New Discussion</CardTitle>
        <CardDescription>Enter a topic for the agents to evaluate</CardDescription>
      </CardHeader>
      <form onSubmit={handleSubmit}>
        <CardContent>
          <textarea
            className="w-full p-2 border rounded-md dark:bg-zinc-800 dark:border-zinc-700"
            rows={4}
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="e.g., Evaluate the potential impact of Layer 2 scaling solutions on Ethereum ecosystem growth"
            disabled={loading}
          />
          {error && (
            <div className="mt-2">
              <ErrorMessage message={error} />
            </div>
          )}
        </CardContent>
        <CardFooter className="flex items-center gap-4">
          <Button type="submit" disabled={!topic || loading}>
            {loading ? 'Starting Discussion...' : 'Start Discussion'}
          </Button>
          {loading && <Spinner size="sm" />}
        </CardFooter>
      </form>
    </Card>
  );
}
