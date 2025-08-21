import { useCallback, useEffect, useState } from "react";

import { Datum, Serie } from "@nivo/line";
import { format } from "date-fns";
import { ko } from "date-fns/locale";

import QuestionChart from "./QuestionChart";
import UserChart from "./UserChart";

export default function Dashboard() {
  const [duration, setDuration] = useState<"day" | "week" | "month" | "year">(
    "week"
  );
  const [userData, setUserData] = useState<Serie[]>([]);
  const [questionData, setQuestionData] = useState<Datum[]>([]);
  const [status, setStatus] = useState<string>("");

  const fetchUserData = useCallback(async () => {
    try {
      const res = await fetch(
        `${import.meta.env.VITE_API_HOST}/dashboard/conversation?duration=${duration}`
      );
      const json = (await res.json()) as {
        date: string;
        count: number;
      }[];

      setUserData([
        {
          id: "User",
          data:
            duration === "day"
              ? json.map((datum) => ({
                  x: format(new Date(datum.date), "HH시"),
                  y: datum.count,
                }))
              : json.map((datum) => ({
                  x: format(new Date(datum.date), "MM-dd(iii)", {
                    locale: ko,
                  }),
                  y: datum.count,
                })),
        },
      ]);
    } catch (e) {
      console.error(e);
    }
  }, [duration]);

  const fetchQuestionData = useCallback(async () => {
    try {
      const res = await fetch(
        `${import.meta.env.VITE_API_HOST}/dashboard/query_type?duration=${duration}`
      );
      const json = (await res.json()) as {
        type: string;
        count: number;
      }[];

      setQuestionData(
        json.map((datum) => ({
          id: datum.type,
          label: datum.type,
          value: datum.count,
        }))
      );
    } catch (e) {
      console.error(e);
    }
  }, [duration]);

  const fetchStatus = useCallback(async () => {
    try {
      const res = await fetch(`${import.meta.env.VITE_API_HOST}`);
      if (res.ok) {
        const data = await res.json();
        setStatus(data.message);
      } else {
        setStatus("API 서버가 작동 중이 아닙니다.");
      }
    } catch {
      setStatus("API 서버가 작동 중이 아닙니다.");
    }
  }, []);

  useEffect(() => {
    fetchStatus();
    fetchUserData();
    fetchQuestionData();
  }, [duration]);

  useEffect(() => {
    fetchStatus();
    fetchUserData();
    fetchQuestionData();
  }, []);

  return (
    <main className="flex w-full flex-col gap-8 p-24">
      <div className="animate-pulse text-center text-sm font-semibold">
        {status}
      </div>
      <select
        className="select select-bordered"
        onChange={(e) =>
          setDuration(e.target.value as "day" | "week" | "month" | "year")
        }
        value={duration}
      >
        <option value="day">오늘</option>
        <option value="week">이번 주</option>
        <option value="month">이번 달</option>
        <option value="year">올해</option>
      </select>
      <div className="w-full">
        <h1 className="title">유저 사용량</h1>
        <UserChart data={userData} />
      </div>
      <div className="w-full">
        <h1 className="title">질문별 사용량</h1>
        <QuestionChart data={questionData} />
      </div>
    </main>
  );
}
