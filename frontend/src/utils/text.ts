/**
 * Strip markdown formatting to get plain text
 */
export function stripMarkdown(text: string): string {
  return text
    .replace(/#{1,6}\s+/g, '') // Headers
    .replace(/\*\*([^*]+)\*\*/g, '$1') // Bold
    .replace(/\*([^*]+)\*/g, '$1') // Italic
    .replace(/`([^`]+)`/g, '$1') // Inline code
    .replace(/```[\s\S]*?```/g, '') // Code blocks
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1') // Links
    .replace(/!\[([^\]]*)\]\([^)]+\)/g, '') // Images
    .replace(/^[-*+]\s+/gm, '') // List items
    .replace(/^\d+\.\s+/gm, '') // Numbered lists
    .replace(/>\s+/g, '') // Blockquotes
    .replace(/\n+/g, ' ') // Newlines to spaces
    .replace(/\s+/g, ' ') // Multiple spaces
    .trim()
}
