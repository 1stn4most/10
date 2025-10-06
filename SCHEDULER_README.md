# Customer Scheduling & Route Optimizer

A web-based application for managing customer service schedules and optimizing routes for cleaning service teams.

## 🌟 Features

- **📤 Spreadsheet Upload**: Import customer data from CSV files
- **✏️ Manual Entry**: Add customers individually through a user-friendly form
- **📅 Schedule Generation**: Automatically calculate next service dates based on cleaning frequency
- **🗺️ Route Optimization**: Generate fuel-efficient routes for your teams
- **💾 Data Export**: Export customer data back to CSV format
- **📊 Service Tracking**: Monitor service status (Current, Due Soon, Overdue)
- **📝 Special Instructions**: Store location-specific notes and requirements

## 🚀 Getting Started

### Installation

1. Clone or download this repository
2. Open `index.html` in a web browser
3. No installation or server required - runs entirely in your browser!

### Quick Start

1. **Upload Data**: Click "Upload File" and select a CSV file with customer information
2. **Or Add Manually**: Fill out the form to add customers one at a time
3. **Generate Schedule**: Click "Generate Schedule" to see upcoming services
4. **Optimize Routes**: Click "Optimize Routes" to create efficient daily routes

## 📋 CSV File Format

Your CSV file should include the following columns:

```csv
Name,Address,Last Service Date,Frequency,Special Instructions
ABC Company,123 Main St,2024-01-15,Monthly,Use back entrance
XYZ Corp,456 Oak Ave,2024-01-10,Quarterly,Call before arrival
Clean Office LLC,789 Pine Rd,2024-01-20,Bi-Weekly,Building code is 1234
```

### Required Fields

- **Name**: Customer or business name
- **Address**: Full service address
- **Last Service Date**: Date in YYYY-MM-DD format
- **Frequency**: One of:
  - Weekly
  - Bi-Weekly
  - Semi-Monthly
  - Monthly
  - Quarterly
  - Semi-Annually
  - Annually
- **Special Instructions**: Optional notes (can be empty)

## 🎯 How It Works

### Service Schedule Calculation

The application automatically calculates the next service date based on:
- Last service date
- Cleaning frequency

**Examples:**
- Monthly service on 01/15 → Next service: 02/15
- Quarterly service on 01/15 → Next service: 04/15

### Service Status

- **🟢 Current**: Next service is more than 14 days away
- **🟡 Scheduled**: Next service is 8-14 days away
- **🟠 Due Soon**: Next service is within 7 days
- **🔴 Overdue**: Service date has passed

### Route Optimization

The route optimizer uses a nearest-neighbor algorithm to:
1. Group customers scheduled for the same day
2. Sort by location (street address)
3. Create an efficient sequence of stops
4. Minimize travel distance and fuel consumption

**Note**: For production use, integrate with Google Maps API or similar service for accurate distance calculations and turn-by-turn directions.

## 💡 Usage Tips

### Best Practices

1. **Regular Updates**: Update the "Last Service Date" after completing each service
2. **Address Format**: Use consistent address formatting for better route optimization
3. **Special Instructions**: Include:
   - Building access codes
   - Parking instructions
   - Contact preferences
   - Equipment requirements
4. **Backup Data**: Regularly export your data using the "Export Data" button

### Route Planning

1. **Daily Routes**: Generate routes for each service day
2. **Starting Location**: Enter your office/warehouse address for accurate routing
3. **Review Schedule**: Check the schedule view to plan team assignments
4. **Print Routes**: Use your browser's print function to create paper copies

## 🔧 Technical Details

### Technology Stack

- **HTML5**: Modern semantic markup
- **CSS3**: Responsive design with flexbox and grid
- **JavaScript (ES6+)**: Pure JavaScript, no frameworks required
- **LocalStorage**: Data persistence in the browser

### Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### Data Storage

All data is stored locally in your browser using localStorage:
- Data persists between sessions
- No server or cloud storage required
- Data is private to your browser
- Clear browser data will remove all customer information

### Data Privacy

- All data stays on your device
- No data is sent to external servers
- No analytics or tracking
- No user accounts required

## 📱 Mobile Support

The application is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones

## 🔮 Future Enhancements

Potential improvements for future versions:

1. **Map Integration**: Visual route display with Google Maps or Mapbox
2. **Advanced Routing**: Implement proper TSP (Traveling Salesman Problem) algorithms
3. **Team Management**: Assign routes to specific team members
4. **Time Estimates**: Calculate service duration and travel time
5. **Customer Portal**: Allow customers to view and manage their schedules
6. **Reporting**: Generate service reports and analytics
7. **Mobile App**: Native iOS/Android applications
8. **Cloud Sync**: Optional cloud backup and multi-device sync
9. **Invoice Integration**: Link to invoicing systems
10. **SMS/Email Reminders**: Automated customer notifications

## 🐛 Troubleshooting

### Common Issues

**Q: My CSV file won't upload**
- Ensure the file is properly formatted
- Check that dates are in YYYY-MM-DD format
- Verify all required columns are present

**Q: Data disappeared after closing browser**
- Check if browser is in incognito/private mode
- Verify localStorage is enabled in browser settings
- Make regular backups using the Export function

**Q: Routes seem inefficient**
- The basic algorithm sorts by street name
- For accurate routing, consider integrating with a mapping API
- Manually adjust route order if needed

## 📞 Support

For issues or questions:
1. Check this documentation
2. Review the sample CSV format
3. Verify browser compatibility
4. Export and backup your data regularly

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Credits

Created to help cleaning service businesses optimize their operations and improve efficiency.

---

**Version**: 1.0.0  
**Last Updated**: 2024
