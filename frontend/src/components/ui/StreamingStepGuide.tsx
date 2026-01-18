import { useState, useEffect, useRef, useCallback } from 'react'
import { Markdown } from './Markdown'
import type { Step } from '../../types'
import { streamingLog } from '../../utils/debugLog'
import './StepGuide.css'
import './Markdown.css'

interface StreamingStepGuideProps {
  title: string
  steps: Step[]
  /** Called when all steps have been displayed and no new ones arrived */
  onComplete?: () => void
  /** Delay between characters in ms (default: 8) */
  charDelay?: number
  /** How long to wait after finishing before calling onComplete (default: 500ms) */
  completeDelay?: number
  /** If true, skip animation and show all content instantly */
  skipAnimation?: boolean
}

/**
 * StepGuide with streaming animation.
 * Each step's content is revealed word by word.
 */
export function StreamingStepGuide({
  title,
  steps,
  onComplete,
  charDelay = 8,
  completeDelay = 500,
  skipAnimation = false,
}: StreamingStepGuideProps) {
  const [completedSteps, setCompletedSteps] = useState<Set<number>>(new Set())
  const [expandedSteps, setExpandedSteps] = useState<Set<number>>(new Set())

  // Animation state
  // animatedStepCount: how many steps are FULLY animated
  // currentCharIndex: character progress for the step currently being animated
  const [animatedStepCount, setAnimatedStepCount] = useState(0)
  const [currentCharIndex, setCurrentCharIndex] = useState(0)

  const onCompleteCalledRef = useRef(false)
  const completeTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  const prevStepsLengthRef = useRef(0)
  const prevSkipAnimationRef = useRef(skipAnimation)

  // Log when skipAnimation prop changes - this is key to finding the bug
  useEffect(() => {
    if (skipAnimation !== prevSkipAnimationRef.current) {
      streamingLog('StepGuide', 'warn', `skipAnimation prop changed!`, {
        from: prevSkipAnimationRef.current,
        to: skipAnimation,
        title,
        animatedStepCount,
        stepsLength: steps.length,
      })
      prevSkipAnimationRef.current = skipAnimation
    }
  }, [skipAnimation, title, animatedStepCount, steps.length])

  // Cancel any pending complete timer
  const cancelCompleteTimer = useCallback(() => {
    if (completeTimerRef.current) {
      clearTimeout(completeTimerRef.current)
      completeTimerRef.current = null
    }
  }, [])

  // Schedule onComplete call
  const scheduleComplete = useCallback(() => {
    cancelCompleteTimer()
    streamingLog('StepGuide', 'event', `Scheduling onComplete`, {
      completeDelay,
      title,
      stepsLength: steps.length,
    })
    completeTimerRef.current = setTimeout(() => {
      if (!onCompleteCalledRef.current) {
        streamingLog('StepGuide', 'event', `Calling onComplete callback`, { title })
        onCompleteCalledRef.current = true
        onComplete?.()
      }
    }, completeDelay)
  }, [cancelCompleteTimer, completeDelay, onComplete, title, steps.length])

  // Handle steps array changes
  useEffect(() => {
    if (steps.length > prevStepsLengthRef.current) {
      cancelCompleteTimer()
      onCompleteCalledRef.current = false
    }
    if (steps.length < prevStepsLengthRef.current) {
      // eslint-disable-next-line react-hooks/set-state-in-effect -- intentional reset on prop change
      setAnimatedStepCount(0)
      setCurrentCharIndex(0)
      onCompleteCalledRef.current = false
      cancelCompleteTimer()
    }
    prevStepsLengthRef.current = steps.length
  }, [steps.length, cancelCompleteTimer])

  // Animation effect - runs on every tick
  useEffect(() => {
    // If skipAnimation is true, DON'T modify animation state
    // Just let the render show all content via getStepDisplayText
    // This prevents the race condition where skipAnimation flips true/false
    // and we lose track of which steps were actually animated
    if (skipAnimation) {
      streamingLog('StepGuide', 'info', `skipAnimation=true, skipping effect (not modifying state)`, {
        animatedStepCount,
        stepsLength: steps.length,
        title,
      })
      return
    }

    // Already completed?
    if (onCompleteCalledRef.current) {
      streamingLog('StepGuide', 'info', `Already completed, skipping`, { title })
      return
    }

    // No steps yet? Wait.
    if (steps.length === 0) return

    // All current steps fully animated?
    if (animatedStepCount >= steps.length) {
      streamingLog('StepGuide', 'event', `All steps animated, scheduling complete`, {
        animatedStepCount,
        stepsLength: steps.length,
        title,
      })
      scheduleComplete()
      return
    }

    // Get the step we're currently animating
    const currentStep = steps[animatedStepCount]
    if (!currentStep) return

    // Get total characters for this step
    const fullText = currentStep.title + ' ' + currentStep.description
    const totalChars = fullText.length

    // Current step fully displayed?
    if (currentCharIndex >= totalChars) {
      streamingLog('StepGuide', 'event', `Step ${animatedStepCount + 1} fully displayed, moving to next`, {
        stepNumber: animatedStepCount + 1,
        totalSteps: steps.length,
        title,
      })
      // Move to next step after a small pause
      const timer = setTimeout(() => {
        setAnimatedStepCount(prev => prev + 1)
        setCurrentCharIndex(0)
      }, 150)
      return () => clearTimeout(timer)
    }

    // Reveal next character (or batch of 2-3 for speed)
    const timer = setTimeout(() => {
      setCurrentCharIndex(prev => Math.min(prev + 2, totalChars))
    }, charDelay)

    return () => clearTimeout(timer)
  }, [animatedStepCount, currentCharIndex, steps, charDelay, scheduleComplete, skipAnimation, title])

  // Cleanup
  useEffect(() => {
    return () => cancelCompleteTimer()
  }, [cancelCompleteTimer])

  const toggleComplete = (stepNumber: number) => {
    setCompletedSteps(prev => {
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
    setExpandedSteps(prev => {
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
    } catch {
      // Silently ignore clipboard errors
    }
  }

  // Get displayed text for a step
  const getStepDisplayText = (step: Step, stepArrayIndex: number): { title: string; description: string } => {
    // If skipAnimation, show all text immediately (but don't modify animation state)
    if (skipAnimation) {
      return { title: step.title, description: step.description }
    }

    // Step already fully animated
    if (stepArrayIndex < animatedStepCount) {
      return { title: step.title, description: step.description }
    }

    // Step not yet started
    if (stepArrayIndex > animatedStepCount) {
      return { title: '', description: '' }
    }

    // Currently animating this step - show partial text
    const fullText = step.title + ' ' + step.description
    const displayedText = fullText.slice(0, currentCharIndex)

    // Find where title ends
    const titleLength = step.title.length
    if (displayedText.length <= titleLength) {
      return { title: displayedText, description: '' }
    } else {
      return {
        title: step.title,
        description: displayedText.slice(titleLength + 1), // +1 for the space
      }
    }
  }

  // Progress calculation - only count completed by user
  const progress = steps.length > 0 ? (completedSteps.size / steps.length) * 100 : 0

  // How many steps to render (fully animated + currently animating one)
  // If skipAnimation, show all steps
  const visibleStepCount = skipAnimation ? steps.length : Math.min(animatedStepCount + 1, steps.length)

  return (
    <div className="step-guide">
      <div className="step-guide-header">
        <span className="step-guide-icon">📋</span>
        <span className="step-guide-title">{title}</span>
        {steps.length > 0 && (
          <span className="step-guide-progress-text">
            {completedSteps.size}/{steps.length}
          </span>
        )}
      </div>
      {steps.length > 0 && (
        <div className="step-guide-progress-bar">
          <div
            className="step-guide-progress-fill"
            style={{ width: `${progress}%` }}
          />
        </div>
      )}
      <div className="step-guide-steps">
        {steps.slice(0, visibleStepCount).map((step, arrayIndex) => {
          const isUserCompleted = completedSteps.has(step.number)
          const isExpanded = expandedSteps.has(step.number)
          const hasDetails = step.details || step.command
          // If skipAnimation, treat all as fully animated for UI purposes
          const isFullyAnimated = skipAnimation || arrayIndex < animatedStepCount
          const { title: displayedTitle, description: displayedDesc } = getStepDisplayText(step, arrayIndex)

          // Don't render if nothing to show yet
          if (!displayedTitle) return null

          return (
            <div
              key={step.number}
              className={`step-item ${isUserCompleted ? 'completed' : ''}`}
            >
              <div className="step-item-main">
                <button
                  className="step-checkbox"
                  onClick={() => toggleComplete(step.number)}
                  aria-label={isUserCompleted ? 'Mark as incomplete' : 'Mark as complete'}
                >
                  {isUserCompleted ? '✓' : step.number}
                </button>
                <div className="step-content">
                  <h5 className="step-title">{displayedTitle}</h5>
                  <div className="step-description markdown-content markdown-compact">
                    <Markdown>{displayedDesc || '\u00A0'}</Markdown>
                  </div>
                </div>
                {hasDetails && isFullyAnimated && (
                  <button
                    className="step-expand"
                    onClick={() => toggleExpanded(step.number)}
                    aria-label={isExpanded ? 'Collapse' : 'Expand'}
                  >
                    {isExpanded ? '▲' : '▼'}
                  </button>
                )}
              </div>
              {hasDetails && isExpanded && isFullyAnimated && (
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
