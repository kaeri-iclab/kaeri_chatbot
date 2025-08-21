import { Link, useLocation } from "react-router-dom";

import cc from "classcat";

export default function Sidebar() {
  const { pathname } = useLocation();
  return (
    <aside className="h-screen w-80 shrink-0 bg-primary-content py-8">
      <div className="h-24 w-full">
        <img
          src="/logo.png"
          alt="logo"
          className="h-full w-full object-contain"
        />
      </div>
      <ul className="mt-8">
        <li>
          <Link
            to={"/dashboard"}
            className={cc([
              "btn btn-ghost btn-lg w-full justify-start hover:bg-white/60 active:bg-white/60",
              pathname === "/dashboard" && "bg-white",
            ])}
          >
            대시보드
          </Link>
        </li>
        <li>
          <Link
            to={"/db"}
            className={cc([
              "btn btn-ghost btn-lg w-full justify-start hover:bg-white/60 active:bg-white/60",
              pathname === "/db" && "bg-white",
            ])}
          >
            DB 업데이트
          </Link>
        </li>
        <li>
          <Link
            to={"/faq"}
            className={cc([
              "btn btn-ghost btn-lg w-full justify-start hover:bg-white/60 active:bg-white/60",
              pathname === "/faq" && "bg-white",
            ])}
          >
            FAQ
          </Link>
        </li>
        <li>
          <Link
            to={"/setting"}
            className={cc([
              "btn btn-ghost btn-lg w-full justify-start hover:bg-white/60 active:bg-white/60",
              pathname === "/setting" && "bg-white",
            ])}
          >
            설정
          </Link>
        </li>
      </ul>
    </aside>
  );
}
