import Card from "../ui/Card";
import { Package } from "lucide-react";

export default function RepositoryHeader({ facts }) {
  return (
    <Card>
      <div className="flex items-center justify-between">
        <div>
          <h1 className="flex items-center gap-3 text-3xl font-bold">
            <Package className="h-8 w-8 text-cyan-500" />

            <span>{facts.name}</span>
          </h1>

          <p className="mt-2 text-slate-500 dark:text-slate-400">
            AI-generated repository analysis
          </p>

          <div className="mt-4 flex flex-wrap gap-2">
            {[
                 ...new Set([
                ...facts.technologies.frontend,
                ...facts.technologies.backend,
                ...facts.technologies.infrastructure,
                ])
            ].map((tech) => (
                <span
                key={tech}
                className="rounded-full bg-blue-100 px-3 py-1 text-xs font-medium text-blue-700 dark:bg-blue-900 dark:text-blue-200"
                >
                {tech}
                </span>
            ))}
            </div>

          <div className="mt-4 flex flex-wrap gap-3 text-sm">
            <span className="rounded-full bg-slate-100 px-3 py-1 dark:bg-slate-700">
                📄 {facts.stats.total_files} Files
            </span>

            <span className="rounded-full bg-slate-100 px-3 py-1 dark:bg-slate-700">
                📁 {facts.stats.total_directories} Directories
            </span>

            <span className="rounded-full bg-slate-100 px-3 py-1 dark:bg-slate-700">
                💻 {facts.stats.languages} Languages
            </span>

            <span className="rounded-full bg-slate-100 px-3 py-1 dark:bg-slate-700">
                ☁️ {facts.terraform.files} Terraform Files
            </span>
            </div>
        </div>

        <div className="hidden md:block">
          <span className="rounded-full bg-emerald-100 px-4 py-2 text-sm font-medium text-emerald-700 dark:bg-emerald-900 dark:text-emerald-200">
            Repository Scan
          </span>
        </div>
      </div>
    </Card>
  );
}