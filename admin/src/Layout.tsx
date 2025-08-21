import { useEffect } from "react";
import { Outlet, useLocation, useNavigate } from "react-router-dom";

import Sidebar from "./components/Sidebar";

function Layout() {
  const { pathname } = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    if (pathname === "/") {
      navigate("/dashboard");
    }
  }, [pathname, navigate]);

  return (
    <div className="flex h-screen w-full bg-white">
      <Sidebar />
      <div className="flex h-screen w-full flex-col overflow-y-auto">
        <Outlet />
      </div>
    </div>
  );
}

export default Layout;
