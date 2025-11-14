import Link from "next/link";

export default function HomePage() {
  return (
    <main className="p-6 space-y-3">
      <h1 className="text-2xl font-bold">AI Othello Dashboard</h1>
      <div className="space-y-2">
        <Link href="/play" className="text-blue-600 hover:underline block">
          Play (Human vs AI)
        </Link>
      </div>
    </main>
  );
}
