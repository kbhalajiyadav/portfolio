const width = Number(process.env.PA11Y_WIDTH || 1440);
const height = Number(process.env.PA11Y_HEIGHT || (width <= 480 ? 844 : 1000));
const chrome = process.env.CHROME_PATH || process.env.PUPPETEER_EXECUTABLE_PATH;

module.exports = {
  defaults: {
    standard: 'WCAG2AA',
    timeout: 30000,
    wait: 500,
    viewport: { width, height },
    chromeLaunchConfig: {
      ...(chrome ? { executablePath: chrome } : {}),
      args: ['--no-sandbox', '--disable-dev-shm-usage']
    },
  },
  threshold: 0,
  concurrency: 2,
  urls: [
    'http://127.0.0.1:4174/notes/',
    'http://127.0.0.1:4174/notes/presentation-method/',
    'http://127.0.0.1:4174/notes/presentation-corrected/',
    'http://127.0.0.1:4174/notes/presentation-retired/',
    'http://127.0.0.1:4174/notes/presentation-withdrawn/'
  ]
};
