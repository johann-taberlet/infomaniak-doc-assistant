import type { UITree } from '@json-render/core';
import { JsonRenderer } from './JsonRenderer';

/**
 * Demo UI tree for testing JsonRenderer
 * Based on the verification test JSON from B1 plan
 */
const demoTree: UITree = {
  root: 'answer-1',
  elements: {
    'answer-1': {
      key: 'answer-1',
      type: 'Answer',
      props: { summary: "Here's how to share a file in kDrive:" },
      children: ['steps-1', 'tip-card', 'platforms'],
    },
    'steps-1': {
      key: 'steps-1',
      type: 'Steps',
      props: { title: 'Sharing a File' },
      children: ['step-1', 'step-2', 'step-3'],
    },
    'step-1': {
      key: 'step-1',
      type: 'Step',
      props: {
        number: 1,
        title: 'Open kDrive',
        description: 'Navigate to your files in the kDrive web app or desktop client.',
      },
    },
    'step-2': {
      key: 'step-2',
      type: 'Step',
      props: {
        number: 2,
        title: 'Right-click the file',
        description: 'Select the file you want to share and right-click to open the context menu.',
      },
    },
    'step-3': {
      key: 'step-3',
      type: 'Step',
      props: {
        number: 3,
        title: 'Click "Share"',
        description: 'Choose sharing options: link, email, or specific users.',
      },
    },
    'tip-card': {
      key: 'tip-card',
      type: 'Card',
      props: {
        title: 'Pro Tip',
        type: 'tip',
      },
      children: ['tip-text'],
    },
    'tip-text': {
      key: 'tip-text',
      type: 'Text',
      props: {
        content: 'You can set an expiration date for shared links to improve security.',
      },
    },
    platforms: {
      key: 'platforms',
      type: 'PlatformBadges',
      props: {
        platforms: ['web', 'macos', 'windows', 'ios', 'android'],
      },
    },
  },
};

/**
 * Demo component showcasing all generative UI components
 */
export function JsonRendererDemo() {
  const handleAction = (action: { name: string; params?: Record<string, unknown> }) => {
    console.log('Action triggered:', action);
    alert(`Action: ${action.name}\nParams: ${JSON.stringify(action.params)}`);
  };

  return (
    <div className="p-8 max-w-3xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">JsonRenderer Demo</h2>
      <p className="text-text-muted mb-6">
        Testing the generative UI components from B1 json-render setup with Tailwind CSS v4.
      </p>

      <div className="bg-white rounded-lg p-6 shadow-md">
        <JsonRenderer tree={demoTree} onAction={handleAction} />
      </div>

      <h3 className="text-xl font-semibold mt-8 mb-4">Additional Components</h3>

      {/* Table Demo */}
      <JsonRenderer
        tree={{
          root: 'table-demo',
          elements: {
            'table-demo': {
              key: 'table-demo',
              type: 'Table',
              props: {
                headers: ['Feature', 'Free', 'Pro', 'Business'],
                rows: [
                  ['Storage', '15 GB', '2 TB', 'Unlimited'],
                  ['File sharing', 'Yes', 'Yes', 'Yes'],
                  ['Version history', '30 days', '1 year', 'Unlimited'],
                ],
              },
            },
          },
        }}
      />

      {/* Comparison Demo */}
      <JsonRenderer
        tree={{
          root: 'comparison-demo',
          elements: {
            'comparison-demo': {
              key: 'comparison-demo',
              type: 'Comparison',
              props: {
                features: ['Cloud Storage', 'Video Calls', 'Team Chat', 'Calendar'],
                items: [
                  { name: 'kDrive', values: [true, false, false, false] },
                  { name: 'kMeet', values: [false, true, false, true] },
                  { name: 'kChat', values: [false, false, true, false] },
                ],
              },
            },
          },
        }}
      />

      {/* Warning Card Demo */}
      <JsonRenderer
        tree={{
          root: 'warning-demo',
          elements: {
            'warning-demo': {
              key: 'warning-demo',
              type: 'Card',
              props: {
                title: 'Important Notice',
                type: 'warning',
              },
              children: ['warning-text'],
            },
            'warning-text': {
              key: 'warning-text',
              type: 'Text',
              props: {
                content: 'Make sure to backup your files before performing bulk operations.',
              },
            },
          },
        }}
      />

      {/* CodeBlock Demo */}
      <JsonRenderer
        tree={{
          root: 'code-demo',
          elements: {
            'code-demo': {
              key: 'code-demo',
              type: 'CodeBlock',
              props: {
                language: 'bash',
                code: 'curl -X POST https://api.infomaniak.com/kdrive/upload \\\n  -H "Authorization: Bearer $TOKEN" \\\n  -F "file=@document.pdf"',
              },
            },
          },
        }}
      />

      {/* Action Buttons Demo */}
      <div className="mt-4">
        <JsonRenderer
          tree={{
            root: 'actions-demo',
            elements: {
              'actions-demo': {
                key: 'actions-demo',
                type: 'Answer',
                props: {},
                children: ['action-1', 'action-2'],
              },
              'action-1': {
                key: 'action-1',
                type: 'ActionSuggestion',
                props: {
                  label: 'Open kDrive',
                  action: 'openApp',
                  params: { app: 'kdrive' },
                },
              },
              'action-2': {
                key: 'action-2',
                type: 'ActionSuggestion',
                props: {
                  label: 'Learn More',
                  action: 'navigate',
                  params: { path: '/docs/kdrive/sharing' },
                },
              },
            },
          }}
          onAction={handleAction}
        />
      </div>
    </div>
  );
}
