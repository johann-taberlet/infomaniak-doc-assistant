// Chat types
export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  language?: string
  uiComponents?: UIComponent[]
}

// Base UI component type
export interface BaseUIComponent {
  type: string
  id: string
}

// Source document for SourceCards
export interface SourceDocument {
  title: string
  product: 'kDrive' | 'kMeet' | 'kChat' | string
  url: string
  snippet: string
  relevanceScore?: number
}

export interface SourceCardsComponent extends BaseUIComponent {
  type: 'source_cards'
  sources: SourceDocument[]
}

// Step for StepGuide
export interface Step {
  number: number
  title: string
  description: string
  details?: string
  command?: string
}

export interface StepGuideComponent extends BaseUIComponent {
  type: 'step_guide'
  title: string
  steps: Step[]
}

// QuickActions
export interface QuickAction {
  label: string
  url?: string
  action?: 'open_docs' | 'contact_support' | 'copy'
  icon?: string
}

export interface QuickActionsComponent extends BaseUIComponent {
  type: 'quick_actions'
  actions: QuickAction[]
}

// PlatformAvailability
export type Platform = 'web' | 'windows' | 'macos' | 'ios' | 'android' | 'linux'
export type Availability = 'full' | 'partial' | 'none'

export interface PlatformStatus {
  platform: Platform
  availability: Availability
  notes?: string
}

export interface PlatformAvailabilityComponent extends BaseUIComponent {
  type: 'platform_availability'
  feature: string
  platforms: PlatformStatus[]
}

// Union type for all UI components
export type UIComponent =
  | SourceCardsComponent
  | StepGuideComponent
  | QuickActionsComponent
  | PlatformAvailabilityComponent

// SSE event types
export interface TokenEvent {
  token: string
}

export interface DoneEvent {
  done: true
  language?: string
  ui_components?: UIComponent[]
}

export type SSEEvent = TokenEvent | DoneEvent
