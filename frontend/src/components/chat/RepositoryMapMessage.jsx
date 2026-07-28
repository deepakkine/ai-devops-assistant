import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import Card from "../ui/Card";
import StatisticsCards from "../repository/StatisticsCards";
import LanguagesCard from "../repository/LanguagesCard";
import TechnologyCard from "../repository/TechnologyCard";
import TerraformCard from "../repository/TerraformCard";
import RepositoryHeader from "../repository/RepositoryHeader";

export default function RepositoryMapMessage({
  facts,
  summary,
}) {
  return (
    <div className="space-y-6">

        <RepositoryHeader facts={facts} />

        <Card title="📦 Repository Overview">
            <StatisticsCards
                stats={facts.stats}
                terraform={facts.terraform}
            />
            </Card>

        <div className="grid gap-6 xl:grid-cols-2">
            <LanguagesCard
            languages={facts.languages}
            />

            <TechnologyCard
            technologies={facts.technologies}
            />
        </div>

        <div className="grid gap-6 xl:grid-cols-2">
            <TerraformCard
            terraform={facts.terraform}
            />

            <Card title="📝 Repository Summary">
                <div className="markdown-content text-base leading-7">
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {summary}
                    </ReactMarkdown>
                </div>
                </Card>
        </div>

        </div>
  );
}