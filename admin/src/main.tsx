import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router-dom";

import Layout from "./Layout.tsx";
import Dashboard from "./dashboard/index.tsx";
import DB from "./db.tsx";
import FAQ from "./faq.tsx";
import "./index.css";
import Setting from "./setting.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="db" element={<DB />} />
          <Route path="setting" element={<Setting />} />
          <Route path="faq" element={<FAQ />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </StrictMode>
);
