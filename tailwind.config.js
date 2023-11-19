/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        black: '#000', // Set black color
      },
      backgroundColor: {
        primary: 'black', // Set black as the primary background color
      },
      textColor: {
        primary: 'white', // Set white as the primary text color
      },
    },
  },
  plugins: [],
}
