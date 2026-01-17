import type { PlatformStatus, Platform, Availability } from '../../types'
import './PlatformAvailability.css'

interface PlatformAvailabilityProps {
  feature: string
  platforms: PlatformStatus[]
}

const platformLabels: Record<Platform, string> = {
  web: 'Web',
  windows: 'Windows',
  macos: 'macOS',
  ios: 'iOS',
  android: 'Android',
  linux: 'Linux',
}

const platformIcons: Record<Platform, string> = {
  web: '🌐',
  windows: '🪟',
  macos: '🍎',
  ios: '📱',
  android: '🤖',
  linux: '🐧',
}

const availabilityIcons: Record<Availability, string> = {
  full: '✓',
  partial: '◐',
  none: '✗',
}

const availabilityColors: Record<Availability, string> = {
  full: '#28a745',
  partial: '#ffc107',
  none: '#dc3545',
}

export function PlatformAvailability({
  feature,
  platforms,
}: PlatformAvailabilityProps) {
  if (!platforms.length) return null

  return (
    <div className="platform-availability">
      <div className="platform-availability-header">
        <span className="platform-availability-icon">📱</span>
        <span className="platform-availability-title">
          Platform Availability: {feature}
        </span>
      </div>
      <div className="platform-availability-grid">
        {platforms.map((status) => (
          <div
            key={status.platform}
            className={`platform-item availability-${status.availability}`}
            title={status.notes}
          >
            <span className="platform-icon">
              {platformIcons[status.platform]}
            </span>
            <span className="platform-label">
              {platformLabels[status.platform]}
            </span>
            <span
              className="platform-status"
              style={{ color: availabilityColors[status.availability] }}
            >
              {availabilityIcons[status.availability]}
            </span>
            {status.notes && (
              <span className="platform-notes">{status.notes}</span>
            )}
          </div>
        ))}
      </div>
      <div className="platform-availability-legend">
        <span className="legend-item">
          <span style={{ color: availabilityColors.full }}>✓</span> Full
        </span>
        <span className="legend-item">
          <span style={{ color: availabilityColors.partial }}>◐</span> Partial
        </span>
        <span className="legend-item">
          <span style={{ color: availabilityColors.none }}>✗</span> None
        </span>
      </div>
    </div>
  )
}
