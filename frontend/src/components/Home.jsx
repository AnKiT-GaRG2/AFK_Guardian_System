
import { FaChartBar, FaUsers } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import Navbar from './Navbar';

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gray-200">
      <Navbar />

      <main className="w-full max-w-6xl mx-auto px-6 py-10">
        <section className="bg-white shadow-lg rounded-lg p-8 md:p-12">
          <h1 className="text-4xl font-bold text-gray-800">AFK Guardian System</h1>
          <p className="text-gray-600 text-lg mt-4 leading-relaxed">
            AFK Guardian helps organizations monitor work activity in real time by collecting
            window usage, keyboard and mouse interaction, speaking status, and eye-state trends.
            It gives admins a clear view of focus patterns and employee productivity.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
            <div className="bg-gray-100 rounded-lg p-6">
              <h2 className="text-2xl font-semibold text-gray-800">What This Project Does</h2>
              <ul className="mt-3 text-gray-600 space-y-2">
                <li>Tracks active application usage over time</li>
                <li>Captures keyboard and mouse engagement signals</li>
                <li>Monitors eye-open, eye-closed, and away durations</li>
                <li>Streams data for admin dashboards and reports</li>
              </ul>
            </div>

            <div className="bg-gray-100 rounded-lg p-6">
              <h2 className="text-2xl font-semibold text-gray-800">Admin Navigation</h2>
              <p className="mt-3 text-gray-600">
                Use Employees or Reports to open the employee dashboard and inspect detailed metrics.
              </p>
              <div className="flex flex-wrap gap-4 mt-6">
                <button
                  onClick={() => navigate('/employees')}
                  className="bg-blue-600 text-white px-5 py-2 rounded-lg hover:bg-blue-700 transition flex items-center gap-2"
                >
                  <FaUsers />
                  Employees
                </button>
                <button
                  onClick={() => navigate('/reports')}
                  className="bg-blue-600 text-white px-5 py-2 rounded-lg hover:bg-blue-700 transition flex items-center gap-2"
                >
                  <FaChartBar />
                  Reports
                </button>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
