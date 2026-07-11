import { PageHeader } from "@/components/layout/PageHeader";
import { ChatInterface } from "@/components/copilot/ChatInterface";

export default function CopilotPage() {
    return (
        <>
            <PageHeader title="AI Investigation Copilot" subtitle="Natural-language queries over the fraud platform" />
            <ChatInterface />
        </>
    );
}
