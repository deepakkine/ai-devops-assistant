import Card from "../ui/Card";

export default function LanguagesCard({ languages }) {
  const entries = Object.entries(languages ?? {});

  const total = entries.reduce(
    (sum, [, count]) => sum + count,
    0
  );

  return (
    <Card title="💻 Languages">
      <div className="space-y-4">
        {entries
          .sort((a, b) => b[1] - a[1])
          .map(([language, count]) => {
            const percent =
              total > 0
                ? ((count / total) * 100).toFixed(1)
                : "0.0";

            return (
              <div key={language}>
                <div className="mb-2 flex justify-between">
                  <span className="font-medium">
                    {language}
                  </span>

                  <span className="text-slate-500">
                    {count} files ({percent}%)
                  </span>
                </div>

                <div className="h-3 rounded-full bg-slate-200 dark:bg-slate-700">
                  <div
                    className="h-3 rounded-full bg-cyan-500 transition-all duration-500"
                    style={{
                      width: `${percent}%`,
                    }}
                  />
                </div>
              </div>
            );
          })}
      </div>
    </Card>
  );
}