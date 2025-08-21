import { useCallback, useEffect, useState } from "react";

import { AxiosError } from "axios";
import { PlusIcon, TrashIcon } from "lucide-react";

export default function FAQ() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [checked, setChecked] = useState<string[]>([]);
  const [faq, setFAQ] = useState<
    {
      question: string;
      answer: string;
      id: string;
    }[]
  >([]);
  const [deleteLoading, setDeleteLoading] = useState(false);
  const [addLoading, setAddLoading] = useState(false);

  const fetchFAQ = useCallback(async () => {
    try {
      const res = await fetch(`${import.meta.env.VITE_API_HOST}/faq`);
      if (res.ok) {
        const data = await res.json();
        setFAQ(data);
      }
    } catch (e) {
      if (e instanceof AxiosError)
        alert((e as AxiosError<{ detail: string }>).response?.data.detail);
    }
  }, []);

  const addFAQ = useCallback(async () => {
    try {
      setAddLoading(true);
      const res = await fetch(`${import.meta.env.VITE_API_HOST}/faq`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question,
          answer,
        }),
      });
      if (res.ok) {
        setQuestion("");
        setAnswer("");
        fetchFAQ();
      }
      setAddLoading(false);
    } catch (e) {
      if (e instanceof AxiosError)
        alert((e as AxiosError<{ detail: string }>).response?.data.detail);
    }
  }, [question, answer, fetchFAQ]);

  const deleteFAQ = useCallback(async () => {
    try {
      setDeleteLoading(true);
      const res = await fetch(`${import.meta.env.VITE_API_HOST}/faq`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          ids: checked,
        }),
      });
      if (res.ok) {
        setChecked([]);
        fetchFAQ();
      }
      setDeleteLoading(false);
    } catch (e) {
      if (e instanceof AxiosError)
        alert((e as AxiosError<{ detail: string }>).response?.data.detail);
    }
  }, [checked, fetchFAQ]);

  useEffect(() => {
    fetchFAQ();
  }, [fetchFAQ]);

  return (
    <main className="flex w-full flex-col p-24">
      <h1 className="title">FAQ 추가</h1>

      <label className="form-control mt-4 w-full">
        <div className="label">
          <span className="label-text text-lg font-semibold">질문</span>
        </div>
        <textarea
          placeholder="Type your question here"
          className="textarea textarea-bordered w-full resize-none"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
      </label>
      <label className="form-control mt-2 w-full">
        <div className="label">
          <span className="label-text text-lg font-semibold">답변</span>
        </div>
        <textarea
          placeholder="Type your answer here"
          className="textarea textarea-bordered w-full resize-none"
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
        />
      </label>

      <button
        className="btn btn-primary mt-4 w-fit self-end"
        onClick={addFAQ}
        disabled={addLoading || !question || !answer}
      >
        {addLoading ? (
          <div className="loading loading-spinner loading-xs" />
        ) : (
          <PlusIcon size={16} />
        )}{" "}
        추가
      </button>

      <div className="mt-12 flex items-center justify-between">
        <h1 className="title">FAQ 목록</h1>
        <button
          className="btn btn-ghost"
          disabled={checked.length === 0 || deleteLoading}
          onClick={deleteFAQ}
        >
          {addLoading ? (
            <div className="loading loading-spinner loading-xs" />
          ) : (
            <TrashIcon size={16} />
          )}{" "}
          삭제
        </button>
      </div>
      <table className="table table-lg">
        <thead>
          <tr>
            <th className="px-2">
              <input
                type="checkbox"
                className="checkbox-primary checkbox checkbox-xs"
                onChange={(e) => {
                  if (e.target.checked) {
                    setChecked(faq.map((f) => f.id));
                  } else {
                    setChecked([]);
                  }
                }}
              />
            </th>
            <th>제목</th>
            <th>내용</th>
          </tr>
        </thead>
        <tbody>
          {faq.map((f) => (
            <tr key={f.id}>
              <td className="px-2">
                <input
                  type="checkbox"
                  className="checkbox-primary checkbox checkbox-xs"
                  checked={checked.includes(f.id)}
                  onChange={(e) => {
                    if (e.target.checked) {
                      setChecked((checked) => [...checked, f.id]);
                    } else {
                      setChecked((checked) =>
                        checked.filter((c) => c !== f.id)
                      );
                    }
                  }}
                />
              </td>
              <td>{f.question}</td>
              <td>{f.answer}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}
