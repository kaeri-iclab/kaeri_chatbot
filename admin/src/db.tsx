import { useCallback, useEffect, useState } from "react";

import axios, { AxiosError } from "axios";
import { ChevronLeft, ChevronRight, UploadIcon, XIcon } from "lucide-react";

import { getFileSizeString } from "./utils/file";

export default function DB() {
  const [files, setFiles] = useState<File[]>([]);
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);

  const [collection, setCollection] = useState<
    {
      id: string;
      title: string;
      content: string;
    }[]
  >([]);

  const fetchDB = useCallback(async () => {
    try {
      const res = await axios.get(
        `${import.meta.env.VITE_API_HOST}/db?page=${page}`
      );
      const data = res.data;
      setCollection(data.collection);
      setTotal(data.num);
    } catch (e) {
      if (e instanceof AxiosError)
        alert((e as AxiosError<{ detail: string }>).response?.data.detail);
    }
  }, [page]);

  const handleUploadFiles = useCallback(async () => {
    try {
      setLoading(true);
      const formData = new FormData();
      files.forEach((file) => {
        formData.append("files", file);
      });
      const res = await fetch(`${import.meta.env.VITE_API_HOST}/db/upload`, {
        method: "POST",
        body: formData,
      });

      if (res.ok) {
        setFiles([]);
        alert("파일이 업로드 되었습니다.");
      }
      setLoading(false);
      fetchDB();
    } catch (e) {
      if (e instanceof AxiosError)
        alert((e as AxiosError<{ detail: string }>).response?.data.detail);
      setLoading(false);
    }
  }, [files, fetchDB]);

  useEffect(() => {
    fetchDB();
  }, [fetchDB]);

  return (
    <main className="flex w-full flex-col p-24">
      <h1 className="title">DB 추가</h1>
      <label
        className="mt-2 flex h-32 w-full shrink-0 cursor-pointer appearance-none items-center justify-center rounded-md border-2 border-dashed border-gray-300 bg-white px-4 transition hover:border-primary hover:text-primary focus:outline-none"
        onDragOver={(e: React.DragEvent<HTMLLabelElement>) => {
          e.preventDefault();
        }}
        onDrop={(e: React.DragEvent<HTMLLabelElement>) => {
          e.preventDefault();
          if (e.dataTransfer.files) {
            setFiles((f) => [...f, ...e.dataTransfer.files]);
          }
        }}
      >
        <span className="text-center font-semibold">
          DB에 추가하실 PDF 파일을 업로드해주세요.
          <br />
          <small>* 원자력 관련 PDF 파일만 추가해주세요.</small>
        </span>
        <input
          type="file"
          name="file_upload"
          className="hidden"
          accept=".pdf"
          multiple
          onChange={(e) =>
            e.target.files && setFiles((f) => [...f, ...e.target.files!])
          }
        />
      </label>
      <div className="mt-2 h-36 shrink-0 overflow-y-auto">
        <table className="table table-pin-rows table-xs">
          <thead>
            <tr>
              <th>파일명</th>
              <th className="text-right">크기</th>
              <th className="text-center">삭제</th>
            </tr>
          </thead>
          <tbody>
            {files.map((file) => (
              <tr key={file.name}>
                <td>{file.name}</td>
                <td className="text-right">{getFileSizeString(file.size)}</td>
                <td className="text-center">
                  <button
                    className="btn btn-ghost btn-xs"
                    onClick={() =>
                      setFiles(files.filter((f) => f.name !== file.name))
                    }
                  >
                    <XIcon size={14} />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <button
        className="btn btn-primary mt-8 self-end"
        disabled={loading}
        onClick={handleUploadFiles}
      >
        {loading ? (
          <div className="loading loading-spinner loading-xs" />
        ) : (
          <UploadIcon size={16} />
        )}
        업로드
      </button>

      <div className="mt-16 flex items-center justify-between">
        <h1 className="title">DB 목록</h1>
        <div className="text-sm">총 {total}개</div>
      </div>

      <table className="table table-sm mt-2">
        <thead>
          <tr>
            <th>제목</th>
            <th>내용</th>
          </tr>
        </thead>

        <tbody>
          {collection.length > 0 ? (
            collection.map((item) => (
              <tr key={item.id}>
                <td className="w-80 font-semibold">
                  <div className="line-clamp-1">{item.title}</div>
                </td>
                <td>
                  <div className="line-clamp-1">{item.content}</div>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan={2} className="py-24 text-center">
                데이터가 없습니다.
              </td>
            </tr>
          )}
        </tbody>
      </table>
      <div className="join mt-4 self-center">
        <button
          className="btn join-item btn-sm"
          disabled={page === 1}
          onClick={() => setPage((p) => p - 1)}
        >
          <ChevronLeft size={14} />
        </button>
        <button className="btn join-item btn-sm">
          {page} of {Math.ceil(total / 20)}
        </button>
        <button
          className="btn join-item btn-sm"
          disabled={page >= Math.ceil(total / 20)}
          onClick={() => setPage((p) => p + 1)}
        >
          <ChevronRight size={14} />
        </button>
      </div>
    </main>
  );
}
