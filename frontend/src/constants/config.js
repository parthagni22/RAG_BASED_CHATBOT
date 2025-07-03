export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_URL || 'http://localhost:8080',
  ENDPOINTS: {
    CHAT: '/llmtrigger',
    HEALTH: '/health'
  }
};

export const QUICK_ACTIONS = [
  {
    id: 'course-search',
    title: 'Course Search',
    description: 'Find specific courses and their details',
    message: 'Help me search for courses',
    icon: '🔍'
  },
  {
    id: 'prerequisites',
    title: 'Prerequisites',
    description: 'Check course prerequisites and requirements',
    message: 'What are the prerequisites for courses?',
    icon: '📚'
  },
  {
    id: 'degree-planning',
    title: 'Degree Planning',
    description: 'Plan your academic path and requirements',
    message: 'Help me plan my degree',
    icon: '🎯'
  },
  {
    id: 'schedules',
    title: 'Class Schedules',
    description: 'Get information about class timings',
    message: 'Show me class schedules and timings',
    icon: '📅'
  }
];

export const THEME_STORAGE_KEY = 'aggie-theme';

export const CHAT_SETTINGS = {
  MAX_MESSAGE_LENGTH: 2000,
  TYPING_DELAY: 100,
  AUTO_SCROLL_DELAY: 300
};