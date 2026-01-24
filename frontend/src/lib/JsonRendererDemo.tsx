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
 * Using Infomaniak Design System
 */
export function JsonRendererDemo() {
  const handleAction = (action: { name: string; params?: Record<string, unknown> }) => {
    console.log('Action triggered:', action);
    alert(`Action: ${action.name}\nParams: ${JSON.stringify(action.params)}`);
  };

  return (
    <div className="min-h-screen bg-ik-bg-page p-8">
      <div className="max-w-[900px] mx-auto">
        <h2 className="text-2xl font-bold text-ik-text-primary mb-2">JsonRenderer Demo</h2>
        <p className="text-ik-text-secondary mb-6">
          Testing the generative UI components with Infomaniak Design System.
        </p>

        <div className="bg-ik-bg-card rounded-ik-lg p-6 shadow-ik-md border border-ik-border-light">
          <JsonRenderer tree={demoTree} onAction={handleAction} />
        </div>

        <h3 className="text-xl font-semibold text-ik-text-primary mt-10 mb-4">Additional Components</h3>

        {/* Table Demo */}
        <div className="bg-ik-bg-card rounded-ik-lg p-6 shadow-ik-md border border-ik-border-light mb-6">
          <h4 className="text-sm font-semibold text-ik-text-secondary mb-2">Table Component</h4>
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
        </div>

        {/* Comparison Demo */}
        <div className="bg-ik-bg-card rounded-ik-lg p-6 shadow-ik-md border border-ik-border-light mb-6">
          <h4 className="text-sm font-semibold text-ik-text-secondary mb-2">Comparison Component</h4>
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
        </div>

        {/* Card Variants Demo */}
        <div className="bg-ik-bg-card rounded-ik-lg p-6 shadow-ik-md border border-ik-border-light mb-6">
          <h4 className="text-sm font-semibold text-ik-text-secondary mb-2">Card Variants</h4>
          {(['info', 'warning', 'tip', 'important'] as const).map((type) => (
            <JsonRenderer
              key={type}
              tree={{
                root: `card-${type}`,
                elements: {
                  [`card-${type}`]: {
                    key: `card-${type}`,
                    type: 'Card',
                    props: {
                      title: `${type.charAt(0).toUpperCase() + type.slice(1)} Card`,
                      type,
                    },
                    children: [`text-${type}`],
                  },
                  [`text-${type}`]: {
                    key: `text-${type}`,
                    type: 'Text',
                    props: {
                      content: `This is an example of a ${type} card with important information.`,
                    },
                  },
                },
              }}
            />
          ))}
        </div>

        {/* CodeBlock Demo */}
        <div className="bg-ik-bg-card rounded-ik-lg p-6 shadow-ik-md border border-ik-border-light mb-6">
          <h4 className="text-sm font-semibold text-ik-text-secondary mb-2">CodeBlock Component</h4>
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
        </div>

        {/* Action Buttons Demo */}
        <div className="bg-ik-bg-card rounded-ik-lg p-6 shadow-ik-md border border-ik-border-light">
          <h4 className="text-sm font-semibold text-ik-text-secondary mb-4">Action Suggestions</h4>
          <div className="flex flex-wrap gap-2">
            <JsonRenderer
              tree={{
                root: 'actions-demo',
                elements: {
                  'actions-demo': {
                    key: 'actions-demo',
                    type: 'Answer',
                    props: {},
                    children: ['action-1', 'action-2', 'action-3'],
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
                  'action-3': {
                    key: 'action-3',
                    type: 'ActionSuggestion',
                    props: {
                      label: 'Copy Link',
                      action: 'copy',
                      params: { text: 'https://kdrive.infomaniak.com/share/abc123' },
                    },
                  },
                },
              }}
              onAction={handleAction}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
