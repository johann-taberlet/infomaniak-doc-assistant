import type { ComponentRegistry } from '@json-render/react';

/**
 * Docs Registry - Maps catalog components to React implementations
 * Using Infomaniak Design System with Tailwind CSS v4
 */
export const docsRegistry: ComponentRegistry = {
  Answer: ({ element, children }) => (
    <div className="my-4">
      {element.props.summary && (
        <p className="italic text-ik-text-secondary mb-4">{element.props.summary}</p>
      )}
      {children}
    </div>
  ),

  Steps: ({ element, children }) => (
    <div className="mt-6 rounded-ik-md bg-ik-bg-tertiary border border-ik-border">
      {/* Header */}
      <div className="flex items-center gap-2 px-4 py-3 border-b border-ik-border">
        <span className="text-base">📋</span>
        {element.props.title && (
          <span className="flex-1 font-semibold text-sm text-ik-text-secondary">
            {element.props.title}
          </span>
        )}
      </div>
      {/* Steps list */}
      <div className="py-2">{children}</div>
    </div>
  ),

  Step: ({ element }) => (
    <div className="animate-step-enter border-b border-ik-border last:border-b-0">
      <div className="flex items-start gap-3 px-4 py-3">
        {/* Step number circle */}
        <span className="shrink-0 w-7 h-7 flex items-center justify-center bg-ik-bg-card border-2 border-ik-border rounded-full text-xs font-semibold text-ik-text-secondary transition-colors hover:border-ik-primary hover:text-ik-primary">
          {element.props.number}
        </span>
        {/* Content */}
        <div className="flex-1 min-w-0">
          <h4 className="m-0 mb-1 text-sm font-semibold text-ik-text-primary">
            {element.props.title}
          </h4>
          <p className="text-[0.8125rem] text-ik-text-secondary leading-snug">
            {element.props.description}
          </p>
        </div>
      </div>
    </div>
  ),

  Card: ({ element, children }) => {
    const typeStyles: Record<string, string> = {
      info: 'bg-ik-info-bg border-l-4 border-ik-info',
      warning: 'bg-ik-warning-bg border-l-4 border-ik-warning',
      tip: 'bg-ik-tip-bg border-l-4 border-ik-tip',
      important: 'bg-ik-important-bg border-l-4 border-ik-important',
    };
    return (
      <div className={`rounded-ik-sm p-4 my-4 ${typeStyles[element.props.type] || ''}`}>
        <h4 className="m-0 mb-2 text-sm font-semibold text-ik-text-primary">
          {element.props.title}
        </h4>
        <div className="text-sm text-ik-text-secondary">{children}</div>
      </div>
    );
  },

  Table: ({ element }) => (
    <div className="my-4 overflow-x-auto">
      <table className="w-full border-collapse text-sm">
        <thead>
          <tr>
            {element.props.headers.map((header: string, i: number) => (
              <th
                key={i}
                className="p-3 text-left font-semibold text-ik-text-primary bg-ik-bg-secondary border border-ik-border"
              >
                {header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {element.props.rows.map((row: string[], i: number) => (
            <tr key={i} className="even:bg-ik-bg-tertiary hover:bg-ik-primary-light transition-colors">
              {row.map((cell: string, j: number) => (
                <td key={j} className="p-3 text-left border border-ik-border">
                  {cell}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  ),

  Comparison: ({ element }) => {
    const { features, items } = element.props as {
      features: string[];
      items: { name: string; values: boolean[] }[];
    };
    return (
      <div className="my-4 overflow-x-auto">
        <table className="w-full border-collapse text-sm">
          <thead>
            <tr>
              <th className="p-3 text-left font-semibold text-ik-text-primary bg-ik-bg-secondary border border-ik-border">
                Feature
              </th>
              {items.map((item, i) => (
                <th
                  key={i}
                  className="p-3 text-center font-semibold text-ik-text-primary bg-ik-bg-secondary border border-ik-border"
                >
                  {item.name}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {features.map((feature, i) => (
              <tr key={i} className="even:bg-ik-bg-tertiary hover:bg-ik-primary-light transition-colors">
                <td className="p-3 text-left border border-ik-border">{feature}</td>
                {items.map((item, j) => (
                  <td key={j} className="p-3 text-center border border-ik-border">
                    <span className={item.values[i] ? 'text-ik-success font-bold' : 'text-ik-text-muted'}>
                      {item.values[i] ? '✓' : '—'}
                    </span>
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  },

  CodeBlock: ({ element }) => (
    <div className="my-4">
      <pre className="bg-[#212529] text-[#f8f8f2] p-4 rounded-ik-sm overflow-x-auto font-mono text-[0.8125rem] leading-relaxed">
        <code>{element.props.code}</code>
      </pre>
    </div>
  ),

  ActionSuggestion: ({ element, onAction }) => (
    <button
      className="inline-flex items-center gap-1.5 px-4 py-2 bg-white border border-ik-border rounded-full text-[0.8125rem] text-ik-text-secondary font-medium cursor-pointer transition-all duration-200 hover:border-ik-primary hover:text-ik-primary hover:bg-ik-primary-light"
      onClick={() => onAction?.({ name: element.props.action, params: element.props.params })}
    >
      {element.props.label}
    </button>
  ),

  PlatformBadges: ({ element }) => (
    <div className="mt-6 rounded-ik-sm bg-ik-bg-tertiary border border-ik-border">
      <div className="flex items-center gap-2 px-4 py-3 border-b border-ik-border">
        <span className="text-base">📱</span>
        <span className="font-semibold text-sm text-ik-text-secondary">Available on</span>
      </div>
      <div className="grid grid-cols-[repeat(auto-fit,minmax(100px,1fr))] gap-2 p-4">
        {element.props.platforms.map((platform: string) => (
          <div
            key={platform}
            className="flex flex-col items-center p-3 bg-ik-bg-card border border-ik-border rounded-md text-center"
          >
            <span className="text-2xl mb-1">
              {platform === 'web' && '🌐'}
              {platform === 'ios' && '📱'}
              {platform === 'android' && '🤖'}
              {platform === 'macos' && '🍎'}
              {platform === 'windows' && '🪟'}
              {platform === 'linux' && '🐧'}
            </span>
            <span className="text-xs font-medium text-ik-text-secondary capitalize">{platform}</span>
          </div>
        ))}
      </div>
    </div>
  ),

  Text: ({ element }) => (
    <p className="my-2 text-ik-text-primary leading-relaxed">{element.props.content}</p>
  ),
};
