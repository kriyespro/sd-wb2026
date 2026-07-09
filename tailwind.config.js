/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./templates/**/*.jinja'],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#eef2f9',
          100: '#d9e2f2',
          200: '#b3c5e5',
          300: '#8da8d8',
          400: '#4a6fad',
          500: '#1e3a6e',
          600: '#162f5c',
          700: '#0f2448',
          800: '#0a1a38',
          900: '#06122b',
          950: '#030b1a',
        },
        gold: {
          50: '#fbf7eb',
          100: '#f5ecd0',
          200: '#ebd9a1',
          300: '#e0c572',
          400: '#d4af37',
          500: '#c9a227',
          600: '#a8861f',
          700: '#876818',
        },
        accent: {
          300: '#e0c572',
          400: '#d4af37',
          500: '#c9a227',
        },
        ink: {
          900: '#06122b',
          800: '#0a1a38',
          700: '#0f2448',
        },
      },
      fontFamily: {
        sans: ['"DM Sans"', 'system-ui', 'sans-serif'],
        display: ['Outfit', '"DM Sans"', 'sans-serif'],
        serif: ['"Playfair Display"', 'Georgia', 'serif'],
      },
      keyframes: {
        'fade-up': {
          '0%': { opacity: '0', transform: 'translateY(24px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        marquee: {
          '0%': { transform: 'translateX(0)' },
          '100%': { transform: 'translateX(-50%)' },
        },
      },
      animation: {
        'fade-up': 'fade-up 0.7s cubic-bezier(0.16,1,0.3,1) both',
        marquee: 'marquee 32s linear infinite',
      },
    },
  },
  plugins: [],
};
