import Card from "../ui/Card";
export default function TerraformCard({
  terraform,
}) {
  return (
    <Card title="☁️ Terraform">
        <div className="grid gap-8 lg:grid-cols-2">
        {/* Providers */}

        <div>
            <h3 className="mb-4 text-lg font-semibold">
            Providers
            </h3>

            <div className="flex flex-wrap gap-2">
            {terraform.providers.map((provider) => (
                <span
                key={provider}
                className="rounded-full bg-emerald-100 px-3 py-1 text-sm font-medium text-emerald-700 dark:bg-emerald-900 dark:text-emerald-200"
                >
                {provider}
                </span>
            ))}
            </div>
        </div>

        {/* Modules */}

        <div>
            <h3 className="mb-4 text-lg font-semibold">
            Modules
            </h3>

            <div className="flex flex-wrap gap-2">
            {terraform.modules.map((module) => (
                <span
                key={module}
                className="rounded-full bg-cyan-100 px-3 py-1 text-sm font-medium text-cyan-700 dark:bg-cyan-900 dark:text-cyan-200"
                >
                📦 {module}
                </span>
            ))}
            </div>
        </div>
        </div>
    </Card>
    );
}