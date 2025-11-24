import React, { useState, useEffect } from 'react';
import { Server, Navigation, Activity, Cpu, HardDrive, Radio, MapPin } from 'lucide-react';
import './App.css';

function App() {
  const [nodes, setNodes] = useState([]);
  const [services, setServices] = useState([]);
  const [templates, setTemplates] = useState([]);
  const [stats, setStats] = useState(null);
  const [selectedTemplate, setSelectedTemplate] = useState('');

  const fetchData = async () => {
    try {
      const [nodesRes, servicesRes, templatesRes, statsRes] = await Promise.all([
        fetch('/api/nodes'),
        fetch('/api/services'),
        fetch('/api/templates'),
        fetch('/api/stats')
      ]);

      setNodes(await nodesRes.json());
      setServices(await servicesRes.json());
      setTemplates(await templatesRes.json());
      setStats(await statsRes.json());
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 2000);
    return () => clearInterval(interval);
  }, []);

  const deployService = async () => {
    if (!selectedTemplate) return;

    try {
      await fetch('/api/services', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ template: selectedTemplate })
      });
      fetchData();
    } catch (error) {
      console.error('Error deploying service:', error);
    }
  };

  const deleteService = async (serviceId) => {
    try {
      await fetch(`/api/services/${serviceId}`, { method: 'DELETE' });
      fetchData();
    } catch (error) {
      console.error('Error deleting service:', error);
    }
  };

  const getDomainIcon = (domain) => {
    switch (domain) {
      case 'ADAS': return <Navigation className="icon" />;
      case 'Infotainment': return <MapPin className="icon" />;
      case 'Telematics': return <Radio className="icon" />;
      default: return <Server className="icon" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'running': return '#10b981';
      case 'pending': return '#f59e0b';
      case 'failed': return '#ef4444';
      default: return '#6b7280';
    }
  };

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <div className="header-title">
            <Activity className="header-icon" />
            <h1>SDV Service Orchestrator</h1>
          </div>
          <p className="subtitle">Location Services Deployment Management</p>
        </div>
      </header>

      <div className="container">
        {/* Stats Overview */}
        {stats && (
          <div className="stats-grid">
            <div className="stat-card">
              <Server className="stat-icon" style={{ color: '#3b82f6' }} />
              <div>
                <div className="stat-value">{stats.resources.nodes}</div>
                <div className="stat-label">Vehicle Nodes</div>
              </div>
            </div>
            <div className="stat-card">
              <Activity className="stat-icon" style={{ color: '#10b981' }} />
              <div>
                <div className="stat-value">{stats.services.running}</div>
                <div className="stat-label">Running Services</div>
              </div>
            </div>
            <div className="stat-card">
              <Cpu className="stat-icon" style={{ color: '#f59e0b' }} />
              <div>
                <div className="stat-value">{stats.resources.cpu_utilization}%</div>
                <div className="stat-label">CPU Utilization</div>
              </div>
            </div>
          </div>
        )}

        {/* Deploy Service Section */}
        <div className="section">
          <h2 className="section-title">Deploy Location Service</h2>
          <div className="deploy-controls">
            <select 
              className="select"
              value={selectedTemplate}
              onChange={(e) => setSelectedTemplate(e.target.value)}
            >
              <option value="">Select a service...</option>
              {templates.map(template => (
                <option key={template.key} value={template.key}>
                  {template.name} ({template.type})
                </option>
              ))}
            </select>
            <button 
              className="button button-primary"
              onClick={deployService}
              disabled={!selectedTemplate}
            >
              Deploy Service
            </button>
          </div>
        </div>

        <div className="grid">
          {/* Vehicle Nodes */}
          <div className="section">
            <h2 className="section-title">Vehicle Compute Nodes</h2>
            <div className="nodes-grid">
              {nodes.map(node => (
                <div key={node.id} className="card node-card">
                  <div className="node-header">
                    {getDomainIcon(node.domain)}
                    <div>
                      <h3 className="node-name">{node.name}</h3>
                      <span className="node-domain">{node.domain}</span>
                    </div>
                  </div>
                  
                  <div className="node-resources">
                    <div className="resource-item">
                      <Cpu size={16} />
                      <span>CPU: {node.available_cpu.toFixed(1)}/{node.total_cpu} cores</span>
                    </div>
                    <div className="resource-item">
                      <HardDrive size={16} />
                      <span>RAM: {node.available_memory}/{node.total_memory} MB</span>
                    </div>
                    <div className="resource-item">
                      <Radio size={16} />
                      <span>GPU: {node.has_gpu ? 'Yes' : 'No'}</span>
                    </div>
                  </div>

                  <div className="utilization">
                    <div className="utilization-bar">
                      <div 
                        className="utilization-fill"
                        style={{ 
                          width: `${node.utilization.cpu}%`,
                          backgroundColor: node.utilization.cpu > 80 ? '#ef4444' : '#3b82f6'
                        }}
                      />
                    </div>
                    <span className="utilization-label">CPU: {node.utilization.cpu}%</span>
                  </div>

                  <div className="services-count">
                    {node.deployed_services.length} service(s) deployed
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Active Services */}
          <div className="section">
            <h2 className="section-title">Deployed Services</h2>
            <div className="services-list">
              {services.length === 0 ? (
                <div className="empty-state">
                  No services deployed yet. Deploy a location service to get started.
                </div>
              ) : (
                services.map(service => (
                  <div key={service.id} className="card service-card">
                    <div className="service-header">
                      <div>
                        <h3 className="service-name">{service.name}</h3>
                        <span className="service-type">{service.type}</span>
                      </div>
                      <div 
                        className="status-badge"
                        style={{ backgroundColor: getStatusColor(service.status) }}
                      >
                        {service.status}
                      </div>
                    </div>

                    <div className="service-details">
                      <div className="detail-row">
                        <span className="detail-label">Node:</span>
                        <span className="detail-value">
                          {service.deployed_node 
                            ? nodes.find(n => n.id === service.deployed_node)?.name || 'Unknown'
                            : 'Not deployed'}
                        </span>
                      </div>
                      <div className="detail-row">
                        <span className="detail-label">CPU:</span>
                        <span className="detail-value">{service.requirements.cpu_cores} cores</span>
                      </div>
                      <div className="detail-row">
                        <span className="detail-label">Memory:</span>
                        <span className="detail-value">{service.requirements.memory_mb} MB</span>
                      </div>
                      <div className="detail-row">
                        <span className="detail-label">GPU:</span>
                        <span className="detail-value">{service.requirements.gpu_required ? 'Required' : 'Not required'}</span>
                      </div>
                    </div>

                    <button 
                      className="button button-danger"
                      onClick={() => deleteService(service.id)}
                    >
                      Undeploy
                    </button>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
