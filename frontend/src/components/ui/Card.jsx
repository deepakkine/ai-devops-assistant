export default function Card({ title, children, className = "" }) {
  return (
    <div
      className={`rounded-xl border border-slate-200 bg-white p-6 shadow dark:border-slate-700 dark:bg-slate-800 ${className}`}
    >
      {title && (
        <h2 className="mb-6 text-2xl font-bold">
          {title}
        </h2>
      )}

      {children}
    </div>
  );
}