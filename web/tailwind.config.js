/** @type {import('tailwindcss').Config} */
import { join } from 'path';
import { skeleton } from '@skeletonlabs/tw-plugin';

export default {
  darkMode: 'class',
  content: [
    './src/**/*.{html,js,svelte,ts}',
    join(require.resolve(
      '@skeletonlabs/skeleton'),
      '../**/*.{html,js,svelte,ts}'
    )
  ],
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
  plugins: [
    skeleton
  ],
}

