import React from 'react';
import { FaUserCircle } from 'react-icons/fa';
import { Link } from 'react-router-dom';
import logo from '../assets/AFK.png';

function Navbar() {
  return (
    <nav className="w-full bg-blue-800/90 text-white py-4 shadow-2xl flex justify-between items-center px-6">
      {/* Logo */}
      <div className="flex items-center space-x-2">
        <img src={logo} alt="AFK Guardian" className="h-10 w-10 object-contain" />
        <h1 className="text-xl font-semibold">AFK Guardian</h1>
      </div>

      {/* Navigation Links */}
      <div className="hidden md:flex space-x-6">
        <Link to="/" className="hover:underline hover:text-blue-500">Home</Link>
        <Link to="/employees" className="hover:underline">Employees</Link>
        <Link to="/reports" className="hover:underline">Reports</Link>
        <a href="#" className="hover:underline">Settings</a>
      </div>

      {/* User Profile */}
      <div className="flex items-center space-x-2 cursor-pointer">
        <FaUserCircle className="text-2xl" />
        <span className="text-sm">Admin</span>
      </div>
    </nav>
  );
}

export default Navbar;
