const config = {
  content: ["*.html", "./src/**/*.{html,js,svelte,ts}"],

  theme: {
    extend: {
      colors: {
        'highlight': "#2A9D8F",
        'bul-secondary': "#FFBF00",
        'bul-tertiary': "#264653",
        'bul-neutral': "#7F8E93",
        'bul-text-body': "#4A5A5D",
        'bul-text-heading': "#264653",
        'bul-bg-page': "#F6F7F6",
      },
      fontFamily: {
        sans: ['Roboto', 'Helvetica Neue', 'Calibri', 'Liberation Sans', 'sans-serif'],
      }
    }
  },

  plugins: [],
};

module.exports = config;
