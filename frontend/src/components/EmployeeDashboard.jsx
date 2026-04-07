import { FaHome, FaUsers, FaChartBar, FaCog, FaSignOutAlt, FaPlus, FaTasks, FaFileAlt, FaUserCircle } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
import logo from '../assets/AFK.png';

const initialEmployees = [
  { id: 1, name: 'Rohan Sharma', role: 'Software Engineer' },
  { id: 2, name: 'Ananya Verma', role: 'UI/UX Designer' },
  { id: 3, name: 'Karan Mehta', role: 'Data Analyst' },
];

export default function EmployeeDashboard() {
  const navigate = useNavigate();
  const [employees, setEmployees] = useState(initialEmployees);
  const [showAddForm, setShowAddForm] = useState(false);
  const [newEmployee, setNewEmployee] = useState({
    name: '',
    role: '',
    email: '',
  });

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setNewEmployee((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  const handleAddEmployee = (event) => {
    event.preventDefault();

    const nextId = employees.length > 0 ? Math.max(...employees.map((employee) => employee.id)) + 1 : 1;
    const employeeToAdd = {
      id: nextId,
      name: newEmployee.name.trim(),
      role: newEmployee.role.trim(),
      email: newEmployee.email.trim(),
    };

    setEmployees((previous) => [...previous, employeeToAdd]);
    setNewEmployee({ name: '', role: '', email: '' });
    setShowAddForm(false);
  };

  return (
    <div className="min-h-screen flex bg-gray-200">
      <aside className="w-72 bg-blue-800 text-white min-h-screen p-6 flex flex-col justify-between">
        <div>
          <div className="flex flex-col items-center mb-6">
            <img src={logo} alt="AFK Guardian" className="h-20 w-20 object-contain mb-2" />
            <h2 className="text-2xl font-bold text-center">AFK Guardian</h2>
          </div>
          <nav>
            <ul className="space-y-4">
              <li className="flex items-center space-x-3 p-3 rounded-lg hover:bg-blue-700 transition cursor-pointer" onClick={() => navigate('/')}>
                <FaHome className="text-lg" />
                <span>Home</span>
              </li>
              <li className="flex items-center space-x-3 p-3 rounded-lg hover:bg-blue-700 transition cursor-pointer" onClick={() => navigate('/dashboard')}>
                <FaUsers className="text-lg" />
                <span>Employees</span>
              </li>
              <li className="flex items-center space-x-3 p-3 rounded-lg hover:bg-blue-700 transition cursor-pointer" onClick={() => navigate('/dashboard')}>
                <FaChartBar className="text-lg" />
                <span>Reports</span>
              </li>
              <li className="flex items-center space-x-3 p-3 rounded-lg hover:bg-blue-700 transition cursor-pointer" onClick={() => navigate('/settings')}>
                <FaCog className="text-lg" />
                <span>Settings</span>
              </li>
            </ul>
          </nav>

          <div className="mt-10">
            <h3 className="text-lg font-semibold mb-3">Quick Actions</h3>
            <ul className="space-y-4">
              <li className="flex items-center space-x-3 p-3 rounded-lg bg-blue-700 hover:bg-blue-600 transition cursor-pointer" onClick={() => setShowAddForm(true)}>
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

        <div className="flex items-center space-x-3 p-3 rounded-lg hover:bg-red-600 transition cursor-pointer" onClick={() => alert('Logging out...')}>
          <FaSignOutAlt className="text-lg" />
          <span>Logout</span>
        </div>
      </aside>

      <div className="flex-1 flex flex-col ">
        <nav className="w-full bg-blue-800 text-white py-4 px-6 flex justify-between items-center shadow-lg">
          <div className="flex items-center space-x-2">
            <img src={logo} alt="AFK Guardian" className="h-10 w-10 object-contain" />
            <h1 className="text-xl font-semibold">AFK Guardian</h1>
          </div>
          <div className="flex items-center space-x-2 cursor-pointer">
            <FaUserCircle className="text-2xl" />
            <span className="text-sm">Admin</span>
          </div>
        </nav>

        <div className="text-center mt-6">
          <h1 className="text-4xl font-bold text-gray-800">Welcome to Employee Dashboard</h1>
          <p className="text-gray-600 text-lg mt-2">Manage your team efficiently</p>
        </div>

        <div className="w-full max-w-6xl mx-auto bg-white shadow-lg rounded-lg p-8 mt-8">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-semibold text-gray-800">Employee List</h2>
            <button className="bg-blue-600 text-white px-5 py-2 rounded-lg hover:bg-blue-700 transition" onClick={() => setShowAddForm(true)}>
              + Add Employee
            </button>
          </div>

          {showAddForm && (
            <form onSubmit={handleAddEmployee} className="bg-gray-100 rounded-lg p-6 mb-8">
              <h3 className="text-xl font-semibold text-gray-800 mb-4">Add New Employee</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <input
                  type="text"
                  name="name"
                  value={newEmployee.name}
                  onChange={handleInputChange}
                  placeholder="Employee Name"
                  className="bg-white border border-gray-300 rounded-lg px-4 py-2"
                  required
                />
                <input
                  type="text"
                  name="role"
                  value={newEmployee.role}
                  onChange={handleInputChange}
                  placeholder="Role"
                  className="bg-white border border-gray-300 rounded-lg px-4 py-2"
                  required
                />
                <input
                  type="email"
                  name="email"
                  value={newEmployee.email}
                  onChange={handleInputChange}
                  placeholder="Email"
                  className="bg-white border border-gray-300 rounded-lg px-4 py-2"
                  required
                />
              </div>
              <div className="flex gap-3 mt-4">
                <button type="submit" className="bg-blue-600 text-white px-5 py-2 rounded-lg hover:bg-blue-700 transition">
                  Save Employee
                </button>
                <button type="button" onClick={() => setShowAddForm(false)} className="bg-gray-300 text-gray-800 px-5 py-2 rounded-lg hover:bg-gray-400 transition">
                  Cancel
                </button>
              </div>
            </form>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {employees.map((employee) => (
              <div key={employee.id} className="bg-gray-100 hover:bg-gray-200 p-6 rounded-lg shadow-lg cursor-pointer transition flex flex-col items-center text-center">
                <div className="w-24 h-24 bg-blue-500 text-white flex items-center justify-center rounded-full text-3xl font-semibold">
                  {employee.name.charAt(0)}
                </div>

                <h3 className="text-xl font-medium text-gray-700 mt-4">{employee.name}</h3>
                <p className="text-sm text-gray-500">{employee.role}</p>
                <p className="text-sm text-gray-500">{employee.email || 'no-email@company.com'}</p>

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
