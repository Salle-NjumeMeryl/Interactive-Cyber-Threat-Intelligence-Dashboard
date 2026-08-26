// State object for active filters
const activeFilters = {
  startDate: '',
  endDate: '',
  attackType: 'all',
  country: '',
  severity: 'all'
};

document.addEventListener('DOMContentLoaded', () => {
  // Bind Filter Events
  document.getElementById('applyFiltersBtn').addEventListener('click', handleFilterApply);
  document.getElementById('resetFiltersBtn').addEventListener('click', resetFilters);

  // Initial dashboard load
  loadDashboardData();
});

function handleFilterApply() {
  activeFilters.startDate = document.getElementById('startDate').value;
  activeFilters.endDate = document.getElementById('endDate').value;
  activeFilters.attackType = document.getElementById('attackTypeSelect').value;
  activeFilters.country = document.getElementById('countrySearch').value.trim();
  activeFilters.severity = document.getElementById('severitySelect').value;

  loadDashboardData();
}

function resetFilters() {
  document.getElementById('startDate').value = '';
  document.getElementById('endDate').value = '';
  document.getElementById('attackTypeSelect').value = 'all';
  document.getElementById('countrySearch').value = '';
  document.getElementById('severitySelect').value = 'all';

  handleFilterApply();
}

async function loadDashboardData() {
  // 1. Build Query String dynamically
  const params = new URLSearchParams();
  if (activeFilters.startDate) params.append('start_date', activeFilters.startDate);
  if (activeFilters.endDate) params.append('end_date', activeFilters.endDate);
  if (activeFilters.attackType !== 'all') params.append('attack_type', activeFilters.attackType);
  if (activeFilters.country) params.append('country', activeFilters.country);
  if (activeFilters.severity !== 'all') params.append('severity', activeFilters.severity);

  const queryString = params.toString() ? `?${params.toString()}` : '';

  try {
    // 2. Fetch payload from backend endpoint with filter query string
    const response = await fetch(`/api/dashboard${queryString}`);
    const data = await response.json();

    // 3. Simultaneously update all components on the dashboard
    updateKPIs(data.kpis);
    updateMapMarkers(data.mapData);
    updateDistributionCharts(data.charts);
    updateTrendLineChart(data.trendData);
    updatePulsesTable(data.recentPulses);

  } catch (error) {
    console.error("Failed to fetch filtered dashboard data:", error);
  }
}