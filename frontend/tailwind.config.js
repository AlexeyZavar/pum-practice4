const plugin = require('tailwindcss/plugin')
const scrollbar = plugin(function ({ addUtilities, matchUtilities, theme }) {
  const scrollbarTrackColorValue = value => ({
    '--scrollbar-track': value,
    '&::-webkit-scrollbar-track': {
      'background-color': value
    }
  })

  const scrollbarTrackRoundedValue = value => ({
    '&::-webkit-scrollbar-track': {
      'border-radius': value
    }
  })

  const scrollbarThumbColorValue = value => ({
    '--scrollbar-thumb': value,
    '&::-webkit-scrollbar-thumb': {
      'background-color': value
    }
  })

  const scrollbarThumbRoundedValue = value => ({
    '&::-webkit-scrollbar-thumb': {
      'border-radius': value
    }
  })

  addUtilities({
    '.scrollbar': {
      '--scrollbar-thumb': '#cdcdcd',
      '--scrollbar-track': '#f0f0f0',
      '--scrollbar-width': '17px',
      'scrollbar-color': 'var(--scrollbar-thumb) var(--scrollbar-track)',
      '&::-webkit-scrollbar': {
        width: 'var(--scrollbar-width)'
      }
    },
    '.scrollbar-thin': {
      '--scrollbar-width': '8px',
      'scrollbar-width': 'thin'
    }
  })

  Object.entries(theme('colors')).forEach(([colorName, color]) => {
    switch (typeof color) {
      case 'object':
        matchUtilities(
          {
            [`scrollbar-track-${colorName}`]: value => (scrollbarTrackColorValue(value)),
            [`scrollbar-thumb-${colorName}`]: value => (scrollbarThumbColorValue(value))
          },
          {
            values: color
          }
        )
        break
      case 'function':
        addUtilities({
          [`.scrollbar-track-${colorName}`]: scrollbarTrackColorValue(color({})),
          [`.scrollbar-thumb-${colorName}`]: scrollbarThumbColorValue(color({}))
        })
        break
      case 'string':
        addUtilities({
          [`.scrollbar-track-${colorName}`]: scrollbarTrackColorValue(color),
          [`.scrollbar-thumb-${colorName}`]: scrollbarThumbColorValue(color)
        })
        break
    }
  })

  matchUtilities(
    {
      'scrollbar-track-rounded': value => (scrollbarTrackRoundedValue(value)),
      'scrollbar-thumb-rounded': value => (scrollbarThumbRoundedValue(value))
    },
    {
      values: theme('borderRadius')
    }
  )
})

module.exports = {
  content: [
    './components/**/*.{js,vue,ts}',
    './layouts/**/*.vue',
    './pages/**/*.vue',
    './plugins/**/*.{js,ts}',
    './nuxt.config.{js,ts}'
  ],
  theme: {
    extend: {
      colors: {
        poetry: {
          100: '#f8f9fc',
          200: '#f1f3f9',
          300: '#dee3ed',
          400: '#c2c9d6',
          500: '#8f96a3',
          600: '#5e636e',
          700: '#2f3237',
          800: '#1d1e20',
          900: '#111213'
        },
        default: '#093d8d'
      }
    },
    fontFamily: {
      nunito: 'Nunito Sans'
    }
  },
  plugins: [scrollbar]
}
