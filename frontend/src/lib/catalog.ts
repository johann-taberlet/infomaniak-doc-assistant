import { createCatalog } from '@json-render/core';
import { z } from 'zod';

/** Action names defined in the catalog */
const ACTION_NAMES = ['navigate', 'copy', 'openApp'] as const;

/**
 * Docs Catalog - Defines all allowed components for generative UI
 * Based on PRD section 4.3 for kSuite documentation assistant,
 * extended with Text component and action definitions
 */
export const docsCatalog = createCatalog({
  name: 'kSuite Documentation',
  components: {
    // Container for structured answers
    Answer: {
      props: z.object({ summary: z.string().optional() }),
      hasChildren: true,
      description: 'Top-level container for structured documentation answers',
    },

    // Step-by-step procedures
    Steps: {
      props: z.object({ title: z.string().optional() }),
      hasChildren: true,
      description: 'Container for step-by-step instructions',
    },
    Step: {
      props: z.object({
        number: z.number().int().min(1),
        title: z.string(),
        description: z.string(),
      }),
      description: 'Individual step in a procedure',
    },

    // Information cards
    Card: {
      props: z.object({
        title: z.string(),
        type: z.enum(['info', 'warning', 'tip', 'important']),
      }),
      hasChildren: true,
      description: 'Callout card for highlighting information',
    },

    // Data tables
    Table: {
      props: z.object({
        headers: z.array(z.string()),
        rows: z.array(z.array(z.string())),
      }),
      description: 'Tabular data display',
    },

    // Feature comparisons
    Comparison: {
      props: z.object({
        features: z.array(z.string()),
        items: z.array(
          z.object({
            name: z.string(),
            values: z.array(z.boolean()),
          })
        ),
      }),
      description: 'Feature comparison matrix',
    },

    // Code blocks
    CodeBlock: {
      props: z.object({
        language: z.string().optional(),
        code: z.string(),
      }),
      description: 'Formatted code snippet',
    },

    // Links to related actions
    ActionSuggestion: {
      props: z.object({
        label: z.string(),
        action: z.enum(ACTION_NAMES),
        params: z.record(z.string(), z.unknown()).optional(),
      }),
      description: 'Suggested action button for user interaction',
    },

    // Platform availability
    PlatformBadges: {
      props: z.object({
        platforms: z.array(
          z.enum(['web', 'ios', 'android', 'macos', 'windows', 'linux'])
        ),
      }),
      description: 'Platform availability indicators',
    },

    // Simple text content
    Text: {
      props: z.object({
        content: z.string(),
      }),
      description: 'Plain text content',
    },
  },
  actions: {
    navigate: {
      params: z.object({ path: z.string() }),
      description: 'Navigate to a documentation page',
    },
    copy: {
      params: z.object({ text: z.string() }),
      description: 'Copy text to clipboard',
    },
    openApp: {
      params: z.object({
        app: z.enum(['kdrive', 'kmeet', 'kchat']),
        action: z.string().optional(),
      }),
      description: 'Open a kSuite application',
    },
  },
  validation: 'strict',
});

// Export catalog schema for backend JSON generation
export type DocsCatalog = typeof docsCatalog;

// Export component names for type safety
export const componentNames = docsCatalog.componentNames;

// Export action names for dynamic handler generation
export { ACTION_NAMES };
