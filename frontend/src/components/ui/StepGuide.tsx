import { useState } from 'react'
import { Markdown } from './Markdown'
import type { Step } from '../../types'
import './StepGuide.css'
import './Markdown.css'

interface StepGuideProps {
  title: string
  steps: Step[]
}

export function StepGuide({ title, steps }: StepGuideProps) {
  const [completedSteps, setCompletedSteps] = useState<Set<number>>(new Set())
  const [expandedSteps, setExpandedSteps] = useState<Set<number>>(new Set())

  const toggleComplete = (stepNumber: number) => {
    setCompletedSteps((prev) => {
      const next = new Set(prev)
      if (next.has(stepNumber)) {
        next.delete(stepNumber)
      } else {
        next.add(stepNumber)
      }
      return next
    })
  }

  const toggleExpanded = (stepNumber: number) => {
    setExpandedSteps((prev) => {
      const next = new Set(prev)
      if (next.has(stepNumber)) {
        next.delete(stepNumber)
      } else {
        next.add(stepNumber)
      }
      return next
    })
  }

  const copyCommand = async (command: string) => {
    try {
      await navigator.clipboard.writeText(command)
    } catch (err) {
      console.error('Failed to copy:', err)
    }
  }

  const progress = (completedSteps.size / steps.length) * 100

  return (
    <div className="step-guide">
      <div className="step-guide-header">
        <span className="step-guide-icon">📋</span>
        <span className="step-guide-title">{title}</span>
        <span className="step-guide-progress-text">
          {completedSteps.size}/{steps.length}
        </span>
      </div>
      <div className="step-guide-progress-bar">
        <div
          className="step-guide-progress-fill"
          style={{ width: `${progress}%` }}
        />
      </div>
      <div className="step-guide-steps">
        {steps.map((step) => {
          const isCompleted = completedSteps.has(step.number)
          const isExpanded = expandedSteps.has(step.number)
          const hasDetails = step.details || step.command

          return (
            <div
              key={step.number}
              className={`step-item ${isCompleted ? 'completed' : ''}`}
            >
              <div className="step-item-main">
                <button
                  className="step-checkbox"
                  onClick={() => toggleComplete(step.number)}
                  aria-label={isCompleted ? 'Mark as incomplete' : 'Mark as complete'}
                >
                  {isCompleted ? '✓' : step.number}
                </button>
                <div className="step-content">
                  <h5 className="step-title">{step.title}</h5>
                  <div className="step-description markdown-content markdown-compact">
                    <Markdown>{step.description}</Markdown>
                  </div>
                </div>
                {hasDetails && (
                  <button
                    className="step-expand"
                    onClick={() => toggleExpanded(step.number)}
                    aria-label={isExpanded ? 'Collapse' : 'Expand'}
                  >
                    {isExpanded ? '▲' : '▼'}
                  </button>
                )}
              </div>
              {hasDetails && isExpanded && (
                <div className="step-details markdown-content markdown-compact">
                  {step.details && <Markdown>{step.details}</Markdown>}
                  {step.command && (
                    <div className="step-command">
                      <code>{step.command}</code>
                      <button
                        className="step-copy"
                        onClick={() => copyCommand(step.command!)}
                        title="Copy command"
                      >
                        📋
                      </button>
                    </div>
                  )}
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
