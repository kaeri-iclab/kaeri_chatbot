import daisyui from "daisyui";
import tailwindScrollbar from "tailwind-scrollbar";

/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#0c519e",
      },
    },
  },
  daisyui: {
    themes: [
      {
        nord: {
          ...require("daisyui/src/theming/themes")["corporate"],
          primary: "#0c519e",
          "primary-content": "#edf4ff",
          secondary: "#ffffff",

          "base-100": "#ffffff",
          "base-200": "#f7fafc",
          "base-300": "#edf2f7",
        },
      },
    ],
  },
  plugins: [daisyui, tailwindScrollbar],
};
