/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      fontFamily: {
        "serif": ["Lora"],
        "sans": ["Montserrat"],
        "cursive": ["Allura"],
      },
      backgroundImage: {
        'site': "url('/gradient-bg.svg')",
        'site2': "url('/gradient-bg2.svg')",
        'blue-waves': "url('backgrounds/blue-waves.svg')",
      }
    },
  },
  plugins: [],
}

