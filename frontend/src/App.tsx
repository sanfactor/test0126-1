import { useState } from 'react';
import { Discussion } from './types/discussion';
import { NewDiscussion } from './components/NewDiscussion';
import { DiscussionCard } from './components/DiscussionCard';
import { LoadingOverlay } from './components/LoadingOverlay';

function App() {
  const [discussion, setDiscussion] = useState<Discussion | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleDiscussionCreated = (newDiscussion: Discussion) => {
    setDiscussion(newDiscussion);
    setIsLoading(false);
  };

  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-zinc-900 p-4 sm:p-8">
      <div className="max-w-4xl mx-auto space-y-8">
        <header className="text-center">
          <h1 className="text-4xl font-bold text-zinc-900 dark:text-zinc-50">TokenCourt</h1>
          <p className="mt-2 text-zinc-600 dark:text-zinc-400">Web3 Project Evaluation System</p>
        </header>

        <NewDiscussion 
          onDiscussionCreated={handleDiscussionCreated}
          onStartLoading={() => setIsLoading(true)}
        />
        
        {discussion && <DiscussionCard discussion={discussion} />}
        {isLoading && <LoadingOverlay message="Agents are discussing the topic..." />}
      </div>
    </div>
  );
}

export default App;
