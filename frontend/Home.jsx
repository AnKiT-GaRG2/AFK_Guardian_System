import React from 'react';
// import { useNavigate } from 'react-router-dom';

const Home = ({ employees }) => {
  // const navigate = useNavigate();
  
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      {/* Navbar */}
      <nav className="bg-blue-600 text-white shadow-lg">
        <div className="container mx-auto px-6 py-3 flex justify-between items-center">
          <div className="flex items-center">
            <span className="text-xl font-bold">EmpTrack</span>
          </div>
          <div className="flex items-center space-x-4">
            <a href="/" className="hover:text-blue-200 transition">Dashboard</a>
            <a href="/reports" className="hover:text-blue-200 transition">Reports</a>
            <a href="/settings" className="hover:text-blue-200 transition">Settings</a>
            <div className="ml-4 relative">
              <button className="flex items-center focus:outline-none">
                <div className="w-8 h-8 rounded-full bg-white flex items-center justify-center">
                  <span className="text-blue-700 font-bold">JD</span>
                </div>
              </button>
            </div>
          </div>
        </div>
      </nav>
      
      {/* Main Content */}
      <div className="container mx-auto px-6 py-8">
        <h1 className="text-3xl font-semibold text-gray-800 mb-6">Employee Productivity Dashboard</h1>
        
        {/* Employee Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {employees.map((employee) => (
            <div 
              key={employee.id}
              className="bg-white rounded-lg shadow-md hover:shadow-lg transition cursor-pointer"
              // onClick={() => navigate(`/employee/${employee.id}`)}
            >
              <div className="p-5 border-b border-gray-200">
                <div className="flex items-center justify-between">
                  <div>
                    <h2 className="text-lg font-medium text-gray-700">{employee.name}</h2>
                    <p className="text-sm text-gray-500">{employee.role}</p>
                  </div>
                  <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center">
                    <span className="text-blue-600 font-bold">
                      {employee.name.split(' ').map(n => n[0]).join('')}
                    </span>
                  </div>
                </div>
              </div>
              
              <div className="p-5">
                <div className="flex justify-between items-center mb-3">
                  <span className="text-sm font-medium text-gray-600">Productivity</span>
                  <span className="text-sm font-medium text-blue-600">
                    {employee.productivity || '85%'}
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-blue-600 h-2 rounded-full" 
                    style={{ width: employee.productivity || '85%' }}
                  ></div>
                </div>
              </div>
              
              <div className="px-5 py-3 bg-gray-50 flex justify-between items-center rounded-b-lg">
                <span className="text-sm text-gray-500">
                  Last active: {employee.lastActive || 'Today'}
                </span>
                <span className="text-blue-600">→</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Home;