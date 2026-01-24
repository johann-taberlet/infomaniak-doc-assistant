import { Component, type ReactNode } from 'react';
import type { UITree, Action } from '@json-render/core';
import { Renderer, JSONUIProvider, type ComponentRenderProps } from '@json-render/react';
import { docsRegistry } from './registry';
import { ACTION_NAMES } from './catalog';

/**
 * Props for the JsonRenderer component
 * @property tree - The UI tree structure to render, or null for fallback
 * @property fallback - Optional React node displayed when tree is null
 * @property onAction - Optional callback invoked when user triggers an action
 */
interface JsonRendererProps {
  tree: UITree | null;
  fallback?: ReactNode;
  onAction?: (action: Action) => void;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

/**
 * Error boundary to catch rendering errors in json-render components
 * Prevents a single malformed element from crashing the entire app
 */
class JsonRendererErrorBoundary extends Component<
  { children: ReactNode; fallback?: ReactNode },
  ErrorBoundaryState
> {
  constructor(props: { children: ReactNode; fallback?: ReactNode }) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error(
      'JsonRenderer: Error rendering UI tree. This may indicate malformed data from the backend.',
      { error, componentStack: errorInfo.componentStack }
    );
  }

  render() {
    if (this.state.hasError) {
      return (
        this.props.fallback ?? (
          <div className="bg-[var(--ik-error-bg)] border border-[var(--ik-error)] rounded-[var(--ik-radius-sm)] p-4 text-[var(--ik-error)] my-4">
            <p className="font-medium">Unable to display this content</p>
            <p className="text-sm mt-1">
              An error occurred while rendering. Please try refreshing the page.
            </p>
          </div>
        )
      );
    }

    return this.props.children;
  }
}

/** Fallback component for unknown element types */
function FallbackComponent({ element }: ComponentRenderProps) {
  // Log for debugging - helps identify catalog mismatches between frontend and backend
  console.error(
    `JsonRenderer: Unknown component type "${element.type}". ` +
      `This may indicate a catalog mismatch between frontend and backend.`,
    { key: element.key, props: element.props }
  );

  return (
    <div className="bg-[var(--ik-error-bg)] border border-[var(--ik-error)] rounded-[var(--ik-radius-sm)] p-4 text-[var(--ik-error)] my-4">
      Unknown component type: {element.type}
    </div>
  );
}

/**
 * Generate action handlers dynamically from catalog action names.
 * This ensures handlers stay in sync with the catalog definition.
 */
function createActionHandlers(onAction: (action: Action) => void) {
  return Object.fromEntries(
    ACTION_NAMES.map((name) => [
      name,
      (params: Record<string, unknown>) => {
        onAction({ name, params });
        return Promise.resolve();
      },
    ])
  ) as Record<string, (params: Record<string, unknown>) => Promise<void>>;
}

/**
 * JsonRenderer - Wrapper component for rendering json-render UI trees
 * Provides error boundary protection and fallback support
 */
export function JsonRenderer({ tree, fallback, onAction }: JsonRendererProps) {
  if (!tree) {
    if (!fallback) {
      console.debug('JsonRenderer: Received null tree with no fallback. Rendering nothing.');
    }
    return fallback ?? null;
  }

  const actionHandlers = onAction ? createActionHandlers(onAction) : undefined;

  return (
    <JsonRendererErrorBoundary fallback={fallback}>
      <JSONUIProvider registry={docsRegistry} actionHandlers={actionHandlers}>
        <Renderer
          tree={tree}
          registry={docsRegistry}
          loading={false}
          fallback={FallbackComponent}
        />
      </JSONUIProvider>
    </JsonRendererErrorBoundary>
  );
}

// Re-export UITree type for convenience
export type { UITree };
