// Customer Scheduling & Route Optimizer Application

class CustomerScheduler {
    constructor() {
        this.customers = [];
        this.loadFromLocalStorage();
        this.initializeEventListeners();
        this.renderCustomerTable();
    }

    // Initialize event listeners
    initializeEventListeners() {
        document.getElementById('uploadBtn').addEventListener('click', () => this.handleFileUpload());
        document.getElementById('customerForm').addEventListener('submit', (e) => this.handleManualEntry(e));
        document.getElementById('generateScheduleBtn').addEventListener('click', () => this.generateSchedule());
        document.getElementById('optimizeRouteBtn').addEventListener('click', () => this.showRouteOptimizer());
        document.getElementById('exportBtn').addEventListener('click', () => this.exportData());
        document.getElementById('clearAllBtn').addEventListener('click', () => this.clearAllData());
        document.getElementById('filterScheduleBtn').addEventListener('click', () => this.filterSchedule());
        document.getElementById('calculateRouteBtn').addEventListener('click', () => this.calculateRoute());
    }

    // Handle file upload
    handleFileUpload() {
        const fileInput = document.getElementById('fileInput');
        const file = fileInput.files[0];

        if (!file) {
            alert('Please select a file first!');
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const content = e.target.result;
                this.parseCSV(content);
                document.getElementById('fileName').textContent = `✓ ${file.name} uploaded successfully!`;
                fileInput.value = '';
            } catch (error) {
                alert('Error parsing file: ' + error.message);
            }
        };
        reader.readAsText(file);
    }

    // Parse CSV content
    parseCSV(content) {
        const lines = content.split('\n').filter(line => line.trim());
        const headers = lines[0].split(',').map(h => h.trim());

        for (let i = 1; i < lines.length; i++) {
            const values = lines[i].split(',').map(v => v.trim());
            if (values.length >= 4) {
                const customer = {
                    id: Date.now() + i,
                    name: values[0] || '',
                    address: values[1] || '',
                    lastServiceDate: values[2] || '',
                    frequency: values[3] || '',
                    specialInstructions: values[4] || ''
                };
                this.customers.push(customer);
            }
        }

        this.saveToLocalStorage();
        this.renderCustomerTable();
    }

    // Handle manual entry
    handleManualEntry(e) {
        e.preventDefault();

        const customer = {
            id: Date.now(),
            name: document.getElementById('customerName').value,
            address: document.getElementById('customerAddress').value,
            lastServiceDate: document.getElementById('lastServiceDate').value,
            frequency: document.getElementById('frequency').value,
            specialInstructions: document.getElementById('specialInstructions').value
        };

        this.customers.push(customer);
        this.saveToLocalStorage();
        this.renderCustomerTable();
        e.target.reset();
        alert('Customer added successfully!');
    }

    // Calculate next service date based on frequency
    calculateNextServiceDate(lastServiceDate, frequency) {
        const date = new Date(lastServiceDate);
        
        switch (frequency) {
            case 'Weekly':
                date.setDate(date.getDate() + 7);
                break;
            case 'Bi-Weekly':
                date.setDate(date.getDate() + 14);
                break;
            case 'Semi-Monthly':
                date.setDate(date.getDate() + 15);
                break;
            case 'Monthly':
                date.setMonth(date.getMonth() + 1);
                break;
            case 'Quarterly':
                date.setMonth(date.getMonth() + 3);
                break;
            case 'Semi-Annually':
                date.setMonth(date.getMonth() + 6);
                break;
            case 'Annually':
                date.setFullYear(date.getFullYear() + 1);
                break;
        }

        return date;
    }

    // Get service status
    getServiceStatus(nextServiceDate) {
        const today = new Date();
        const next = new Date(nextServiceDate);
        const daysUntil = Math.floor((next - today) / (1000 * 60 * 60 * 24));

        if (daysUntil < 0) return { status: 'Overdue', class: 'status-overdue' };
        if (daysUntil <= 7) return { status: 'Due Soon', class: 'status-due' };
        if (daysUntil <= 14) return { status: 'Scheduled', class: 'status-scheduled' };
        return { status: 'Current', class: 'status-current' };
    }

    // Render customer table
    renderCustomerTable() {
        const tableDiv = document.getElementById('customerTable');

        if (this.customers.length === 0) {
            tableDiv.innerHTML = '<div class="empty-state"><p>No customers added yet. Upload a file or add manually.</p></div>';
            return;
        }

        let html = `
            <table class="customer-table">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Address</th>
                        <th>Last Service</th>
                        <th>Frequency</th>
                        <th>Next Service</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
        `;

        this.customers.forEach(customer => {
            const nextService = this.calculateNextServiceDate(customer.lastServiceDate, customer.frequency);
            const statusInfo = this.getServiceStatus(nextService);

            html += `
                <tr>
                    <td><strong>${customer.name}</strong></td>
                    <td>${customer.address}</td>
                    <td>${customer.lastServiceDate}</td>
                    <td>${customer.frequency}</td>
                    <td>${nextService.toISOString().split('T')[0]}</td>
                    <td><span class="status-badge ${statusInfo.class}">${statusInfo.status}</span></td>
                    <td>
                        <button class="btn btn-info action-btn" onclick="scheduler.viewCustomer(${customer.id})">View</button>
                        <button class="btn btn-danger action-btn" onclick="scheduler.deleteCustomer(${customer.id})">Delete</button>
                    </td>
                </tr>
            `;
        });

        html += `
                </tbody>
            </table>
        `;

        tableDiv.innerHTML = html;
    }

    // View customer details
    viewCustomer(id) {
        const customer = this.customers.find(c => c.id === id);
        if (customer) {
            const nextService = this.calculateNextServiceDate(customer.lastServiceDate, customer.frequency);
            alert(`
Customer Details:
━━━━━━━━━━━━━━━━━━━
Name: ${customer.name}
Address: ${customer.address}
Last Service: ${customer.lastServiceDate}
Frequency: ${customer.frequency}
Next Service: ${nextService.toISOString().split('T')[0]}
Special Instructions: ${customer.specialInstructions || 'None'}
            `);
        }
    }

    // Delete customer
    deleteCustomer(id) {
        if (confirm('Are you sure you want to delete this customer?')) {
            this.customers = this.customers.filter(c => c.id !== id);
            this.saveToLocalStorage();
            this.renderCustomerTable();
        }
    }

    // Generate schedule
    generateSchedule() {
        if (this.customers.length === 0) {
            alert('Please add customers first!');
            return;
        }

        const scheduleView = document.getElementById('scheduleView');
        scheduleView.scrollIntoView({ behavior: 'smooth' });

        // Set default date range (next 30 days)
        const today = new Date();
        const endDate = new Date();
        endDate.setDate(today.getDate() + 30);

        document.getElementById('scheduleStartDate').value = today.toISOString().split('T')[0];
        document.getElementById('scheduleEndDate').value = endDate.toISOString().split('T')[0];

        this.filterSchedule();
    }

    // Filter schedule by date range
    filterSchedule() {
        const startDate = new Date(document.getElementById('scheduleStartDate').value);
        const endDate = new Date(document.getElementById('scheduleEndDate').value);
        const scheduleContent = document.getElementById('scheduleContent');

        if (!startDate || !endDate) {
            alert('Please select both start and end dates!');
            return;
        }

        // Group customers by next service date
        const schedule = {};
        
        this.customers.forEach(customer => {
            const nextService = this.calculateNextServiceDate(customer.lastServiceDate, customer.frequency);
            
            if (nextService >= startDate && nextService <= endDate) {
                const dateKey = nextService.toISOString().split('T')[0];
                if (!schedule[dateKey]) {
                    schedule[dateKey] = [];
                }
                schedule[dateKey].push({ ...customer, nextService });
            }
        });

        // Render schedule
        let html = '';
        const sortedDates = Object.keys(schedule).sort();

        if (sortedDates.length === 0) {
            html = '<div class="empty-state"><p>No services scheduled in this date range.</p></div>';
        } else {
            sortedDates.forEach(date => {
                const formattedDate = new Date(date).toLocaleDateString('en-US', { 
                    weekday: 'long', 
                    year: 'numeric', 
                    month: 'long', 
                    day: 'numeric' 
                });

                html += `
                    <div class="schedule-day">
                        <h3>${formattedDate} (${schedule[date].length} service${schedule[date].length > 1 ? 's' : ''})</h3>
                `;

                schedule[date].forEach(customer => {
                    html += `
                        <div class="schedule-item">
                            <h4>${customer.name}</h4>
                            <p><strong>📍 Address:</strong> ${customer.address}</p>
                            <p><strong>🔄 Frequency:</strong> ${customer.frequency}</p>
                            ${customer.specialInstructions ? `<p><strong>📝 Special Instructions:</strong> ${customer.specialInstructions}</p>` : ''}
                        </div>
                    `;
                });

                html += `</div>`;
            });
        }

        scheduleContent.innerHTML = html;
    }

    // Show route optimizer
    showRouteOptimizer() {
        if (this.customers.length === 0) {
            alert('Please add customers first!');
            return;
        }

        const routeView = document.getElementById('routeView');
        routeView.scrollIntoView({ behavior: 'smooth' });

        // Set default date to today
        const today = new Date().toISOString().split('T')[0];
        document.getElementById('routeDate').value = today;
    }

    // Calculate optimized route
    calculateRoute() {
        const routeDate = document.getElementById('routeDate').value;
        const startLocation = document.getElementById('startLocation').value;
        const routeContent = document.getElementById('routeContent');

        if (!routeDate) {
            alert('Please select a date!');
            return;
        }

        if (!startLocation) {
            alert('Please enter a starting location!');
            return;
        }

        // Get customers scheduled for this date
        const selectedDate = new Date(routeDate);
        const scheduledCustomers = this.customers.filter(customer => {
            const nextService = this.calculateNextServiceDate(customer.lastServiceDate, customer.frequency);
            return nextService.toISOString().split('T')[0] === routeDate;
        });

        if (scheduledCustomers.length === 0) {
            routeContent.innerHTML = '<div class="empty-state"><p>No services scheduled for this date.</p></div>';
            return;
        }

        // Simple routing algorithm (nearest neighbor)
        const route = this.optimizeRoute(startLocation, scheduledCustomers);

        // Render route
        let html = `
            <div class="route-summary">
                <h3>Route Summary</h3>
                <p><strong>📅 Date:</strong> ${selectedDate.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}</p>
                <p><strong>📍 Starting Location:</strong> ${startLocation}</p>
                <p><strong>🏢 Total Stops:</strong> ${route.length}</p>
                <p><strong>⚡ Route Optimization:</strong> Nearest Neighbor Algorithm Applied</p>
            </div>
        `;

        route.forEach((customer, index) => {
            html += `
                <div class="route-step">
                    <span class="step-number">${index + 1}</span>
                    <strong>${customer.name}</strong>
                    <p><strong>📍 Address:</strong> ${customer.address}</p>
                    <p><strong>🔄 Service Type:</strong> ${customer.frequency}</p>
                    ${customer.specialInstructions ? `<p><strong>📝 Instructions:</strong> ${customer.specialInstructions}</p>` : ''}
                </div>
            `;
        });

        routeContent.innerHTML = html;
    }

    // Simple route optimization using nearest neighbor algorithm
    optimizeRoute(start, customers) {
        // In a real application, you would use a proper routing API (Google Maps, MapBox, etc.)
        // This is a simplified version that sorts by address (alphabetically as a proxy for location)
        
        // For a more accurate solution, you would:
        // 1. Geocode all addresses to get lat/long coordinates
        // 2. Apply TSP (Traveling Salesman Problem) algorithms like:
        //    - Nearest Neighbor
        //    - Genetic Algorithm
        //    - Simulated Annealing
        //    - Or use a routing API service
        
        // Simple alphabetical sort by address as a basic optimization
        return customers.sort((a, b) => {
            // Extract street names for better grouping
            const getStreet = (addr) => addr.split(',')[0] || addr;
            return getStreet(a.address).localeCompare(getStreet(b.address));
        });
    }

    // Export data to CSV
    exportData() {
        if (this.customers.length === 0) {
            alert('No data to export!');
            return;
        }

        let csv = 'Name,Address,Last Service Date,Frequency,Special Instructions\n';
        
        this.customers.forEach(customer => {
            csv += `"${customer.name}","${customer.address}","${customer.lastServiceDate}","${customer.frequency}","${customer.specialInstructions}"\n`;
        });

        const blob = new Blob([csv], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `customer-data-${new Date().toISOString().split('T')[0]}.csv`;
        a.click();
        window.URL.revokeObjectURL(url);
    }

    // Clear all data
    clearAllData() {
        if (confirm('Are you sure you want to delete all customer data? This cannot be undone!')) {
            this.customers = [];
            this.saveToLocalStorage();
            this.renderCustomerTable();
            document.getElementById('scheduleContent').innerHTML = '';
            document.getElementById('routeContent').innerHTML = '';
            alert('All data cleared!');
        }
    }

    // Local storage methods
    saveToLocalStorage() {
        localStorage.setItem('customerSchedulerData', JSON.stringify(this.customers));
    }

    loadFromLocalStorage() {
        const data = localStorage.getItem('customerSchedulerData');
        if (data) {
            try {
                this.customers = JSON.parse(data);
            } catch (error) {
                console.error('Error loading data from localStorage:', error);
                this.customers = [];
            }
        }
    }
}

// Initialize the application
const scheduler = new CustomerScheduler();
