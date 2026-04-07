import './App.css'
import Home from './components/Home'
import EmployeeDetail from './components/EmployeeDetail'
import EmployeeDashboard from './components/EmployeeDashboard'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<EmployeeDashboard />} />
        <Route path="/employees" element={<EmployeeDashboard />} />
        <Route path="/reports" element={<EmployeeDashboard />} />
        <Route path="/employee/:id" element={<EmployeeDetail />} />
      </Routes>
    </Router>
  )
}

export default App
