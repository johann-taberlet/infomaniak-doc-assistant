import type { UITree } from '@json-render/core';
import type { Action } from '@json-render/core';
import { Renderer, JSONUIProvider, type ComponentRenderProps } from '@json-render/react';
import { docsRegistry } from './registry';

interface JsonRendererProps {
  tree: UITree | null;
  fallback?: React.ReactNode;
  onAction?: (action: Action) => void;
}

// Fallback component for unknown element types
function FallbackComponent({ element }: ComponentRenderProps) {
  return (
    <div className="bg-red-50 border border-red-400 rounded p-4 text-red-800 my-4">
      Unknown component type: {element.type}
    </div>
  );
}

/**
 * JsonRenderer - Wrapper component for rendering json-render UI trees
 * Provides error handling and fallback support
 */
export function JsonRenderer({ tree, fallback, onAction }: JsonRendererProps) {
  if (!tree) {
    return fallback ?? null;
  }

  // Convert onAction to action handlers format
  const actionHandlers = onAction
    ? {
        // Generic handler that forwards all actions
        navigate: (params: Record<string, unknown>) => {
          onAction({ name: 'navigate', params });
          return Promise.resolve();
        },
        copy: (params: Record<string, unknown>) => {
          onAction({ name: 'copy', params });
          return Promise.resolve();
        },
        openApp: (params: Record<string, unknown>) => {
          onAction({ name: 'openApp', params });
          return Promise.resolve();
        },
      }
    : undefined;

  return (
    <JSONUIProvider
      registry={docsRegistry}
      actionHandlers={actionHandlers}
    >
      <Renderer
        tree={tree}
        registry={docsRegistry}
        loading={false}
        fallback={FallbackComponent}
      />
    </JSONUIProvider>
  );
}

// Re-export UITree type for convenience
export type { UITree };
