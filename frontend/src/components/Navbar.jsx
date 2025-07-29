import React from 'react';
import { FaUserCircle } from 'react-icons/fa';

function Navbar() {
  return (
    <nav className="w-full bg-blue-800/90 text-white py-4 shadow-2xl flex justify-between items-center px-6">
      {/* Logo */}
      <div className="flex items-center space-x-2">
        {/* <img src="/logo.png" alt="Company Logo" className="h-10 w-10" /> */}
        <h1 className="text-xl font-semibold">Employee Dashboard</h1>
      </div>

      {/* Navigation Links */}
      <div className="hidden md:flex space-x-6">
        <a href="/" className="hover:underline hover:text-blue-500">Home</a>
        <a href="#" className="hover:underline">Analytics</a>
        <a href="#" className="hover:underline">Reports</a>
        <a href="#" className="hover:underline">Settings</a>
      </div>

      {/* User Profile */}
      <div className="flex items-center space-x-2 cursor-pointer">
        <FaUserCircle className="text-2xl" />
        <span className="text-sm">John Doe</span>
      </div>
    </nav>
  );
}

export default Navbar;
