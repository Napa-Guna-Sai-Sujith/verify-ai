/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        trust: {
          50: '#f0f4ff',
          100: '#e0e9fe',
          200: '#bae0fd',
          300: '#7cd4fd',
          400: '#36bffa',
          500: '#0ca5eb',
          600: '#0084ca',
          700: '#0169a5',
          800: '#065988',
          900: '#0b4a72',
          950: '#072f4a',
        },
        slate: {
          850: '#151e2e',
          900: '#0f172a',
          950: '#090d16',
        },
        verity: {
          green: '#10b981',
          yellow: '#f59e0b',
          red: '#ef4444',
          accent: '#6366f1',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
      boxShadow: {
        'glow-teal': '0 0 25px -5px rgba(16, 185, 129, 0.25)',
        'glow-amber': '0 0 25px -5px rgba(245, 158, 11, 0.25)',
        'glow-rose': '0 0 25px -5px rgba(239, 68, 68, 0.25)',
        'glow-indigo': '0 0 30px -5px rgba(99, 102, 241, 0.3)',
      }
    },
  },
  plugins: [],
}
