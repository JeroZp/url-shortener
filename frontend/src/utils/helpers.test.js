import { describe, it, expect } from 'vitest';
import { isValidUrl, formatDate, formatClicks } from './helpers';

describe('isValidUrl', () => {
  it('returns true for a valid http URL', () => {
    expect(isValidUrl('https://example.com/path?q=1')).toBe(true);
  });

  it('returns false for a random string', () => {
    expect(isValidUrl('not-a-url')).toBe(false);
  });

  it('returns false for an empty string', () => {
    expect(isValidUrl('')).toBe(false);
  });

  it('rejects non-http protocols', () => {
    expect(isValidUrl('ftp://files.example.com')).toBe(false);
  });
});

describe('formatDate', () => {
  it('formats an ISO string into a readable date', () => {
    const result = formatDate('2025-01-15T10:30:00Z');
    expect(result).toContain('2025');
  });

  it('returns "Never" for null', () => {
    expect(formatDate(null)).toBe('Never');
  });
});

describe('formatClicks', () => {
  it('formats a count with plural', () => {
    const result = formatClicks(1234);
    expect(result).toMatch(/1.234 clicks/);
  });

  it('uses singular for 1', () => {
    expect(formatClicks(1)).toBe('1 click');
  });

  it('handles zero', () => {
    expect(formatClicks(0)).toBe('0 clicks');
  });
});
