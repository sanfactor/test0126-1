import { Discussion, TopicRequest } from '../types/discussion';

const API_URL = import.meta.env.VITE_API_URL;
console.log('API URL:', API_URL); // Debug log

export const createDiscussion = async (topic: TopicRequest): Promise<Discussion> => {
  try {
    console.log('Creating discussion with topic:', topic); // Debug log
    const response = await fetch(`${API_URL}/api/v1/discussions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(topic),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('API Error:', errorText); // Debug log
      throw new Error(`Failed to create discussion: ${errorText}`);
    }

    return response.json();
  } catch (error) {
    console.error('Error creating discussion:', error);
    throw error;
  }
};

export const getDiscussion = async (id: string): Promise<Discussion> => {
  try {
    const response = await fetch(`${API_URL}/api/v1/discussions/${id}`);

    if (!response.ok) {
      const errorText = await response.text();
      console.error('API Error:', errorText);
      throw new Error(`Failed to fetch discussion: ${errorText}`);
    }

    return response.json();
  } catch (error) {
    console.error('Error fetching discussion:', error);
    throw error;
  }
};

export const listDiscussions = async (): Promise<Discussion[]> => {
  try {
    const response = await fetch(`${API_URL}/api/v1/discussions`);

    if (!response.ok) {
      const errorText = await response.text();
      console.error('API Error:', errorText);
      throw new Error(`Failed to fetch discussions: ${errorText}`);
    }

    return response.json();
  } catch (error) {
    console.error('Error listing discussions:', error);
    throw error;
  }
};
