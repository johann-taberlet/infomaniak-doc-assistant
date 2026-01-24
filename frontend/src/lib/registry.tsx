import type { ComponentRegistry } from '@json-render/react';

/**
 * Docs Registry - Maps catalog components to React implementations
 * Using Tailwind CSS v4 utility classes
 */
export const docsRegistry: ComponentRegistry = {
  Answer: ({ element, children }) => (
    <div className="my-4">
      {element.props.summary && (
        <p className="italic text-text-muted mb-4">{element.props.summary}</p>
      )}
      {children}
    </div>
  ),

  Steps: ({ element, children }) => (
    <div className="my-4">
      {element.props.title && (
        <h4 className="text-lg font-semibold mb-3">{element.props.title}</h4>
      )}
      <ol className="list-none p-0 m-0">{children}</ol>
    </div>
  ),

  Step: ({ element }) => (
    <li className="flex gap-3 mb-4 items-start">
      <span className="w-6 h-6 bg-primary text-white rounded-full text-center leading-6 shrink-0 text-sm font-semibold">
        {element.props.number}
      </span>
      <div className="flex-1">
        <strong className="block mb-1">{element.props.title}</strong>
        <p className="m-0 text-text-muted">{element.props.description}</p>
      </div>
    </li>
  ),

  Card: ({ element, children }) => {
    const typeStyles: Record<string, string> = {
      info: 'bg-info-bg border-l-4 border-info-border',
      warning: 'bg-warning-bg border-l-4 border-warning-border',
      tip: 'bg-tip-bg border-l-4 border-tip-border',
      important: 'bg-important-bg border-l-4 border-important-border',
    };
    return (
      <div className={`rounded-lg p-4 my-2 ${typeStyles[element.props.type] || ''}`}>
        <h4 className="m-0 mb-2 text-base font-semibold">{element.props.title}</h4>
        <div className="m-0">{children}</div>
      </div>
    );
  },

  Table: ({ element }) => (
    <table className="w-full border-collapse my-4">
      <thead>
        <tr>
          {element.props.headers.map((header: string, i: number) => (
            <th key={i} className="p-2 border border-gray-300 text-left bg-gray-100 font-semibold">
              {header}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {element.props.rows.map((row: string[], i: number) => (
          <tr key={i}>
            {row.map((cell: string, j: number) => (
              <td key={j} className="p-2 border border-gray-300 text-left">
                {cell}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  ),

  Comparison: ({ element }) => {
    const { features, items } = element.props as {
      features: string[];
      items: { name: string; values: boolean[] }[];
    };
    return (
      <table className="w-full border-collapse my-4">
        <thead>
          <tr>
            <th className="p-2 border border-gray-300 text-left bg-gray-100 font-semibold">Feature</th>
            {items.map((item, i) => (
              <th key={i} className="p-2 border border-gray-300 text-center bg-gray-100 font-semibold">
                {item.name}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {features.map((feature, i) => (
            <tr key={i}>
              <td className="p-2 border border-gray-300 text-left">{feature}</td>
              {items.map((item, j) => (
                <td key={j} className="p-2 border border-gray-300 text-center">
                  {item.values[i] ? '✓' : '—'}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    );
  },

  CodeBlock: ({ element }) => (
    <pre className="bg-zinc-900 text-zinc-300 p-4 rounded-md overflow-x-auto font-mono text-sm my-4">
      <code>{element.props.code}</code>
    </pre>
  ),

  ActionSuggestion: ({ element, onAction }) => (
    <button
      className="bg-primary text-white border-none py-2 px-4 rounded cursor-pointer text-sm m-1 transition-opacity hover:opacity-90 active:opacity-80"
      onClick={() => onAction?.({ name: element.props.action, params: element.props.params })}
    >
      {element.props.label}
    </button>
  ),

  PlatformBadges: ({ element }) => (
    <div className="flex gap-2 flex-wrap my-2">
      {element.props.platforms.map((platform: string) => (
        <span key={platform} className="bg-gray-200 py-1 px-2 rounded text-xs capitalize">
          {platform}
        </span>
      ))}
    </div>
  ),

  Text: ({ element }) => <p className="my-2 leading-relaxed">{element.props.content}</p>,
};
