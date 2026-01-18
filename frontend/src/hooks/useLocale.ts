import { useMemo } from 'react'
import { translations } from '../i18n/translations'
import type { Translations } from '../i18n/translations'

type SupportedLanguage = 'en' | 'fr'

function detectLanguage(): SupportedLanguage {
  const browserLang = navigator.language || (navigator as { userLanguage?: string }).userLanguage || 'en'
  const langCode = browserLang.split('-')[0].toLowerCase()

  if (langCode === 'fr') {
    return 'fr'
  }

  return 'en'
}

export function useLocale(): { lang: SupportedLanguage; t: Translations } {
  const lang = useMemo(() => detectLanguage(), [])
  const t = translations[lang]

  return { lang, t }
}
