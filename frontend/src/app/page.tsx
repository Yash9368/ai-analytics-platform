export default function Home() {
  return (
    <main className="min-h-screen bg-gray-100 p-10">

      <h1 className="text-4xl font-bold mb-8">
        AI Analytics Dashboard
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

        <div className="bg-white p-6 rounded-xl shadow">
          <h2 className="text-xl font-semibold">
            Users
          </h2>

          <p className="text-3xl mt-4">
            0
          </p>
        </div>

        <div className="bg-white p-6 rounded-xl shadow">
          <h2 className="text-xl font-semibold">
            Sessions
          </h2>

          <p className="text-3xl mt-4">
            0
          </p>
        </div>

        <div className="bg-white p-6 rounded-xl shadow">
          <h2 className="text-xl font-semibold">
            Bounce Rate
          </h2>

          <p className="text-3xl mt-4">
            0%
          </p>
        </div>

      </div>

    </main>
  );
}