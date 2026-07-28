import {
  FileText,
  Folder,
  Code2,
  Cloud,
} from "lucide-react";

export default function StatisticsCards({ stats, terraform }) {
  const cards = [
    {
        label: "Files",
        value: stats.total_files,
        icon: FileText,
        iconColor: "text-blue-600 dark:text-blue-400",
        bgColor: "bg-blue-100 dark:bg-blue-900/30",
    },
    {
        label: "Directories",
        value: stats.total_directories,
        icon: Folder,
        iconColor: "text-amber-600 dark:text-amber-400",
        bgColor: "bg-amber-100 dark:bg-amber-900/30",
    },
    {
        label: "Languages",
        value: stats.languages,
        icon: Code2,
        iconColor: "text-emerald-600 dark:text-emerald-400",
        bgColor: "bg-emerald-100 dark:bg-emerald-900/30",
    },
    {
        label: "Terraform Files",
        value: terraform.files,
        icon: Cloud,
        iconColor: "text-purple-600 dark:text-purple-400",
        bgColor: "bg-purple-100 dark:bg-purple-900/30",
    },
    ];

  return (
    <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      {cards.map((card) => {
        const Icon = card.icon;

        return (
          <div
            key={card.label}
            className="group rounded-xl border border-slate-700 bg-slate-800 p-5 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-xl hover:border-cyan-500/50"
          >
            <div
            className={`inline-flex h-12 w-12 items-center justify-center rounded-lg ${card.bgColor}`}
            >
            <Icon className={`h-6 w-6 ${card.iconColor}`} />
            </div>

            <div className="mt-3 text-3xl font-bold">
              {card.value}
            </div>

            <div className="mt-1 text-sm text-slate-400">
              {card.label}
            </div>
          </div>
        );
      })}
    </div>
  );
}