import {useEffect,useState} from 'react';
import {Routes,Route,Link,useNavigate,useLocation} from 'react-router-dom';
import {Activity,Camera,Map,BarChart3,Bell,Settings,Users,LogOut,LayoutDashboard} from 'lucide-react';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import Cameras from './pages/Cameras';
import Zones from './pages/Zones';
import Analytics from './pages/Analytics';
const nav=[['Dashboard','/',LayoutDashboard],['Monitoring','/cameras',Camera],['Zones','/zones',Map],['Analytics','/analytics',BarChart3],['Alerts','/alerts',Bell],['Settings','/settings',Settings]];
export default function App(){const [auth,setAuth]=useState(()=>!!localStorage.getItem('cc_token'));const navigate=useNavigate();const location=useLocation();
 useEffect(()=>{if(!auth&&location.pathname!='/login')navigate('/login')},[auth]);
 if(!auth)return <Routes><Route path='*' element={<Login onLogin={()=>setAuth(true)}/>}/></Routes>;
 return <div className="app"><aside><div className="brand"><div className="brandMark"><Users/></div><div><b>CrowdCount</b><span>Security Analytics</span></div></div><nav>{nav.map(([label,path,Icon])=>{const active=location.pathname===path;return <Link key={String(path)} className={active?'active':''} to={String(path)}><Icon size={18}/>{String(label)}</Link>})}</nav><button className="logout" onClick={()=>{localStorage.removeItem('cc_token');setAuth(false)}}><LogOut size={18}/> Sign out</button></aside><main><Routes><Route path='/' element={<Dashboard/>}/><Route path='/cameras' element={<Cameras/>}/><Route path='/zones' element={<Zones/>}/><Route path='/analytics' element={<Analytics/>}/><Route path='/alerts' element={<Dashboard alertsOnly/>}/><Route path='/settings' element={<Dashboard settings/>}/></Routes></main></div>
}
