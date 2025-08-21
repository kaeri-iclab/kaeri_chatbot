import { useCallback, useEffect, useState } from "react";

import { AxiosError } from "axios";
import { SaveIcon } from "lucide-react";

import { MODEL_LIST } from "./constants";

export default function Setting() {
  const [setting, setSetting] = useState<{
    key: string;
    queryModel: string;
    AIModel: string;
  }>({
    key: "",
    queryModel: "",
    AIModel: "",
  });
  const [loading, setLoading] = useState(false);

  const fetchSetting = useCallback(async () => {
    try {
      setLoading(true);
      const res = await fetch(`${import.meta.env.VITE_API_HOST}/setting`);
      if (res.ok) {
        const data = await res.json();
        setSetting({
          key: data.key,
          queryModel: data.query_model,
          AIModel: data.ai_model,
        });
      }
      setLoading(false);
    } catch (e) {
      console.error(e);
    }
  }, []);

  const changeSetting = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch(`${import.meta.env.VITE_API_HOST}/setting`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          key: setting.key,
          query_model: setting.queryModel,
          ai_model: setting.AIModel,
        }),
      });
      if (res.ok) {
        alert("저장되었습니다.");
      } else {
        alert("저장에 실패했습니다.");
      }
      setLoading(false);
    } catch (e) {
      if (e instanceof AxiosError)
        alert((e as AxiosError<{ detail: string }>).response?.data.detail);
    }
  }, [setting]);

  useEffect(() => {
    fetchSetting();
  }, [fetchSetting]);

  return (
    <main className="flex w-full flex-col p-24">
      <h1 className="title">API 키 관리</h1>
      <label className="input input-bordered mt-4 flex items-center gap-2">
        API 키
        <input
          type="text"
          className="grow"
          placeholder="sk-****"
          value={setting.key}
          onChange={(e) => {
            setSetting({ ...setting, key: e.target.value });
          }}
        />
      </label>

      <h1 className="title mt-12">모델 관리</h1>
      <div className="mt-4 grid grid-cols-[200px_200px] items-center gap-y-4">
        <div className="text-lg font-semibold">쿼리 분류 모델</div>
        <select
          className="select select-bordered"
          value={setting.queryModel}
          onChange={(e) => {
            setSetting({ ...setting, queryModel: e.target.value });
          }}
        >
          {MODEL_LIST.map((model) => (
            <option key={model} value={model}>
              {model}
            </option>
          ))}
        </select>

        <div className="text-lg font-semibold">AI 답변 생성 모델</div>
        <select
          className="select select-bordered"
          value={setting.AIModel}
          onChange={(e) => {
            setSetting({ ...setting, AIModel: e.target.value });
          }}
        >
          {MODEL_LIST.map((model) => (
            <option key={model} value={model}>
              {model}
            </option>
          ))}
        </select>
      </div>

      <button
        className="btn btn-primary mt-4 w-fit self-end"
        onClick={changeSetting}
        disabled={loading}
      >
        {loading ? (
          <div className="loading loading-spinner loading-xs" />
        ) : (
          <SaveIcon size={16} />
        )}
        저장
      </button>
    </main>
  );
}
