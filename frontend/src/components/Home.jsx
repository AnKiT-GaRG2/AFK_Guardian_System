

// import { useRouter } from 'next/navigation';
import { FaHome, FaUsers, FaChartBar, FaCog, FaSignOutAlt, FaPlus, FaTasks, FaFileAlt, FaUserCircle } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';

const employees = [
  { id: 1, name: 'Rohan Sharma', role: 'Software Engineer' },
  { id: 2, name: 'Ananya Verma', role: 'UI/UX Designer' },
  { id: 3, name: 'Karan Mehta', role: 'Data Analyst' },
];

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex bg-gray-200">
      {/* Sidebar */}
      <aside className="w-72 bg-blue-800 text-white min-h-screen p-6 flex flex-col justify-between">
        <div>
          <h2 className="text-2xl font-bold mb-6 text-center">Dashboard</h2>
          <nav>
            <ul className="space-y-4">
              <li className="flex items-center space-x-3 p-3 rounded-lg hover:bg-blue-700 transition cursor-pointer" onClick={() => router.push('/')}> 
                <FaHome className="text-lg" />
                <span>Home</span>
              </li>
              <li className="flex items-center space-x-3 p-3 rounded-lg hover:bg-blue-700 transition cursor-pointer" onClick={() => router.push('/employees')}>
                <FaUsers className="text-lg" />
                <span>Employees</span>
              </li>
              <li className="flex items-center space-x-3 p-3 rounded-lg hover:bg-blue-700 transition cursor-pointer" onClick={() => router.push('/reports')}>
                <FaChartBar className="text-lg" />
                <span>Reports</span>
              </li>
              <li className="flex items-center space-x-3 p-3 rounded-lg hover:bg-blue-700 transition cursor-pointer" onClick={() => router.push('/settings')}>
                <FaCog className="text-lg" />
                <span>Settings</span>
              </li>
            </ul>
          </nav>

          {/* Quick Actions */}
          <div className="mt-10">
            <h3 className="text-lg font-semibold mb-3">Quick Actions</h3>
            <ul className="space-y-4">
              <li className="flex items-center space-x-3 p-3 rounded-lg bg-blue-700 hover:bg-blue-600 transition cursor-pointer">
                <FaPlus className="text-lg" />
                <span>Add New Employee</span>
              </li>
              <li className="flex items-center space-x-3 p-3 rounded-lg bg-blue-700 hover:bg-blue-600 transition cursor-pointer">
                <FaTasks className="text-lg" />
                <span>Manage Tasks</span>
              </li>
              <li className="flex items-center space-x-3 p-3 rounded-lg bg-blue-700 hover:bg-blue-600 transition cursor-pointer">
                <FaFileAlt className="text-lg" />
                <span>Generate Report</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Logout Option */}
        <div className="flex items-center space-x-3 p-3 rounded-lg hover:bg-red-600 transition cursor-pointer" onClick={() => alert('Logging out...')}>
          <FaSignOutAlt className="text-lg" />
          <span>Logout</span>
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col ">
      <nav className="w-full bg-blue-800 text-white py-4 px-6 flex justify-between items-center shadow-lg">
          <h1 className="text-xl font-semibold">Employee Dashboard</h1>
          <div className="flex items-center space-x-2 cursor-pointer">
            <FaUserCircle className="text-2xl" />
            <span className="text-sm">John Doe</span>
          </div>
        </nav>
        {/* Page Title */}
        <div className="text-center mt-6">
          <h1 className="text-4xl font-bold text-gray-800">Welcome to Employee Dashboard</h1>
          <p className="text-gray-600 text-lg mt-2">Manage your team efficiently</p>
        </div>

        {/* Employee List */}
        <div className="w-full max-w-6xl mx-auto bg-white shadow-lg rounded-lg p-8 mt-8">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-semibold text-gray-800">Employee List</h2>
            <button className="bg-blue-600 text-white px-5 py-2 rounded-lg hover:bg-blue-700 transition">
              + Add Employee
            </button>
          </div>

          {/* Employee Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {employees.map((employee) => (
              <div key={employee.id} className="bg-gray-100 hover:bg-gray-200 p-6 rounded-lg shadow-lg cursor-pointer transition flex flex-col items-center text-center">
                {/* Employee Avatar */}
                <div className="w-24 h-24 bg-blue-500 text-white flex items-center justify-center rounded-full text-3xl font-semibold">
                  {employee.name.charAt(0)}
                </div>

                {/* Employee Info */}
                <h3 className="text-xl font-medium text-gray-700 mt-4">{employee.name}</h3>
                <p className="text-sm text-gray-500">{employee.role}</p>

                {/* View Profile Button */}
                <button className="mt-4 bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition cursor-pointer" onClick={() => navigate(`/employee/${employee.id}`)}>
                  View Profile
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
