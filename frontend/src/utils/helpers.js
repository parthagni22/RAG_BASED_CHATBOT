export const generateChatId = () =>
  `chat-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

export const formatTimestamp = (timestamp) => {
  return new Date(timestamp).toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit'
  });
};

export const debounce = (func, wait) => {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
};

export const scrollToBottom = (element) => {
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' });
  }
};

export const truncateText = (text, maxLength = 50) => {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength) + '...';
};

export const classNames = (...classes) => {
  return classes.filter(Boolean).join(' ');
};