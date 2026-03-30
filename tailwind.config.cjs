const config = {
  content: ["*.html", "./src/**/*.{html,js,svelte,ts}"],

  theme: {
    extend: {
      colors: {
        'highlight': "#e20025",
        'bul-secondary': "#48a9a6",
        'bul-tertiary': "#1b2631",
        'bul-neutral': "#757575",
        'bul-text-body': "#555",
        'bul-text-heading': "#1b2631",
        'bul-bg-page': "#f2f2f2",
      },
      fontFamily: {
        sans: ['Roboto', 'Helvetica Neue', 'Calibri', 'Liberation Sans', 'sans-serif'],
      }
    }
  },

  plugins: [],
};

module.exports = config;
