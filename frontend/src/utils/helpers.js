export function isValidUrl(str) {
  try {
    const url = new URL(str);
    return url.protocol === 'http:' || url.protocol === 'https:';
  } catch {
    return false;
  }
}

export function formatDate(isoString) {
  if (!isoString) return 'Never';
  return new Date(isoString).toLocaleString();
}

export function formatClicks(count) {
  return `${Number(count).toLocaleString()} click${count === 1 ? '' : 's'}`;
}
