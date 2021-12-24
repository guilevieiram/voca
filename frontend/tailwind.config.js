module.exports = {
  purge: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html",
    ".src/**/**/*.{js,jsx,ts,tsx}"
  ],
  darkMode: 'class', // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
        light: "#ebebeb",
        dark: "#141414",
        blue: "#068d9d",
        purple: "#831161",
        red: "#ff0000"
      },
      fontFamily:{
        title: ['Cardo', 'ui-serif'],
        body: ['Quicksand', 'ui-sans-serif']
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
