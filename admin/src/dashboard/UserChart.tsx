import { ResponsiveLine, Serie } from "@nivo/line";

export default function UserChart({ data }: { data: Serie[] }) {
  return (
    <div className="h-96 w-full">
      <ResponsiveLine
        data={data}
        colors={() => "#0c519e"}
        axisBottom={{
          tickSize: 5,
          tickPadding: 5,
          tickRotation: 0,
          legend: "날짜",
          legendPosition: "middle",
          legendOffset: 32,
          truncateTickAt: 0,
        }}
        axisLeft={{
          tickSize: 5,
          tickPadding: 5,
          tickRotation: 0,
          legend: "채팅 수",
          legendPosition: "middle",
          legendOffset: -40,
          truncateTickAt: 0,
        }}
        margin={{ top: 40, right: 100, bottom: 40, left: 60 }}
        axisRight={null}
      />
    </div>
  );
}
