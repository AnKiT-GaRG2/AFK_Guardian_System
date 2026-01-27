import { useParams } from 'react-router-dom';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer, Legend } from 'recharts';
import Navbar from './Navbar';
import axios from 'axios';
import { useEffect, useState } from 'react';

const employees = [
  { id: 1, name: 'Rohan Sharma', role: 'Software Engineer', status: 'Active' },
  { id: 2, name: 'Ananya Verma', role: 'UI/UX Designer', status: 'Away' },
  { id: 3, name: 'Karan Mehta', role: 'Data Analyst', status: 'Distracted' },
];

const COLORS = ['#4CAF50', '#F44336'];

const calculateProductivity = (activitySummary) => {
  const NOT_SPEAKING = activitySummary['NOT SPEAKING'] || 0;
  const SPEAKING = activitySummary['SPEAKING'] || 0;
  const eyes_open_time = activitySummary['eyes_open_time'] || 0;
  const eyes_closed_time = activitySummary['eyes_closed_time'] || 0;
  const eyes_not_detected_time = activitySummary['eyes_not_detected_time'] || 0;
  
  const total = SPEAKING + NOT_SPEAKING + eyes_open_time + eyes_closed_time + eyes_not_detected_time;
  if (total === 0) return 0;
  
  const x = (NOT_SPEAKING + eyes_open_time) / total * 100;
  console.log('Productivity:', x);
  return x;
};

export default function EmployeeDetail() {
  const { id } = useParams();
  const [data, setData] = useState(null);
  const [productivityGraphData, setProductivityGraphData] = useState([]);
  const [windowMouseData, setWindowMouseData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(`http://localhost:5000/employee/${id}`);
        setData(response.data);

        const activityData = response.data?.data;
      
        if (activityData) {
          const graphData = Object.entries(activityData).map(([date, details]) => ({
            date,
            productivity: calculateProductivity(details.activity_summary),
            
          }));
          setProductivityGraphData(graphData);

          const mouseWindowData = Object.entries(activityData).flatMap(([date, details]) =>
            Object.entries(details.window_activity).map(([window, activity]) => ({
              date,
              window,
              keyboardActivity: activity.activities.keyboard_activity.count,
              mouseClicks: activity.activities.mouse_clicks.count,
              mouseMovements: activity.activities.mouse_movement_distance.count,
              mouseScrolls: activity.activities.mouse_scrolls.count,
            }))
          );
          setWindowMouseData(mouseWindowData);
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };
    
    fetchData();
    const interval = setInterval(fetchData, 10000); // Fetch data every 10 seconds
    return () => clearInterval(interval);
  }, [id]);

  const employee = employees.find(emp => emp.id === parseInt(id));

  if (!employee) {
    return <div className="text-center text-red-500 mt-10">Employee not found</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="w-full max-w-6xl mx-auto bg-white shadow-lg rounded-lg p-6 mt-6">
        
        {/* Employee Details */}
        <div className="flex items-center space-x-6 p-6 bg-gray-100 rounded-lg">
          <div className="w-24 h-24 bg-blue-500 text-white flex items-center justify-center rounded-full text-3xl font-semibold">
            {employee.name.charAt(0)}
          </div>
          <div className="flex-1">
            <h2 className="text-3xl font-semibold text-gray-800">{employee.name}</h2>
            <p className="text-lg text-gray-500">{employee.role}</p>
            <p className={`text-sm mt-2 font-medium ${
              employee.status === 'Active' ? 'text-green-500' : 
              employee.status === 'Away' ? 'text-yellow-500' : 'text-red-500'
            }`}>
              Status: {employee.status}
            </p>
          </div>
        </div>

        {/* Window and Mouse Activities */}
        {windowMouseData.length > 0 && (
          <div className="w-full bg-gray-100 p-4 rounded-lg my-6">
            <h3 className="text-lg font-medium text-gray-700 mb-2">Window and Mouse Activities</h3>
            {windowMouseData.map((entry, index) => (
              <div key={index} className="mb-4">
                <p><strong>Date:</strong> {entry.date}</p>
                <p><strong>Window:</strong> {entry.window}</p>
                <p><strong>Keyboard Activity:</strong> {entry.keyboardActivity}</p>
                <p><strong>Mouse Clicks:</strong> {entry.mouseClicks}</p>
                <p><strong>Mouse Movements:</strong> {entry.mouseMovements}</p>
                <p><strong>Mouse Scrolls:</strong> {entry.mouseScrolls}</p>
              </div>
            ))}
          </div>
        )}

        {/* Productivity Graph */}
        <div className="bg-gray-100 p-4 rounded-lg">
          <h3 className="text-lg font-medium text-gray-700 mb-4">Productivity Over Time</h3>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={productivityGraphData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="productivity" stroke="#4CAF50" name="Productivity (%)" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Bar and Pie Charts */}
        <div className="grid grid-cols-2 gap-4 mt-6">
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={windowMouseData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="window" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="mouseClicks" fill="#8884d8" name="Mouse Clicks" />
              <Bar dataKey="keyboardActivity" fill="#82ca9d" name="Keyboard Activity" />
            </BarChart>
          </ResponsiveContainer>
          <div className="flex flex-col items-center">
  {/* Scrollable Legend Container */}
  <div className="h-40 overflow-y-auto border border-gray-300 rounded-lg p-2 w-72 bg-white shadow-md">
    <h3 className="text-center text-sm font-semibold mb-2">Mouse Clicks per Window</h3>
    <ul>
      {windowMouseData.map((entry, index) => (
        <li key={index} className="text-sm text-gray-700 flex items-center">
          <span 
            className="inline-block w-4 h-4 mr-2 rounded-full" 
            style={{ backgroundColor: COLORS[index % COLORS.length] }}
          ></span>
          {entry.window}
        </li>
      ))}
    </ul>
  </div>

  {/* Pie Chart Without Labels */}
  <ResponsiveContainer width={300} height={250}>
    <PieChart>
      <Pie 
        data={windowMouseData} 
        dataKey="mouseClicks" 
        nameKey="window" 
        cx="50%" 
        cy="50%" 
        outerRadius={90} 
        innerRadius={40}
        fill="#8884d8"
      >
        {windowMouseData.map((entry, index) => (
          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
        ))}
      </Pie>
      <Tooltip />
    </PieChart>
  </ResponsiveContainer>
</div>


        </div>
      </div>
    </div>
  );
}
