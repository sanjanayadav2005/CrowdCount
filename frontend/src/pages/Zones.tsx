import { useEffect, useState } from 'react';
import { api } from '../services/api';
import { Trash2, Plus } from 'lucide-react';

export default function Zones() {
  const [cameras, setCameras] = useState<any[]>([]);
  const [zones, setZones] = useState<any[]>([]);
  const [camera, setCamera] = useState(1);
  const [name, setName] = useState('Zone 1');
  const [threshold, setThreshold] = useState(10);

  const load = () => api('/zones').then(setZones).catch(() => {});

  useEffect(() => {
    load();
    api('/cameras').then((data: any[]) => {
      setCameras(data);
      if (data[0]) setCamera(data[0].id);
    }).catch(() => {});
  }, []);

  async function add() {
    await api('/zones', {
      method: 'POST',
      body: JSON.stringify({
        camera_id: camera,
        name,
        threshold,
        coordinates: [[100, 100], [400, 100], [400, 400], [100, 400]],
      }),
    });
    load();
  }

  async function remove(id: number) {
    await api(`/zones/${id}`, { method: 'DELETE' });
    load();
  }

  return (
    <section>
      <header>
        <div><h1>Zone configuration</h1><p>Polygon regions and overcrowding thresholds</p></div>
      </header>
      <div className="zoneEditor">
        <div className="editorCanvas">
          <div className="zonePolygon"><span>Zone preview</span></div>
          <p>Normalized coordinates are stored per camera.</p>
        </div>
        <div className="panel zoneForm">
          <h3>Create zone</h3>
          <label>Camera</label>
          <select value={camera} onChange={e => setCamera(+e.target.value)}>
            {cameras.map(c => <option value={c.id} key={c.id}>{c.name}</option>)}
          </select>
          <label>Zone name</label>
          <input value={name} onChange={e => setName(e.target.value)} />
          <label>Maximum occupancy</label>
          <input type="number" value={threshold} onChange={e => setThreshold(+e.target.value)} />
          <button className="primary" onClick={add}><Plus size={16} /> Create zone</button>
        </div>
      </div>
      <div className="tableCard">
        <table>
          <thead><tr><th>Zone</th><th>Camera</th><th>Threshold</th><th>Action</th></tr></thead>
          <tbody>
            {zones.map(z => (
              <tr key={z.id}><td>{z.name}</td><td>{z.camera_id}</td><td>{z.threshold}</td>
                <td><button className="iconButton" onClick={() => remove(z.id)}><Trash2 size={15} /></button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
