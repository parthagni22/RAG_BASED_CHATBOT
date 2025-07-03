export const MessageFormatter = {
  escapeHtml: (text) => {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  },

  formatLLMResponse: (text) => {
    let formattedText = text;

    // Headers
    formattedText = formattedText.replace(/^##\s*(.*)$/gm, '<h2 class="text-lg font-semibold mt-6 mb-3 text-foreground border-b border-border pb-2">$1</h2>');

    // Subheaders
    formattedText = formattedText.replace(/^###\s*(.*)$/gm, '<h3 class="text-md font-medium mt-4 mb-2 text-foreground">$1</h3>');

    // Bold text
    formattedText = formattedText.replace(/\*\*(.*?)\*\*/g, '<strong class="text-primary font-semibold">$1</strong>');

    // Italic text
    formattedText = formattedText.replace(/\*(.*?)\*/g, '<em class="italic text-muted-foreground">$1</em>');

    // Code blocks
    formattedText = formattedText.replace(/`([^`]+)`/g, '<code class="bg-muted px-2 py-1 rounded text-sm font-mono text-accent">$1</code>');

    // List items
    formattedText = formattedText.replace(/^- (.*)$/gm, '<li class="ml-4 list-disc text-foreground mb-1">$1</li>');
    formattedText = formattedText.replace(/(<li.*?<\/li>\s*)+/gs, '<ul class="space-y-1 my-4 ml-4">$&</ul>');

    // Numbered lists
    formattedText = formattedText.replace(/^\d+\.\s(.*)$/gm, '<li class="ml-4 list-decimal text-foreground mb-1">$1</li>');

    // Horizontal rules
    formattedText = formattedText.replace(/^---\s*$/gm, '<hr class="border-border my-6">');

    // Paragraphs
    formattedText = formattedText.split('\n\n').map(paragraph => {
      if (paragraph.trim().startsWith('<') || paragraph.trim() === '') {
        return paragraph;
      }
      return `<p class="leading-relaxed text-foreground mb-4">${paragraph.replace(/\n/g, '<br>')}</p>`;
    }).join('');

    return formattedText;
  },

  formatMessageTime: (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffInHours = (now - date) / (1000 * 60 * 60);

    if (diffInHours < 24) {
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } else if (diffInHours < 168) { // 7 days
      return date.toLocaleDateString([], { weekday: 'short', hour: '2-digit', minute: '2-digit' });
    } else {
      return date.toLocaleDateString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
    }
  }
};