import type { ComponentRegistry } from '@json-render/react';

/**
 * Docs Registry - Maps catalog components to React implementations
 * Placeholder versions for B1, will be styled in B3
 */
export const docsRegistry: ComponentRegistry = {
  Answer: ({ element, children }) => (
    <div className="answer">
      {element.props.summary && (
        <p className="answer-summary">{element.props.summary}</p>
      )}
      {children}
    </div>
  ),

  Steps: ({ element, children }) => (
    <div className="steps">
      {element.props.title && (
        <h4 className="steps-title">{element.props.title}</h4>
      )}
      <ol className="steps-list">{children}</ol>
    </div>
  ),

  Step: ({ element }) => (
    <li className="step">
      <span className="step-number">{element.props.number}</span>
      <div className="step-content">
        <strong className="step-title">{element.props.title}</strong>
        <p className="step-description">{element.props.description}</p>
      </div>
    </li>
  ),

  Card: ({ element, children }) => (
    <div className={`card card--${element.props.type}`}>
      <h4 className="card-title">{element.props.title}</h4>
      <div className="card-content">{children}</div>
    </div>
  ),

  Table: ({ element }) => (
    <table className="table">
      <thead>
        <tr>
          {element.props.headers.map((header: string, i: number) => (
            <th key={i}>{header}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {element.props.rows.map((row: string[], i: number) => (
          <tr key={i}>
            {row.map((cell: string, j: number) => (
              <td key={j}>{cell}</td>
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
      <table className="comparison">
        <thead>
          <tr>
            <th>Feature</th>
            {items.map((item, i) => (
              <th key={i}>{item.name}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {features.map((feature, i) => (
            <tr key={i}>
              <td>{feature}</td>
              {items.map((item, j) => (
                <td key={j}>{item.values[i] ? '✓' : '—'}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    );
  },

  CodeBlock: ({ element }) => (
    <pre
      className={`codeblock ${element.props.language ? `language-${element.props.language}` : ''}`}
    >
      <code>{element.props.code}</code>
    </pre>
  ),

  ActionSuggestion: ({ element, onAction }) => (
    <button
      className="action-suggestion"
      onClick={() => onAction?.({ name: element.props.action, params: element.props.params })}
    >
      {element.props.label}
    </button>
  ),

  PlatformBadges: ({ element }) => (
    <div className="platform-badges">
      {element.props.platforms.map((platform: string) => (
        <span key={platform} className="platform-badge">
          {platform}
        </span>
      ))}
    </div>
  ),

  Text: ({ element }) => <p className="text">{element.props.content}</p>,
};
