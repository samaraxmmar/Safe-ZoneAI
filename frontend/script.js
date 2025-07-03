// Variables globales
let data = [];
let currentPage = 1;
const itemsPerPage = 10;
let sortColumn = 'Nom';
let sortDirection = 'asc';
let chartInstance = null;
let filterTimeout = null;

// Charger les données
async function loadData() {
    document.getElementById('loader').classList.remove('d-none');
    try {
        const response = await axios.get('/api/workers', { timeout: 5000 });
        data = response.data || [];
        populateWorkerNames();
        updateDashboard();
        renderChart();
    } catch (error) {
        showToast('Erreur lors du chargement des données : ' + error.message);
        console.error('Erreur:', error);
    } finally {
        document.getElementById('loader').classList.add('d-none');
    }
}

function populateWorkerNames() {
    const datalist = document.getElementById('workerNames');
    datalist.innerHTML = '';
    const uniqueNames = [...new Set(data.map(item => item.Nom))].sort();
    uniqueNames.forEach(name => {
        const option = document.createElement('option');
        option.value = name;
        datalist.appendChild(option);
    });
}

function updateDashboard() {
    const filteredData = filterData();
    updateStats(filteredData);
    renderTable(filteredData);
    renderPagination(filteredData);
}

function updateStats(filteredData) {
    const totalWorkers = filteredData.length;
    const compliantWorkers = filteredData.filter(item =>
        item.Helmet === 'Oui' && item.Vest === 'Oui' &&
        item.Gloves === 'Oui' && item.Boots === 'Oui' &&
        item.Goggles === 'Oui'
    ).length;
    const alertsCount = filteredData.filter(item =>
        item.Helmet === 'Non' || item.Vest === 'Non' ||
        item.Gloves === 'Non' || item.Boots === 'Non' ||
        item.Goggles === 'Non'
    ).length;

    document.getElementById('totalWorkers').textContent = totalWorkers;
    document.getElementById('compliantWorkers').textContent = compliantWorkers;
    document.getElementById('alertsCount').textContent = alertsCount;

    document.getElementById('totalWorkersPct').textContent = totalWorkers > 0 ? '100%' : '-';
    document.getElementById('compliantWorkersPct').textContent = totalWorkers > 0 ? `${Math.round((compliantWorkers / totalWorkers) * 100)}%` : '-';
    document.getElementById('alertsCountPct').textContent = totalWorkers > 0 ? `${Math.round((alertsCount / totalWorkers) * 100)}%` : '-';
}

function filterData() {
    const nameFilter = document.getElementById('nameFilter').value.toLowerCase().trim();
    const helmetFilter = document.getElementById('helmetFilter').value;
    const vestFilter = document.getElementById('vestFilter').value;
    const glovesFilter = document.getElementById('glovesFilter').value;
    const bootsFilter = document.getElementById('bootsFilter').value;
    const gogglesFilter = document.getElementById('gogglesFilter').value;
    const alertFilter = document.getElementById('alertFilter').value;

    return data.filter(item => {
        const matchesName = item.Nom.toLowerCase().includes(nameFilter);
        const matchesHelmet = helmetFilter ? item.Helmet === helmetFilter : true;
        const matchesVest = vestFilter ? item.Vest === vestFilter : true;
        const matchesGloves = glovesFilter ? item.Gloves === glovesFilter : true;
        const matchesBoots = bootsFilter ? item.Boots === bootsFilter : true;
        const matchesGoggles = gogglesFilter ? item.Goggles === gogglesFilter : true;
        const hasAlert = item.Helmet === 'Non' || item.Vest === 'Non' || item.Gloves === 'Non' || item.Boots === 'Non' || item.Goggles === 'Non';
        const matchesAlert = alertFilter ? (alertFilter === 'Oui' ? hasAlert : !hasAlert) : true;
        return matchesName && matchesHelmet && matchesVest && matchesGloves && matchesBoots && matchesGoggles && matchesAlert;
    });
}

function sortTable(column) {
    if (sortColumn === column) {
        sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
    } else {
        sortColumn = column;
        sortDirection = 'asc';
    }

    data.sort((a, b) => {
        const valueA = a[column] || '';
        const valueB = b[column] || '';
        return sortDirection === 'asc' ? valueA.localeCompare(valueB, 'fr', { sensitivity: 'base' }) : valueB.localeCompare(valueA, 'fr', { sensitivity: 'base' });
    });

    updateDashboard();
}

function renderTable(filteredData) {
    const start = (currentPage - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    const paginatedData = filteredData.slice(start, end);

    const tableBody = document.getElementById('equipment-table');
    tableBody.innerHTML = '';

    paginatedData.forEach(item => {
        const alertStatus = item.Helmet === 'Non' || item.Vest === 'Non' || item.Gloves === 'Non' || item.Boots === 'Non' || item.Goggles === 'Non';
        const row = document.createElement('tr');
        row.innerHTML = `
            <td class="fw-medium" data-label="Nom">${item.Nom}</td>
            <td data-label="Casque"><span class="badge bg-${item.Helmet === 'Oui' ? 'success' : 'danger'}">${item.Helmet === 'Oui' ? 'Porté' : 'Non porté'}</span></td>
            <td data-label="Gilet"><span class="badge bg-${item.Vest === 'Oui' ? 'success' : 'danger'}">${item.Vest === 'Oui' ? 'Porté' : 'Non porté'}</span></td>
            <td data-label="Gants"><span class="badge bg-${item.Gloves === 'Oui' ? 'success' : 'danger'}">${item.Gloves === 'Oui' ? 'Porté' : 'Non porté'}</span></td>
            <td data-label="Bottes"><span class="badge bg-${item.Boots === 'Oui' ? 'success' : 'danger'}">${item.Boots === 'Oui' ? 'Porté' : 'Non porté'}</span></td>
            <td data-label="Lunettes"><span class="badge bg-${item.Goggles === 'Oui' ? 'success' : 'danger'}">${item.Goggles === 'Oui' ? 'Porté' : 'Non porté'}</span></td>
            <td data-label="Alertes">${alertStatus ? '<i class="fas fa-exclamation-circle text-danger me-1"></i> Alerte' : '<i class="fas fa-check-circle text-success me-1"></i> Conforme'}</td>
        `;
        tableBody.appendChild(row);
    });
}

function renderPagination(filteredData) {
    const pageCount = Math.ceil(filteredData.length / itemsPerPage);
    const pagination = document.getElementById('pagination');
    pagination.innerHTML = '';

    for (let i = 1; i <= pageCount; i++) {
        const li = document.createElement('li');
        li.className = `page-item ${i === currentPage ? 'active' : ''}`;
        li.innerHTML = `<a class="page-link" href="#" onclick="changePage(${i})">${i}</a>`;
        pagination.appendChild(li);
    }
}

function changePage(page) {
    currentPage = page;
    updateDashboard();
}

function showToast(message) {
    const toast = document.getElementById('alertToast');
    toast.querySelector('.toast-body').textContent = message;
    const bsToast = new bootstrap.Toast(toast, { delay: 4000 });
    bsToast.show();
}

function resetFilters() {
    document.getElementById('nameFilter').value = '';
    document.getElementById('helmetFilter').value = '';
    document.getElementById('vestFilter').value = '';
    document.getElementById('glovesFilter').value = '';
    document.getElementById('bootsFilter').value = '';
    document.getElementById('gogglesFilter').value = '';
    document.getElementById('alertFilter').value = '';
    currentPage = 1;
    updateDashboard();
}

function exportToCSV() {
    const filteredData = filterData();
    const csv = [
        ['Nom', 'Casque', 'Gilet', 'Gants', 'Bottes', 'Lunettes', 'Alertes'],
        ...filteredData.map(item => [
            item.Nom,
            item.Helmet === 'Oui' ? 'Porté' : 'Non porté',
            item.Vest === 'Oui' ? 'Porté' : 'Non porté',
            item.Gloves === 'Oui' ? 'Porté' : 'Non porté',
            item.Boots === 'Oui' ? 'Porté' : 'Non porté',
            item.Goggles === 'Oui' ? 'Porté' : 'Non porté',
            (item.Helmet === 'Non' || item.Vest === 'Non' || item.Gloves === 'Non' || item.Boots === 'Non' || item.Goggles === 'Non') ? 'Oui' : 'Non'
        ])
    ].map(row => row.map(cell => `"${cell}"`).join(',')).join('\n');

    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `conformite_equipements_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
}

function exportToPDF() {
    const element = document.querySelector('.table-responsive');
    const opt = {
        margin: 0.5,
        filename: `conformite_equipements_${new Date().toISOString().split('T')[0]}.pdf`,
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
    };
    html2pdf().set(opt).from(element).save();
}

function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
}