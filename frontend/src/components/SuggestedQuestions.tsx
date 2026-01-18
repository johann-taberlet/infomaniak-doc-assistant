import { useMemo } from 'react'
import { getRandomQuestions } from '../data/suggestedQuestions'
import './SuggestedQuestions.css'

interface SuggestedQuestionsProps {
  lang: 'en' | 'fr'
  onSelect: (question: string) => void
}

export function SuggestedQuestions({ lang, onSelect }: SuggestedQuestionsProps) {
  const questions = useMemo(() => getRandomQuestions(lang, 5), [lang])

  return (
    <div className="suggested-questions">
      {questions.map((question, index) => (
        <button
          key={index}
          className="suggested-question"
          onClick={() => onSelect(question)}
          type="button"
        >
          {question}
        </button>
      ))}
    </div>
  )
}
