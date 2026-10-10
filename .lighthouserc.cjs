const desktop = process.env.LHCI_FORM_FACTOR === 'desktop';
const outputDir = desktop ? 'artifacts/lighthouse-desktop' : 'artifacts/lighthouse-mobile';

module.exports = {
  ci: {
    collect: {
      numberOfRuns: 2,
      url: [
        'http://127.0.0.1:4173/',
        'http://127.0.0.1:4173/outputs/',
        'http://127.0.0.1:4173/research/',
        'http://127.0.0.1:4173/publication/adhesives-wearable/',
        'http://127.0.0.1:4173/project/quantitative-thermal-imaging/'
      ],
      settings: {
        ...(desktop ? { preset: 'desktop' } : {}),
        chromeFlags: '--no-sandbox --disable-dev-shm-usage',
        onlyCategories: ['performance', 'accessibility', 'best-practices', 'seo']
      }
    },
    assert: {
      assertions: {
        'categories:accessibility': ['error', { minScore: 0.98 }],
        'categories:seo': ['error', { minScore: 1.00 }],
        'categories:best-practices': ['error', { minScore: 0.95 }],
        'categories:performance': ['error', { minScore: 0.90 }],
        'cumulative-layout-shift': ['error', { maxNumericValue: 0.10 }],
        'largest-contentful-paint': ['error', { maxNumericValue: 2500 }],
        'total-blocking-time': ['error', { maxNumericValue: 300 }],
        'total-byte-weight': ['error', { maxNumericValue: 1000000 }]
      }
    },
    upload: {
      target: 'filesystem',
      outputDir
    }
  }
};
