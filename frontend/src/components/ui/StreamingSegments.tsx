import { useState, useEffect, useCallback, useRef } from 'react'
import { Markdown } from './Markdown'
import type { MessageSegment, UIComponent } from '../../types'
import { StreamingText } from './StreamingText'
import { StreamingStepGuide } from './StreamingStepGuide'
import { SourceCards } from './SourceCards'
import { QuickActions } from './QuickActions'
import { PlatformAvailability } from './PlatformAvailability'
import { streamingLog } from '../../utils/debugLog'
import './Markdown.css'

interface StreamingSegmentsProps {
  segments: MessageSegment[]
  /** Whether streaming is still active */
  isStreaming: boolean
  /** Message ID to detect new messages and reset animation state */
  messageId?: string
}

/**
 * Renders segments with queued animations.
 * Each segment waits for the previous one to finish animating.
 */
export function StreamingSegments({
  segments,
  isStreaming,
  messageId,
}: StreamingSegmentsProps) {
  // How many segments have completed their animation
  const [completedCount, setCompletedCount] = useState(0)
  const prevSegmentsLengthRef = useRef(0)
  const prevMessageIdRef = useRef(messageId)
  // Track step counts for step_guide segments to detect updates
  const stepGuideStepCountsRef = useRef<Map<number, number>>(new Map())

  // Reset when message ID changes (new message) or segments array shrinks
  useEffect(() => {
    if (messageId !== prevMessageIdRef.current) {
      // eslint-disable-next-line react-hooks/set-state-in-effect -- intentional reset on prop change
      setCompletedCount(0)
      prevSegmentsLengthRef.current = 0
      prevMessageIdRef.current = messageId
      stepGuideStepCountsRef.current.clear()
    } else if (segments.length < prevSegmentsLengthRef.current) {
      setCompletedCount(0)
      stepGuideStepCountsRef.current.clear()
    }
    prevSegmentsLengthRef.current = segments.length
  }, [segments.length, messageId])

  // Detect when a completed step_guide receives new steps and "un-complete" it
  useEffect(() => {
    if (!isStreaming) return

    segments.forEach((segment, index) => {
      if (segment.type === 'component') {
        const component = segment.component as UIComponent
        if (component.type === 'step_guide') {
          const currentStepCount = component.steps?.length || 0
          const prevStepCount = stepGuideStepCountsRef.current.get(index) || 0

          if (currentStepCount > prevStepCount) {
            streamingLog('Segments', 'event', `Step guide received new steps`, {
              segmentIndex: index,
              prevStepCount,
              currentStepCount,
              completedCount,
              willResetCompletedCount: index < completedCount,
            })
            stepGuideStepCountsRef.current.set(index, currentStepCount)

            if (index < completedCount) {
              streamingLog('Segments', 'warn', `Resetting completedCount for new steps`, {
                from: completedCount,
                to: index,
              })
              setCompletedCount(index)
            }
          }
        }
      }
    })
  }, [segments, completedCount, isStreaming])

  // Handle animation complete for current segment
  const handleSegmentComplete = useCallback((source?: string) => {
    setCompletedCount(prev => {
      streamingLog('Segments', 'event', `handleSegmentComplete called`, {
        source: source || 'unknown',
        prevCount: prev,
        newCount: prev + 1,
        totalSegments: segments.length,
      })
      return prev + 1
    })
  }, [segments.length])

  // Auto-complete instant components (source_cards, quick_actions, platform_availability)
  // This must be in useEffect to avoid React strict mode issues with setTimeout in render
  // NOTE: We DON'T skip when !isStreaming - animation queue should continue after streaming ends
  const autoCompleteRef = useRef(false)
  useEffect(() => {
    const currentSegment = segments[completedCount]
    if (!currentSegment) {
      streamingLog('Segments', 'info', `No segment at index ${completedCount}`, {
        segmentsLength: segments.length,
      })
      return
    }

    streamingLog('Segments', 'state', `Checking segment ${completedCount}`, {
      type: currentSegment.type,
      componentType: currentSegment.type === 'component' ? (currentSegment.component as UIComponent).type : null,
    })

    // Only auto-complete component segments that are "instant"
    if (currentSegment.type === 'component') {
      const component = currentSegment.component as UIComponent
      const isInstantComponent =
        component.type === 'source_cards' ||
        component.type === 'quick_actions' ||
        component.type === 'platform_availability'

      if (isInstantComponent && !autoCompleteRef.current) {
        streamingLog('Segments', 'event', `Auto-completing instant component`, {
          componentType: component.type,
          segmentIndex: completedCount,
        })
        autoCompleteRef.current = true
        const timer = setTimeout(() => {
          handleSegmentComplete(`auto-complete:${component.type}`)
          autoCompleteRef.current = false
        }, 50)
        return () => {
          clearTimeout(timer)
          autoCompleteRef.current = false
        }
      }
    }
  }, [segments, completedCount, handleSegmentComplete])

  // Render a segment
  const renderSegment = (segment: MessageSegment, index: number) => {
    const isCurrentlyAnimating = index === completedCount
    const isCompleted = index < completedCount
    const shouldShow = isCompleted || isCurrentlyAnimating

    // Log render decisions for step_guide segments
    if (segment.type === 'component') {
      const component = segment.component as UIComponent
      if (component.type === 'step_guide') {
        streamingLog('Segments', 'info', `Rendering step_guide segment ${index}`, {
          isCompleted,
          isCurrentlyAnimating,
          shouldShow,
          skipAnimation: isCompleted,
          stepsCount: component.steps?.length || 0,
          completedCount,
        })
      }
    }

    // Don't show future segments until animation queue reaches them
    // This applies both during AND after streaming - animation should complete naturally
    if (!shouldShow) return null

    if (segment.type === 'text') {
      if (!segment.content.trim()) return null

      // Only show instant if animation is truly complete
      if (isCompleted) {
        return (
          <div key={`text-${index}`} className="message-content markdown-content">
            <Markdown>{segment.content}</Markdown>
          </div>
        )
      }

      // Currently animating OR waiting to animate: use streaming text
      return (
        <div key={`text-${index}`} className="message-content markdown-content">
          <StreamingText
            content={segment.content}
            onComplete={handleSegmentComplete}
          />
        </div>
      )
    }

    // Component segment
    const component = segment.component as UIComponent

    if (component.type === 'step_guide') {
      // ALWAYS use StreamingStepGuide to prevent remounting when new steps arrive
      // after the component was "completed". The streaming component handles both
      // animating and completed states internally.
      // Pass skipAnimation=true if this segment is already completed to show content instantly
      return (
        <StreamingStepGuide
          key={component.id || `step-guide-${index}`}
          title={component.title}
          steps={component.steps || []}
          onComplete={handleSegmentComplete}
          skipAnimation={isCompleted}
        />
      )
    }

    // Instant components - rendered immediately, auto-completed via useEffect
    // Note: !shouldShow is already handled at the top of renderSegment
    if (component.type === 'source_cards') {
      return (
        <SourceCards
          key={component.id || `sources-${index}`}
          sources={component.sources}
        />
      )
    }

    if (component.type === 'quick_actions') {
      return (
        <QuickActions
          key={component.id || `actions-${index}`}
          actions={component.actions}
        />
      )
    }

    if (component.type === 'platform_availability') {
      return (
        <PlatformAvailability
          key={component.id || `platform-${index}`}
          feature={component.feature}
          platforms={component.platforms}
        />
      )
    }

    return null
  }

  return <>{segments.map((segment, index) => renderSegment(segment, index))}</>
}
