import { Discussion } from '../types/discussion';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { MessageSquare, Vote, CheckCircle2 } from 'lucide-react';

interface DiscussionCardProps {
  discussion: Discussion;
}

export function DiscussionCard({ discussion }: DiscussionCardProps) {
  const approveCount = discussion.votes.filter(v => v.choice === 'approve').length;
  const totalVotes = discussion.votes.length;
  const approvePercentage = Math.round((approveCount / totalVotes) * 100);
  return (
    <Card>
      <CardHeader>
        <CardTitle>Discussion Results</CardTitle>
        <CardDescription>{discussion.topic}</CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <div>
          <div className="flex items-center gap-2 mb-4">
            <MessageSquare className="h-5 w-5 text-zinc-500" />
            <h3 className="font-semibold">Agent Messages</h3>
          </div>
          <div className="space-y-4">
            {discussion.messages.map((message, index) => (
              <div key={index} className="p-4 bg-white dark:bg-zinc-800 rounded-lg">
                <div className="flex justify-between items-start mb-2">
                  <span className="font-medium text-zinc-900 dark:text-zinc-50">
                    {message.agent_id}
                  </span>
                  <span className="text-sm text-zinc-500">
                    {new Date(message.timestamp).toLocaleString()}
                  </span>
                </div>
                <p className="text-zinc-600 dark:text-zinc-300 whitespace-pre-wrap">{message.content}</p>
              </div>
            ))}
          </div>
        </div>

        <div>
          <div className="flex items-center gap-2 mb-4">
            <Vote className="h-5 w-5 text-zinc-500" />
            <h3 className="font-semibold">Agent Votes</h3>
            <span className="ml-auto text-sm text-zinc-500">
              {approveCount} of {totalVotes} Approve ({approvePercentage}%)
            </span>
          </div>
          <div className="space-y-4">
            {discussion.votes.map((vote, index) => (
              <div key={index} className="p-4 bg-white dark:bg-zinc-800 rounded-lg">
                <div className="flex justify-between items-start mb-2">
                  <span className="font-medium text-zinc-900 dark:text-zinc-50">
                    {vote.agent_id}
                  </span>
                  <span className={`px-2 py-1 rounded text-sm ${
                    vote.choice === 'approve' 
                      ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100' 
                      : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100'
                  }`}>
                    {vote.choice.toUpperCase()}
                  </span>
                </div>
                <p className="text-zinc-600 dark:text-zinc-300">{vote.reasoning}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="mt-6 p-4 bg-zinc-100 dark:bg-zinc-800 rounded-lg">
          <div className="flex items-center gap-2 mb-4">
            <CheckCircle2 className="h-5 w-5 text-zinc-500" />
            <h3 className="font-semibold">Final Decision</h3>
          </div>
          <p className="text-lg font-medium text-zinc-900 dark:text-zinc-50">
            {discussion.conclusion}
          </p>
          <p className="mt-2 text-sm text-zinc-500">
            Discussion completed on {new Date(discussion.updated_at).toLocaleString()}
          </p>
        </div>
      </CardContent>
    </Card>
  );
}
