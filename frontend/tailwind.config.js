module.exports = {
  purge: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html",
    ".src/**/**/*.{js,jsx,ts,tsx}"
  ],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
        light: "#ebebeb",
        dark: "#141414",
        blue: "#068d9d",
        purple: "#831161"
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
