const desktop = process.env.LHCI_FORM_FACTOR === 'desktop';
const outputDir = desktop ? 'artifacts/lighthouse-desktop' : 'artifacts/lighthouse-mobile';

module.exports = {
  ci: {
    collect: {
      numberOfRuns: 1,
      url: [
        'http://127.0.0.1:4173/',
        'http://127.0.0.1:4173/research/',
        'http://127.0.0.1:4173/publication/adhesives-wearable/',
        'http://127.0.0.1:4173/project/peel-trace-evaluation/'
      ],
      settings: {
        ...(desktop ? { preset: 'desktop' } : {}),
        chromeFlags: '--no-sandbox --disable-dev-shm-usage',
        onlyCategories: ['performance', 'accessibility', 'best-practices', 'seo']
      }
    },
    assert: {
      assertions: {
        'categories:accessibility': ['error', { minScore: 0.95 }],
        'categories:seo': ['error', { minScore: 0.95 }],
        'categories:best-practices': ['error', { minScore: 0.90 }],
        'categories:performance': ['error', { minScore: 0.85 }],
        'cumulative-layout-shift': ['error', { maxNumericValue: 0.10 }],
        'largest-contentful-paint': ['error', { maxNumericValue: 4000 }],
        'total-byte-weight': ['error', { maxNumericValue: 1500000 }]
      }
    },
    upload: {
      target: 'filesystem',
      outputDir
    }
  }
};
