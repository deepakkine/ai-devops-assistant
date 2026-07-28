import Card from "../ui/Card";
function Badge({ children, color }) {
  return (
    <span
      className={`rounded-full px-3 py-1 text-sm font-medium ${color}`}
    >
      {children}
    </span>
  );
}

export default function TechnologyCard({
  technologies,
}) {
  const sections = [
    {
      title: "Frontend",
      icon: "🖥️",
      color:
        "bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-200",
      items: technologies.frontend,
    },
    {
      title: "Backend",
      icon: "⚙️",
      color:
        "bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-200",
      items: technologies.backend,
    },
    {
      title: "Infrastructure",
      icon: "☁️",
      color:
        "bg-purple-100 text-purple-700 dark:bg-purple-900 dark:text-purple-200",
      items: technologies.infrastructure,
    },
  ];

  return (
    <Card title="🛠 Technology Stack">
        <div className="space-y-6">
        {sections.map((section) => (
            <div key={section.title}>
            <h3 className="mb-3 text-lg font-semibold">
                {section.icon} {section.title}
            </h3>

            <div className="flex flex-wrap gap-2">
                {section.items.map((item) => (
                <Badge
                    key={item}
                    color={section.color}
                >
                    {item}
                </Badge>
                ))}
            </div>
            </div>
        ))}
        </div>
    </Card>
    );
}